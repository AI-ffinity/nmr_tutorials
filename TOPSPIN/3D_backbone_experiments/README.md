# Protein Backbone 3D NMR Spectra Acquisition Workflow

---

## 1 · Initial Calibrations and Test HSQCs

First we did 1H pulse calibration (exp.&nbsp;1), while for 13C and 15N we used the default parameters from `getprosol`.  
Then we measured a short 15N HSQC (exp.&nbsp;2) and a short 13C HSQC (exp.&nbsp;3) with full spectral width on N and C, respectively.

---

## 2 · CBCAcoNH N–HN Plane Comparison

We also measured the N–HN planes of two types of CBCAcoNH pulse programs, the standard version and the one with Water-Gate, 
and we want to select the best one for this sample.

* `xfb` – process the N–HN planes from both CBCAcoNH experiments (exp.&nbsp;4 and&nbsp;5) and then `.ph` to correct their phase.  
*  `.md` – overlay the N–HN planes from exp.&nbsp;4 and&nbsp;5, then click **“copy the contour 
levels from first to other datasets.”** The standard version (red; exp.&nbsp;4) seems to be more sensitive.

![fig1](images/fig1.png)

---

## 3 · Set-Up of Full-Length HSQC Experiments

`re 2` to display the test 15N HSQC (experiment&nbsp;2) and hit `new` to create a new 15N HSQC with the desired spectral 
width in the N dimension. Name it **21**.  

![fig2](images/fig2.png)  

`re 2` again, zoom into the region of interest, then **Right-click → Save Display Region To… → Parameters ABSF1/2**. In 
**PROCPARS** note the N-axis boundaries, e.g. **100 ppm → 135 ppm**.

`re 21`, then `eda` to open **ACQUPARS**. Set:

| Parameter | Value |
|-----------|-------|
| `SW{F1}`  | 135-100 ppm  |
| `O1P{F1}` | 100+(135-100)/2 ppm |
| `NS`      | 16 |

![fig3](images/fig3.png)

`re 3`, followed by `new`, to create a full 13C HSQC from the test 13C HSQC (experiment&nbsp;3). Name it **22**.  

![fig4](images/fig4.png)

`re 3` again, zoom into the region of interest, then **Right-click → Save Display Region To… → Parameters ABSF1/2**. 
Record the aliphatic-C limits, e.g. **4.6 ppm → 77.5 ppm**.  

`re 22`, then `eda` and set:

| Parameter | Value                       |
|-----------|-----------------------------|
| `SW{F1}`  | 77.5-4.6 (=72.9) ppm        |
| `O1P{F1}` | 4.6 + 72.9 ⁄ 2 (=41.05) ppm |
| `NS`      | 16                          |

Run `expt` to estimate the experimental time.

---

## 4 · Set-Up of CBCAcoNH Experiments

Note the N and aliphatic-C spectral widths from the 15N HSQC (exp.&nbsp;21) and 13C HSQC (exp.&nbsp;22).  

![fig5](images/fig5.png)  

`re 4` to load the selected standard CBCAcoNH, then `new` to create **23**. In **PROCPARS** set:

| Parameter | Value                           |
|-----------|---------------------------------|
| `TD{F2}`  | 60                              |
| `TD{F1}`  | 128                             |
| `SW{F1}`  | 73.0 ppm                        |
| `O1P{F1}` | 41.1 ppm                        |
| `SW{F2}`  | 35 ppm (default value, keep it) |
| `O1P{F2}` | 117.5 ppm                       |

![fig6](images/fig6.png)  

Because we have already measured the N–HN plane, we do **not** repeat `pulsecal`. Run `gs` (interactive acquisition) to 
check that the experiment runs smoothly. TopSpin raises an error within seconds if, for example, a negative interval 
occurs or the signal overflows. If everything is fine, press `stop`. Ideally, monitor the first increment only.

![fig7](images/fig7.png)

`re 21`, then `new`, to create a short QC 15N HSQC named **25** that checks protein stability. Adjust the Title, then `eda` and set:

| Parameter | Value |
|-----------|-------|
| `NS` | 2 |

![fig8](images/fig8.png)  

---

## 5 · General 3D Motif

For each 3D experiment we will:  
1. Create the full-length 3D experiment.  
2. Run `pulsecal` to calibrate the 1H 90° pulse. A window shows the 90° pulse and its power level; click **OK** to accept.  
3. Record a short QC 15N HSQC after the 3D experiment.

