# Peak Picking in 3D Spectrum with POKY

## Overview

The general workflow of this tutorial starts with **referencing and converting** the spectra to **POKY/Sparky** format. Then, we will **create 2D projection** from the 3D spectrum, which will help us reference it properly but also to accurate peak picking.

For **peak picking**, we will follow a **systematic strategy** that, although more involved, will allow for **higher precision** in identifying peaks in the 3D spectrum while minimizing noise. Since the **N-HN projection is derived directly from the 3D spectrum**, it provides a more accurate reference than the 15N-HSQC spectrum, whose peak centers may deviate slightly from those in the N-HN projection.

To ensure **accurate peak selection**, we will use the **N-HN projection as intermediate reference point** for restricted peak picking in the 3D spectrum. The workflow is as follows:

1. Load and adjust the appearance of spectra
3. Use the  15N-HSQC spectrum as reference to perform **restricted peak picking** in the 3D spectrum
4. **Unfold or unalias peaks** as necessary  
5. **Remove noise peaks** from the 3D spectrum  

By following this approach, we ensure that the final set of picked peaks in the **3D spectrum** is as accurate and noise-free as possible.


#### Step 1. Rename Axes

Rename the axes in the `1H-15N HSQC` and `1H-13C HSQC` spectra otherwise the strip plotting (`sp`) won't work:

```shell
ucsfdata -a1 15N -a2 1H 15N_HSQC.ucsf
ucsfdata -a1 13C -a2 1H 13C_HSQC.ucsf
```

Print the axis values of the `3D HNCO`:

```shell
ucsfdata HNCO.ucsf
```

Example output:

```shell
axis                          w1          w2          w3
nucleus                      13C         15N          1H
matrix size                  512         256         560
block size                    32          16          35
upfield ppm              169.233     100.089       6.488
downfield ppm            183.233     135.089      10.274
spectrum width Hz       3346.171    3370.900    3597.862
transmitter MHz          239.012      96.311     950.374
```

Renames the axis for easier spectra manipulation:

```shell
ucsfdata -a1 13C -a2 15N -a3 1H HNCO.ucsf
```

> **IMPORTANT:** Make sure that axes are named consistently in all spectra; otherwise, you will encounter problems during peak picking.

---

### Step 2. Load the Spectra

**Load the spectra**
- Open the UCSF files with the `fm` command (make sure to display **Poky Spectrum** type of files in the pop-up browser),
navigate to the folder, and select your spectra.
- Use `xa` to show the nucleus types on the axes, `xr` to roll the axes and `xx` to transpose them.
- Fix the aspect ratio by hitting `vt` and increasing the **Aspect (ppm)** for example to `18`, and then **Apply**.

---


### Step 3. Adjust the Spectra

**Synchronize spectra**
- Click `yt` to synchronize the `15N` axes of the `1H-15N HSQC` and `HNCO`.
- Then synchronize the `1H` axes of those same spectra. Remember to synchronize one axis at a time!

**Correct the contour levels and colors**  
- Type `ec` to bring up the easy contour dialog allowing you to adjust all loaded spectra, including their colors and contour levels.
- If you double-click on a spectrum in the dialog it will open up the contour level dialog (equivalent to the `ct` command).
- Adjust the contour levels (both positive and negative) in the `15N HSQC` spectrum to optimize peak visibility.

**Overlay spectra**
- Switch to the `HNCO`, hit `ol` and overlay the `15N_HSQC` onto that spectrum.
- Type `ec` and decrease the positive and negative level values of `15N_HSQC` to 1. That will allow you to view clearer the
peak of HNCO on the overlay.

!Note: here I assume that both `HNCO` and `15N_HSQC` are referenced. In not then you must align them using the
`2D_N-HN_proj` (see the other tutorial).

---

### Step 4. Peak Picking

**Adjusting Contour Levels and Preparing Reference Peaks**

- Press `F8` to enter peak picking mode and select all visible peaks in `15N HSQC`.
- Use the following Python function to estimate the expected number of N-H (in-phase) peaks from the amino acid sequence in the **multiplicity edited 15N HSQC**:

```python
def estimate_15N_hsqc_peaks(sequence: str) -> int:
    # Count backbone amides = total residues minus any prolines and the N-terminus
    backbone_peaks = sum(1 for aa in sequence if aa != 'P') -1
    # Count side-chain peaks from R (NE–HE), K (NZ–QZ), W (NE1–HE1), and H (ND1-HD1)
    sidechain_peaks = sequence.count('R') + sequence.count('K') + sequence.count('W') + sequence.count('H')
    return backbone_peaks + sidechain_peaks
```

- Gradually increase or decrease the contour levels until the **number of in-phase (positive intensity)** picked peaks is
close to the expected number of N-H peaks (149 for AR-V7 protein, 254 for NatD).

**Restricted peak picking round 1**

