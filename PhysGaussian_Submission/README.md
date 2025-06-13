# PhysGaussian Homework Submission

This submission contains all custom code, configurations, and results for the PhysGaussian homework assignment covering material simulations and MPM parameter studies.

## 🚨 **IMPORTANT: File Placement Instructions**

**These files are designed to work with the original PhysGaussian repository and should be placed in the PhysGaussian folder after cloning.**

### **Setup Steps**:
1. **Clone PhysGaussian repository** (original repo)
2. **Copy files from this submission** to the PhysGaussian folder:
   ```bash
   # After cloning PhysGaussian repository
   cd PhysGaussian/
   
   # Copy config files
   cp /path/to/submission/configs/*.json config/
   
   # Copy scripts to PhysGaussian root directory
   cp /path/to/submission/scripts/*.py ./
   ```
3. **Run the custom scripts** as documented below

**⚠️ Note**: The scripts in this submission are **standalone additions** that do not modify any original PhysGaussian code. They work alongside the existing repository structure.

## 📁 Submission Structure

```
PhysGaussian_Submission/
├── README.md                          # This file
├── configs/                           # Material configuration files
│   ├── pillow2sofa_metal.json        # Metal material configuration
│   └── pillow2sofa_snow.json         # Snow material configuration
├── scripts/                           # Custom scripts developed
│   ├── parameter_study.py            # Main parameter study automation
│   ├── evaluate_psnr.py             # PSNR evaluation with frame analysis
│   └── run_material_simulations.py  # Material simulation automation
├── results/                           # Study results
│   └── complete_parameter_study.json # Complete PSNR analysis results
└── documentation/
    └── HOMEWORK_GUIDE.md             # Comprehensive homework guide
```


## 🔧 Custom Code Description

### 1. `parameter_study.py`
**Purpose**: Automated parameter study script for both metal and snow materials.

**Key Features**:
- Tests 8 parameter variations on both materials (16 total simulations)
- Automatically runs baseline simulations
- Computes PSNR for each variation vs baseline
- Uses enhanced middle-frame analysis for better sensitivity
- Saves comprehensive results in JSON format

**Usage**:
```bash
python parameter_study.py --material both --output_dir part2_parameter_study
```

**Parameters Tested**:
- `n_grid`: 60, 150 (vs baseline 100)
- `substep_dt`: 2e-5, 5e-4 (vs baseline 1e-4)  
- `grid_v_damping_scale`: 0.1, 5.0 (vs baseline 1.1)
- `softening`: 0.001, 1.0 (vs baseline 0.1)

### 2. `evaluate_psnr.py`
**Purpose**: Enhanced PSNR evaluation with frame-range analysis.



**Usage**:
```bash
python evaluate_psnr.py \
    --baseline_dir baseline_output \
    --modified_dir modified_output \
    --output_file psnr_results.json
```

### 3. `run_material_simulations.py`
**Purpose**: Automated script for running both metal and snow material simulations.


**Usage**:
```bash
python run_material_simulations.py
```

### 4. Material Configuration Files

**`pillow2sofa_metal.json`**:
- Material type: "metal"
- Uses metal constitutive model behavior
- Same base physical properties as snow for fair comparison

**`pillow2sofa_snow.json`**:
- Material type: "snow" 
- Uses snow constitutive model behavior
- Same base physical properties as metal for fair comparison

Both configs use identical base parameters (E=1e4, density=2000, nu=0.3) to isolate MPM parameter effects.

## 📊 Key Results Summary

From `complete_parameter_study.json`:

### **Complete Results Table**:
| Material | Parameter | Baseline | New Value | PSNR | Effect Level |
|----------|-----------|----------|-----------|------|--------------|
| Metal    | grid_v_damping_scale | 1.1 | 0.1 | **16.46** | 🔴 Excellent |
| Snow     | grid_v_damping_scale | 1.1 | 0.1 | **16.99** | 🔴 Excellent |
| Metal    | substep_dt | 1e-4 | 5e-4 | **21.01** | 🟠 Significant |
| Metal    | n_grid | 100 | 60 | **21.38** | 🟠 Significant |
| Metal    | substep_dt | 1e-4 | 2e-5 | **22.50** | 🟠 Significant |
| Snow     | substep_dt | 1e-4 | 5e-4 | **23.45** | 🟠 Good |
| Metal    | n_grid | 100 | 150 | **24.24** | 🟡 Good |
| Snow     | n_grid | 100 | 60 | **26.22** | 🟡 Noticeable |
| Snow     | substep_dt | 1e-4 | 2e-5 | **27.13** | 🟡 Noticeable |
| Snow     | n_grid | 100 | 150 | **33.27** | 🟡 Subtle |
| Metal    | softening | 0.1 | 0.001 | **70.80** | ⚪ Minimal |
| Metal    | softening | 0.1 | 1.0 | **70.92** | ⚪ Minimal |
| Metal    | grid_v_damping_scale | 1.1 | 5.0 | **71.07** | ⚪ Minimal |
| Snow     | grid_v_damping_scale | 1.1 | 5.0 | **90.07** | ⚪ Minimal |
| Snow     | softening | 0.1 | 1.0 | **90.20** | ⚪ Minimal |
| Snow     | softening | 0.1 | 0.001 | **90.67** | ⚪ Minimal |

