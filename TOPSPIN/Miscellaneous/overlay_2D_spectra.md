# Visualizing and Modifying Overlaid Spectra in Bruker Topspin 4.1.4

## Example: Overlay of Spectra HSQCETF3GPSI / o3p 119 ppm (Exp.no. 2_1) with 4D(HChmqc)noesy(NHhsqc) / 600 MHz F3–F4 (Exp.no. 106_1)

---

This tutorial guides you through the process of visualizing and modifying overlaid spectra in Bruker Topspin 4.1.4, using the example of overlaying spectra from experiments **2_1** and **106_1**.

### Table of Contents

- [Opening Spectra](#opening-spectra)
- [Entering Overlay Mode](#entering-overlay-mode)
- [Adding a Second Spectrum](#adding-a-second-spectrum)
- [Overlay Options and Toolbar Explanation](#overlay-options-and-toolbar-explanation)
- [Exiting Overlay Mode](#exiting-overlay-mode)
- [Adding More Spectra to the Overlay](#adding-more-spectra-to-the-overlay)
- [Changing Peak Contour Levels](#changing-peak-contour-levels)

---

## Opening Spectra

1. **Open the First Spectrum:**

   - Navigate to the **experiment list** on the left side of the Topspin interface.
   - Open the spectrum from **Exp.no. 2_1** by either:
     - Dragging and dropping it into the workspace.
     - Clicking on the spectrum name.

## Entering Overlay Mode

1. **Activate Overlay Mode:**

   - Click on the **"Multiple display [.md]"** button in the toolbar.
   - A dialog will open on the lower left, displaying the names of the overlaid spectra.

## Adding a Second Spectrum

1. **Add the Second Spectrum:**

   - Add the spectrum from **Exp.no. 106_1** by either:
     - Dragging and dropping it onto the currently open spectrum.
     - Clicking on its name in the experiment list.
   - The second spectrum's name will appear in the overlay dialog on the left.

   > **Note:** The units of the spectra must match for proper overlay.

## Overlay Options and Toolbar Explanation

Once you have overlaid the spectra, several options become available for manipulation and customization. Below is an explanation of the buttons found in the toolbar at the top of the overlay window, listed from left to right:

1. **Deselect All Datasets**  
   *Deselects all spectra in the overlay.*

2. **Reset Individual Scaling and Shift**  
   *Resets any scaling or shifting adjustments made to the spectra.*

3. **Remove All Selected Datasets from Display**  
   *Removes selected spectra from the overlay. Note that the template spectrum cannot be removed using this option.*

4. **Move the Selected Dataset in the List Up**  
   *Moves the selected spectrum up in the overlay list.*

5. **Move the Selected Dataset in the List Down**  
   *Moves the selected spectrum down in the overlay list.*

6. **Copy the Contour Levels from First to Other Datasets**  
   *Normalizes the contour levels of all spectra to match the first spectrum.*

7. **Show Previous File for Comparison**  
   *Displays the previous spectrum file for comparison purposes.*

8. **Show Next File for Comparison**  
   *Displays the next spectrum file for comparison purposes.*

9. **Edit the "Show Next/Previous" Options**  
   *Allows customization of the options for displaying next or previous files.*

10. **Scale the Selected Spectra ×2**  
    *Doubles the scale (intensity) of the selected spectra.*

11. **Scale the Selected Spectra ÷2**  
    *Halves the scale (intensity) of the selected spectra.*

12. **Scale the Selected Spectra**  
    *Opens a dialog to input a specific scaling factor for the selected spectra.*

13. **Shift the Selected Spectra Up/Down**  
    *Vertically shifts the selected spectra.*

14. **Move the Selected Spectra Around**  
    *Allows free movement (both horizontally and vertically) of the selected spectra.*

15. **Shift the Selected Spectra Left/Right**  
    *Horizontally shifts the selected spectra.*

## Exiting Overlay Mode

- **To exit overlay mode:**

  - Click the **"Return [.ret]"** button in the toolbar.

  > **Note:** Topspin remembers the combinations of overlaid spectra. The next time you enter overlay mode, the last overlay setup will reappear.

## Adding More Spectra to the Overlay

- **To add additional spectra:**

  - Drag and drop or click on the respective spectrum names in the experiment list.

  > **Note:** When overlaying many spectra, peak colors may repeat. To change the color of peaks:
  >
  > - Right-click on the spectrum.
  > - Select **"Spectra Display Preferences"**.
  > - Choose a new color for the peaks.

## Changing Peak Contour Levels

- **To adjust peak contour levels for a specific spectrum:**

  1. **Select the Spectrum:**

     - Click on the spectrum whose contour levels you wish to change.

  2. **Adjust Contour Levels:**

     - Use the **scroll function** of your mouse (mouse wheel) to increase or decrease the contour levels interactively.

---

# Authors

  - Lisa-Maria Weinhold