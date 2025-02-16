Overview of Window Function Parameters (PROCPARS tab) for Protein Spectra
---

### 1. WDW (Window Function Type)

**What It Is:**  
WDW sets the type of weighting (apodization) function applied to the time-domain data before Fourier transform. Common choices include:  
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

### Choosing Values by Experiment Dimension

#### 1H–15N HSQC
- **Direct 1H dimension:** Use `EM` or `GM` with LB ≈ 0.3–0.5 Hz.
- **Indirect 15N dimension:** Typically use `SINE` (or `QSINE`) with SSB ≈ 2–3; alternatively, Gaussian parameters (negative LB, GB ≈ 0.1–0.3) can be applied.

#### 1H–13C HSQC
- **Direct 1H dimension:** Similar to the HSQC above.
- **Indirect 13C dimension:** Use QSINE with SSB ≈ 2–3 or mild Gaussian parameters, depending on the data quality.

#### Triple-Resonance Experiments (e.g., HN(CO)CA, CBCA(CO)NH, HNCACB)
- Typically 3D experiments:
  - **Direct 1H dimension:** Exponential or Gaussian weighting with modest LB.
  - **Indirect 15N and 13C dimensions:** QSINE is a common default with SSB around 2–3. Adjust slightly (e.g., larger SSB or modest LB of 1–3 Hz) if peaks are broader.

#### NOESY Experiments (3D/4D, including HCNH NOESY, HCCH NOESY, N-/C-edited 3D NOESY)
- **Direct 1H dimension:** Often processed using `EM` or `GM`.
- **Indirect dimensions (1H, 13C, 15N):** SINE/QSINE weighting is very common to reduce t1 noise, with SSB ≈ 2–3.  
- For 4D experiments with multiple indirect dimensions, similar strategies apply to each dimension.

#### Trapezoidal (TM1/TM2)
- Use only if a linear ramp is specifically desired.
- Typical settings: TM1 = 10–15% and TM2 = 10–15% of the total number of FID points.

---

### Key Takeaways

- **WDW:** Defines the overall window function. Choices include `EM`, `GM`, `SINE`, `QSINE`, or `TM`.  
- **LB:** Specifies line broadening (positive for exponential; negative for Gaussian).  
- **GB:** Adjusts the width of the Gaussian window when using `GM`.  
- **SSB:** Shifts the sine bell function (typical values around 2–3 for indirect dimensions).  
- **TM1/TM2:** Only applicable for trapezoidal weighting to set ramp-up and ramp-down times.

The exact choices depend on the trade-off between resolution and S/N, and you may adjust these parameters based on the spectral quality and the specific characteristics of the experiment.

