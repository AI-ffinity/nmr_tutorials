---
title: "15N HSQC Titration Experiment Setup"
layout: default
---

# 15N HSQC Titration Experiment Setup

This tutorial outlines the step-by-step setup for a 15N HSQC titration experiment using an NMR spectrometer.

## Starting the Experiment

1. **Eject Current Sample:**
   - Use `sx` or `ej` to eject the current sample from the spectrometer.

2. **Insert New Sample:**
   - Command `sx <position>` starts the carousel, and the sample at the specified position will be inserted into the 
   spectrometer. Replace `<position>` with the actual position number of your sample.

## Setting Up a 1D Experiment in Folder "Praktikum"

Proceed with the following steps to set up and start the 1D experiment:

1. **Create a New Experiment:**
   - Use the command `new` to create a new experiment based on an active one. Add an appropriate description to 
   differentiate this setup.

2. **Automatic Matching and Tuning:**
   - Execute `ww` to automatically match and tune the system. Aim to align the bottom of the well with the vertical 
   central line of the display for optimal performance.

3. **Lock the Magnetic Field:**
   - Use `lock` and select "H2O + D2O" from the dropdown list. The system will measure a simple spectrum to adjust the 
   frequency, ensuring the stability of the magnetic field throughout long experiments.

4. **Automatic Shimming:**
   - Enter `topshim gui` to initiate automatic 1D shimming, which optimizes the magnetic field homogeneity.

5. **Pulse Program Setup:**
   - Input `p1` followed by `1 P1 1` to configure the pulse program settings.

6. **Start the Experiment:**
   - Use the command `zg` to start the experiment. This will initiate the acquisition of the 1D NMR spectrum.

## Setting Up a 2D Experiment in Folder "Praktikum"

1. **Create a New 2D Experiment:**
   - Use the command `new` to create a new experiment and add its details.

2. **Sample Insertion:**
   - Place your sample into a cuvette holder and use `sx <position>` to start the carousel. This command inserts the 
   sample at the specified position into the spectrometer. Replace `<position>` with the actual position number of 
   your sample.

3. **Automatic Tuning and Matching:**
   - Execute `atma` to automatically tune and match the 15N and 1H channels. Use the arrows on the display to center 
   the well on the vertical line for optimal tuning.

4. **Frequency Lock:**
   - Select "H2O + D2O" using the `lock` command. This setup measures a simple spectrum of D2O to adjust and lock the 
   frequency, ensuring magnetic field stability throughout long experiments.

5. **Shimming:**
   - Run `topshim gui` for automatic 1D shimming to optimize the magnetic field homogeneity.

6. **Pulse Calibration:**
   - Use `pulsecal` to calculate the length of the 90° hydrogen pulse P1 for 10W. This is recalculated for each sample 
   as differences, though small, depend more on buffer salt concentration and temperature than on the protein and ligand. 
   For salt concentrations > 150 mM, the pulse is longer (e.g., 14 ms). Optimal pulse length is crucial for maximizing 
   signal acquisition.

7. **Set Pulse and Power:**
   - Execute `getprosol 1H P1 xW`, for example, `getprosol 1H 0.71 10W`. Insert the previously determined value P1 with 
   the appropriate power value.

8. **Fourier Transform Check:**
   - Run `xfb` to perform a Fourier transform in both dimensions to monitor how the 2D spectrum develops. Typically, 
   signals in the 15N dimension improve more significantly than those in the 1H dimension as the experiment progresses, 
   although eventually only noise is added. This is more pronounced in small, flexible proteins or intrinsically 
   disordered proteins (IDPs), which can be recorded for longer durations.

9. **Spectrum Processing:**
   - Execute `qfp` to process the spectrum, which applies the macro for quadrature sine bell window (`qsin`), Fourier 
   transform 1D (`ft`), and phase correction (`pk`).

10. **Interactive Phase Correction:**
    - Use `.ph` for phase correction. Drag on the "0" icon and click the "save" icon when adjustments are completed.

11. **Multidisplay Mode:**
    - Enter `.md` of the "two parallel FIDs" icon to switch to multidisplay mode. This allows overlaying and comparing 
    different spectra by clicking and dragging them into the window.

12. **Baseline Correction:**
    - Perform baseline correction using `basl`. The baseline appears in red, with the spectrum in blue. This step is 
    necessary because automatic correction often fails to achieve perfect results.

13. **Monitor Progress:**
    - Run `xfb` again to continue monitoring the progress of the experiment.

## Other Useful Commands

1. **Recalculating Pulse Power:**
   - `pulse <x>W` recalculates the pulse for `<x> Watt`, which in our context is usually 10. Replace `<x>` with the actual power level you need to set.

2. **Pulse Program Commands:**
   - Use `p1` followed by `1 P1 1` to set or check the pulse program configurations.

3. **Stopping the Experiment:**
   - The command `stop` is used to halt the measurement process at any point.

4. **Setting Number of Scans and Delay:**
   - `1 NS 1` sets the number of scans to 1, optimizing the acquisition time.
   - `d1` sets the delay time between scans, allowing for system relaxation and accurate results.

5. **Enhanced Fourier Processing:**
   - Execute `efp` for a combined command sequence:
     - `em` (exponentially multiply) applies broadening with a factor of `1b`.
     - `ft` performs a Fourier transform on the 1D data.
     - `pk` applies phase correction, using phc0 and phc1 parameters to adjust the spectrum.

6. **Receiver Gain Setting:**
   - `1 RG 64` sets the receiver gain of experiment "1" to 64, optimizing signal detection and amplification. Receiver 
   gain is a crucial parameter in NMR spectroscopy that adjusts the level of amplification of the NMR signal received 
   by the hardware. Proper adjustment of the receiver gain is essential to obtain a signal with good signal-to-noise 
   ratio without saturating the receiver.
   - In case of a strong signal, too much RG will lead to a distorted spectrum and the spectrometer will issue an error message.
   - `101` is the maximum value. If you are not sure, the command `RGA` will set the correct receiver gain automatically. 

## General Remarks

- **Water Signal:** In NMR spectroscopy, water typically appears at 4.7 ppm. This is a crucial reference point for calibrating and interpreting NMR spectra, especially in aqueous samples.
- **FCOR value:** `FCOR=0.5` if `PHC0==0.0` and `PHC1==0.0`, and `FCOR=1.0` if `PHC0!=0.0` or `PHC1!=0.0` (e.g. `-90` and `180 degrees`).
- **echo-antiecho:** if this is a gradient selection experiment, then `MC2{F1}=echo-antiecho`

-----------------------------
## Authors

- **adapted by Thomas Evangelidis from an NMR course offered by Vaclav Veverka, Pavel Srb and Rozalie Hexnerova at IOCB Prague**