#!/usr/bin/env python3
"""
Simple PSNR evaluation script for PhysGaussian parameter comparison.
This script computes PSNR between a baseline simulation and modified parameter simulations.
"""

import os
import sys
import torch
import cv2
import numpy as np
from pathlib import Path
import argparse
import json

# Add gaussian splatting utils to path
sys.path.append("gaussian-splatting")
from utils.image_utils import psnr

def robust_psnr(img1, img2):
    """Robust PSNR computation that handles tensor contiguity issues."""
    try:
        return psnr(img1, img2)
    except RuntimeError as e:
        if "view size is not compatible" in str(e):
            # Use reshape instead of view for non-contiguous tensors
            mse = (((img1 - img2)) ** 2).reshape(img1.shape[0], -1).mean(1, keepdim=True)
            return 20 * torch.log10(1.0 / torch.sqrt(mse))
        else:
            raise e

def load_images_from_directory(image_dir):
    """Load all PNG images from a directory and convert to tensors."""
    images = []
    image_files = sorted([f for f in os.listdir(image_dir) if f.endswith('.png')])
    
    for img_file in image_files:
        img_path = os.path.join(image_dir, img_file)
        img = cv2.imread(img_path)
        if img is not None:
            # Convert BGR to RGB and normalize to [0,1]
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = img.astype(np.float32) / 255.0
            # Convert to tensor: (H, W, C) -> (1, C, H, W)
            img_tensor = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).cuda()
            images.append(img_tensor)
    
    return images, image_files

def compute_psnr_between_sequences(baseline_dir, modified_dir):
    """Compute PSNR between two image sequences."""
    baseline_images, baseline_files = load_images_from_directory(baseline_dir)
    modified_images, modified_files = load_images_from_directory(modified_dir)
    
    if len(baseline_images) == 0 or len(modified_images) == 0:
        print(f"Error: No images found in directories")
        return None, []
    
    min_length = min(len(baseline_images), len(modified_images))
    print(f"Comparing {min_length} frames")
    
    psnr_values = []
    for i in range(min_length):
        # Use robust PSNR computation
        psnr_val = robust_psnr(baseline_images[i], modified_images[i])
        psnr_values.append(psnr_val.item())
    
    mean_psnr = np.mean(psnr_values)
    return mean_psnr, psnr_values

def main():
    parser = argparse.ArgumentParser(description='Evaluate PSNR between baseline and modified parameter simulations')
    parser.add_argument('--baseline_dir', type=str, required=True, help='Directory containing baseline simulation images')
    parser.add_argument('--modified_dir', type=str, required=True, help='Directory containing modified simulation images')
    parser.add_argument('--output_file', type=str, default='psnr_results.json', help='Output JSON file for results')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.baseline_dir):
        print(f"Error: Baseline directory {args.baseline_dir} does not exist")
        return
        
    if not os.path.exists(args.modified_dir):
        print(f"Error: Modified directory {args.modified_dir} does not exist")
        return
    
    print(f"Computing PSNR between:")
    print(f"  Baseline: {args.baseline_dir}")
    print(f"  Modified: {args.modified_dir}")
    
    mean_psnr, psnr_values = compute_psnr_between_sequences(args.baseline_dir, args.modified_dir)
    
    if mean_psnr is not None:
        print(f"Mean PSNR: {mean_psnr:.4f}")
        print(f"PSNR Range: {min(psnr_values):.4f} - {max(psnr_values):.4f}")
        
        # Save results
        results = {
            'mean_psnr': mean_psnr,
            'psnr_values': psnr_values,
            'num_frames': len(psnr_values),
            'baseline_dir': args.baseline_dir,
            'modified_dir': args.modified_dir
        }
        
        with open(args.output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to {args.output_file}")
    else:
        print("Failed to compute PSNR")

if __name__ == "__main__":
    main() 