---
title: "window functions"
layout: default
---

Overview of Window Function Parameters (PROCPARS tab) for Protein Spectra
---

### 1. WDW (Window Function Type)

**What It Is:**  
WDW sets the type of **weighting (apodization) function** applied to the time-domain data before Fourier transform. Common choices include:  
- `no` (no window function)  
- `EM` (exponential multiplication, often referred to as “line broadening”)  
- `GM` (Gaussian multiplication)  
- `SINE` or `QSINE` (sine bell or shifted sine bell)  
- `TM` (trapezoidal multiplication)  

**Why/When to Use:**  
Applying a window function shapes the FID to trade off resolution versus signal-to-noise (S/N) and to reduce truncation artifacts (e.g., t1 noise).  
- **Exponential (EM):** Adds line-broadening, improving S/N at the cost of some resolution.  
- **Gaussian (GM):** Can provide some sharpening while still enhancing S/N.  
- **Sine bell (SINE/QSINE):** Commonly used in multi-dimensional experiments (especially in indirect dimensions) to suppress artifacts.  
- **Trapezoidal (TM):** Used when a specific linear ramp (fade in/fade out) is desired.

**Typical Selections:**  
- **Direct 1H dimension:** Often set to `EM` or `GM`.  
- **Indirect dimensions (2D/3D/4D):** Typically set to `SINE` or `QSINE`.  
- In some cases (especially for NOESY data), a trapezoidal function may be used to emphasize early FID points.

---

### 2. LB (Line Broadening)

**What It Is:**  
LB is the exponential broadening in Hz applied if **WDW** is set to `EM` or `GM`.  
- For `EM`, LB is a positive value specifying the decay constant.  
- For `GM`, LB is negative to indicate Gaussian weighting. 

**Why/When to Use:**  
Exponential weighting (with LB > 0) boosts S/N but broadens peaks. Excessive LB can degrade resolution.  
- For Gaussian weighting (LB < 0), the shape helps reduce truncation artifacts while still affecting peak widths.

**Typical Selections (Approximate Guidelines):**  
- **Direct 1H dimension (HSQC, triple resonance):** LB ≈ 0.3–0.5 Hz (if moderate broadening is acceptable).  
- **Indirect dimensions (15N or 13C):** A slightly larger LB (e.g., 1–3 Hz) might be chosen to enhance S/N.

---

### 3. GB (Gaussian Broadening Factor)

**What It Is:**  
GB is used specifically with the Gaussian window (i.e., when **WDW** is set to `GM`) to adjust the “width” of the Gaussian function. Its value typically ranges between 0.0 and 1.0. Larger GB values result in a narrower Gaussian window, which tends to preserve resolution but may be less effective at suppressing truncation artifacts.

**Why/When to Use:**  
Gaussian weighting offers a compromise between enhancing S/N and preserving resolution. GB fine-tunes that balance. 

**Typical Selections:**  
- Values in the range of ~0.1–0.3 are common.  
- Adjust upward if you want a sharper weighting, or downward for more broadening.

---

### 4. SSB (Sine Bell Shift)

**What It Is:**  
When **WDW** is set to a sine bell function (e.g., `SINE` or `QSINE`), **SSB** is the shift parameter. For example, SSB = 2.0 means the sine bell “starts” later, emphasizing the early points of the FID and more strongly tapering the end. 

**Why/When to Use:**  
Shifted sine bell weighting helps reduce truncation and t1 noise. The shift parameter allows you to adjust how aggressively the later time points are damped.

**Typical Selections:**  
- For indirect dimensions in triple-resonance or NOESY experiments, SSB values around 2–3 are common.  
- A larger shift results in greater damping of later points, which can improve noise characteristics at the cost of some resolution.

---

### 5. TM1 and TM2 (Trapezoidal Multiplication Factors)

**What They Are:**  
TM1 and TM2 are used if **WDW** is set to `TM` (trapezoidal multiplication) or if you use commands like `tm`, `traf`, or `trafs`. They define the ramp-up and ramp-down phases (leading and trailing edges) of the trapezoidal window. Typically, these parameters are expressed as a percentage of the total FID length. 

**Why/When to Use:**  
A trapezoidal window creates a linear ramp up → plateau → linear ramp down pattern. This approach offers a gradual “fade in/fade out” compared to sine bell or Gaussian functions. It is used in specific cases where emphasizing certain parts of the FID is necessary.