---

## 6 · HNCACB (exp.&nbsp;25)

`re 6`, then `new` → **25**. In `eda` set:

| Parameter | Value |
|-----------|-------|
| `SW{F1}`  | 73.0 ppm |
| `O1P{F1}` | 41.1 ppm |
| `O1P{F2}` | 117.5 ppm |

Run `pulsecal` (automatic 1H 90° calibration). After collecting some data this command will pop up a window with a 
90o pulse and its associated power level. Clicking "OK" will enter the displayed values into the current parameter set. 
For 13C and 15N we used the default parameters in the "prosol" parameters table (command `getprosol`). If we wanted to 
optimize the 13C 90o pulse and 15N 90o pulse, there are special calibration pulse sequences which we should have launched as 
individual experiments (`zg` command).

![fig9](images/fig9.png)  

Run `gs`; if no error appears, press `stop`.  
Create QC 15N HSQC: `re 24` → `new` → **26**.

---

## 7 · HNCO (exp.&nbsp;27)

![fig10](images/fig10.png)  

`re 7`, `new` → **27**. In `eda` set:

| Parameter | Value |
|-----------|-------|
| `TD{F2}`  | 60 |
| `O1P{F2}` | 117.5 ppm |

Run `pulsecal`, then `gs`, then `stop`.  
Create QC 15N HSQC → `re 24` → `new` → **28**.

---

## 8 · HNcaCO (exp.&nbsp;29)

`re 8`, `new` → **29**. Set:

| Parameter | Value |
|-----------|-------|
| `TD{F2}`  | 60 |
| `O1P{F2}` | 117.5 ppm |

![fig11](images/fig11.png)  

Run `pulsecal`, `gs`, `stop`.

Create QC 15N HSQC → `re 24` → `new` → **30**.

---

## 9 · HNcoCA (exp.&nbsp;31)

`re 3`, zoom into the CA–HA region, and save the C range (e.g. 42–76 ppm).  

![fig12](images/fig12.png)

`re 9`, `new` → **31**. In `eda` set:

| Parameter | Value |
|-----------|-------|
| `TD{F2}`  | 60 |
| `SW{F1}`  | 76−42 ppm |
| `O1P{F1}` | 42+(76−42)/2 ppm |
| `O1P{F2}` | 117.5 ppm |

![fig13](images/fig13.png)

Run `pulsecal`, `gs`, `stop`.

Create QC 15N HSQC → `re 24` → `new` → **32**.

---

## 10 · HNCA (exp.&nbsp;33)

`re 10`, `new` → **33**. Use the same CA window (42–76 ppm) and set:

| Parameter | Value |
|-----------|------|
| `TD{F2}`  | 60 |
| `SW{F1}`  | 76-42 ppm |
| `O1P{F1}` | 42+(76-42)/2 ppm |
| `O1P{F2}` | 117.5 ppm |

![fig14](images/fig14.png)  

Run `pulsecal`, `gs`, `stop`.

Create QC 15N HSQC → `re 24` → `new` → **34**.

---

## 11 · hNcaNNH (exp.&nbsp;35)

`re 11`, `new` → **35**. Then set: 

| Parameter | Value |
|-----------|-------|
| `TD{F2}`  | 60 |
| `SW{F1}`  | 35 ppm (keep) |
| `SW{F2}`  | 35 ppm (keep) |
| `O1P{F1}` | 117.5 ppm |
| `O1P{F2}` | 117.5 ppm |

![fig15](images/fig15.png)  

Run `pulsecal`, `gs`, `stop`.

Create QC 15N HSQC: `re 24` → `new` → **36**.

---

## 12 · Queue Management

`re 21`, then `multiexpt 16` to estimate the total time for all 16 experiments.

![fig16](images/fig16.png)  

`re 27` to switch to HNCO (the most sensitive 3D). In `eda` set `DS` = 4, then `zg` to acquire one increment. When 
finished, run `qsin`, `ft`, `.ph`. After confirming protein signal, stop with `halt` (or `stop`) and reset `DS` back to 32.

![fig17](images/fig17.png) 

Finally, `re 21`, then `multizg 16` to launch all experiments serially.

![fig18](images/fig18.png)  

