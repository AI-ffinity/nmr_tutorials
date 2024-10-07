# This must be integrated to 3D.md (2.10.2024).
# Phase Correction on a 3D Spectrum (13C-edited NOESY) 
# E.g. Carbonic_Anhydrase_II_wt/AIffinity_950/81/ and 83/

## Steps for Phase Correction

1. **Identify Region of Interest (ROI):**
   - The vertical lines in the center of the F2-F3 plane represent water. Pulse sequences are designed to be symmetrical
, meaning the space before and after the water line should be the same.
   - Note down the start and end positions of the ROI (e.g., 390-1990).

2. **Open the Raw 3D Spectrum:**
   - Issue the commands:
     ```sh
     rser 1
     qsin
     fp
     ```

3. **Manual Phase Correction:**
   - Start manual phase correction on F1 with `.ph`.
   - Align the noise "baseline" horizontally.
   - Once optimal PHC0 and PHC1 values are found, save them to the raw 3D.

4. **Recreate 2D Projections:**
   - Open the raw 3D spectrum and issue `xfb` to create the 2D projections.
   - If the spectrum looks half blue and half green, in the raw 3D set `PHC0 += 90` and repeat `xfb`.

5. **Fourier Transform:**
   - If satisfied with the phase correction, open the raw 3D and conduct Fourier transform with `ft3d`.
   - Note: If the spectrum was measured without NUS, no NUS reconstruction is needed.

# Baseline Correction on a 3D Spectrum

## Steps for Baseline Correction

1. **Increase FID Dimensions:**
   - Increase FID dimensions by x2, maximum x3 (e.g., if the dimension size is 60).

2. **Set Baseline:**
   - Choose a baseline where there are no peaks. In the proton dimension, set `ABSF1 -> 9.0 ppm` and `ABSF2 -> -4.0 ppm`.

3. **Fourier Transform:**
   - Perform Fourier transform with `ft3d`.

4. **Contour Level Adjustment:**
   - Click on the "hill" icon, set Contour level sign to positive, Level increment to 1.2, and the number of levels to 30.

5. **Navigate and Adjust Peaks:**
   - Navigate in depth (F2) by clicking the "+" icon until you reach two overlapping peaks.
   - Note down the plane number (e.g., 27/256).
   - Iterate with different FID sizes, window functions, and linear predictions until the peaks separate. Do not apply 
linear prediction on the proton dimension because many points are acquired, but it can be done in the direct dimension. 
Avoid overdoing it.

6. **Baseline Correction:**
   - Perform baseline correction with the commands:
     ```sh
     tabs1
     tabs3
     ```
   - This corrects the baseline in F1 and F3 dimensions.
