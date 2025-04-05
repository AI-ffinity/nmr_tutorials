# Peak Picking in 4D Spectrum with POKY

## Overview

The general workflow of this tutorial starts with **referencing and converting** the spectra to **POKY/Sparky** format. Then, we will **create 2D projections** from the 4D spectrum, which will help us reference it properly.

For **peak picking**, we will follow a **systematic strategy** that, although more involved, will allow for **higher precision** in identifying peaks in the 4D spectrum while minimizing noise. Since the **2D projections are derived directly from the 4D spectrum**, they provide a more accurate reference than the HSQC spectra, whose peak centers may deviate slightly from those in the projections.

To ensure **accurate peak selection**, we will use the **2D projections as intermediate reference points** for restricted peak picking in the 4D spectrum. The workflow is as follows:

1. **Overlay the projections onto the corresponding HSQC spectra**  
2. **Identify peak centers** by using the **HSQC spectra as references**  
3. **Use these peak centers** to perform **restricted peak picking** in the 4D spectrum  
4. **Unfold or unalias peaks** as necessary  
5. **Remove noise peaks** from the 4D spectrum  

By following this approach, we ensure that the final set of picked peaks in the **4D spectrum** is as accurate and noise-free as possible.

## Prerequisites

- Installation of POKY or NMRFAM-Sparky; license for POKY.
- Access to the specified Ubiquitin 4D and 15N HSQC spectrum files.

## Steps

---

### Step 1. Reference the `HSQC` Spectra in Topspin

Follow [the instructions](../TOPSPIN/Referencing_shifts/Referencing_Spectra.md) to reference the `1H-15N` and `1H-13C HSQC` in Topspin with BioTop.

---

### Step 2. Prepare the Spectra Files

#### 2.1 Reference the HSQC spectra in Topspin

- If you don't have the **BioTop** Topspin extension, install the spectrometer-related dependencies by running `expinstall` and keeping the default values. 
- Open the `1H-15N HSQC` spectrum and issue the command `btproc biorefonly`. If the temperature is not `298 K`, then you have to manually do spectral referencing by setting it in the `btproc` browser window.
- Do the same for the `1H-13C HSQC`. The `2rr` files will be updated automatically.
- You do not need to reference the `4D HCNH NOESY` because this will be compensated for by aligning to the HSQC spectra
  during peak picking.

#### 2.2 Convert Spectra to UCSF Format

Enter the directory where each spectrum is saved in Bruker format and run `bruk2ucsf` from there—running it from another directory will fail.  
For example, to convert the `1H-15N`, `1H-13C HSQC` spectra, and the 4D HCNH NOESY:

```shell
 bruk2ucsf_run 6/pdata/1/2rr /srv/NMR/Peak_Picking/Nanoluc/15N_HSQC.ucsf
 bruk2ucsf_run 7/pdata/1/2rr /srv/NMR/Peak_Picking/Nanoluc/13C_HSQC.ucsf
 bruk2ucsf_run 5/pdata/1/4rrr /srv/NMR/Peak_Picking/Nanoluc/4D_HCNH_NOESY.ucsf
```

> Note: You can also [convert the spectra from Bruker to UCSF format in POKY/Sparky](Miscellaneous/convert_spectra_POKY.md), 
> but you cannot rename the axes in that process.

#### 2.3 Rename Axes

Rename the axes in the `1H-15N` and `1H-13C HSQC` spectra:

```shell
ucsfdata -a1 N -a2 HN 15N_HSQC.ucsf
ucsfdata -a1 C -a2 HC 13C_HSQC.ucsf
```

Print the axis values of the `4D HCNH NOESY`:

```shell
ucsfdata 4D_HCNH_NOESY.ucsf
```

Example output:

```shell
axis                          w1          w2          w3          w4
nucleus                       1H         13C         15N          1H
matrix size                  256         256         256         416
block size                     8           8           8          13
upfield ppm                1.194       6.301     101.402       5.279
downfield ppm              8.208      73.001     133.002      10.622
spectrum width Hz       6666.667   15939.978    3043.445    5078.125
transmitter MHz          950.374     238.980      96.311     950.374
```

From the `upfield` and `downfield` rows, you can guess which axis is `HC` and which is `HN`. In this example, the following 
command renames them properly—amidic protons have higher shift values than the aliphatic protons:

```shell
ucsfdata -a1 HC -a2 C -a3 N -a4 HN 4D_HCNH_NOESY.ucsf
```

> **IMPORTANT:** Make sure that axes are named consistently in all spectra; otherwise, you will encounter problems during peak picking.