---

## Notes

* The 3D experiments **employ shaped pulses**, unlike the 2D HSQCs. `pulsecal` optimises the 1H 90° pulse **and** 
recalculates all shaped pulses (including decoupling) with the new value. Otherwise, we would have to copy the 
calibrated 1H 90° pulse parameters from the 2D to the 3D experiment and optimise each shaped pulse manually.  
* HSQC spectra define the H, C and N windows (`SW`, `O1P`) that we copy into the 3D experiment setups.  
* `TD` (size of FID), `SW` (spectral width) and `AQ` (acquisition time) are inter-dependent: setting any two automatically 
determines the third in TopSpin.  



## 13C and 15N 90-Degree Hard Pulse Calibration

* `lock`
* `atmm`: select “1H” and match/tune; then select “13C”; then “15N.” Finally, click **Close and Store Values**.
* `loopadj`
* `topshim gui`: set **Dimension** → 1D; **Optimise for** → 1H; **After** → Z-X-Y-XZ-YZ-Z; **Only** → yes. Click **Start**.
* Once completed, set **After** → off and run:

  ```
  topshim ordmax=7
  ```

  This optimizes all parameters containing Z up to the 7th order (the maximum order of Z is 8). One strategy is to first roughly optimize Z up to 5th order, then the combinations of Y and Z up to 5th order, and finally Z up to 7th order.

![pulsecal\_fig1](images/pulse_calibration/fig1.png)

* `re 1` to switch to the 1D ¹H PP; then `P1` to check that the 90° high-power pulse length is correctly set. Next, run:

  ```
  zg
  efp
  ```

  to verify that the signal from D₂O isn’t distorted (it must appear as a perfect symmetric bell shape).

![fig2](images/pulse_calibration/fig2.png)

### Calibrate 13C 90-Degree Hard Pulse Length

* Copy the ¹³C and ¹⁵N pulse-calibration experiments to a new directory. These contain a special pulse sequence: when the 90° high-power pulse length is optimal, the signal is zero; if shorter than optimal, the signal is positive; if longer, the signal is negative. Enter the ¹³C experiment and run:

  ```
  pulsecal
  ```

  to calibrate the ¹H pulse length (P1) first. `pulsecal` will also read and update **P3** (the 90° high-power pulse for ¹³C) from the “prosol” table.

![pulsecal\_fig2](images/pulse_calibration/fig2.png)

* Run `ased` and inspect **P3**. It should be the default value from the “prosol” table (14.2 μs here). Set it to a lower value (e.g. 5.0 μs, or divide by 2) to get a spectrum you can phase—otherwise, a near-90° pulse will nullify the signal. Then run:

  ```
  zg
  qsin
  ft
  .ph
  ```

  to acquire and phase the spectrum. Correct phasing is crucial, as this spectrum feeds into the next step (`popt`); without it, signals will have dispersion character (positive and negative peaks), making the 0-signal point ambiguous.

![pulsecal\_fig3](images/pulse_calibration/fig3.png)

* Zoom into the signal region to be optimized. Right-click → **Save Display Region To…** → **Parameters F1/F2** → **OK**.

![pulsecal\_fig4](images/pulse_calibration/fig4.png)

* Run `popt` to open the parameter-optimization window. Set:

  * **GROUP** → 1
  * **PARAMETER** → P3
  * **OPTIMUM** → ZERO
  * **STARTVAL** → 12
  * **ENDVAL** → 16
  * **INC** → 0.4
    Then click **Save** and **Start Optimize**, overwrite → **y**.

![pulsecal\_fig5](images/pulse_calibration/fig5.png)

* Run `P1` and note its value (e.g. 13.07 μs). Do the same for `PLW1` (e.g. –11.46 dB). These will be needed for `getprosol`.
* Once acquisition finishes, run:

  ```
  re 1 1
  ```

  to invert the signal sign. Skipping this means spectrum “999” won’t load correctly.

![pulsecal\_fig6](images/pulse_calibration/fig6.png)

* Run:

  ```
  re 1 999
  ```

  to display a series of spectra (11 spectra with pulse lengths from 12.0 to 16.0 μs in 0.4-μs increments). If the optimizer doesn’t find an exact zero within these values, it interpolates. Here it reports an optimal **P3** value of 13.382361 μs.

