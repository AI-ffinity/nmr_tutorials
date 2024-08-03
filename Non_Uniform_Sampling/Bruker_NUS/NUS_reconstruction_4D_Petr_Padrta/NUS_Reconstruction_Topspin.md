# NUS Processing of 4D NOESY

This tutorial covers the NUS processing of 4D NOESY for various experiments involving Ubiquitin and SAK 42D using Bruker Topspin software.

## Overview

- **Experiments:** AIffinity/101 (Ubiquitin), AIffinity_2024/12 (Ubiquitin), AIffinity_950/72 (SAK 42D)
- **Software:** Bruker Topspin 4.1.4 on CentOS 7
- **Processing Time:** ~2-3 hours on 16 CPUs
- **Memory Required:** ~20-30GB
- **Parallelization:** 
  - CS/IST algorithm uses all available CPUs
  - MDD algorithm uses 1 CPU (Parameter MDDTHREADS from original MddNMR seems to be ignored here)
- **Licensing:** Requires commercial license for TOPSPIN_NUS and TOPSPIN_NUS_CS
- **Note:** Topspin internally uses modified MddNMR

## Selection of PHC0 and PHC1 Angles for Phase Correction

NUS reconstruction works better when 1D spectra are properly phased. We need to find the PHC0 and PHC1 values only for the direct dimension (F4); the phases in indirect dimensions are ideally given by the pulse programs. There are two ways to do this:

1. **Using 2D Planes with the Same Pulse Program:**
    - Phase correct the 2D planes and copy the PHC0 and PHC1 values to the PROCAPRS of the raw 4D spectrum.

2. **Without 2D Planes:**
    - Process the whole spectrum in faster mode (e.g., with smaller SI values).
    - Perform the HN-N projection with the `projpln` command (see "Visual comparison with 2D HSQC in Topspin").
    - Phase it, copy the PHC0 and PHC1 values to the PROCAPRS of the raw 4D spectrum, and reprocess with full SI.

## Processing of AIffinity/101 (Pulseprogram: noehcnhwg4d_nove)

### Axis Order: HN-15N-13C-HC

1. **Correct 1-Point Delay in 13C:**
    - Create a new nuslist with a 1-point shift in the 13C axis and replace the original nuslist:
      ```sh
      awk '{print $1,$2+1,$3}' nuslist > nuslist.off
      mv nuslist nuslist.back
      mv nuslist.off nuslist
      ```
    - Extend the 13C axis in Topspin by 1 complex point by changing static param NusTD(F2) from 160 to 162:
      ```sh
      2s NusTD 162
      ```
      This should automatically set static TDeff(F2) also to 162 and allow processing with the adjusted nuslist.

2. **Set Main Processing Parameters (`edp`):**
    - **Reference:** Set SI to the next power of 2 of TD. You might try lower SI but be ready to confirm processing of individual planes.
      - SI: 1024 256 256 512
    - **Phase:** Opposite sign of NMRPipe/SSA
      - PHC0: -107 0  0  0 
      - PHC1: 0  0  0  0 
      - PH_mod: pk pk pk pk
    - **Baseline:** Remove solvent
      - BC_mod: qfil no no no
        or
      - BC_mod: qpol no no no
      - Adjust BCFW accordingly
    - **Fourier:** Set ROI in direct dimension, cca 10-6 ppm
      - STSR: 55
      - STSI: 350
      - FCOR: 0.5 0.5 0.5 0.5
    - **NUS:**
      - Mdd_mod: cs
      - When running the processing it automatically sets:
        - MDD_CsAlg: IST 
        - MDD_CsVE: true

3. **Process 4D Spectrum:**
    ```sh
    ftnd 0
    ```

4. **Optional Baseline Correction in F4:**
    ```sh
    absnd 4
    ```

