# Referencing Spectra in Topspin with BioTop (RECOMMENDED)

- If you don't have the **BioTop** Topspin extension, install the spectrometer-related dependencies by running `expinstall` 
and keeping the default values.
- Execute `biotop` to open the browser window.
- Set the measurement conditions correctly: **Labeling**, **Solvent**, **Tube**, **Temperature**. You can also provide 
  the FASTA sequence of the protein, and BioTop will automatically calculate the **Molecular size**. (However, the MW does 
  not affect the axes shift during referencing.)
- Once ready, click **Close** and execute the command:
  ```text
  btproc biorefonly
  ```
- You are all set. The axes should have shifted—check that they are correct.

> **Note**  
> BioTop fails to reference 4D spectra and their 2D projections. In that case, you will use the 2D projections to align
> the 4D spectrum to the HSQC spectrum(s) [during peak picking in POKY](../../SPARKY_and_POKY/Peak_picking_4D_spectrum).

---

# Calibrating (aka Referencing) Manually All Your 2D, 3D, 4D Spectra in Topspin

> **Calibration** is the process of using a referenced spectrum (e.g., `1H-15N HSQC`) to reference another spectrum
> (e.g., `4D HCNH NOESY`).

1. **Select the common axes** between your 2D reference spectrum (for example, the `15N HSQC`) and your 3D or 4D spectra.
   - Example: For a 15N-edited 3D NOESY → `F1: H, F2: N, F3: HN`  
     and a 4D HCNH NOESY → `F1: C, F2: HC, F3: N, F4: HN`  
     you might choose `F2-F3` (for the 3D) and `F3-F4` (for the 4D) to match the dimensions of the reference `15N HSQC`.
   
2. **Create the N-HN positive projections** to identify common peaks with strong signals (which will be used for calibration):  
   - For the 3D NOESY (15N-edited): 
     ```text
     projplp 23 all all 23
     ```  
   - For the 4D HCNH NOESY:
     ```text
     projplp 34 all all 34
     ```
   This will create projections of the planes that correspond to the dimensions matching the `15N HSQC`.

3. **Pick a reference peak in the `15N HSQC`**:
   - Go to the `15N HSQC`, type `.pp` to manually pick a peak, select the chosen reference peak, type `peaks`, 
     and note down its coordinates in ppm.

4. **Go to the 3D spectrum** and display its `F2-F3` plane:
   - Click on the "23" icon to display the `F2-F3` plane.
   - Type `.md` and select and drag the `15N HSQC` spectrum into the display. In the left lower panel, increase contour 
     levels to see the strong signals clearly without showing too much noise.
   - Select the 3D spectrum and start navigating through the `F1` axis by left-clicking and dragging on the "up-down arrow" 
     icon.  
   - While you navigate, watch for the reference peak from the `15N HSQC` that should start appearing as a strong signal 
     in the overlaid `F2-F3` plane.  
   - Once you see the strong signal of the selected reference peak, stop dragging, place your cursor at the peak center, 
     and note its **index(F1)** coordinate (not the ppm coordinate).

5. **Return to the `F2-F3` plane** in the 3D NOESY:
   - Click the "return" icon to go back to the full `F2-F3` plane view.
   - Click the "E" icon and select the `F2-F3` visible plane.  
   - Enter the **index(F1)** you noted down into the text box next to that plane.

6. **Zoom in on the reference peak**:
   - You should now see the reference peak with a strong signal.
   - Zoom in and type `.cal`, then **left-click** at the center of the reference peak.
   - In the pop-up window, enter the ppm coordinates you noted from the `15N HSQC`.  
   - Click **OK**. Both the `F2` and `F3` axes of the 3D NOESY will be shifted accordingly.

7. **Repeat the procedure for the `34` projection** of the 4D NOESY to calibrate it.

---

# Authors
- Thomas Evangelidis