![pulsecal\_fig7](images/pulse_calibration/fig7.png)

* Run `P3` and note its value (e.g. 13.4 μs). Do the same for `PLW1` (e.g. –21.68 dB). These will also be needed for `getprosol`.

## Calibrate 15N 90-Degree Hard Pulse Length

* Run `re 2 1` and then `pulsecal`. Compare the output 90° pulse value (13.10 μs) with the one previously obtained—they must be very similar.
* Run `ased` and set **P21** (the parameter controlling the ¹⁵N 90° hard pulse length) to a lower value, e.g. 10.0 μs, than the default from the “prosol” table (34.0 μs). Then run:

  ```
  zg
  qsin
  ft
  .ph
  ```

  to acquire and phase the spectrum.

![pulsecal\_fig8](images/pulse_calibration/fig8.png)

* Zoom into the signal region to be optimized. Right-click → **Save Display Region To…** → **Parameters F1/F2** → **OK**.

![pulsecal\_fig9](images/pulse_calibration/fig9.png)

* Run `popt` to open the parameter-optimization window and set:

  * **GROUP** → 1
  * **PARAMETER** → P21
  * **OPTIMUM** → ZERO
  * **STARTVAL** → 32
  * **ENDVAL** → 36
  * **INC** → 0.4
    Then click **Save** and **Start Optimize**, overwrite → **y**.

![pulsecal\_fig10](images/pulse_calibration/fig10.png)

* Once acquisition finishes, run `re 2 1` to invert the signal sign, then `re 1 999` to preview the optimization. The result may look too noisy to infer an accurate P21 value—this is because only 4 scans were used.

![pulsecal\_fig11](images/pulse_calibration/fig11.png)

* Repeat the process with more scans. Run:

  ```
  NS 16
  popt
  ```

  and narrow the pulse-length range: **STARTVAL** → 33, **ENDVAL** → 37. Then click **Save** and **Start Optimize**, overwrite → **y**.

![pulsecal\_fig12](images/pulse_calibration/fig12.png)

* When optimization finishes, run `re 2 1` followed by `re 2 999` (the former is required to load spectrum “999”). The 11 spectra with progressively lower signal will be better resolved, and the optimal P21 (e.g. 35.218787 μs) will be displayed—interpolated from the intensities.

![pulsecal\_fig13](images/pulse_calibration/fig13.png)

* Run `P21` and note its value (e.g. 35.2 μs). Do the same for `PLW3` (e.g. –25.55 dB). These will be needed for `getprosol`.

### Apply the Optimum ¹H, ¹³C, and ¹⁵N Pulse Lengths to All Experiments

* Now apply the optimum 90° pulse lengths of ¹H, ¹³C, and ¹⁵N to every experiment you wish to record. Run:

  ```
  re 41
  getprosol 1H 13.07 -11.46 13C 13.4 -21.68 15N 35.2 -25.55
  ```

  Then, for each spectrum, repeat:

  ```
  re 42
  getprosol 1H 13.07 -11.46 13C 13.4 -21.68 15N 35.2 -25.55

  re 43
  getprosol 1H 13.07 -11.46 13C 13.4 -21.68 15N 35.2 -25.55

  re 44
  getprosol 1H 13.07 -11.46 13C 13.4 -21.68 15N 35.2 -25.55

  re 45
  getprosol 1H 13.07 -11.46 13C 13.4 -21.68 15N 35.2 -25.55

  re 46
  getprosol 1H 13.07 -11.46 13C 13.4 -21.68 15N 35.2 -25.55
  ```

  If you had run only `getprosol 1H 13.07 -11.46`, the ¹³C and ¹⁵N values would be pulled from “prosol” and would be suboptimal for this sample.

![pulsecal\_fig14](images/pulse_calibration/fig14.png)

* Finally, verify that all spectra can be recorded without issues. For each experiment:

  ```
  re 41
  o1      # Check transmitter-frequency offset [F2,F1]
  gs      # “Stop”

  re 42
  o1      # optional
  gs      # “Stop”

  re 43
  o1      # optional
  gs      # “Stop”

  re 44
  o1      # optional
  gs      # “Stop”

  re 45
  o1      # optional
  gs      # “Stop”
  ```

  O1 should be identical in all experiments.

![pulsecal\_fig15](images/pulse_calibration/fig15.png)

