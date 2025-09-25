# T1/T2 ^15N relaxation tutorial: TopSpin processing → Bruker Dynamics Center

---

## What we measured

Every day for 7 days in total we measured the following spectra:

* A high-resolution 2D **^1H–^15N HSQC** for QC/peak-list reference.
* A **pseudo-3D HSQC-T1** series (arrayed delays).
* A **pseudo-3D HSQC-T2** series (arrayed delays).

> (Bruker pulse programs commonly used: `hsqct1etf3gpsi3d` and `hsqct2etf3gpsi3d` or close variants. These acquire HSQC
> planes versus relaxation delay in a pseudo-3D dataset.)

> Pseudo-3D note: the third “dimension” is a **non-frequency** delay axis, so you only Fourier-transform the frequency
> axes (^1H and ^15N), and leave the delay axis as a series of 2D planes. TopSpin and Dynamics Center are built for
> exactly this. (\[McGill University]\[2])

---

## Part A — Process each standard ^15N HSQC (QC) in TopSpin

Use standard 2D processing as described in the dedicated tutorial \[ref]. If you don't have it already, then save a
high-quality peak list for the ^15N HSQC of day 1. This will be your *reference* list for all seven days in Dynamics Center.

---

## Part B — Process each pseudo-3D T1/T2 dataset in TopSpin

1. Transform the frequency axes and set phasing from a representative plane. Open the first T1 pseudo-3D dataset (experiment `4`) and issue the following commands:

```
3 SI 4k       ; zero filling in the direct dimension
2 SI 1k       ; zero filling in the 15N (F2) dimension
tf3           ; FT in the 1H dimension
tf2           ; FT in the 15N dimension
2 ME_mod no   ; deactivate linear correction in the 15N dimension
slice         ; extract the first F2–F3 plane to process it
```

> You **do not** Fourier-transform along the delay axis (dimension F1) for pseudo-3D T1/T2; keep it as a series of 2D planes. (Dynamics
> Center will use those planes to fit intensities vs. delay.)

2. **Process the 2D plane** (orientation **23**) to phase it like a normal ^15N HSQC \[ref], then **store the phase back to the 3D**.

3. Overlay with the QC ^15N HSQC (experiment `3`) using `.md`, zoom into the region of interest, right-click and save the
   display region to *STSR/STSI*. Copy these numbers to the pseudo-3D spectrum.

> At the bottom left there are tryptophan side-chain amide peaks. You can safely exclude them from the focus region
> since we are interested in the relaxation properties of the backbone amides only.

> Tip — window/truncation: Zoom the **^1H (F2)** range to your HSQC window (excluding the water line ≈ 4.7 ppm) *before*
> baseline correction; this avoids water-line artifacts influencing the polynomial baseline. Then apply baseline.
> (TopSpin’s `ABSG` governs baseline polynomial degree used by `abs1/abs2`.)

4. Run baseline correction on the pseudo-3D spectrum:

```
abs3    ; on the direct dimension; we don't need to set ABSF2{F3} after the water line at ~4.7 ppm because we truncate with STSR/STSI
        ; the ABSF1{F3} must always be left to a high value like 1000 ppm.
abs2    ; we leave ABSF1{F2} and ABSF2{F2} to high values, like 1000 ppm and -1000 ppm, respectively.
```

5. Select and save the necessary commands you issued to a new macro by right-clicking, then **Save selected command(s) as macro**.
   A window will pop up asking for the name of the new macro. Name it `procT1` and click **OK**. Then an editor will pop up.
   Adjust its contents to look like the following (SI, PHC0, STSR, STSI values will vary in your case):

```
3 SI 4k
2 SI 1k
2 STSR 112
2 ME_mod no
3 STSR 630
3 STSI 920
3 PHC0 120.525
tf3
tf2
tabs3
tabs2
```

6. Process all pseudo-3D T1 spectra in batch mode with the `qumulti` command. In the window that will pop up write
   `procT1` as the command and select the individual experiments that you want to process. E.g., 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43.

7. Repeat steps 1-6 for the pseudo-3D T2 spectra.


---

## Part C — Analyze in **Bruker Dynamics Center** (Protein Dynamics)

## 1) Launch & get oriented

* Open **Dynamics Center**. In the lower-left, click the **Protein Dynamics** tab; you’ll see the method tree with **T1-Relaxation** and **T2-Relaxation** among the options. If you like, set a default data folder via **Config → Preferences → Default Spectrum Path** so every file dialog starts in the right place. &#x20;

