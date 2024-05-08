# Sparky User Manual

## Common Commands

Sparky offers a variety of two-letter accelerators to streamline your workflow. Below, you'll find a categorized list of these commands along with brief descriptions of their functionalities.

### Peak and Spectrum Manipulation

- **a1, a2, a3:** Add spectral width (SW) to a peak in the F1, F2, or F3 dimension. Useful for aliased spectra.
- **A1, A2, A3:** Subtract SW from a peak in the F1, F2, or F3 dimension. For handling aliased spectra.
- **at:** Assignment tool. Assists in assigning peaks.
- **cl:** Adjust the color of an ornament.
- **ct:** Adjust contour levels and colors.
- **ci:** Inverse background color, e.g. black -> white.
- **dr:** Delete resonances not used in any peak assignment. Cleans up the resonance list.
- **eu:** Undo the last peak manipulation.
- **it:** Integration tool for peak integration.
- **kr:** Restrictive peak picking tool.
- **lt:** Opens the peak list for a given spectrum, offering various options.
- **oc:** Ornament copy. Copies assignment/label information between spectra.
- **ol:** Overlay views. Compares different spectra.
- **op:** Ornament paste.
- **oz:** Adjust the size of an ornament.
- **pa:** Select all peaks in a spectrum.
- **pc:** Peak center. Refines the centering of peaks.
- **pv:** Provides a list of sizes and peak counts in all open spectra.
- **rl:** Opens the resonance list for the project, offering various functions and displays.
- **rp:** Read in a list of peaks in Sparky format from external tools like AutoAssign or PINE, aka load sparky list file with assignments to existing spectrum:
    ```
    Assignment         w1         w2  
      Q47NE2-HE22    110.585      6.621 
      Q77NE2-HE22    111.920      6.782 
      N29ND2-HD22    111.860      6.792 
      N73ND2-HD22    111.747      6.806 
      N39ND2-HD22    111.951      6.842 
      N85ND2-HD22    111.527      6.876 
      N64ND2-HD22    114.934      6.913 
           G50N-H    106.253      7.121 
      Q47NE2-HE21    110.576      7.267 
            85N-H    110.658      7.322 
    ```
    Note: For peaks with assignments not following the convention [A-Z][0-9]+[A-Z0-9']+-[A-Z0-9'], use a custom script that modifies the .save file to ensure compatibility.
- **rr:** Resonance rename. Renames resonances for consistency.
- **st:** Spectrum tool. Useful for global axes shift corrections.
- **tb:** Table of resonances for the project. Helps in identifying missing assignments.
- **vc:** View centering. Centers the view on a specific peak, especially useful in 3D spectra.
- **vd:** View duplicate. Duplicates the view of a spectrum into another window.
- **vR:** Show assignments on the edge of the spectrum.
- **vS:** Show 1D slice on the edge of the spectrum.
- **vt:** View settings. Adjusts various spectral settings, including aspect ratio.
- **xa:** Show nucleus type on axis.
- **xe:** Special Python command for saving the peak list in Xeasy format.
- **xr:** Roll axes. Useful for navigating 3D and 4D spectra.
- **xx:** Axis transpose. Swaps the axes.
- **yt:** Synchronize axes of various spectra. Ideal for analyzing series of 3D or 4D spectra.
- **zf, zi, zo, zp:** Zoom full spectrum, zoom in, zoom out, and zoom to the previous view, respectively.

## Pointer Modes

Enhance your interaction with Sparky using different pointer modes:

- **F1:** Selection mode. Selects elements within the spectrum.
- **F6:** Add a label to your spectrum.
- **F7:** Draw a line, useful for marking or measuring.
- **F8:** Peak picking mode. Identifies peaks within the spectrum.
- **F10:** Integration mode. For integrating areas under peaks.
- **F11:** Zoom mode. Zoom in and out of specific areas of the spectrum.

## Tips for Handling Peaks

When using the **rp** command to load a list of peaks, ensure the assignments follow the conventional format ([A-Z][0-9]+[A-Z0-9']+-[A-Z0-9']). For peaks with non-conventional names, consider using a custom script that modifies the .save file to ensure compatibility.

## References

- [Plotting spectra with Sparky](http://nmrwiki.org/wiki/index.php?title=Plotting_spectra_with_Sparky)
- [Resonance Assignment/Sparky](http://www.nmr2.buffalo.edu/nesg.wiki/Resonance_Assignment/Sparky)

