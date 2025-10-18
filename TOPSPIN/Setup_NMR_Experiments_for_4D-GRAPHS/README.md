# OBSOLETE!!! Guide to Set Up 4D NMR Experiments

## Setting Up NMR Experiments

### Downloading Ubiquitin's Parameter Set
For a smooth configuration of your spectrometer, download Ubiquitin's parameter set (the Topsin directory including 
spectra and parameters) from this Google drive link. This parameter set is from a 600 MHz magnet (e.g. generated with 
“wpar”) and can be adapted to your machine using “paracon” and some further fiddling.

In the "Complete_experiments" folder, you will find the following experiments:
- Experiment 3: 13C HSQC
- Experiment 4: 15N HSQC
- Experiment 101: Full 4D HCNH

Next, you can find experiments for individual planes of the 4D experiment derived from Experiment 101:
- Experiment 104: F1-F4, H-H
- Experiment 105: F2-F4, C-H
- Experiment 106: F3-F4, N-H

In the "WPAR_all" directory, you will find parameter sets from all experiments, as these were generated for each one. 
They are from our 600 MHz spectrometer because the most recent experiments were conducted on it, and I have the 
processing pipeline set up for those pulse programs.

Download the planes from 4D HCNH NOESY measured on our 850 MHz with Ubiquitin sample. You can use the data either to 
check the parameters or do the setup from our parameters directly. If you chose the other option, you definitely have 
to go first to edasp and click default to set wiring and frequencies for your hardware. Also, you may need to change 
DIGTYP to the one your hardware uses. Then you need to recalibrate the pulses and that should be it. I suggest not to 
use getprosol as the pulses may be used in a different way than Bruker assumes. It is important to check first with 
an easy sample that you are getting signals, and the spectrum looks as expected.