5. **Correct Known TopSpin Bug (Badly Written CAR) + Correct Shift by 1/4*SW in 13C:**
    - **CAR of HC Axis:** Written as 6.666 ppm, but should be 4.7 ppm
      - Total shift of HC(F1) axis:
        - In Topspin: Set SR(F1) to (6.666-4.7)*600.05 = 1179.698 Hz
          or
        - In POKY: Set HC shift in "st" to -(6.666-4.7) = -1.966 ppm
    - **CAR of 13C Axis:** Written as 39.1096 ppm, but should be 41 ppm. 13C axis is folded by 1/4*SW, relevant peaks are aliased.
      - Total shift of 13C(F2) axis:
        - In Topspin: Set SR(F2) to (58.0333/4 + (41-39.1096))*150.882693 = 2474.283 Hz
          or
        - In POKY: Set 13C shift in "st" to -(58.0333/4 + (41-39.1096)) = -16.398 ppm

## Processing of AIffinity_2024/12 (Pulseprogram: hsqcnoesyhsqccngp4d)

### Axis Order: HN-15N-HC-13C

1. **Set Main Processing Parameters (`edp`):**
    - **Reference:** Set SI to the next power of 2 of TD
      - SI: 1024 256 512 256
    - **Phase:** Opposite sign of NMRPipe/SSA
      - PHC0: 150  0  0  0
      - PHC1: 0  0  0  0 
      - PH_mod: pk pk pk pk
    - **Baseline:** Remove solvent
      - BC_mod: qfil no no no
      - Adjust BCFW accordingly
    - **Fourier:** Set ROI in direct dimension, cca 10-6 ppm
      - STSR: 55
      - STSI: 350
      - FCOR: 0.5 0.5 0.5 0.5
    - **NUS:**
      - Mdd_mod: cs
      - MddF180: false false false
      - MddPHASE: 0 0 0
      - When running the processing it automatically sets:
        - MDD_CsAlg: IST 
        - MDD_CsVE: true

2. **Process 4D Spectrum:**
    ```sh
    ftnd 0
    ```

3. **Optional Baseline Correction in F4:**
    ```sh
    absnd 4
    ```

4. **Correct Shift of HC(F2) Axis (The Axis is Folded by 1/4*SW):**
    - In Topspin: Set SR(F2) to (11.9037/4)*600.05 = 1785.70 Hz
      or
    - In POKY: Set HC shift in "st" to -(11.9037/4) = -2.976 ppm

Note: This correction is not necessary for newer versions of this pulse program, where CAR for HC axis is hardcoded via CNST20=2.6 ppm.

## Processing of AIffinity_950/72 (Pulseprogram: sfhmqc_noe_sfhmqc_4Dhcnh.fl)

### Axis Order: HN-15N-13C-HC

1. **Set Main Processing Parameters (`edp`):**
    - **Reference:** Set SI to the next power of 2 of TD
      - SI: 1024 128 256 256
    - **Phase:** See the comments in the pulseprogram
      - PHC0: -68  90  90 -45
      - PHC1:  0 -180 -180  0 
      - PH_mod: pk pk pk pk
    - **Baseline:** Remove solvent (not necessary here?)
      - BC_mod: no no no no
      - Adjust BCFW accordingly
    - **Fourier:** Set ROI in direct dimension, cca 10.6-6 ppm
      - STSR: 0
      - STSI: 400
      - FCOR: 0.5 1.0 1.0 0.5
    - **NUS:**
      - Mdd_mod: cs
      - MddF180: true true false
      - MddPHASE: 90 90 -45
      - When running the processing it automatically sets:
        - MDD_CsAlg: IST 
        - MDD_CsVE: true

2. **Process 4D Spectrum:**
    ```sh
    ftnd 0
    ```

3. **Correct Shift of HC(F1) Axis:**
    - In Topspin: Set SR(F1) to (O1P-CNST16)*BF1 = (4.7-2.75)*950.37 = 1853.22 Hz
      or
    - In POKY: Set HC shift in "st" to -(O1P-CNST16) = -(4.7-2.75) = -1.95 ppm

## Visual Comparison with 2D HSQC in Topspin

