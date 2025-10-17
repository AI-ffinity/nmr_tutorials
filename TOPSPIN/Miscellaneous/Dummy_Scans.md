### What are “dummy scans” (DS)?

In TopSpin the *dummy scans* (parameter **DS**) are additional scans that are executed **before** the first “real” scan is stored in the FID.  
Their signal is **discarded**, but they still run through the entire pulse sequence (pulse, acquisition time **AQ**, relaxation delay **D1**, gradients, decoupling, etc.).

*Why bother?*  
During the very first few repetitions the system has not yet reached a steady state:

* the bulk magnetisation may be partially saturated from prescan pulses, tuning-matching, shimming, or a previous experiment;  
* the analogue receiver (and automatic receiver-gain regulation) needs a couple of scans to settle;  
* any steady-state gradients or shaped pulses that store longitudinal magnetisation have not yet reached their equilibrium pattern.

By discarding those initial transients you ensure that every **stored** scan is acquired under identical, steady-state conditions, giving you reproducible phase, baseline and intensity.

---

### How is **DS** related to the relaxation delay **D1**?

1. **D1 is executed during every scan—dummy scans included.**  
   If you set D1 = 2 s and DS = 2, the spectrometer will spend 2 s recovering longitudinal magnetisation *before* each of the two dummy scans, just as it will before every stored scan.

2. **DS does *not* compensate for too short D1.**

   * Suppose your analyte’s longest T₁ is 3 s but you choose D1 = 1 s.  
   * After a few dummy scans the sample will indeed reach a *steady* state, but that state is a *saturated* one (magnetisation never fully recovers).  
   * The result is reduced peak integrals and possible line-shape distortions—even though DS was >0.

3. **Choosing DS and D1 in practice.**

   * **D1** should be ≳ 5 × longest T₁ if you need accurate quantitative integrals; shorter is fine for mere identification.  
   * **DS** is usually 2–4 for routine 1D proton spectra; more rarely needed unless you use complicated steady-state pulse trains.

---

### Bottom line

*Dummy scans* are there to throw away the startup “junk” and let the pulse-acquire-relax cycle stabilise **before** you begin averaging.  
They work *with* the relaxation delay **D1**, not in place of it: DS ensures stability, while D1 ensures full magnetisation recovery.  

---

# Authors
- Thomas Evangelidis