[Google Drive Link](https://drive.google.com/drive/folders/1MJaQDYZ0T69Zc-JC1VrY-RWwws8zJBEa?usp=sharing)

## Feasibility Assessment with 2D Experiments

### 15N HSQC (hsqcedetf3gpsi2)
Begin with the 15N HSQC using the hsqcedetf3gpsi2 pulse sequence to obtain in-phase peaks for N-H2 and 
anti-phase peaks for side-chains N-H. This experiment is necessary for chemical shift assignment with 4D-GraFID.

### 13C HSQC (hsqcedetgp)
Conduct a 13C HSQC experiment for in-phase peaks of CH, CH3, and anti-phase for CH2. This experiment is also necessary 
for chemical shift assignment with 4D-GraFID. We don't measure the aromatics in the 13C HSQC. The reason is that we 
use 13C HSQC hsqcedetgp just to identify the CH2 for the assignment. Besides that, the 4D HCNH NOESY is primarily for 
the aliphatic C-H - we see only part of the aromatic carbons in the NOESY. But in any case, it's useful to have the 
aromatic C-H in 13C HSQC, but for them, we don't need the hsqcedetgp.


### Quality Assessment
Evaluate the HN, HC planes of 4D HCNH NOESY to assess quality indicators such as signal-to-noise ratio, peak sharpness, cross-peak intensity, 
and the absence of artifacts. Additionally, check the H-H 2D plane for calibrating the mixing time for the 4D NOESY 
experiment(s). We frequently use intermediate mixing time (e.g. 70 ms).

### NUS Setup
We use Topspins's NUS schedule generator. The number of NUS points and % sampling will depend on you sample. Specifically,
on the required number of scans, D1 delay, and other parameter values required to obtain good S/N.
the available spectrometer time.


# Measurement Setup for HSP90 (25 kDa) on an 850 MHz Spectrometer  
*Goal:* prepare and launch multiple **2D planes** from various **4D HCNH NOESY** pulse programs, evaluate their quality, and choose the most suitable 4D sequence.

---

## Chronological Command Log

| Command | Purpose / Action |
|---------|------------------|
| `1s te` | Set the **temperature**. |
| `lock`  | Opens a solvent‐selection dialog, reads lock parameters (from **`edlock`** table), and performs **autolock**. Suitable for solvents with multiple lock signals. *Selected solvent:* **90 % H₂O / 10 % D₂O**. |
| `edasp` | (opens **ASP** editor; parameters not modified in this run). |
| `p1`, `p3`, `p21` | Display current **pulse lengths**. |
| `atma`  | **Automatic tuning & matching** for every nucleus; repeat for every sample and probe. |
| `atmm`  | **Manual fine-tuning** after `atma`. Adjust two parameters:<br> 1. **Tuning** – align probe resonance with Larmor frequency.<br> 2. **Matching** – match probe impedance (50 Ω). *Warning:* correcting one nucleus may disturb others. |
| `topshim gui` | **Automatic / manual shimming** (homogenize B₀ in z and xy). |
| `loopadj` | Optimize lock parameters **LGAIN**, **LTIME**, **LFILTER**. |
| `pulsecalc` | Calibrate pulse lengths; essential for **¹H** (¹³C/¹⁵N vary less). |
| `getprosol …` | Retrieve / set **pre-calibrated 90° hard-pulse parameters**.<br>Example: <br>`getprosol 1H 13.29 14.529W 13C 12.0 162.93W 15N 37.8 169.82W` |
| `O1` | Set spectral center (in the observed dimension). |
| `O1P`, `O2P`, `O3P` | Set transmitter-offsets (ppm) for 1st, 2nd, 3rd nuclei. |
| `D1`–`D8` | Delay parameters (s). |
| `ZGOPTNS` | Add **compiler flags** (C-style `-D<FLAG>`) passed verbatim to the pulse programme. |

### Common `ZGOPTNS` Flags

| Flag | Typical pulse sets | Enables | Practical effect |
|------|--------------------|---------|------------------|
| `-DLABEL_CN` | Triple-resonance (HNCA, HNCACB, HSQC, …) | Double-labelled (¹³C/¹⁵N) branch | Adds ¹³C decoupling during ¹⁵N evolution; un-comments `P22`, `PL2`, delays that depend on ¹J<sub>CN</sub>. |
| `-DCALC_SP`  | BEST / “b_…” selective or BEST-TROSY | Auto-derives ¹H band-selective shapes from `cnst54/55` | Sequence generates & loads shaped pulses on the fly. |

Other useful flags:

| Flag | Purpose |
|------|---------|
| `-DPRESAT`              | Use **continuous-wave presaturation** during `d1`. |
| `-DWG` or `-DWATERGATE` | Use **WATERGATE** suppression instead of presat. |

---

## Running the 2D Plane Experiments

1. **Iterate through every 2D plane** you have set up.  
2. Launch each with `zg` (queued automatically).  
3. Inspect the resulting spectra; the best plane(s) will dictate the final **4D pulse program** for this sample.

---

## Setting Up the 4D HCNH NOESY

After selecting the optimal 2D planes, create the **4D HCNH NOESY** experiment and copy these parameter values from the chosen 2D datasets:

| Parameter | Meaning |
|-----------|---------|
| `SW{Fx}`     | Spectral width for each dimension F₁–F₄ |
| `IN_F{s}`    | Increment for delay (µs) |
| `CNST{2,4,16,18,19}{Fx}` | Various constants (mainly for ¹H; possibly for ¹³C and ¹⁵N) |
| `SPNAM26{F4}` / `SPNAM1{F4}` | Shape file name for shaped pulse |
| `P1{F4}` / `P17{F4}` | Length of the shaped pulse |

Then **run `getprosol` again** with the updated 90° parameters, e.g.:

```bash
getprosol 1H 13.29 14.529W 13C 12.0 162.93W 15N 37.8 169.82W
```

---

## Miscellaneous Commands

| Command | Description                                                                                         |
| ------- | --------------------------------------------------------------------------------------------------- |
| `ased`  | Edit **acquisition parameters** used by the pulse program.                                          |
| `qfp`   | Macro: applies a **quadrature sine-bell window (qsin)**, performs FT, then phase correction (`fp`). |

---

## Notes & Practical Tips

* **Calibration spectra** for each nucleus must be measured and adjusted before fine-tuning pulse-program parameters.
* “**number of increments**” equals the **`TD`** parameter, which sets **resolution**.

  * Slow-relaxing nuclei: higher `TD` ⇒ higher resolution.
  * Fast-relaxing nuclei: higher `TD` mainly records noise.
* **Increasing scans** improves S/N.
* FID intensity drops rapidly early and slowly later; beyond a point, extra acquisition does **not** improve spectrum quality.

---

# Authors
- Thomas Evangelidis