1. **Create Both 2D Positive and Negative (!) Projections 34 (HN-N) and 12 (or 21) (HC-C):**
    ```sh
    projplp 34 all all 34
    projplp 21 all all 21
    projpln 34 all all 340
    projpln 21 all all 210
    ```

2. **Note on F4:PHC0, PHC1 Values:**
    - Often, the F4:PHC0,PHC1 values are not correct and some peaks are anti-phase. See 4D Phase correction for how to proceed.
    - If the positive projections are completely empty, and all peaks are anti-phase, add 180 to PHC0 and issue `pknd 4`. This will change the phase in the F4 dimension only, but will be slow (no parallelization).
    - Overlay with appropriate HSQC using the Topspin command `.md`.
    - Resulting screenshots are HN-N.png and HC-C.png in individual directories.

## Conversion to POKY

### Convert Topspin 21 and 34 Projections to UCSF and Correct the 13C Width

1. **Convert to UCSF:**
    ```sh
    bruk2ucsf 2rr HC-C_projection_Topspin.ucsf
    ```

2. **Find the 13C Dimension Limits:**
    - Run `ucsfdata HC-C_projection_Topspin.ucsf` to find the limits, e.g.,
    ```
    axis                          w1          w2
    nucleus                      13C          HC
    matrix size                  256         512
    block size                   128         256
    upfield ppm              -51.673      -1.293
    downfield ppm             52.562      10.693
    spectrum width Hz       8441.423    9578.544
    transmitter MHz           80.985     799.134
    ```

3. **Open the 21 Projection in Topspin and Issue `pp2d`:**
    - Example original 13C dimension limits: 65.0265 and 12.9703 ppm.
    - Estimate the scaling factor: `(65.0265 - 12.9703) ÷ (52.562 + 51.673) = 0.503707933`.

4. **Load HC-C Projection to POKY and Type `Pn`:**
    - File -> Poky scripts -> Find Additional Modules from POKY GitHub Repository -> `scale_spectra_width_script.py` and follow the prompt.

### Create 2D Projections with POKY Tools

1. **Convert Resulting 4D Spectrum to UCSF:**
    ```sh
    cd AIffinity/101
    bruk2ucsf pdata/1/4rrrr topspin.ucsf
    ```

2. **Create 2D Projections HN-N and HC-C:**
    ```sh
    ucsfdata -p1 -r -o projection-2-3-4.ucsf topspin.ucsf
    ucsfdata -p1 -r -o projection-3-4.ucsf projection-2-3-4.ucsf
    ucsfdata -p4 -r -o projection-1-2-3.ucsf spectrum.ucsf
    ucsfdata -p3 -r -o projection-1-2.ucsf projection-1-2-3.ucsf
    ```

### Advanced CS Parameters

1. **Faster Processing:**
    - To find the optimal `PHC0`, `PHC1` values, try cutting `TD(F4)` back to 1024 by setting TDeff, and then set `SI(F4)` to 1024. You can also try lowering `SI(F4)` without modifying `TDeff(F4)`.

2. **Zero-Filling:**
    - Changing SI upwards is only additional zero-filling. True resolution is given by the acquisition parameters. Zero-filling cannot add peaks or improve resolution, that's just an illusion. However, in NUS, zero-filling could influence the convergence of reconstruction algorithms to better find "the original spectrum". That's why MddNMR internally uses ZF=2 by default (parameter Mdd_CsZF=2).

3. **BC_mode:**
    - `BC_mode` influences the final spectrum, particularly in the F4 dimension.

4. **Spectrometer Frequency and Reference Values:**
    - Wrong spectrometer frequency `SF` values, OFFSET values, and spectrum reference frequencies (SR) should just shift and/or compress the axes, not the spectrum itself.

5. **Spectral Resolution:**
    - `HZpPT` is to a small extent an indicator of the quality of the final processed spectrum. True resolution is given by acquisition parameters.

6. **SPECTYP Parameter:**
    - The `SPECTYP` parameter value probably does not affect the processed spectrum.

## Authors

- Petr Padrta, 14.6.2024
- Thomas Evangelidis
