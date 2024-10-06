# This must be integrated to 3D.md (2.10.2024).
# Phase Correction on a 3D Spectrum (13C-edited NOESY) 
# E.g. Carbonic_Anhydrase_II_wt/AIffinity_950/81/ and 83/

## Steps for Phase Correction


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