## 2) One-time “Sample” setup (reused for both T1 and T2)

* Go to **Sample** and load your **AA sequence** (FASTA) and a **PDB with hydrogens**. When you click **OK**, the **Sample** leaf turns **green**, meaning it’s ready. This saves time later because you can load this setup into other methods.&#x20;

> Why this matters: the sequence aligns residue-indexed results; the H-complete PDB enables structure-aware displays later if you use them.

## 3) T1 — Add data & peaks (pseudo-3D)

* Open **T1-Relaxation → Data**. Set **Spectrum type = pseudo-3D** and browse to your processed **HSQC-T1** dataset.
* In **Peaks**, pick **use any other peak list** and point to your good **2D ^15N HSQC** peak list (e.g., day-0 reference).
* **Enable peak snapping** and choose **Snap to first plane then copy to others** so the software follows your peaks across delay planes.
* Set **Search radius ≈ 3 points per dimension**.
* In **Integrals**, set **Integral type = intensities**. Click **OK**; **Data** turns green and the planes/peaks are loaded.  &#x20;

> Tip: If you measured the same delay multiple times, see the **Lists** tab (default settings are fine for most cases).&#x20;

## 4) T1 — Fit the decays (Analysis)

* Open **Analysis**. Choose **exponential decays**; keep **automatic starting values**.
* Under **fit error estimation**, select the option that uses **signal-to-noise and variance of repeat experiments**; set **confidence interval = 95%**. Run the fit. It’s fast on typical datasets. &#x20;

> Result: per-residue **T1** with error bars—ready for plotting/export.

## 5) T1 — Make the display useful (View)

* In **View**, enable **fit curves in the main window** and set **“update on left-click”** so clicking a peak updates the fit panel.
* Turn on **error bars for integrals**, the **T1 histogram**, and **error bars on the histogram**.
* The cursor is **linked** across panels: click a peak to see its fit and highlighted bar.
* To focus on a single panel, **right-click** away from fit points and choose **Toggle full display**; repeat to restore the full layout. &#x20;

> If you ever “lose” everything, use **File → Visibility of objects** to bring panels back.&#x20;

## 6) Save your T1 setup (project)

* **Right-click T1 → Save As…** and store, for example, **`T1.project`**. Use **Save As** so T1 and T2 end up as different files.&#x20;

## 7) T2 — Reuse the setup, switch the data, repeat

* Open **T2-Relaxation**, then **right-click → Open…** and select your **`T1.project`**. This preloads **Sample** and your view preferences (the **Sample** node should turn green).
* Go to **Data** and update only the **spectrum path** to your **HSQC-T2** pseudo-3D dataset; keep the same **Peaks/snapping**, **Search radius**, **Integrals**, and **Lists** settings as above.
* Run **Analysis** again with **exponential decays**, S/N-based errors, and **95% CI**.
* In **View**, turn on the **T2 histogram** and error bars; use the same navigation tricks (linked cursor, toggle full display).
* **Save As…** **`T2.project`** when done. &#x20;

## 8) Export results & report

* From T1 and T2, use **Report** to create a PDF, and/or **Export** to get **text/Excel (.xlsx)** with fitted values and errors.
* For quick stats on a histogram, **right-click → Properties**.&#x20;

---

### Mini-FAQ / sanity checks (from the manual)

* **Why pseudo-3D?** You process ^1H and ^15N as normal frequency axes; the “third” axis is **delay**, so Dynamics Center treats it as a stack of HSQC planes vs. time for fitting. (Set it explicitly in **Data → Spectrum type = pseudo-3D**.)&#x20;
* **Do I need my own peak list?** Yes—use your best, clean **2D HSQC** peak list so peaks can be **snapped** to each delay plane.&#x20;
* **Nothing shows / I closed everything.** Use **File → Visibility of objects** to restore panels.&#x20;

---

### What you hand off downstream

Exported tables from **T1** and **T2** let you compute **R1 = 1/T1**, **R2 = 1/T2**, and **R2/R1** outside Dynamics Center (e.g., in Excel or Python), then plot residue-wise trends across days for your time-course analysis.

---

# Part D — Convert to rates and make the summary plots (per day, then compare days)

