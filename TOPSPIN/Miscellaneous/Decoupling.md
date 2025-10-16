# Beginner‑friendly guide to **decoupling** in NMR

> **Goal:** understand why we switch on “proton decoupling” when we record a^13C spectrum and what changes when we move to 3‑D or 4‑D biomolecular experiments.

---

## 1.  Why do we decouple ^13C from ^1H?

### The problem  
*Every carbon that has directly‑bonded hydrogens is “talking” to them through a scalar (J) coupling of ~125Hz.*  
That coupling splits one carbon line into 2, 3 or 4 little peaks (doublet, triplet, quartet). Result:

* weaker individual lines (signal‑to‑noise is spread out)  
* messy spectrum—hard to read or integrate  

### The fix: **broadband proton decoupling**  
While you **detect** the ^13C signal, you keep a separate RF channel blasting the protons with a rapid pulse train (WALTZ‑16, GARP, …).  
Those flips happen so fast that, from carbon’s viewpoint, the proton spin is averaging out—so the coupling disappears.  
**Outcome:** each carbon collapses to a single sharp peak and the spectrum is 2‑3× more intense thanks to the NOE.

---

## 2.  How does decoupling work (nutshell)?

| Step | What happens                                                      |
|------|-------------------------------------------------------------------|
| 1    | A second transmitter is set to the proton frequency.              |
| 2    | During carbon data‑acquisition that transmitter fires a tiny pulse every few microseconds (special phase patterns make it “broadband”). |
| 3    | Proton spins flip ≫100times inside one dwell time → ^13C never “sees” a stable coupling partner; J_CH averages to zero. |

---

## 3.  One‑dimensional ^13C: which decoupling mode should I choose?

| Mode               | When to use it      | What you get                               |
|--------------------|---------------------|--------------------------------------------|
| **Continuous**     | Routine ID / assignment | Single peak per carbon **+ big NOE boost** (fast, beautiful) |
| **Inverse‑gated**  | Quantitative work (integrations) | Turns RF *off* during relaxation delay, *on* during acquisition → no NOE (areas stay accurate) |
| **Off‑resonance**  | Want to see long‑range couplings | Only partly collapses the multiplets—leaves small ^2J/^3J visible |

---

## 4.  What changes in multi‑D protein experiments?

### A) 2‑D HSQC / HMQC  
* Detecting **protons** → keep **^15N or ^13C** decoupled while you read the FID.  
  *Gives one clean cross‑peak instead of a doublet.*

### B) 3‑D triple‑resonance (e.g. HNCO)  
1. **Indirect periods (t₁, t₂)** ‑‑ J‑couplings are **allowed** or **refocused** on purpose (they carry the magnetisation along the backbone).  
2. **Detection period** ‑‑ you decouple only the nucleus directly coupled to the detected one:  
   * Proton‑detected (usual) → decouple **^15N**.  
   * Carbon‑detected (rare) → decouple **^1H** *and* often **^15N**.

### C) 4‑D experiments  
If you decide to **detect carbon**, two other nuclei (^1H and ^15N) are still coupled to it.  
You must run **simultaneous low‑power decoupling on two channels**—a bigger RF‑power juggling act (watch sample heating & SAR limits).  
If you stick with **proton detection** (most common), only one heteronucleus (^15N) needs decoupling.

---

## 5.  Practical checklist when setting up decoupling in TopSpin

1. **Pick a sequence**  
   * Continuous WALTZ‑16 or GARP for routine ^13C.  
   * Inverse‑gated if you care about integrals.
2. **Set the power level (`PL`)** low enough to avoid sample heating but high enough to cover the proton bandwidth.  
3. **Check duty cycle** (percentage of time RF is on) to stay under SAR limits—especially important in 4‑D carbon‑detected work.  
4. **Tune & match** each channel before starting—poor tuning ruins decoupling efficiency.  
5. **Monitor temperature** in long experiments; strong decoupling can warm the sample.

---

## 6.  Key take‑aways

* **Decoupling collapses multiplets → simpler, stronger peaks.**  
* In 1‑D ^13C we decouple protons almost always; in 3‑D/4‑D we decouple only the nuclei that would otherwise split the **detected** dimension.  
* Extra dimensions don’t automatically mean extra decoupling; it depends on which nucleus you are listening to in the final FID.

With these basics you can confidently choose when and how to switch on decoupling in your next NMR experiment.

---

# Authors
- Thomas Evangelidis