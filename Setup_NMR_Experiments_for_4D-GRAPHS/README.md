# Guide to Set Up 4D NMR Experiments

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
anti-phase peaks for side-chains N-H. This experiment is necessary for chemical shift assignment with 4D-GRAPHS.

### 13C HSQC (hsqcedetgp)
Conduct a 13C HSQC experiment for in-phase peaks of CH, CH3, and anti-phase for CH2. This experiment is also necessary 
for chemical shift assignment with 4D-GRAPHS. We don't measure the aromatics in the 13C HSQC. The reason is that we 
use 13C HSQC hsqcedetgp just to identify the CH2 for the assignment. Besides that, the 4D HCNH NOESY is primarily for 
the aliphatic C-H - we see only part of the aromatic carbons in the NOESY. But in any case, it's useful to have the 
aromatic C-H in 13C HSQC, but for them, we don't need the hsqcedetgp.


### Quality Assessment
Evaluate the HN, HC planes of 4D HCNH NOESY to assess quality indicators such as signal-to-noise ratio, peak sharpness, cross-peak intensity, 
and the absence of artifacts. Additionally, check the H-H 2D plane for calibrating the mixing time for the 4D NOESY 
experiment(s). We frequently use intermediate mixing time (e.g. 70 ms).

### NUS Setup
Parameters suggested based on our previous publication:

- **Number of points**: We used 5000 NUS points. Generally, you can go very low with sampling density on simple and 
robust samples; however, usually 5% sampling is a reasonable bet. Adjust the sampling amount (= density) or number 
of scans (and/or d1 delay) to optimize the signal-to-noise ratio. For smaller proteins like Ubiquitin, fewer scans 
might be sufficient.

- **Schedule**: We used Poisson-Gap schedule. It can be generated here: nus@HMS (harvard.edu) (mind that the number of 
points in the indirect dimensions should be half the corresponding TD from TopSpin, i.e., if TD F3 is 32 you need to 
type 16 into the generator). Save the generated schedule and provide the absolute path to TopSpin. Tip: make it short 
otherwise TopSpin will cut the path string and throw an error. Ensure that the estimated measurement time of the NUS 
is what you expect.