**Typical Selections:**  
- Often, TM1 and TM2 are set to around 10–15% of the total data points (for ramp-in and ramp-out, respectively).  
- This method is less common in routine biomolecular NMR unless there is a specific need.

---

## Choosing Values by Experiment Dimension

Below is a nicely formatted Markdown document that summarizes practical, experience‐based guidelines for setting TopSpin window parameters when processing protein spectra. Note that these guidelines are heuristic—your final settings should be fine‐tuned based on your specific hardware, acquisition parameters, and sample characteristics. The TopSpin processing manual itself provides definitions and allowed ranges for these parameters but leaves the final choices to the user citeturn1file1.

---

# Recommended Processing Parameters for Protein Spectra in TopSpin

The following guidelines are often used by experienced NMR spectroscopists when processing protein spectra. They are roughly categorized by protein size (small, medium, and large) and are presented here for common experiments such as 1H–15N HSQC, 1H–13C HSQC, triple-resonance (HNCO, HN(CA)CO, CBCA(CO)NH, HNCACB), and various NOESY experiments (3D/4D). 

> **Note:**  
> The TopSpin reference manual does not provide a “one size fits all” table of recommended parameters (WDW, LB, GB, SSB, TM1, TM2) tailored to protein size or specific experiments. Instead, it outlines the available window functions and their associated parameters, leaving choices to the user’s discretion based on experimental objectives.

---

### 1. Window Function (WDW) Choice

#### General Recommendations

- **Small Proteins (<15 kDa):**  
  - Aim: Maximize resolution while maintaining good signal-to-noise (S/N).  
  - Common Choices:  
    - *Gaussian* (`gm`) or  
    - *Sine-bell squared* (`qsine`).  
  - Rationale: When S/N is strong, sine-bell functions can deliver very sharp lines; if S/N is lower, a Gaussian or exponential option may help emphasize the signal.

- **Medium Proteins (15–35 kDa):**  
  - Aim: Accommodate somewhat broader lines and reduced S/N.  
  - Common Choices:  
    - *Gaussian* (`gm`) or  
    - *Sine-bell* (`sine` or `qsine`) with a modest sine-bell shift (SSB ≈ 2).

- **Large Proteins (>35 kDa):**  
  - Aim: Compensate for rapidly decaying FIDs and broad lines.  
  - Common Choices:  
    - *Exponential multiplication* (`em`) is typical (with a small LB of 1–3 Hz).  
    - In some multi-dimensional experiments, partial sine or trapezoidal windows may also be used.

---

### 2. LB (Lorentzian Broadening) and GB (Gaussian Broadening)

#### When Using Exponential or Gaussian Weighting

- **For Exponential Weighting (WDW = em):**  
  - **LB** is typically set to:
    - **Small proteins:** 0.3–1.0 Hz (especially in indirect dimensions).
    - **Large proteins:** 1–3 Hz (to compensate for faster decay).

- **For Gaussian Weighting (WDW = gm):**  
  - **LB** > 0 is used in conjunction with **GB**.
  - **GB** values generally range from 0.0 to 1.0:
    - **Common Values:** 0.1–0.4 for small/medium proteins.
    - A larger GB results in a narrower main lobe but can cause more distortion if the FID decays quickly.

> **Note:**  
> If you use sine or qsine window functions, LB and GB typically do not apply unless you mix function types (e.g., sinc/qsinc).

---

### 3. SSB (Sine Bell Shift)

- **Applicability:**  
  Used when applying a sine-bell (WDW = sine) or sine-bell squared (WDW = qsine).

- **General Guidelines:**  
  - Typical SSB values range from 0 to 3.
  - **Small Proteins:** An SSB of around 2 often provides a good compromise between resolution and S/N.
  - **Larger Proteins:** If signals decay more rapidly, you might opt for a slightly lower shift or consider switching to exponential/Gaussian weighting.

---

### 4. TM1 / TM2 (Trapezoidal Window)

- **Applicability:**  
  Use when choosing a trapezoidal window function (WDW = trap).

