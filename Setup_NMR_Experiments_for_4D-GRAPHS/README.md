# Guide to Set Up 4D NMR Experiments

## Setting Up NMR Experiments
### Useful links:
- https://nesgwiki.chem.buffalo.edu/index.php/Main_Page
- https://docs.google.com/document/d/10K0E-0WJLDmBAJ4hL7NtagGtRenpb2_KYGo626Ufo6I/edit?usp=sharing
- https://docs.google.com/document/d/1sFsTlhKcgcQ7EOTAfzFYBbgGZgjL1Y1L9hCSZisr1dI/edit?usp=sharing
- https://docs.google.com/document/d/1-G85BHjtCY-79RyG-cctNSj8fIh2jNmi4OUSO0uOYUg/edit?usp=sharing
- https://ethz.ch/content/dam/ethz/special-interest/biol/mol-biol/bnsp-dam/NMRmanual/Topspin-ver4.pdf

# Steps
- Tuning and Matching: Adjust the probe for optimal sensitivity and performance. 
- Deuterium Lock 
- Shimming: Optimize the magnetic field homogeneity over the sample volume. 
- Pulse Calibration: Calibrate pulse widths for uniform flip angles across the sample.
- Setting Parameters: Adjust spectral width, number of scans, relaxation delay, etc., to optimize signal-to-noise ratio and resolution.
- Temperature Calibration: Maintain a consistent temperature throughout the acquisition to ensure data consistency.
- Chemical shift referencing

Advanced operation

    Deuterium pulse width calibration and decoupling


### Downloading Ubiquitin's Parameter Set (OBSOLETE: it's Novacek-Tripsianes pp which we don't use anymore)
For a smooth configuration of your spectrometer, download Ubiquitin's parameter set (the Topsin directory including 
spectra and parameters) from this Google drive link. This parameter set is from a 600 MHz magnet (e.g. generated with 
`wpar` command) and can be adapted to your machine using `paracon` and some further fiddling.

In the "Complete_experiments" folder, you will find the following experiments:
### OBSOLETE: update the folder names
- Experiment 3: 13C HSQC
- Experiment 4: 15N HSQC
- Experiment 101: Full 4D HCNH

Next, you can find experiments for individual planes of the 4D experiment derived from Experiment 101:
### OBSOLETE: update the folder names
- Experiment 104: F1-F4, H-H
- Experiment 105: F2-F4, C-H
- Experiment 106: F3-F4, N-H

In the "WPAR_all" directory, you will find parameter sets from all experiments, as these were generated for each one.

#### Spectrometer Setting Adjustments
Download the planes from 4D HCNH NOESY measured on our 850 MHz with Ubiquitin sample. You can use the data either to 
check the parameters or do the setup from our parameters directly. If you chose the other option, you definitely have 
to go first to `edasp` and click default to set wiring and frequencies for your hardware. Also, you may need to change 
`DIGTYP` to the one your hardware uses. Then you need to recalibrate the pulses and that should be it. 
It is important to check first with an easy sample that you are getting signals, and the spectrum looks as expected.

[Google Drive Link](https://drive.google.com/drive/folders/1MJaQDYZ0T69Zc-JC1VrY-RWwws8zJBEa?usp=sharing)

## Feasibility Assessment with 2D Experiments

### 15N HSQC (hsqcedetf3gpsi2)
Begin with the 15N HSQC using the hsqcedetf3gpsi2 pulse sequence to achieve in-phase peaks for backbone HN and anti-phase peaks for side-chains HN. This experiment is necessary for chemical shift assignment with 4D-GRAPHS.

### 13C HSQC (hsqcedetgp)
Conduct a 13C HSQC experiment for in-phase peaks of CH, CH3, and anti-phase for CH2. This experiment is also necessary 
for chemical shift assignment with 4D-GRAPHS. We don't measure the aromatics in the 13C HSQC. The reason is that we use 
13C HSQC hsqcedetgp just to identify the CH2 for the assignment as we don't see aromatic peaks in the 
4D HCNH NOESY.

### 4D HCNH NOESY Pulse Programs (pp)
We currently use two 4D HCNH NOESY pp, which are both available in the latest Topspin version under the names: 
1) `sfhmqc_noe_sfhmqc_4Dhcnh.fl` is the 4D [13C,1H]-SOFAST-HMQC-NOESY-[15N,1H]-SOFAST-HMQC
2) `hsqcnoesyhsqccngp4d` (C13)HSQC-NOESY-(N15)HSQC 4D sequence with homonuclear correlation via dipolar coupling

Topspin has also a 4D 13C SOFAST HMQC-NOESY- 15N SOFAST HMQC for methyl/H(N) NOEs named `sf_mehmqcnoesyhmqchcnh4d`, which
is suitable for very large proteins.

### 4D HCCH NOESY Pulse Programs (pp)
We currently use two 4D HCCH NOESY pp, which are both available in the latest Topspin version under the names: 
1) `sfhmqc_noe_sfhmqc_4Dhcch.fl` is the 4D [13C,1H]-SOFAST-HMQC-NOESY-[15N,1H]-SOFAST-HMQC
2) `hsqcnoesyhsqcccgp4d` (C13)HSQC-NOESY-(C13)HSQC 4D sequence with homonuclear correlation via dipolar coupling

Topspin has also a 4D SOFAST HMQC-NOESY-SOFAST HMQC for methyl/methyl NOEs named `sf_mehmqcnoesyhmqc4d`, which
is suitable for very large proteins.

### Selection of 4D pp
To select the most suitable 4D pp for your sample, evaluate the HC planes to assess quality indicators such as 
signal-to-noise ratio, peak sharpness, cross-peak intensity, and the absence of artifacts.


### Mixing Times Configuration
Use an intermediate mixing time based on your protein. Usually 70 ms is good choice.

### NUS Setup

- **Number of points**: We used 5000 NUS points. Generally, you can go very low with sampling density on simple and 
robust samples; however, usually 5% sampling is a reasonable bet. Adjust the sampling amount (= density) or number of scans (and/or d1 delay) to optimize the signal-to-noise ratio. For smaller proteins like Ubiquitin, fewer scans might be sufficient.

- **Schedule**: use Topspin's NUS scheduler.


