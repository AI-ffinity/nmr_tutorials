# Guide to Set Up 4D NMR Experiments

## Setting Up NMR Experiments

### Downloading Ubiquitin's Parameter Set
For a smooth configuration of your spectrometer, download Ubiquitin's parameter set (the Topsin directory including spectra and parameters) from this Google drive link. This parameter set is from a 600 MHz magnet (e.g. generated with “wpar”) and can be adapted to your machine using “paracon” and some further fiddling.

In the "Complete_experiments" folder, you will find the following experiments:
- Experiment 3: 13C HSQC
- Experiment 4: 15N HSQC
- Experiment 101: Full 4D HCNH

Next, you can find experiments for individual planes of the 4D experiment derived from Experiment 101:
- Experiment 104: F1-F4, H-H
- Experiment 105: F2-F4, C-H
- Experiment 106: F3-F4, N-H

In the "WPAR_all" directory, you will find parameter sets from all experiments, as these were generated for each one. They are from our 600 MHz spectrometer because the most recent experiments were conducted on it, and I have the processing pipeline set up for those pulse programs.

#### Spectrometer Setting Adjustments
But beware, if you tweak the spectrometer parameters then you might also need to modify hard code parameters in the pulse sequence! A user did "getprosol" on an 800 MHz spectrometer using our Ubiquitin's settings from the 600 MHz spectrometer, but the HH plane of 4D (13C)HMQC-NOESY-(15N)HSQC (ns=8) looked weird. The fix was to set SSB in F1 to 2 instead of 0. After that, the HH plane looked good and overlaid nicely with the test experiment of Ubiquitin we sent to him.

Download the planes from 4D HCNH NOESY measured on our 850 MHz with Ubiquitin sample. You can use the data either to check the parameters or do the setup from our parameters directly. If you chose the other option, you definitely have to go first to edasp and click default to set wiring and frequencies for your hardware. Also, you may need to change DIGTYP to the one your hardware uses. Then you need to recalibrate the pulses and that should be it. I suggest not to use getprosol as the pulses may be used in a different way than Bruker assumes. It is important to check first with an easy sample that you are getting signals, and the spectrum looks as expected.

[Google Drive Link](https://drive.google.com/drive/folders/1MJaQDYZ0T69Zc-JC1VrY-RWwws8zJBEa?usp=sharing)

## Feasibility Assessment with 2D Experiments

### 15N HSQC (hsqcedetf3gpsi2)
Begin with the 15N HSQC using the hsqcedetf3gpsi2 pulse sequence to achieve in-phase peaks for backbone HN and anti-phase peaks for side-chains HN. This experiment is necessary for chemical shift assignment with 4D-GRAPHS.

### 13C HSQC (hsqcedetgp)
Conduct a 13C HSQC experiment for in-phase peaks of CH, CH3, and anti-phase for CH2. This experiment is also necessary for chemical shift assignment with 4D-GRAPHS. We don't measure the aromatics in the 13C HSQC. The reason is that we use 13C HSQC hsqcedetgp just to identify the CH2 for the assignment. Besides that, the 4D HCNH NOESY is primarily for the aliphatic C-H - we see only part of the aromatic carbons in the NOESY. But in any case, it's useful to have the aromatic C-H in 13C HSQC, but for them, we don't need the hsqcedetgp.

### 4D HMQC-NOESY-HSQC (HCNH) Pulse Sequence
Download the 4D HMQC-NOESY-HSQC pulse sequence file, as it's not available in Bruker's Topspin. Below are some representative parameters we used in the past when we measured only one 4D HCNH NOESY spectrum. Highlighted values need to be adjusted for each protein individually.
- Transfer of magnetization between 1H (t1) and 13C (t2) was done using an HMQC building block, with 1H chemical shift evolution in a semi-constant time manner.
- 1H (t4) to 15N (t3) magnetization transfer used a reverse HSQC after a 70 ms NOESY mixing time.
- Spectral widths: 12,500 (acq.) x 30 ppm (15N) × 40 ppm (13C) × 12,5 (1H) Hz.
- Indirect detection times: 50 ms (15N), 10 ms (13C), 20 ms (1H).
- This corresponds to 100 (15N) x 80 (13C) x 200 (1H) = 1.6M hypercomplex points
- Used 8 scans per increment with an 8-step phase cycle and 1.0 s delay.

### Quality Assessment
Evaluate the HN, HC planes to assess quality indicators such as signal-to-noise ratio, peak sharpness, cross-peak intensity, and the absence of artifacts. Additionally, check the H-H 2D plane for calibrating the mixing time for the 4D NOESY experiment(s). If the protein is small (<= 10 kDa), then only one 4D HCNH NOESY with intermediate mixing time (usually 70 ms) is sufficient. For larger proteins we measure twice this experiment with varying mixing times (see below). We may also measure the CBCA(CO)NH to help 4D-GRAPHS in the assignment in challenging cases.

### Mixing Times Configuration
Decide on the range and increment of mixing times (e.g., 30 ms, 40 ms, up to 80 ms). Use a lower mixing time (e.g. 50 ms) for resonance assignment as NOEs are generally stronger, and a higher mixing time (e.g. 80 ms) for structure calculations to detect weak long-range NOEs.

### NUS Setup
Parameters suggested based on our previous publication:

- **Number of points**: We used 5000 NUS points. Generally, you can go very low with sampling density on simple and robust samples; however, usually 5% sampling is a reasonable bet. Adjust the sampling amount (= density) or number of scans (and/or d1 delay) to optimize the signal-to-noise ratio. For smaller proteins like Ubiquitin, fewer scans might be sufficient.

- **Schedule**: We used Poisson-Gap schedule. It can be generated here: nus@HMS (harvard.edu) (mind that the number of points in the indirect dimensions should be half the corresponding TD from TopSpin, i.e., if TD F3 is 32 you need to type 16 into the generator). Save the generated schedule and provide the absolute path to TopSpin. Tip: make it short otherwise TopSpin will cut the path string and throw an error. Ensure that the estimated measurement time of the NUS is what you expect.