- Type `pa` to select all peaks in the `15N HSQC`.
- Type `kr` to open the **Restricted Peak Picking** window.
- Under **Find peaks**, select the **HNCO** spectrum.
- Under **Using peaks in**, select the **15N_HSQC**.
- First use low thresholds: 0.1 ppm for 15N and 0.01 ppm for 1H.
- Click the **Pick Peaks** button.


**Manual Refinement using Strip Plots**

- On the `HNCO` window hit `vz` and set the "w1 C" values to `9999`.
- Adjust their size and keep the `HNCO` and `15N HSQC` windows next to each other.
- Select all `15N HSQC` peaks by typing `pa` and then `sp` to open the **Strip Plot** window.
- In the drop-down menu click at "Show" and activate `HNCO` spectrum. Then click on "[+] Peaks" button. Type also `lt`
to have the peak list window open and see the peak intensities.
- Select and remove the `HNCO` peaks with negative intensity. If you still have far more the expected number of N-H
you calculated earlier, then you can remove low intensity peaks until you reach a "safe number" of potentially real peaks.
- Iterate through every strip and remove noise peaks based on their intensity, number of expected peaks, location in
the N-H plane of `HNCO` and your intuition. Sometimes a strip may contain more than one real peaks (two or more residues
with the same N-H frequencies but distinct C' frequencies).
- Select the remaining strong peak(s), hit 'nt' and write "s" to remember that these peaks were reviewed in the strip plot.
The "s" should appear in `lt` window if you activate the "Note" radiobutton under "Options...".

**Manual Refinement using the overlay of `15N HSQC` to `HCNO`**

- Select a group of peaks in `HNCO` that were supposed to be a single peak according to your peak selection in `15N HSQC`.

![](images/peak_picking_3D/peak_group.png)

- Hit `lt` on the `HNCO` window. Hold Ctrl and left mouse click on the peak from the group with the highest
"Data Height" to unselect it. Then click the "Delete" keyboard button to delete the weaker peaks. So this way only the
strongest peak will remain.
- Select the remaining strong peak(s), hit 'nt' and write "r" to remember that these peaks were reviewed. The "r" should appear
in `lt` window if you activate the "Note" radiobutton under "Options...".
- Repeat this process for all groups of HNCO peaks.

**Restricted peak picking round 2**

- Select in `15N HSQC` only the peaks which had no equivalent in the HNCO in the 1st round or restricted peak picking.
- Type `kr` to open the **Restricted Peak Picking** window and following the same procedure, but this time use higher
thresholds: 0.2 ppm for 15N and 0.02 ppm for 1H.
- Follow the same manual refinement steps as before.

---

### Step 5. Exporting Peak Lists

**Export Picked Peaks for 4D-GRAPHS**
- Switch to the `15N HSQC` spectrum, type `lt` to open the peak list, click on "Options" to display only the
"Assignment", `w1`, `w2`, `Data Height`, and export the peak list to a file.
- Switch to the 3D spectrum and do the same.

---

# Peak Picking a Combination of two 3D Spectra with POKY

For the peak picking of the combination HNcoCA/HNCA we will use the same workflow as in HNCO, but since HNcoCA gives us
the Cα(i-1), N(i), Hn(i) and HNCA Cα(i-1), Cα(i), N(i), Hn(i), the we will peak pick one spin system at a time using
strip plots. In summary the steps are following:

- Do the restricted peak picking in two rounds, remove negative peaks and low intensity positive peaks from both spectra,
 as described for `HNCO`.
- In addition to `15 HSQC`, load and adjust also the `13C HSQC`.
- First select all peaks of `HNcoCA` (more sensitive experiment) by hitting `pa`, then `sp` to strip plot and
display both spectra.
- Iterate through each pair of strip plots and search for pattern of peaks, like that
in the figure below.

![](images/peak_picking_3D/HNCA_HNcoCA_strip_plot.png)

- Select the real peaks and mark them with "s" by hitting `nt` and then delete the noise peaks.
- Repeat the above steps for all pairs of strips. Then select all peaks of `HNCA` and repeat the same procedure.

---

# Merge peaks from a 3D spectrum measured on two spectrometers

- Follow all previous steps to load and adjust the spectra.
- First select all peaks of `HNCO 850MHz` by hitting `pa`, then `sp` to strip plot and
display both spectra.
- Iterate through each pair of strip plots and search for unique peaks in one of the two, like that
in the figure below.

![](images/peak_picking_3D/strip_plot_merge_3D_peaks.png)

- Select the unique peaks, hit `nt` and mark them with "u" to remember them later.
- One you finish with all the strip plots, select all peaks of `HNCO 950MHz` and repeat the same
steps.
- At the end export both HNCO peaks lists along with the "Note column" and combine them manually
by adding the `HNCO 850 MHz` peaks marked with "u" to `HNCO 950 MHz`.

