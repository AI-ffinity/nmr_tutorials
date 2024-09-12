Tutorials:  http://www.nmr.chem.uu.nl/~abonvin/tutorials/Assignment-Data/assignment.html
            http://www.nmr2.buffalo.edu/nesg.wiki/Resonance_Assignment/Sparky


### Sparky NMR Analysis Quick Guide

**Finding and Loading Spectra:**
- Navigate to your NMR data directory and execute `find . -name 2rr` to locate all 2D spectrum files (TOCSY, ROESY, NOESY).
- Load the identified files into Sparky for analysis.

**Viewing Options and Pointer Modes:**
- Access spectrum viewing options by `vt` shortcut or through `View -> View options`. Alternatively, right-click inside a spectrum window.
- Default pointer mode can be initiated via `View -> Pointer Modes` or with `F1-F12` keys.

**Peak Selection and Manipulation:**
- Select peaks using `F8`.
- Adjust contour levels with the `ct` shortcut to modify signal visibility.
- Move or delete peaks by switching to "select" mode, using the mouse to drag or select, and pressing the delete key to remove peaks.
- Undo peak deletions with `eu`.

**Peak Labeling and Copying:**
- To label a peak, type `at` and fill in the details in the prompt for residue and atom assignment.
- Copy peaks with assignments using `oc` (ornament copy), then paste using `op` in another spectrum window.

**Spectrum Overlay and Printing:**
- Overlay spectra using `ol` after ensuring axes are named identically.
- Print contour plots to a PostScript printer with `pt`; save outputs directly if supported.

**Peak Assignment Commands:**
- Assign or select peaks using specific commands like `pa` for all peaks, `pF` for fully assigned, or `pL` for long range assignments.
- Change peak color selection with `pC` and invert selections with `pI`.

**Miscellaneous Commands:**
- Display axis atom names with `xa`.
- Duplicate spectrum views for comparison with `vd`.
- Adjust label font sizes in contour plots using `oz`.
- For precise plotting dimensions, refer to [Plotting spectra with Sparky](http://nmrwiki.org/wiki/index.php?title=Plotting_spectra_with_Sparky).

**View Management:**
- Hide or reveal views using `vh` to hide, or select by name from the View menu to reveal.
- Manage crowded screen space by iconifying or maximizing views as needed.

**Additional Resources:**
- For chemical shift statistics and starting points for assignments, check commands under `shift.tcl`.