### **Material-Specific Insights**:
- **Metal is more sensitive** to parameter changes than snow (consistently lower PSNR)
- **Grid damping reduction (0.1)** creates most dramatic visual differences in both materials
- **Heavy damping (5.0) and extreme softening** have minimal visual impact (PSNR 70-90)
- **Grid resolution and timestep changes** show clear parameter sensitivity (PSNR 20-35)
- **Snow shows higher resistance** to extreme parameter changes (higher PSNR values)

## 🚀 How to Reproduce Results

### Prerequisites
- **PhysGaussian repository** cloned and set up (original repo)
- **Trained model**: `../pillow2sofa_whitebg-trained/` (Download the pillow2sofa_whitebg-trained model from the original repo and place it in a folder named 'pillow2sofa_whitebg-trained' at the same level as the PhysGaussian repo.)
- **Python environment** with required dependencies (PyTorch, CUDA, etc.)

### Step 1: Setup PhysGaussian Repository
```bash
# Clone the original PhysGaussian repository
git clone [PhysGaussian-repo-url]
cd PhysGaussian/

# Set up the environment as per PhysGaussian instructions
# (install dependencies, set up CUDA, etc.)
```

### Step 2: Copy Submission Files
```bash
# Copy config files to PhysGaussian config directory
cp /path/to/submission/configs/pillow2sofa_metal.json config/
cp /path/to/submission/configs/pillow2sofa_snow.json config/

# Copy custom scripts to PhysGaussian root directory  
cp /path/to/submission/scripts/parameter_study.py ./
cp /path/to/submission/scripts/evaluate_psnr.py ./
cp /path/to/submission/scripts/run_material_simulations.py ./
```

### Step 3: Run Parameter Study
```bash
# Make sure you're in the PhysGaussian root directory
cd PhysGaussian/

# Run the complete parameter study
python parameter_study.py
```

This will:
1. Run metal and snow baseline simulations
2. Run 8 parameter variations for each material
3. Compute PSNR for each variation vs baseline
4. Save results to `part2_parameter_study/complete_parameter_study.json`

### Step 4: Individual Material Testing (Optional)
```bash
# Test only metal
python parameter_study.py --material metal

# Test only snow  
python parameter_study.py --material snow

# Run material simulations for Part 1
python run_material_simulations.py
```

### Expected Directory Structure After Setup:
```
PhysGaussian/                           # Original cloned repository
├── [original PhysGaussian files...]
├── config/
│   ├── [original config files...]
│   ├── pillow2sofa_metal.json         # ← Added from submission
│   └── pillow2sofa_snow.json          # ← Added from submission
├── parameter_study.py                  # ← Added from submission
├── evaluate_psnr.py                   # ← Added from submission
├── run_material_simulations.py        # ← Added from submission
└── part2_parameter_study/              # ← Generated by scripts
    └── complete_parameter_study.json
```

## 💡 Key Learning Outcomes

1. **MPM parameters have different effects** on metal vs snow materials
2. **Grid velocity damping** is the most visually impactful parameter
3. **Frame timing matters** - analyzing active deformation vs final state
4. **Extreme parameter values** are needed for meaningful visual differences
5. **Quantitative analysis (PSNR)** provides objective comparison metrics

## 🎯 **Results Analysis**

**Achieved PSNR Ranges**:
- 🔴 **16-17**: Excellent differences (grid_v_damping_scale = 0.1)
- 🟠 **21-24**: Significant differences (substep_dt variations, n_grid = 60)
- 🟡 **26-33**: Good to noticeable differences (n_grid variations, fine timesteps)
- ⚪ **70-90**: Minimal differences (extreme softening, heavy damping)

