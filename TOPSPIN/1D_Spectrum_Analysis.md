# TopSpin Tutorial: 1D spectra integration, calibration and deconvolution.

---

## Integrating a 1D Spectrum

1. **Switch to Integration Mode**  
- `.int` to switch to integration mode


2. **Manual Integration of Peaks**  
- Focus on the N-H region of the spectrum (~6.5-10.2 ppm).  
- Integrate all peaks manually. Note that interactive bias or slope correction might not be effective.

3. **Save Peak Integral Data**  
- After integrating, save the results by navigating to:
  ```
  Save Region as... -> Save & Show list
  ```
- Save the list of peak integrals to a file for future reference.

4. **Calibrate a Peak's Integral**  
- Select a peak that you believe corresponds to a single NH-NH.
- Right-click on the peak and select:
  ```
  Calibrate Current Integral
  ```
- Set the value to **1.0**. This will scale the integrals of other peaks based on this reference, helping you count 
the NH-NH signals in each peak.

5. **Verify the Reference Peak**  
- To check if the reference peak you selected is correct, run the following command:
  ```bash
  awk "NR>5" 58/pdata/1/1D_normalized_peak_integrals.txt | awk '{sum+=$4} END { print "", sum }'
  ```
- The output should give you a number close to **N-1**, where **N** is the number of residues in the peptide.

6. **Optional: Deconvolution**  
- For complicated peaks, you can attempt deconvolution:
  ```
  Right-click on the peak integral -> Deconvolution -> Deconvolute & display Integrals
  ```
- Note: Deconvolution may not always be accurate, so use this feature with caution.

---