#### 2.4 Create C-HC and N-HN Projections

For a detailed tutorial, see [Create_2D_projections_from_4D_spectrum](../SPARKY_and_POKY/Create_2D_projections_from_4D_spectrum.md).
Briefly, extract the `N-HN projection` from the `4D HCNH NOESY`. You may need to adjust the `-p[1-4]` values according 
to your 4D spectrum dimension order:

```shell
ucsfdata -p1 -r -o C-N-HN.ucsf 4D_HCNH_NOESY.ucsf
ucsfdata -p1 -r -o 2D_N-HN_proj.ucsf C-N-HN.ucsf
```

Similarly, for the `C-HC projection`:

```shell
ucsfdata -p4 -r -o HC-C-N.ucsf 4D_HCNH_NOESY.ucsf
ucsfdata -p3 -r -o 2D_HC-C_proj.ucsf HC-C-N.ucsf
```

---

### Step 3. Loading the Spectra

**Load the spectra**
- Open the UCSF files with the `fo` command (make sure to display **Poky Spectrum** type of files in the pop-up browser), 
navigate to the folder, and select your spectra. Alternatively, you can copy the full path to each spectrum (for 
example, `realpath 4D_HCNH_NOESY.ucsf` in the Shell) and paste it into the pop-up browser.
- Do the same with the 2D projections and the `HSQC` spectra.
- Use `xa` to show the nucleus types on the axes., `xr` to roll the axes and `xx` to transpose them.
- Fix the aspect ratio by hitting `vt` and increasing the **Aspect (ppm)** for example to `12`, and then **Apply**.

---

### Step 4. Adjusting the Spectra

**Synchronize Spectra**  
- Click `yt` to synchronize the `N` axes of the `1H-15N HSQC` and `4D_HCNH_NOESY` first, and then synchronize the `HN` 
axes of those same spectra. Remember to synchronize one axis at a time!  
- Do the same for the `1H-13C HSQC` and `4D_HCNH_NOESY`, and then for both `HSQC` spectra and the respective 2D projections.

**Correct the contour levels and colors**  
- Type `vC` to bring up the contour level control scrollbars and adjust the contour levels.
- Type `ec` to bring up the easy contour dialog allowing you to adjust all loaded spectra, including their colors.
- If you double-click on a spectrum in the dialog it will open up the contour level dialog (equivalent to the `ct` command).

