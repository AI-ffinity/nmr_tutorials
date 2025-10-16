## SOFAST‑HMQC
**- Pros:**
  - Ultra‑fast acquisition (30 s–5 min per 2D spectrum) by using Ernst‑angle excitation and very short recycle delays, ideal for screening many ligands quickly.
  - Very short recycle delays lead to minimal sample heating, reducing thermal drift in temperature‑sensitive IDPs.
  - Excellent for rapidly triaging compounds to see which produce any detectable chemical‑shift changes.

**- Cons:**
  - HMQC’s multiplet line shapes in the indirect dimension broaden peaks, worsening overlap in the congested amide region of an IDP.
  - Lower digital resolution compared to HSQC, with fewer points across each peak.
  - At low protein concentrations (< 100 µM), sensitivity may be insufficient and you’ll need to increase scans (longer measurement times), eroding the speed advantage.
  - Severe peak overlap may make it impossible to distinguish or track individual resonances.

---

## BEST‑HSQC
**- Pros:**
  - Band‑selective excitation preserves pure single‑quantum coherence of HSQC, producing sharp, singlet cross‑peaks and the narrowest possible line widths.
  - Short recycle delays (~0.5 s) allow each spectrum to be recorded in 5–10 min, balancing speed and resolution for detailed CSP mapping.
  - Higher inherent sensitivity than SOFAST‑HMQC, especially important at lower protein concentrations (50–200 µM).
  - Resolves overlapping peaks while collecting enough data points for accurate K_D fitting within a practical timeframe.

**- Cons:**
  - Takes a few minutes longer per spectrum than SOFAST‑HMQC, making very large library screens more time‑consuming.
  - Requires custom pulse programs or careful calibration of selective inversion shapes on some spectrometers.

---

## BEST‑TROSY
**- Pros:**
  - TROSY selection cancels certain relaxation pathways, narrowing peaks and boosting sensitivity at ultra‑high field (950 MHz and above).
  - Particularly valuable for larger proteins (>20 kDa) or cases of severe spectral overlap.

**- Cons:**
  - More complex pulse sequence and phase cycling increase the risk of artifacts if not optimized.
  - Offers minimal benefit for a 14 kDa IDP, where tumbling is already fast.
  - Adds an extra minute or two per spectrum compared to BEST‑HSQC.

---

## Conventional HSQC (+ Non‑Uniform Sampling)
**- Pros:**
  - Provides the purest single‑quantum transfer and the highest fidelity for measuring small chemical‑shift changes.
  - Serves as the reference standard for K_D determination and precise CSP analysis.
  - When combined with 25–50% non‑uniform sampling, acquisition time can be reduced 2–4×, yielding high‑resolution spectra in under an hour at moderate concentrations (≥ 100 µM).

**- Cons:**
  - Without NUS, each spectrum can take 15–30 min or more, making full titrations span days.
  - At very low protein concentrations (< 100 µM), NUS reconstruction becomes unreliable—insufficient S/N in individual increments can introduce artifacts—so you must either increase scans or revert to uniform sampling.
  - Processing NUS data requires reconstruction algorithms and extra computational validation to avoid artifacts.
  - Dense spectral fitting and NUS reconstruction demand significant workstation time.

---

**Recommended Workflow for a 14 kDa IDP:**  
1. **Assess protein concentration:**  
   - **≥ 150 µM:** SOFAST‑HMQC is viable for initial screening.  
   - **100–150 µM:** BEST‑HSQC with NUS provides the best balance of sensitivity, resolution, and speed.  
   - **< 100 µM:** BEST‑HSQC with uniform sampling ensures reliable data; avoid NUS to minimize reconstruction artifacts.  

2. **Initial screen:**  
   - If concentration allows (≥ 150 µM), record SOFAST‑HMQC spectra (minutes per point) to quickly triage binders.  

3. **Detailed mapping:**  
   - Use BEST‑HSQC (with NUS at moderate concentrations) or uniform sampling at low concentrations to collect high‑resolution spectra in ~30–60 min per point, ensuring clear CSPs even at low S/N.  

4. **Fallback/advanced:**  
   - Reserve BEST‑TROSY only if you move to larger constructs or encounter unresolved overlap that BEST‑HSQC cannot resolve.  

---

# Authors
- Thomas Evangelidis