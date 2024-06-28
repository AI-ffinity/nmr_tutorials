# TopSpin Commands for Spectra Processing

## Fourier Transform and Baseline Correction
1. **`ft`** - Performs a one-dimensional Fourier Transform on the data.
2. **`fp`** - Alias for performing a Fourier Transform.
3. **`ef`** - Alias for performing an exponential Fourier Transform.
4. **`efp`** - Performs an exponential Fourier Transform followed by phase correction.
5. **`edmac qfp`** - Create a new macro named `qfp` that applies a quadrature sine bell window function (`qsin`), 
performs a Fourier Transform, and then phase correction (`fp`).
6. **`xfb`** - Executes a Fourier Transform on both dimensions of a 2D dataset. Variants include `xfb n`, `xf2`, and `xf1` to focus on specific dimensions or to discard imaginary data.
7. **`ft3d n`** - Process 3D data including Fourier Transform, without creating an imaginary file (only 3rrr file in pdata folder).
8. **`ftnd 0`** - Execute NUS reconstruction with Fourier transformation.
9. **`ftnd 0 nusft`** - Execute Fourier transformation without NUS reconstruction. Sorts FID’s, leaving blanks where no data was collected (xf2, xfb, ftnd)
9. **`ftnd 0 nd2d`** - Leaves FID’s in the acquired order (xf2 only).
10. **`abs`** - Performs baseline correction. The parameters `absf1` & `absf2` specify the range in ppm for the correction.
11. **`abs1`** - Baseline correction specifically for the F1 dimension of a 2D spectrum.
12. **`abs2`** - Baseline correction specifically for the F2 dimension of a 2D spectrum.
13. **`tabs3`, `tabs2`, `tabs1`** - Perform baseline correction in the F3, F2, and F1 axes, respectively.

## Special Options
1. **`nusft`** – sort FID’s, leaving blanks where no data was collected (`xf2`, `xfb`, `ftnd`). Quick processing with tons of artifacts!
2. **`nd2d`** – leave FID’s in the acquired order (xf2 only)

## Phase Correction
1. **`.ph`** - Enters interactive phase correction mode.
2. **`pk`** - Applies previously set phase corrections (`phc0` and `phc1`) to the spectrum.
3. **`apk`** - Executes automated phase correction, suitable for simple spectra like methanol.
4. **`apk2d`** - Automatically performs phase correction on 2D spectra, streamlining the adjustment of both zero-order 
and first-order phase settings to optimize spectral clarity and symmetry.
4. **`pknd`** - Performs a phase correction of data of dimension ≥3D, applying the values of PHC0 and PHC1 only on one dimension. 

## Window Functions
1. **`em`** - Applies exponential multiplication to the data, used for line broadening.
2. **`sin`** - Multiplies the data by a sine window, phase-shifted by π/ssb.
3. **`qsin`** - Multiplies the data by a quadrature sine window, similar to `sin` but typically with different phase adjustments.

## Data Extraction and Manipulation
1. **`slice`** - Extract a specific plane from multidimensional data.
2. **`xht1`** - Command to reconstruct the imaginary dimension in F1.
3. **`xht2`** - Command to reconstruct the imaginary dimension in F2.
4. **`projplp 34 all all 34`** and **`projplp 21 all all 21`** - Generates positive projections of the specified dimensions for visualization.
5. **`projpln 34 all all 340`** and **`projpln 21 all all 210`** - Generates the Negative Projection for specified dimensions.
6. **`rser`** - Read row from 2D raw data (a series of FIDs) and store as 1D FID (2D,1D).
7. **`rpl`** - Read plane from data ≥ 3D and store as 2D data.

## Miscellaneous Processing
1. **`eda`** - Displays parameters for the indirect dimensions of 2D, 3D spectra such as sweep width, time domain size, and offsets.
2. **`tf3 n; tf2 n; tf1 n`** - Fourier Transforms the specified dimension in a 3D dataset. The 'n' indicates that no imaginary data is generated.
3. **`edp`** - Used to access and modify processing parameters in the "ProcPars" window.
4. **`.gr`** - Refresh the graphical display.
5. **`levcalc`** automatically calculates and sets optimal contour levels based on the signal intensity and 
 noise characteristics to ensure that the peaks are visible and informative without being overwhelmed by noise. 
Use `dis2d` or `dis3d` (depending on the dimensionality of your data) to display the spectrum with the 
automatically calculated contour levels.

### Spectrometer Control and Spectra Recording Commands:
1. **`sx` and `ej`** - Commands used to eject the current sample from the spectrometer.
2. **`sx <position>`** - Starts the carousel and inserts the sample at the specified position into the spectrometer.
3. **`new`** - Creates a new experiment based on an active one.
4. **`ww`** - Executes automatic matching and tuning of the system.
5. **`lock`** - Locks the magnetic field, usually selecting "H2O + D2O" from the dropdown list.
6. **`topshim gui`** - Initiates automatic 1D shimming to optimize the magnetic field homogeneity.
7. **`p1` followed by `1 P1 1`** - Configures pulse program settings.
8. **`zg`** - Starts the experiment, initiating the acquisition of the NMR spectrum.
9. **`atma`** - Automatically tunes and matches the channels, typically used for 15N and 1H channels.
10. **`pulsecal`** - Calculates the length of the 90° hydrogen pulse P1 for 10W.
11. **`getprosol 1H P1 xW`** - Sets pulse and power, inserting previously determined value P1 with the appropriate power value.
12. **`stop`** - Stops the measurement process.
13. **`pulse <x>W`** - Recalculates the pulse for `<x> Watt`.

