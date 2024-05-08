# Tutorial: Peak Picking in 4D Spectrum with Sparky

This tutorial guides you through the process of peak picking in a 4D HCNH NOESY spectrum using Sparky, with a focus on working with Ubiquitin data. We'll also utilize a 15N HSQC file for synchronization and peak selection.

## Prerequisites

- Sparky installed and ready to use.
- Access to the specified Ubiquitin 4D and 15N HSQC spectrum files.

## Steps

### Loading the Spectrum Files

1. **Load the 4D HCNH NOESY Spectrum**
   - Open Sparky and load the 4D HCNH NOESY file from the specified path:
     ```
     /home2/shared_files/NMR/Ubiquitin_4D_2022_07/101_new2023/nuft/roi_6_10/4D_HCNH_NOESY_NUS_reconstructed.ucsf
     ```

2. **Load the 15N HSQC File**
   - Load the 15N HSQC file located at:
     ```
     /home2/shared_files/NMR/Ubiquitin_4D_2022_07/2/pdata/1/15N_HSQC.ucsf
     ```

### Adjusting the Spectra

3. **Correct the Contour Levels of HSQC**
   - Click `ct` to adjust the contour levels for the HSQC spectrum for better visibility.

4. **Display Nucleus Types on the 4D Spectrum Axes**
   - On the 4D spectrum, click `xa` to show the nucleus types on the axes.

5. **View the C-H Plane in the 4D Spectrum**
   - Click `xr` twice on the 4D spectrum to focus on the C-H plane.

6. **Synchronize Spectra**
   - Click `yt` to synchronize the 15N of the HSQC and 4D NOESY first, and then synchronize the 1H of the same spectra. Remember, synchronize one nucleus at a time!

### Peak Picking

7. **Switch to Peak Picking Mode**
   - Press `F8` to enter peak picking mode.

8. **Pick Peaks in the 15N HSQC**
   - With the cursor, capture all peaks in the 15N HSQC spectrum. You can later view these picked peaks by clicking `lt`.

9. **Switch Back to Peak Selection Mode**
   - Press `F1` to return to peak selection mode. To select all peaks of the spectrum, click `pa`. Note: This works for the 15N HSQC, not for the C-H planes of the 4D NOESY.

10. **Center View on C-H Plane in 4D NOESY**
    - Select a peak in the 15N HSQC and click `vc` to center the view on the corresponding C-H plane in the 4D NOESY.

11. **Pick Peaks in the C-H Plane**
    - In the C-H plane of the 4D NOESY, press `F8` to switch to picking mode and capture peaks that are real (not noise). You can delete any mistakenly picked peaks by selecting them and pressing the "Delete" key.

12. **Review and Manage Picked Peaks**
    - Use `lt` to review your picked peaks. For a better analysis, display the intensity by navigating to Options -> Data Height and sort them by 15N frequency via Options -> Sort by: "Frequency" and change "Sort axis:" to 3, then click "OK".

13. **Work with Multiple C-H Planes**
    - To open multiple C-H planes, click `vd` to duplicate the view of a 4D spectrum into another window. In each window, you can focus on different C-H planes by selecting a different 15N HSQC peak with `F1` and clicking `vc` to center it.

### Exporting Picked Peaks

14. **Export Picked Peaks for 4D-GRAPHS**
    - Click `lt` (no need to click "update"), then "Save". Ensure you include the "Data Height" in your saved data as it is necessary for 4D-GRAPHS.

