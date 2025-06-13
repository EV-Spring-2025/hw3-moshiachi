#!/usr/bin/env python3
"""
Automated parameter study script for PhysGaussian homework Part 2.
This script runs parameter variations on both metal and snow baseline simulations.
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
import argparse

def load_config(config_path):
    """Load configuration from JSON file."""
    with open(config_path, 'r') as f:
        return json.load(f)

def save_config(config, output_path):
    """Save configuration to JSON file."""
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)

def run_simulation(model_path, config_path, output_path, white_bg=True):
    """Run PhysGaussian simulation."""
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
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error running simulation: {result.stderr}")
        return False
    
    return True

def evaluate_psnr(baseline_dir, modified_dir, output_file):
    """Evaluate PSNR between baseline and modified simulation."""
    cmd = [
        'python', 'evaluate_psnr.py',
        '--baseline_dir', baseline_dir,
        '--modified_dir', modified_dir,
        '--output_file', output_file
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error evaluating PSNR: {result.stderr}")
        return None
    
    # Load and return PSNR result
    try:
        with open(output_file, 'r') as f:
            return json.load(f)
    except:
        return None

def main():
    parser = argparse.ArgumentParser(description='Parameter study on both metal and snow materials')
    parser.add_argument('--model_path', type=str, 
                       default='../pillow2sofa_whitebg-trained/',
                       help='Path to the trained model')
    parser.add_argument('--output_dir', type=str, default='part2_parameter_study', 
                       help='Output directory for results')
    parser.add_argument('--white_bg', action='store_true', default=True,
                       help='Use white background')
    parser.add_argument('--material', type=str, choices=['metal', 'snow', 'both'], 
                       default='both', help='Which material(s) to test')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Define materials to test
    materials_to_test = []
    if args.material == 'both':
        materials_to_test = ['metal', 'snow']
    else:
        materials_to_test = [args.material]
    
    # Define base configs for each material
    base_configs = {
        'metal': './config/pillow2sofa_metal.json',
        'snow': './config/pillow2sofa_snow.json'
    }
    
    # Parameter variations to test (from homework requirements)
    parameter_tests = [
        # n_grid variations - more extreme differences
        {'name': 'n_grid_60', 'param': 'n_grid', 'value': 60},
        {'name': 'n_grid_150', 'param': 'n_grid', 'value': 150},
        
        # substeps (substep_dt) variations - more extreme differences
        {'name': 'substep_dt_2e-5', 'param': 'substep_dt', 'value': 2e-5},
        {'name': 'substep_dt_5e-4', 'param': 'substep_dt', 'value': 5e-4},
        
        # grid_v_damping_scale variations - more extreme differences
        {'name': 'damping_0.1', 'param': 'grid_v_damping_scale', 'value': 0.1},
        {'name': 'damping_5.0', 'param': 'grid_v_damping_scale', 'value': 5.0},
        
        # softening variations - more extreme differences
        {'name': 'softening_0.001', 'param': 'softening', 'value': 0.001},
        {'name': 'softening_1.0', 'param': 'softening', 'value': 1.0},
    ]
    
    all_results = {}
    
    # Process each material
    for material in materials_to_test:
        print(f"\n{'='*60}")
        print(f"TESTING {material.upper()} MATERIAL")
        print(f"{'='*60}")
        
        # Load base configuration for this material
        base_config_path = base_configs[material]
        if not os.path.exists(base_config_path):
            print(f"❌ Base config not found: {base_config_path}")
            continue
            
        base_config = load_config(base_config_path)
        
        # Create material-specific output directory
        material_dir = os.path.join(args.output_dir, material)
        os.makedirs(material_dir, exist_ok=True)
        
        # Run baseline simulation for this material
        print(f"\n=== Running {material.upper()} Baseline Simulation ===")
        baseline_output = os.path.join(material_dir, 'baseline')
        baseline_config_path = os.path.join(material_dir, f'{material}_baseline_config.json')
        save_config(base_config, baseline_config_path)
        
        if not run_simulation(args.model_path, baseline_config_path, baseline_output, args.white_bg):
            print(f"Failed to run {material} baseline simulation")
            continue
        
        material_results = {'baseline': baseline_output}
        psnr_results = {}
        
        # Run parameter variations for this material
        for test in parameter_tests:
            print(f"\n=== Running {material.upper()} - {test['name']} ===")
            
            # Create modified config
            modified_config = base_config.copy()
            
            if 'value_factor' in test:
                # For relative changes (like softening)
                original_value = base_config.get(test['param'], 1.0)
                modified_config[test['param']] = original_value * test['value_factor']
                actual_value = modified_config[test['param']]
            else:
                # For absolute values
                modified_config[test['param']] = test['value']
                actual_value = test['value']
            
            # Save modified config
            modified_config_path = os.path.join(material_dir, f"{test['name']}_config.json")
            save_config(modified_config, modified_config_path)
            
            # Run simulation
            modified_output = os.path.join(material_dir, test['name'])
            if run_simulation(args.model_path, modified_config_path, modified_output, args.white_bg):
                material_results[test['name']] = modified_output
                
                # Evaluate PSNR against baseline
                psnr_file = os.path.join(material_dir, f"{test['name']}_psnr.json")
                psnr_result = evaluate_psnr(baseline_output, modified_output, psnr_file)
                
                if psnr_result:
                    baseline_value = base_config.get(test['param'], 'N/A')
                    psnr_results[test['name']] = {
                        'parameter': test['param'],
                        'baseline_value': baseline_value,
                        'new_value': actual_value,
                        'mean_psnr': psnr_result['mean_psnr'],
                        'material': material
                    }
                    print(f"  PSNR vs {material} baseline: {psnr_result['mean_psnr']:.4f}")
                    print(f"  Parameter change: {test['param']} {baseline_value} → {actual_value}")
                else:
                    print(f"  Failed to compute PSNR for {test['name']}")
            else:
                print(f"  Failed to run simulation for {test['name']}")
        
        all_results[material] = {
            'baseline_config': base_config,
            'results_directories': material_results,
            'psnr_comparisons': psnr_results
        }
    
    # Save comprehensive summary
    summary = {
        'materials_tested': materials_to_test,
        'parameter_variations': parameter_tests,
        'results_by_material': all_results
    }
    
    summary_path = os.path.join(args.output_dir, 'complete_parameter_study.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print comprehensive summary
    print(f"\n{'='*80}")
    print("COMPLETE PARAMETER STUDY SUMMARY")
    print(f"{'='*80}")
    
    for material in materials_to_test:
        if material in all_results:
            print(f"\n{material.upper()} MATERIAL RESULTS:")
            print("-" * 40)
            psnr_results = all_results[material]['psnr_comparisons']
            
            for test_name, result in psnr_results.items():
                print(f"  {test_name}:")
                print(f"    Parameter: {result['parameter']}")
                print(f"    Change: {result['baseline_value']} → {result['new_value']}")
                print(f"    PSNR vs baseline: {result['mean_psnr']:.4f}")
                print()
    
    print(f"📁 Complete results saved to: {summary_path}")
    print(f"\n📋 For your homework report, compare how the same parameter changes")
    print(f"    affect PSNR differently between metal and snow materials!")

if __name__ == "__main__":
    main() 