* Run:

  ```
  re 41
  multiexpt 6
  ```

  to estimate total experiment time. If satisfied, run:

  ```
  multizg 6
  ```

  to start the recordings.


### Bottom-up 13C and 15N 90° Hard Pulse Calibration on 850 MHz by Me

* `lock`
* On high-field cryo-probes, Bruker recommends doing automatic tuning-matching from the nucleus with the highest frequency to the lowest, namely `1H → 13C → 15N`. You can either select the nuclei manually or, better, issue:

  ```
  atma high
  ```

  to do it automatically.
* Once finished, hit:

  ```
  atmm
  ```

  for manual refinement. Optimize the 15N. The Wobble sweep width of 13C is very wide (12.017 MHz by default); therefore, we must zoom in on the baseline of the signal. Set it to 4.0 and click **Set**, then refine the position of the minimum. Likewise, set the Wobble sweep width of 1H to 4.0 MHz (default: 12.754 MHz) and refine manually.

![pulsecal\_fig16](images/pulse_calibration/fig16.png)

* `topshim`
* `loopadj`
* `topshim gui`: set **Dimension** → 1D, **Optimise for** → 1H, **After** → Z-X-Y-XZ-YZ-Z, **Only** → yes. Click **Start**.
  The “3D” option is more thorough but much slower; it’s usually unnecessary unless you’ve recently replaced the probe. It helps for water-containing samples in wider tubes (e.g. Shigemi 5 mm), but in a 3 mm tube there’s little X-Y inhomogeneity to correct. To save time—since we already completed the 1D optimization—issue:

  ```
  topshim ordmax=7
  ```

  to optimize all Z combinations up to 7th order (default is 5th).

![pulsecal\_fig17](images/pulse_calibration/fig17.png)

* Let’s measure and check the 1D proton now. Run:

  ```
  re 1
  ased
  ```

  The existing **P1** value (13.130 μs) is too high and will give a very strong signal (probably left by a previous `pulsecal` or `getprosol`). Lower it to 1.0.

![pulsecal\_fig18](images/pulse_calibration/fig18.png)

* Run:

  ```
  zg
  efp
  .ph
  ```

  for manual phase correction. Zoom into the peak and verify that the shape is symmetric.

![pulsecal\_fig19](images/pulse_calibration/fig19.png)

### Calibrate 13C 90° Hard Pulse Length

Nothing new.

### Calibrate 15N 90° Hard Pulse Length

Nothing new.

### Apply the Optimum ¹H, ¹³C, and ¹⁵N Pulse Lengths to All Experiments

* Run `re 1` and zoom in on the peak region. Place your cursor in the middle to see the maximum O1 value (water’s resonance frequency in this sample), here 3991.1 Hz. However, the optimum may deviate by a few Hz; therefore, issue:

  ```
  o1calib
  ```

  which calculates it. Then apply the output O1 value to the spectra you want to measure and, using:

  ```
  gs
  ```

  assess the FID shape to decide the exact O1. This is important because experiments with water-signal suppression work best when O1 is exactly at the water resonance. Here we measure only gradient-selected experiments, where it’s less critical; regardless, it’s ideal to set an accurate O1.

![pulsecal\_fig20](images/pulse_calibration/fig20.png)

* When it finishes, run:

  ```
  O1
  ```

  to display the found value; in this case, 3994.21 Hz.

![pulsecal\_fig21](images/pulse_calibration/fig21.png)

* Execute `getprosol` with the ¹H, ¹³C, and ¹⁵N calibrated parameters for all experiments to be measured.

* Run `re 8` to switch to the 3D experiment and experimentally find the optimum O1 value. Hit `gs`, go to the **Offset** table, enter the O1 value from `o1calib` (3994.21 Hz), and press Enter.

![pulsecal\_fig22](images/pulse_calibration/fig22.png)

* Then enter the previous value, 3991.10 Hz, and press Enter. You will see a less wavy FID, indicating it is better than 3994.21 Hz. This occurs because the modular differences between observed and resonance frequencies are minimized, giving a smoother FID. In principle, one could manually alter O1 and observe its effect, but here it is redundant. Finally, click **Stop**.

![pulsecal\_fig23](images/pulse_calibration/fig23.png)

* Update the `O1` value in all experiments you plan to run.


---

# Authors
- Thomas Evangelidis