---
title: "setup 4D acquisition"
layout: default
---

Here’s a simple visual to lock it in:

```
Indirect dimension (evolution time, t)

UNIFORM (full sampling):
t=0 |x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|  ... up to TD/2-1  → AQ(full)

NUS (good schedule: dense early, sparse late, but reaches long t):
t=0 |x|x| |x| | |x| | | |x|       |   |   |  x           |   → AQ(effective) ≈ desired
             (Poisson-gap / exp-biased; includes some long-t points)

NUS (bad schedule: truncated early by too-small NusT2):
t=0 |x|x| |x| | |x| | | |x|                           (stops halfway)
                                          ^ 
                                          longest sampled point << TD/2-1
                                          → AQ(effective) ≪ desired (peaks broaden)
```

* **TD** sets the full grid (max digital resolution if fully sampled).
* **AQ = TD / (2·SW)** is the full-evolution time *if* you sampled all points.
* **NusT2** caps how far along t you allow the NUS scheduler to go.

  * If NUSLIST’s max index ≈ **TD/2−1** → you’re reaching the *designed* long times.
  * If it tops out much earlier → your **effective AQ shrinks** → broader peaks.

---

# 4D NUS Pre-Flight Checklist (TopSpin) — for **HCCH-NOESY** and **HCNH-NOESY**

## A) Set chemical targets per dimension

* **Choose SW** to only cover what you need

  * ¹H aliphatic: ~0.5–5.5 ppm
  * ¹³C aliphatic: ~0–80 ppm
  * ¹⁵N (if present in other 4Ds): ~90–130 ppm
* **Pick desired AQ (ms)** from relaxation + crowding

  * ¹H(indirect): **4–6 ms** at ~25 kDa (3–8 ms typical)
  * ¹³C(indirect): **12–16 ms** (10–20 ms typical)

## B) Convert to TD (TopSpin relation)

* **AQ = TD / (2·SW)**  ⇒  **TD = 2·SW·AQ**  (SW in Hz)
* Round TD to convenient values (e.g., 64/96/128/160/192).

## C) Generate NUS with correct *reach*

* **Set `NusT2 = 2 × desired AQ`** for each indirect dim (critical to reach long t).
* Use **Poisson-gap / exp-biased** schedules (dense early, sparse late, but not flat).
* **%NUS (total samples):** start **2–5 %** for 4D NOESY at 25 kDa.

## D) Balance %NUS vs NS (time budgeting)

* Keep **NS per increment minimal** (e.g., **8 scans**).
* Prefer **more unique points (higher %NUS)** over cranking NS for better time-efficiency.
* S/N scales ≈ **√NS**; resolution comes from **TD/AQ**, not %NUS.

## E) Sanity-check the actual NUSLIST (do this every time)

* For each indirect dim, ensure the **max index ≈ TD/2 − 1** appears (at least a few entries).
* Density should **decay** with t (not flat).
* If max index ≪ TD/2 − 1 → **increase NusT2** and regenerate.

## F) Processing guards for fast-decaying ¹H(indirect)

* **Apodization:** QSINE (SSB 2–3) to tame t₁-noise.
* **Linear Prediction (optional, conservative):** forward or forward-backward, extend **+10–20 %** max; skip if S/N is weak or there’s a water ridge.
* **Zero-fill** to next power of two; mild baseline correction.

## G) Quick numeric templates (25 kDa, aliphatic 4D)

* **If F1 = ¹H(indirect):** SW ≈ 5 kHz, **AQ 5 ms → TD ≈ 50 → use 64**; set **`NusT2 ≈ 10 ms`**
* **¹³C(indirect) dims (F2/F3):** SW ≈ 12 kHz, **AQ 14 ms → TD ≈ 336 → use 320/352**; **`NusT2 ≈ 28 ms`**
* **Direct ¹H (F4):** TD 1024–2048 (AQ ~0.10–0.15 s)

## H) One-minute pre-launch pilot

* Start a **short pilot** (a few minutes), reconstruct, and check:

  * **F1/F2 linewidths** (no truncation)
  * **S/N** acceptable
  * **No obvious NUS artefacts** → if issues, adjust `%NUS` / `NusT2` / apodization.

**Same rules apply** whether F1 is ¹H in **HCCH** or **HCNH** NOESY: ¹H(indirect) has short T₂ → keep AQ modest, ensure NUS reaches long-t via `NusT2 = 2×AQ`, and bias sampling toward early times while still touching the tail.


