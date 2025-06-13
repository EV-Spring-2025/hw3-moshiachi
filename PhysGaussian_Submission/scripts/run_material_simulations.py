#!/usr/bin/env python3
"""
Script to run material simulations for PhysGaussian homework Part 1.
This script runs simulations for metal and snow materials.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_simulation(model_path, config_path, output_path, material_name, white_bg=True):
    """Run PhysGaussian simulation for a specific material."""
    print(f"\n=== Running {material_name.upper()} Material Simulation ===")
    
    cmd = [
        'python', 'gs_simulation.py',
        '--model_path', model_path,
        '--output_path', output_path,
        '--config', config_path,
        '--render_img',
        '--compile_video'
    ]
    
    if white_bg:
        cmd.append('--white_bg')
    
    print(f"Command: {' '.join(cmd)}")
    print(f"Output directory: {output_path}")
    
    # Create output directory
    os.makedirs(output_path, exist_ok=True)
    
    # Run simulation
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {material_name.capitalize()} simulation completed successfully!")
        
        # Check if video was created
        video_path = os.path.join(output_path, "output.mp4")
        if os.path.exists(video_path):
            print(f"📹 Video saved: {video_path}")
        else:
            print("⚠️  Video not found, but images should be available")
            
        return True
    else:
        print(f"❌ {material_name.capitalize()} simulation failed!")
        print(f"Error: {result.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Run metal and snow material simulations for homework Part 1')
    parser.add_argument('--model_path', type=str, 
                       default='../pillow2sofa_whitebg-trained/',
                       help='Path to the trained model')
    parser.add_argument('--output_dir', type=str, default='part1_materials', 
                       help='Base output directory for results')
    parser.add_argument('--white_bg', action='store_true', default=True,
                       help='Use white background')
    parser.add_argument('--material', type=str, choices=['metal', 'snow', 'both'], 
                       default='both', help='Which material(s) to simulate')
    
    args = parser.parse_args()
    
    # Check if model path exists
    if not os.path.exists(args.model_path):
        print(f"❌ Model path does not exist: {args.model_path}")
        print("Please make sure the pillow2sofa model is in the correct location.")
        return
    
    # Create base output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    materials_to_run = []
    if args.material == 'both':
        materials_to_run = ['metal', 'snow']
    else:
        materials_to_run = [args.material]
    
    results = {}
    
    for material in materials_to_run:
        if material == 'metal':
            config_path = './config/pillow2sofa_metal.json'
        elif material == 'snow':
            config_path = './config/pillow2sofa_snow.json'
        
        if not os.path.exists(config_path):
            print(f"❌ Config file not found: {config_path}")
            continue
            
        output_path = os.path.join(args.output_dir, f'{material}_simulation')
        
        success = run_simulation(
            args.model_path, 
            config_path, 
            output_path, 
            material,
            args.white_bg
        )
        
        results[material] = {
            'success': success,
            'output_path': output_path,
            'config_path': config_path
        }
    
    # Print summary
    print(f"\n{'='*50}")
    print("SIMULATION SUMMARY")
    print(f"{'='*50}")
    
    for material, result in results.items():
        status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
        print(f"{material.upper()}: {status}")
        if result['success']:
            print(f"  📁 Output: {result['output_path']}")
            video_path = os.path.join(result['output_path'], "output.mp4")
            if os.path.exists(video_path):
                print(f"  📹 Video: {video_path}")
    
    print(f"\n📋 For your homework report, you can describe:")
    print(f"   • Visual differences between metal and snow behavior")
    print(f"   • How material properties affect the simulation")
    print(f"   • Physical realism of the simulations")

if __name__ == "__main__":
    main() 