---
title: "INCOMPLETE! Measurement of S/N ratio in 15N-edited 3D NOESY and in 4D HCNH NOESY."
layout: default
---

# INCOMPLETE! Measurement of S/N ratio in 15N-edited 3D NOESY and in 4D HCNH NOESY.

------------

15N-edited 3D NOESY -> F1: H, F2: N, F3: HN
4D HCNH NOESY -> F1: C, F2: HC, F3: N, F4: HN

* First we look up at the N-HN positive projections to identify common peaks between the two spectra 
with strong signal, which we will use for comparison of the S/N.
* `projplp 23 all all 23` in 15N-edited 3D NOESY and `projplp 34 all all 34` in 4D HCNH NOESY.
* Open the `34` projection of the 4D and type `pp` for automated peak picking. Switch the 
"Minimum intensity" to the "highest contour level" and then click "OK".
* Type `peaks` and sort the peaks by intensity. Then iterate through all of them from the 
beginning one by one, double-clicking and identifying non-overlaping peaks. You just need 3-5
with strong signals, not all of them. For example, I chose peaks 221, 212, 209, 207 (!), 204 (!).
* Note down the coordinates of the chosen peaks, switch to the `23` projection of the 3D NOESY
and look them up.

---

# Authors
- Thomas Evangelidis