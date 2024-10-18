# Measurement of S/N ratio in 15N-edited 3D NOESY and in 4D HCNH NOESY.

------------

15N-edited 3D NOESY -> F1: H, F2: N, F3: HN
4D HCNH NOESY -> F1: C, F2: HC, F3: N, F4: HN

* First we look up at the N-HN positive projections to identify common peaks between the two spectra 
with strong signal, which we will use for comparison of the S/N.
* `projplp 23 all all 23` in 15N-edited 3D NOESY and `projplp 34 all all 34` in 4D HCNH NOESY.
* Open the `34` projection of the 4D and type `pp` for automated peak picking. Switch the 
"Minimum intensity" to the "highest contour level" and then click "OK".
* Type `peaks` and sort the peaks by intensity. Then iterate through all of them from the 
beginning one by one, double-clicking and identifying non-overlaping peaks. You just need 3-5
with strong signals, not all of them. For example, I chose peaks 221, 212, 209, 207 (!), 204 (!).
* Note down the coordinates of the chosen peaks, switch to the `23` projection of the 3D NOESY
and look them up.

*ALTERNATIVE AVENUE*
* overlay the F2-F3 projection of the 3D NOESY to the F3-F4 projection of the 4D NOESY.
* Search for common, well-shaped, strong signal peaks. I selected those in green circles.
* Close all opened spectra.
* Open the processed 3D NOESY, switch to the F2-F3 plane representation by clicking to the "23" icon, overlay on it
the F2-F3 projection and start navigating in the F1 dimension by left-click and dragging on the "double-headed arrow" 
icon until the first selected peak starts to appear in the F2-F3 plane of the 3D. Note down the index of that plane on
the F1 dimension (botton left), e.g. 98.
* Exit the overlay mode and issue the `rser2d ` command. The following window will appear.
* Set the values shows in the image and click "OK".
* In the new EXPNO that will appear, double-click on spectrum 1 (raw 2D plane from the 3D NOESY) and issue `xfb` to process it.

** Signal-to-Noise Ration Measurement **
* Enter interactive integration mode by entering the command ".int".
* Click on the tool button "define new integration region".
* First integrate the signal of interest: identify the selected peak and drag a region around it while keeping the left mouse button depressed. When the button 
is released, a popup menu is opened. Click on an "integrate" entry, e.g. the first one (which one doesn't matter).
* Then define the noise area: Move the mouse to a signal-free region and drag again the mouse to
mark the region. Again click on an "integrate" entry when releasing the left mouse button.
* Click on the "Export integration regions" icon and select "Export integration regions".
* The "wmisc" window is opened. Click on "Write new...". Enter a filename, e.g. "int2d_idx98". The file is stored in the
`.../list/intrng2d` directory, which can be inspected using the `rmisc` command. 
* Exit the integration mode.
* Perform 2D-SINO Calculation: issue the `sino2d` command and in the window that pops up enter the full path of the file you just saved.
* After that the "Results sino2d" window will pop up with the requested results displayed in a text window, which allows you to store the result in a file.


** Extract 2D plane from the 4D **
* Now close all open windows and switch to the 4D HCNH NOESY spectrum. 
* The same process with the 4D spectrum is more involved since it's not easy to navigate through F1 and F2 simultaneously.
* Open the F3-F4 projection and find the coordinates of the selected peak in index numbers, e.g. F4: 134 and F3: 196.
* Switch to the 4D spectrum, click on the "E" tool button and set the F3 and F4 position to 134 and 196 respectively.
* Execute `rpl`, select the `12` plane and give index position 134 to F3 and 196 to F4. Name the new EXPNO `134196`.
* Select one strong aliphatic peak in the `134196` spectrum, and not down its position in index numbers ,e.g. F1: 86
 and F2: 81.
* Go back to the 4D spectrum, click on the "E" tool button and set the F1 and F2 position to 86 and 81 respectively.
* Execute `rpl`, select the `34` plane and give index position 86 to F1 and 81 to F2. Name the new EXPNO `8681`.
* Follow the same steps under ** Signal-to-Noise Ration Measurement **.