1. **Export fitted values from Dynamics Center (not raw intensities).**
   From each **T1** or **T2** method, use **Export** (or **Report**) to get per‑residue **T1**/**T2** plus their uncertainties. These are the quantities Dynamics Center fits and displays in the fit/histogram panels, and they’re the correct basis for downstream plots.

2. **Compute rates (with units) and propagate errors.**
   Work in seconds. For each residue:

* **R1 = 1/T1** (s⁻¹)
* **R2 = 1/T2** (s⁻¹)
  Recommended first‑order uncertainties: **σ(R) ≈ σ(T)/T²**. Keep these errors; use them as error bars in your bar plots.

3. **Optionally compute the ratio for trends (not absolute τc).**

* **R2/R1** is a useful *relative* proxy for changes in effective tumbling. With **T1/T2 only** (no hetNOE), treat R2/R1 as **comparative across days**, not as a standalone τc map; exchange and diffusion anisotropy can bias it.

4. **Merge days and align residues.**
   Use the **same day‑0 HSQC peak list** that you snapped to in Dynamics Center so residue IDs align across days. If a residue is missing on a given day (fit failed / SNR low), leave it blank rather than forcing an estimate.

5. **Plot clearly, with uncertainties.**
   For each day, build per‑residue bar plots for **T1**, **T2**, **R1**, **R2**, and (optionally) **R2/R1**, **with error bars**. Arrange days vertically (or side‑by‑side) so trends are easy to see. Also keep the **T1/T2 histograms** from Dynamics Center—they’re a quick check of global shifts day‑to‑day.

6. **Sanity controls for the 7‑day series.**

* Keep **sample temperature** and acquisition conventions identical across days.
* Use the **same Dynamics Center Data settings** everywhere (pseudo‑3D, peak snapping mode, search radius ≈ 3 points, integrals = **intensities**) so fits remain comparable.

---

# Part E — Interpretation of relaxation plots (what T1/T2 alone can tell you)

Below is a concise, T1/T2‑only cheatsheet. It focuses on **fitted T1/T2 (and derived R1/R2)**—not raw plane intensities.

**Global size / tumbling changes**

* **Aggregation / oligomerization / tighter complexes:**
  Expect **shorter T2** → **larger R2** (broader lines), often **modest T1 changes**. If **R2** rises broadly across many residues from day‑to‑day, that’s consistent with **slower tumbling (larger apparent τc)** and/or added **Rex**. Your **R2/R1** may also **increase** globally.
* **Degradation / unfolding into smaller species:**
  Expect **longer T2** → **smaller R2** (narrower lines) for fragments that tumble faster; **R2/R1** tends to **decrease**. New peaks can appear at new positions (fragments/unfolded regions).

**Local dynamics vs. exchange (limits of T1/T2‑only)**

* **Chemical exchange (Rex)** inflates **R2** without a matching **R1** change. Residues with unusually high **R2** (outliers in the histogram) are **exchange candidates**; with T1/T2 alone you can flag them, but you can’t robustly deconvolve Rex from size effects.

**What not to over‑interpret**

* **Absolute τc from R2/R1** using only T1/T2 is **not** recommended; keep it **relative** across days.
* **Raw intensity stacks** across days are confounded by gain/SNR; rely on **fitted** T1/T2 (with errors) and their histograms.

**Practical readouts for your 7‑day study**

* **Histogram shifts:** a left shift of **R2** (smaller R2 / longer T2) suggests **smaller/faster** species; a right shift (larger R2 / shorter T2) suggests **larger/slower** or **more exchange**.
* **Residue‑specific flags:** peaks whose **R2** jumps beyond the day’s interquartile spread (and is significant within error bars) are potential **exchange/interaction hotspots** worth inspecting in spectra.


In this folder there is a tiny Excel template that ingests PDC exports and spits out **day-stacked R2 barplots with error bars** (and computes R1, R2, R2/R1 for you).

Quick how-to for the spreadsheet:

* Paste your PDC exports into **Exports\_T1** and **Exports\_T2** (columns: Residue, Day, T1\_s, T1\_err\_s / T2\_s, T2\_err\_s).
* The template computes **R1 = 1/T1**, **R2 = 1/T2**, **R2/R1**, and error bars in **Rates**.
* **Charts** shows a ready-made clustered bar chart: **R2 by Residue and Day** with custom error bars. It auto-expands as you add rows (thanks to Excel Tables).
* If you use more than \~50 residues, duplicate the chart or extend the plotted ranges in the **Charts** sheet.