**Key Finding**: Grid velocity damping reduction creates the most dramatic visual differences, while extreme softening parameters have surprisingly little visual impact.

This comprehensive analysis provides both quantitative metrics and qualitative insights into MPM simulation parameter effects on different material types. 

## 🎥 Simulation Videos

### Metal Simulations
- Baseline: [results/metal_baseline.mp4](results/metal_baseline.mp4)
- n_grid=60: [results/metal_n_grid_60.mp4](results/metal_n_grid_60.mp4)
- n_grid=150: [results/metal_n_grid_150.mp4](results/metal_n_grid_150.mp4)
- substep_dt=2e-5: [results/metal_substep_dt_2e-5.mp4](results/metal_substep_dt_2e-5.mp4)
- substep_dt=5e-4: [results/metal_substep_dt_5e-4.mp4](results/metal_substep_dt_5e-4.mp4)
- grid_v_damping_scale=0.1: [results/metal_damping_0.1.mp4](results/metal_damping_0.1.mp4)
- grid_v_damping_scale=5.0: [results/metal_damping_5.0.mp4](results/metal_damping_5.0.mp4)
- softening=0.001: [results/metal_softening_0.001.mp4](results/metal_softening_0.001.mp4)
- softening=1.0: [results/metal_softening_1.0.mp4](results/metal_softening_1.0.mp4)

### Snow Simulations
- Baseline: [results/snow_baseline.mp4](results/snow_baseline.mp4)
- n_grid=60: [results/snow_n_grid_60.mp4](results/snow_n_grid_60.mp4)
- n_grid=150: [results/snow_n_grid_150.mp4](results/snow_n_grid_150.mp4)
- substep_dt=2e-5: [results/snow_substep_2e-5.mp4](results/snow_substep_2e-5.mp4)
- substep_dt=5e-4: [results/snow_substep_5e-4.mp4](results/snow_substep_5e-4.mp4)
- grid_v_damping_scale=0.1: [results/snow_damping_0.1.mp4](results/snow_damping_0.1.mp4)
- grid_v_damping_scale=5.0: [results/snow_damping_5.0.mp4](results/snow_damping_5.0.mp4)
- softening=0.001: [results/snow_softening_0.001.mp4](results/snow_softening_0.001.mp4)
- softening=1.0: [results/snow_softening_1.0.mp4](results/snow_softening_1.0.mp4)

## 🌟 Bonus: Automatic Material Parameter Inference

To extend PhysGaussian for automatic parameter inference of arbitrary materials, I propose a learning-based framework that combines real-world material observations with differentiable physics simulation. Here's the proposed approach:

### 1. Data Collection Pipeline
- **Multi-modal Material Observations**: Gather real-world data of material behavior through:
  - High-speed video of material deformation
  - Force-displacement measurements
  - Surface property measurements (roughness, reflectance)
  - Material composition data (if available)

### 2. Neural Material Parameter Predictor
- **Architecture**: Design a neural network that takes multi-modal material observations as input and predicts:
  - MPM parameters (n_grid, substep_dt, grid_v_damping_scale, softening)
  - Material-specific parameters (Young's modulus, Poisson ratio, density)
  - Constitutive model selection or blending weights
- **Feature Extraction**:
  - Visual features from deformation sequences
  - Physical measurement features
  - Material composition embeddings

### 3. Differentiable Physics-based Training
- **Loss Components**:
  1. **Visual Reconstruction Loss**: Compare simulated vs. real deformation
  2. **Physical Behavior Loss**: Match measured force-displacement curves
  3. **Material Property Consistency**: Ensure predicted parameters are physically plausible
- **Training Process**:
  - Use differentiable physics simulation for end-to-end training
  - Gradient backpropagation through the physics engine
  - Progressive training from simple to complex deformations

### 4. Material Knowledge Base
- Build a database of known materials with verified parameters
- Use transfer learning to adapt to new materials
- Implement few-shot learning capabilities for rapid adaptation

### 5. Validation Framework
- **Physical Validation**: Compare predicted behavior with real material tests
- **Visual Validation**: Assess visual fidelity of simulated results
- **Cross-material Verification**: Test generalization across material categories

This framework would enable PhysGaussian to automatically adapt to new materials while maintaining physical plausibility and visual quality. The multi-modal approach ensures robust parameter inference, while the differentiable physics training allows for direct optimization of simulation parameters. 