**Align the `2D_N-HN_proj` to the `15N_HSQC`**  
- The 4D axes are usually completely off and must be aligned to the reference HSQC spectra. To achieve this, use the 2D 
projections.   
- Hit `ol` to overlay `2D_N-HN_proj.ucsf` onto `15N_HSQC`.
- You may reduce the contour number to 1 for one of the two spectra for better visibility. Also hit `oz` to increse the contour thickness and the peak marker thickness.
- Manually pick the most "trustworthy" peak in the `15N_HSQC` (`F8` to enter peak picking mode, `F1` to exit it) and find the 
same peak in the 4D.  
- Type `al`, and in the pop-up:  
  - Set **Align spectrum** to `2D_N-HN_proj`  
  - Set **using peak in** to `15N_HSQC`  
  - The axes should match, thanks to the renaming we did earlier.  
  - Now hold the `Shift` key and select one "trustworthy" peak in each spectrum for alignment.  
  - Hit **Align**.
  - Alternatively pick a set of matching peaks (button `F8`) in both spectra and click the **Auto align** option (slower and doesn't always work well).

![](images/N-HN_alignment.png)

**Align the `2D_HC-C_proj` to the `13C_HSQC`**  
Follow the same procedure described in the previous step.

![](images/HC-C_alignment.png)

**Reference the `4D_HCNH_NOESY`**  
- Hit `st` and copy the shift values from the aligned `2D_N-HN_proj` to `4D_HCNH_NOESY`.  
- Make sure that every time you copy a shift value from one spectrum to the other, you click **Apply**, or else the value is not saved.  
- Similarly, copy the shift values from the aligned `2D_HC-C_proj` to `4D_HCNH_NOESY`.  
- When you finish, click **OK**, and the `4D_HCNH_NOESY` will be referenced!  

---

### Step 5. Peak Picking

# Adjusting Contour Levels and Preparing Reference Peaks

- Adjust the contour levels (both positive and negative) in the `15N HSQC` spectrum to optimize peak visibility.
- Press `F8` to enter peak picking mode and select all visible peaks.
- Use the following Python function to estimate the expected number of N-H (in-phase) peaks from the amino acid sequence in the **multiplicity edited 15N HSQC**:
```python
def estimate_15N_hsqc_peaks(sequence: str) -> int:
    # Count backbone amides = total residues minus any prolines and the N-terminus
    backbone_peaks = sum(1 for aa in sequence if aa != 'P') -1
    # Count side-chain peaks from R (NE–HE), K (NZ–QZ), W (NE1–HE1), and H (ND1-HD1)
    sidechain_peaks = sequence.count('R') + sequence.count('K') + sequence.count('W') + sequence.count('H')
    return backbone_peaks + sidechain_peaks
```
- Gradually increase or decrease the contour levels until the number of inphase (positive intensity) picked peaks is approximately the expected number of N-H peaks (292 for CA2 protein).
I set the contour level to 1.4e+06, which captured 274 in-phase peaks, as below that a lot of noise peaks were emerging.
  ![](images/15N_HSQC_contour_level.png)
- Press `lt` to open the peak list and export the peak list from the `15N HSQC` spectrum by saving it to a file.
- Switch to the `2D N-HN projection` and overlay the `15N HSQC` spectrum.
- Delete all current peaks from the `2D N-HN projection`.
- Press `rp` to load the saved peak list from the `15N HSQC`. Altnatively, just copy (Ctrl+c)-paste (Ctrl+v) from one spectrum to the other.
- Press `pa` to select all peaks.
- Press `pc` to adjust the peak positions to the **contour centers** of the `2D projection`.
- Manually adjust or create peak markers to ensure they align with the actual peak centers in the `2D projection`.
- At the end count the peak markers in both spectra using `lt`. They must be the same. If not, check for peaks with the same coordinates - they are seen as one.
- These peaks will be used as **reference points** for **restricted peak picking** in the `4D spectrum` later on.

#--------------------------------

**Pick all peaks in the reference 1H-15N HSQC**  
Go to the `15N_HSQC`, hit `F8` to enter peak picking mode, and drag a box around all signals. This will pick all the visible peaks. Hit `F1` to return to selection mode. Select and delete all peaks that you deem to be noise.

> **TIP:** Use `lt` to view the peak list.

**Use those peaks to find peaks in the 4D**  
- While you have only real peaks in `15N_HSQC`, type `lt` and export the peak list to a file.
- Switch to the `2D_N-HN_proj` window and hit `rp` to load the list of peaks.
- Select **Auto detect dimensions** and click **Create peaks**.
- Hit `pa` to select all loaded peak markers and then `pc` to center them to the contour hills of `2D_N-HN_proj`.
- Hit `ol` and overlay `15N_HSQC` to `2D_N-HN_proj`.
- Go through all the peak markers, visualize them and adjust their position manually to be at the center of the contours hills
in the `2D_N-HN_proj`. To help you spot the overlapping peak parkers, hit `lt`, **sort by frequency** and go through the list
search for peaks with identical coordinates. Double click on them and adjust their position based on the `15N_HSQC`.
 
  **THIS IS FOR 3D SPECTRA:** For the indirect NOE-HC dimension, set the tolerance to **999** because we want to find 
all NOE cross peaks, not just the diagonals!  

> The picking will take a while, but you can see its progress in the window:

![Restrictive_peak_picking_in-progress_window](./images/Peak_picking_running.png)

#------------------------------------------

**Pick all peaks in the HC-C projection that match with reference 1H-13C HSQC**  
Since `1H-13C HSQC` is very crowded and is not ideal for setting landmarks for restricted peak selection, we will use it in 
combinations ith the `2D_HC-C_proj`. Overlay the two spectra and select the peaks in `2D_HC-C_proj` that you believe are
within the general boundaries defined by the `1H-13C HSQC` and are not noise - a bit of intuition will be helpful here. 
Inspect visually the selected peaks in the `2D_HC-C_proj` and add/remove peaks by holding the **Shift** button.
These will be your landmarks for restrictive peak selection. Repeat the previous step to select the relevant peaks in the
`4D_HCNH_NOESY` (hit the **Select peaks** button this time). Keep only those peaks that you deem to be real by hitting `pI`
for inverted selection followed by **Delete** button.

**Use those peaks to delete noise peaks in the 4D**  
While you have only real peaks in `13C_HSQC`, type `kr` to enter the peak transfer dialogue:  
- Set **Find peaks in** to `4D_HCNH_NOESY`  
- Set **Using peaks in** to `13C_HSQC`  
- Adjust the tolerances: use higher tolerances because the `1H-13C HSQC` spectrum is very crowded. For example, 0.4 ppm for `C` and 0.04 ppm for `HC`.  
- This time, hit the **Select peaks** button.  
- Once the selection is finished, type `pI` to invert the peak selection and click **Delete** to remove those noise peaks.  
- In the end, you should see only peaks that are close to the `13C_HSQC` contours, but there may still be many peaks that fall outside and are noise. Refine your peak selection by repeating restricted peak picking with gradually lower tolerances, inverting the selection, and deleting the peaks that you deem to be noise.

Tolerances for `kr`:
2D_N-HN_proj -> 4D_HCNH_NOESY: N=0.2 ppm and HN=0.02 ppm or if tpp many peaks are picked, N=0.1 ppm and HN=0.01 ppm
2D_HC-C_proj -> 4D_HCNH_NOESY: C=0.4 ppm and HN=0.04 ppm because the HC-C projection is more crowded. You want to add peaks manually (`F8` button) at crowded regions (e.g. CA) where no peak markers were created with `13C_HSQC`->`2D_HC-C_proj` restricted peak selection.

## Optimizing Restricted Peak Picking for Higher Accuracy

- For **more accurate restricted peak picking** and to **reduce noise**, it is recommended to use **different tolerances** for peaks based on their **radius**.
- Since **measuring distances between two markers is not supported in POKY**, we will manually determine appropriate tolerances by analyzing peaks in the **2D projection spectra**.
- Open each **projection spectrum**, sort the peaks by **data height**, and **start from the highest intensity peaks**.
- **Double-click on peaks** in the `lt` table to visualize them and estimate **suitable tolerance values** that will capture all corresponding peaks in the 4D spectrum within that **region of the 2D plane**.
- Keep **notes** of the chosen tolerance values by pressing `NT`, selecting the peak, and **applying the same tolerance to all peaks with similar data height**.
- Perform **multiple restricted peak picking queries**, each time selecting a **set of peaks that share the same tolerances**.
- Start with the **N-HN projection**, enabling **restricted peak picking** in the `4D NOESY` spectrum.
- Each time, enable **"Use only selected peaks"** and set the corresponding **tolerance values**.
- After finishing with the **N-HN projection**, switch to the **HC projection**.
- This time, **do not enable peak picking**, but instead, **select peaks** based on the same grouping strategy.
- Each time a **set of peaks** is selected in the **4D spectrum**, press `NT` and **add a note** with the **tolerance values used**.
- After completing all iterations of **grouping peaks in the projections** based on their **common tolerance values** and **performing restricted peak selection in the 4D spectrum**, you can **sort all peaks in the `lt` table by note**.
- **Select and delete peaks that do not have a note**, as they likely represent noise.
- **Manual refinement of 4D peak list:** Overlay the `HC-C_projection` and the `13C_HSQC` on the `4D_HCNH_NOESY` with the selected peak list and manually remove peaks that are not in regions with signal of at least one of the 2D spectra.


Aliased Peaks:
`C < 25` ppm and `HC > 3` ppm. 

[FIGURE here]

---

### Step 6. Validation Tips

**View the C-H Plane in the 4D Spectrum**  
- Click `xr` twice on the 4D spectrum to focus on the C-H plane. Type `xx` to make the H axis horizontal and C vertical.  
- You can type `xa` to show the nucleus types on the axes.

**Open the peak lists**  
Bring up the `lt` windows for both the 2D and the 4D; sort the peaks by the direct `HN` or `N` frequency, and select the useful columns to display:

![the pick list options](./images/Peak_list_columns.png)

(Linewidth should be unchecked!)

Click on each peak in the 2D list and validate them.

**If you wish to start over completely**  
Type `pa` to select all peaks, and hit **Delete** to remove all peaks.

**If you want to find new peaks to add**  
Don't forget to check the **Use selected peaks only?** box in the `kr` dialogue!

**View the nD spectrum from different C-H planes**  
To open multiple C-H planes, click `vd` to duplicate the view of a 4D spectrum into another window. In each window, you 
can focus on different C-H planes by selecting a different `15N HSQC` peak with `F1` and clicking `vc` to center it.

**Discard the noise peaks using a S/N cutoff**
- Hit `st` and in the text box **"noise as median of"** write 10000 or another high number.
- Click **"Recompute"** several times.
- If the **"Estimated noise:"** changes a lot, increase the **"noise as median of"** and repeat the process.
- Once you settle on an **"Estimated noise:"** value, open the peak list by hitting `lt`, display the **S/N** and sort by **Data Height**.
- Select all peaks with absolute **S/N** value less than the **"Estimated noise:"** and delete them. For stricter peak picking, you can set the cutoff to 3x or 5x the **"Estimated noise:"**.

** OPTIONAL: Discard the noise peaks using a weak peak as a reference**  
- Overlay the `N-HN_proj` onto the `15N_HSQC` and increase the contour levels until noise peaks start to emerge.  
- Select a `15N_HSQC` peak with weak signal in `N-HN_proj` and check its HC-C plane by switching to `4D_HCNH_NOESY` and hitting `vc`.  
- Review the picked peaks (previously found by `kr`), adjusting the contour levels until all visible peaks are captured.  
- If you cannot achieve this, pick another weak peak in the `15N_HSQC` and repeat the process.  
- Once you succeed, select the **weakest picked peak** and hit `ss`. This command will select all 4D peaks that have lower intensity than the selected one. Type `lt` to check that.  
- Click **Delete** to remove them.

> **Note**: This comparison is made using signed intensities: negative peaks with large absolute intensity will also be 
selected! Check them manually and deselect if needed: hold `Ctrl` and drag over the selected peaks with your mouse.

![peak list](./images/peak-list-window.png)

(^ There should be a GIF here showing large negative peaks.)

---

### Step 7. Exporting Peak Lists

**Export Picked Peaks for 4D-GRAPHS**  
Go to the 4D peak list (type `lt`) and select the columns `w1`, `w2`, `w3`, `w4`, `Data Height` and `Note`. Click **Apply**, then **Save...**.
Further editing of the projections and the HSQCs is needed.


# Improve the Precision of the 13C HSQC Peak List using the 4D HCNH NOESY Peak List  

- Once you have finalized the **peak list** from the **HC-C projection**, **export it to a file**.  
- Press `fo` and reopen the **13C HSQC spectrum** in a **new window**.  
- Press `st` and **rename** that window to **"13C HSQC - 4D Peak List"**.  
- Hit `rp`, toggle on **Auto detect dimensions** and load the **4D HCNH NOESY peak list**. 
- Verify that the **aliased/folded peaks** are unaliased/unfolded, just as on the 4D spectrum (POKY does this automatically).  
- Hit `lt` and through the "Options" display the "Data Height".
- **Export the updated peak list** to a new file named `13C_HSQC_with_4D_HCNH_NOESY_peaks.list`.

We follow this approach because the **13C HSQC spectrum** is **very noisy**, with **large dispersion effects**, meaning 
that the **peak centers deviate** from those identified in **4D HCNH NOESY spectrum**.  
Consequently, since the entire assignment relies on the 4D spectrum, it is **more accurate** to use the peak 
markers from it, but **enhanced with the intensity signs** present in the **13C HSQC spectrum**.  
The 13C HSQC spectrum provides information on whether a peak corresponds to a **methylene group**, which improves 
both **accuracy and coverage** for **chemical shift assignment** in **4D-GRAPHS**.


# Improve the Precision of the 15N HSQC Peak List using the 2D N-HN projection Peak List  
The `15N HSQC peak list` for 4D-GRAPHS must have only one peak for each spin system, therefore we will apply the 
previous trick but using the `**N-HN projection peak list* instead of the 4D HCNH NOESY peak list.

---

## Notes for Special Cases

**Unaliasing Peaks in POKY**  
When you do restricted peak picking (`kr`) using as a reference Peaks that have not been unaliased or unfolded, POKY 
will automatically check for possible aliased peaks. If the spectrum width of the source 2D is larger than that of the 
nD (n = [3,4]), POKY will find and mark the peaks in the 3D as aliased. 

However, BEWARE that when your reference peaks are aliased or unfolded, POKY won't match the correct peaks in the 
target spectrum unless they are also unalias/unafolded. It may catch some peaks but they will be irrelevant. Therefore, 
do not unalias/unfold the peaks in the 2D HC-C and N-HN projections! Do the unaliasing/unfolding directly on the 4D 
HCNH NOESY.

Below are examples of the `13C-HSQC` spectra with aliased peaks (in yellow boxes):

| Protein 1 | Example 13C-HSQC - Protein 2 |
|------------------------------------------------------------------|--------------------------------------------------------------------|
| ![13C-HSQC-ac1](./images/13C-HSQC-ac1-aliased.png) | ![13C-HSQC-sy15](./images/13C-HSQC-sy15-aliased.png) |

---

# Authors
- Thomas Evangelidis  
- Ekaterina Burakova
