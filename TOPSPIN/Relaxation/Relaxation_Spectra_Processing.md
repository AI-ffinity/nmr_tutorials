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

---

## Part D — Analyze in **Bruker Dynamics Center** (Protein Dynamics)

1. **Open Dynamics Center** → switch to **Protein Dynamics**. Choose **T1** or **T2** method from the method tree. 
2. **Data → Add datasets:** point to the processed pseudo-3D T1 or T2.
3. **Peak list:** import the **day-0 15N HSQC** peak list as reference, so peaks are tracked despite day-to-day 
chemical-shift drift. (This is standard practice and supported in the PDC workflow.) 
4. **Fit:** use defaults (single-exponential fits of peak intensities vs. delay).
5. **Display options:** enable **error bars** on residue plots for T1/T2 to visualize fit uncertainty.
6. **Export:** save tables to CSV/Excel for downstream calculations/reporting. (Dynamics Center is Bruker’s solution 
for automated/semi-automated analysis of datasets with one non-frequency dimension like T1/T2.) 

---

## Part E — Convert to rates and make the summary plots

* Compute **R1 = 1/T1** and **R2 = 1/T2** per residue; then compute **R2/R1**.

> R2/R1 is often used as a proxy for local effective correlation time; many labs even estimate τ\_c maps from this ratio.

* For the **7-day time course**, make per-residue bar plots (T1, T2, R2/R1) stacked day-by-day so you can spot trends.

**Interpretation cheatsheet (amide ^15N):**

* **Longer T2 (smaller R2)** → narrower lines → typically **more flexible/disordered** local environment or **smaller 
* fragments** (if the protein degrades). ([Chemistry LibreTexts][12])
* **Shorter T2 (larger R2)** → broader lines → **more rigid** cores / **larger effective size** (aggregation, 
* oligomerization). (Remember R2 also gets contributions from chemical exchange, R\_ex.) ([imserc.northwestern.edu][13])
* **R2/R1** generally **increases** with **longer τ\_c** (bigger apparent size/slow tumbling), but be cautious: R\_ex 
and diffusion anisotropy can bias simple τ\_c estimates for large proteins; advanced methods (e.g., TRACT and 
cross-correlated approaches) exist if you need robust τ\_c. ([SpringerLink][14])

---

## Optional tricks you might like later

* If you ever want to **split** a pseudo-3D into individual 2D datasets (one per delay) for bespoke processing, there 
* are AU tools/recipes (e.g., `splitser3d`) and the common **orientation 13/23 + `xfb`** approach. ([Gist][15])

---

# Interpretation of relaxation barplots

The relaxation data are signal intensities at pre-specified time points plotted together.
T2 relaxation is more sensitive to the MW and therefore more informative.
From this data we obtain primarily two types of information:
1) If the protein forms aggregates or multimers then the MW of the complex increases, the tumbling rate drops, and the T2 
relaxation of its nuclei shortens (faster relaxation), which results to signal drop.
2) On the opposite, if the protein unfolds or is degraded (is broken down to smaller parts), then the tumbling rate
increases, the T2 relaxation of its nuclei increases (slower relaxation), which results to signal increase.