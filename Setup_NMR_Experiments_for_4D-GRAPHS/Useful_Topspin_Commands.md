Here's an outline for a README.md file summarizing the basic TopSpin commands for setting up NMR experiments:

---

# TopSpin Basic Commands for NMR Experiments

This guide provides a quick reference to essential TopSpin commands for setting up and running NMR experiments.

---

## Table of Contents

- [Sample Preparation](#sample-preparation)
- [Experiment Setup](#experiment-setup)
- [Calibration](#calibration)
- [Data Processing](#data-processing)
- [Procedures](#procedures)
  - [Temperature Calibration](#temperature-calibration)
  - [1D Proton Measurement](#1d-proton-measurement)
  - [Solvent Flip-Back Calibration](#solvent-flip-back-calibration)
  - [2D Experiment Setup](#2d-experiment-setup)
  - [3D Experiment Setup](#3d-experiment-setup)
- [Helpful Tips](#helpful-tips)

---

## Sample Preparation

| Action                    | Command      | Description                                                      |
|---------------------------|--------------|------------------------------------------------------------------|
| Display lock window       | `lockdisp`   | Adjust lock gain for ~80% lock                                   |
| Inject sample             | `ij`         | Use after verifying target temperature                           |
| Lock sample               | `lock`       | Options: `[90% H2O/10% D2O]`, `[D2O]`, or `[Methanol-d4]`        |
| Adjust lock feedback      | `loopadj N`  | Set N from 1-10 for response time adjustment                     |
| Automatic tune/match      | `atma`       | Slower but more precise                                          |

## Experiment Setup

| Action                    | Command      | Description                                                      |
|---------------------------|--------------|------------------------------------------------------------------|
| Edit experiment           | `edc`        | Set up experiment name, number, and directory                    |
| Load parameters           | `rpar *.all` | Load standard parameter set (filter available)                   |
| Write data                | `wrpa`       | Save acquired and processed data                                 |
| Edit pulse parameters     | `ased`       | Set pulse sequence parameters                                    |
| Adjust acquisition params | `eda`        | Configure parameters for indirect dimensions in 2D, 3D           |

## Calibration

- **Temperature Calibration**: `calctemp`
- **90° Hard Pulse Calibration**: `HCN90`
- **DOTALL Experiment Setup**: `xxx90`
- **Set Up Bruker Experiment**: `getprosol`

## Data Processing

| Action                    | Command      | Description                                                      |
|---------------------------|--------------|------------------------------------------------------------------|
| Fourier Transform (1D)    | `ft`, `fp`   | Perform 1D Fourier transform                                     |
| Phase Correction          | `.ph`        | Interactive; `.sret` to save                                     |
| Automated Phase Correction| `apk`        | Use for simple spectra like methanol                             |
| Baseline Correction       | `abs`        | For 1D; `abs1`, `abs2` for 2D dimensions                        |
| Fourier Transform (2D)    | `xfb`        | Process both dimensions of 2D data                               |

## Procedures

### Temperature Calibration
1. Create a new experiment with `edc`.
2. Load calibration parameters: `rpar methanol4.eth`.
3. Inject methanol sample with `ij`, lock (`lock`), and set temperature (`edte`).
4. Perform tuning, shimming, and measurement with `atma; topshim; zg; ef; apk; calctemp`.

### 1D Proton Measurement
1. Set up new experiment (`edc`) and load parameters (`rpar *.eth`).
2. Set lock display (`lockdisp`) and inject sample.
3. Start automatic shimming with `topshim gui`.
4. Record spectrum with `zg`.

### Solvent Flip-Back Calibration
1. Perform 90° calibration (`HCN90`).
2. Read flipback calibration parameters (`rpar flips.all`).
3. Adjust pulse power and phase correction for solvent suppression (`gs`).

### 2D Experiment Setup
1. Start new experiment (`edc`) and load 2D parameters (`rpar *.all`).
2. Adjust acquisition and processing parameters as needed (`ased`, `eda`).
3. Begin 2D acquisition (`zg`) and process (`xfb`).

### 3D Experiment Setup
1. Set up 3D experiment similarly to 2D (`edc`, `rpar`, `ased`).
2. Process each dimension (`tf3`, `tf2`, `tf1`) with Fourier transforms.

## Helpful Tips

- **Troubleshooting Low Signal**: Increase `ns` if the signal-to-noise ratio is low.
- **Interactive Adjustments**: Use `gs` to interactively optimize acquisition parameters.
- **Save and Restore Shim Settings**: Use `rsh` and `wrpa` for shim profiles.

---