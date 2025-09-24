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

## Part D — Convert to rates and make the summary plots

* Compute **R1 = 1/T1** and **R2 = 1/T2** per residue; then compute **R2/R1**.
> R2/R1 is often used as a proxy for local effective correlation time; many labs even estimate τ\_c maps from this ratio.
* For the **7-day time course**, make per-residue bar plots (T1, T2, R2/R1) stacked day-by-day so you can spot trends.
**Interpretation cheatsheet (amide ^15N):**
* **Longer T2 (smaller R2)** → narrower lines → typically **more flexible/disordered** local environment or **smaller 
fragments** (if the protein degrades).
* **Shorter T2 (larger R2)** → broader lines → **more rigid** cores / **larger effective size** (aggregation, 
oligomerization). (Remember R2 also gets contributions from chemical exchange, R\_ex.)
* **R2/R1** generally **increases** with **longer τ\_c** (bigger apparent size/slow tumbling), but be cautious: R\_ex 
and diffusion anisotropy can bias simple τ\_c estimates for large proteins; advanced methods (e.g., TRACT and 
cross-correlated approaches) exist if you need robust τ\_c.

---

# Interpretation of relaxation barplots

The relaxation data are signal intensities at pre-specified time points plotted together.
T2 relaxation is more sensitive to the MW and therefore more informative.
From this data we obtain primarily two types of information:
1) If the protein forms aggregates or multimers then the MW of the complex increases, the tumbling rate drops, and the T2 
relaxation of its nuclei shortens (faster relaxation), which results to signal drop.
2) On the opposite, if the protein unfolds or is degraded (is broken down to smaller parts), then the tumbling rate
increases, the T2 relaxation of its nuclei increases (slower relaxation), which results to signal increase.