- **General Guidelines:**  
  - **TM1** sets the ramp-up (starting edge) and **TM2** the ramp-down (ending edge) of the FID.
  - Typical values (expressed as a fraction of the total FID length):
    - **Small Proteins:** TM1 ≈ 0.05 and TM2 ≈ 0.95.
    - **Medium Proteins:** TM1 ≈ 0.10 and TM2 ≈ 0.90.
    - **Large Proteins:** Similar to medium, though some users may opt for slightly broader ramps if necessary.

---

### 5. Experiment-Specific Notes

| **Experiment Type**                | **Direct Dimension (1H)**                                                     | **Indirect Dimensions (15N, 13C, or 1H in NOESY)**                                                                                                  |
|------------------------------------|-------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1H–15N HSQC / 1H–13C HSQC**       | **WDW:** EM<br>**LB:**<br>- Small: ~0.3 Hz<br>- Medium: ~0.5 Hz<br>- Large: ~1 Hz  | **WDW:** QSINE or GM<br>**LB:**<br>- Small: ~1 Hz<br>- Medium: ~2 Hz<br>- Large: ~3 Hz<br>**GB:** ~0.2 (if using GM)<br>**SSB:**<br>- Small: ~2<br>- Medium: ~2.5<br>- Large: ~3  |
| **Triple-Resonance (HNCO, HN(CA)CO, CBCA(CO)NH, HNCACB)** | **WDW:** EM<br>**LB:**<br>- Small: ~0.3 Hz<br>- Medium: ~0.5 Hz<br>- Large: ~1 Hz  | **WDW:** QSINE or GM<br>**LB:**<br>- Small: ~1 Hz<br>- Medium: ~2 Hz<br>- Large: ~3 Hz<br>**GB:** ~0.2<br>**SSB:**<br>- Small: ~2<br>- Medium: ~2.5<br>- Large: ~3  |
| **NOESY (3D/4D NOESY, N-/C-edited NOESY, HSQC-NOESY)**   | **WDW:** EM<br>**LB:**<br>- Small: ~0.3 Hz<br>- Medium: ~0.5 Hz<br>- Large: ~1 Hz  | **WDW:** QSINE (preferred) or GM<br>**LB:**<br>- Small: ~1 Hz<br>- Medium: ~2 Hz<br>- Large: ~3 Hz<br>**GB:** ~0.2<br>**SSB:**<br>- Small: ~2<br>- Medium: ~2.5<br>- Large: ~3<br>**TM1/TM2:**<br>- If using trap: Small ≈ 0.05/0.95, Medium ≈ 0.10/0.90, Large ≈ 0.10/0.90  |

---

### 6. Summary of Typical Starting Values

The table below provides a “starting point” matrix for processing parameters. These values are meant as guidelines and should be adjusted based on visual inspection and further optimization:

| **Protein Size** | **WDW (Indirect Dimensions)** | **LB (Hz)**             | **GB**         | **SSB**     | **TM1 / TM2 (if Trap is used)** |
|------------------|-------------------------------|-------------------------|----------------|-------------|----------------------------------|
| **Small**        | qsine or gm                  | 0.3 – 0.7               | 0.2 – 0.3      | 1 – 2       | 0.05 / 0.95                      |
| **Medium**       | gm (or qsine)                | 0.5 – 1.5               | 0.1 – 0.3      | 1 – 2       | 0.10 / 0.90                      |
| **Large**        | em or gm                     | 1 – 3                   | 0.0 – 0.2      | ~1          | 0.10 / 0.90                      |

> **Final Note:**  
> These recommendations are starting points only. In practice, you should perform a quick transform (using commands such as xf2, xfb, or tf1) to inspect the spectral quality, then fine-tune the parameters according to your sample’s specific characteristics and experimental requirements.

---

### Key Takeaways

- **WDW:** Defines the overall window function. Choices include `EM`, `GM`, `SINE`, `QSINE`, or `TM`.  
- **LB:** Specifies line broadening (positive for exponential; negative for Gaussian).  
- **GB:** Adjusts the width of the Gaussian window when using `GM`.  
- **SSB:** Shifts the sine bell function (typical values around 2–3 for indirect dimensions).  
- **TM1/TM2:** Only applicable for trapezoidal weighting to set ramp-up and ramp-down times.

The exact choices depend on the trade-off between resolution and S/N, and you may adjust these parameters based on the spectral quality and the specific characteristics of the experiment.

---

## Authors

- **Thomas Evangelidis**