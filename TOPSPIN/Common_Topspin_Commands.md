# TopSpin Commands for Spectra Processing

## Fourier Transform and Baseline Correction
* **`ft`** - Performs a one-dimensional Fourier Transform on the data.
* **`fp`** - Alias for performing a Fourier Transform.
* **`ef`** - Alias for performing an exponential Fourier Transform.
* **`efp`** - Performs an exponential Fourier Transform followed by phase correction.
* **`edmac qfp`** - Create a new macro named `qfp` that applies a quadrature sine bell window function (`qsin`), performs a Fourier Transform, and then phase correction (`fp`).
* **`xfb`** - Executes a Fourier Transform on both dimensions of a 2D dataset. Variants include `xfb n`, `xf2`, and `xf1` to focus on specific dimensions or to discard imaginary data.
* **`ft3d n`** - Process 3D data including Fourier Transform, without creating an imaginary file (only 3rrr file in pdata folder).
* **`ftnd 0`** - Execute NUS reconstruction with Fourier transformation.
* **`ftnd 0 nusft`** - Execute Fourier transformation without NUS reconstruction. Sorts FID’s, leaving blanks where no data was collected (xf2, xfb, ftnd)
* **`ftnd 0 nd2d`** - Leaves FID’s in the acquired order (xf2 only).
* **`abs`** - Performs baseline correction. The parameters `absf1` & `absf2` specify the range in ppm for the correction.
* **`abs1`** - Baseline correction specifically for the F1 dimension of a 2D spectrum.
* **`abs2`** - Baseline correction specifically for the F2 dimension of a 2D spectrum.
* **`tabs3`, `tabs2`, `tabs1`** - Perform baseline correction in the F3, F2, and F1 axes, respectively.

## Phase Correction
* **`.ph`** - Enters interactive phase correction mode.
* **`pk`** - Applies previously set phase corrections (`phc0` and `phc1`) to the spectrum.
* **`apk`** - Executes automated phase correction, suitable for simple spectra like methanol.
* **`apk2d`** - Automatically performs phase correction on 2D spectra, streamlining the adjustment of both zero-order 
and first-order phase settings to optimize spectral clarity and symmetry.
* **`pknd`** - Performs a phase correction of data of dimension ≥3D, applying the values of PHC0 and PHC1 only on one dimension. 

## Window Functions
* **`em`** - Applies exponential multiplication to the data, used for line broadening.
* **`sin`** - Multiplies the data by a sine window, phase-shifted by π/ssb.
* **`qsin`** - Multiplies the data by a quadrature sine window, similar to `sin` but typically with different phase adjustments.

## Data Extraction and Manipulation
* **`slice`** - Extract a specific plane from multidimensional data.
* **`xht1`** - Command to reconstruct the imaginary dimension in F1.
* **`xht2`** - Command to reconstruct the imaginary dimension in F2.
* **`projplp 34 all all 34`** and **`projplp 21 all all 21`** - Generates positive projections of the specified dimensions for visualization.
* **`projpln 34 all all 340`** and **`projpln 21 all all 210`** - Generates the Negative Projection for specified dimensions.
* **`rser`** - Read row from 2D raw data (a series of FIDs) and store as 1D FID (2D,1D).
* **`rpl`** - Read plane from data ≥ 3D and store as 2D data.
* **`totxt`** - save currently displayed region as a text file (1D and 2D)

## Miscellaneous Processing
* **`eda`** - Displays parameters for the indirect dimensions of 2D, 3D spectra such as sweep width, time domain size, and offsets.
* **`tf3 n; tf2 n; tf1 n`** - Fourier Transforms the specified dimension in a 3D dataset. The 'n' indicates that no imaginary data is generated.
* **`edp`** - Used to access and modify processing parameters in the "ProcPars" window.

### Display adjustments
* **`dlp`** - Save the currently displayed region as default for this processed data
* **`.lv` or `edlev`** - Manually enter contour levels mode to adjust "level increment" and "number of levels".
* **`.gr`** - Refresh the graphical display.
* **`levcalc`** automatically calculates and sets optimal contour levels based on the signal intensity and 
 noise characteristics to ensure that the peaks are visible and informative without being overwhelmed by noise. 
Use `dis2d` or `dis3d` (depending on the dimensionality of your data) to display the spectrum with the 
automatically calculated contour levels.


### Spectrometer Control and Spectra Recording Commands:
* **`sx` and `ej`** - Commands used to eject the current sample from the spectrometer.
* **`sx <position>`** - Starts the carousel and inserts the sample at the specified position into the spectrometer.
* **`new`** - Creates a new experiment based on an active one.
* **`ww`** - Executes automatic matching and tuning of the system.
* **`lock`** - Locks the magnetic field, usually selecting "H2O + D2O" from the dropdown list.
* **`topshim gui`** - Initiates automatic 1D shimming to optimize the magnetic field homogeneity.
* **`p1` followed by `1 P1 1`** - Configures pulse program settings.
* **`zg`** - Starts the experiment, initiating the acquisition of the NMR spectrum.
* **`atma`** - Automatically tunes and matches the channels, typically used for 15N and 1H channels.
* **`pulsecal`** - Calculates the length of the 90° hydrogen pulse P1 for 10W.
* **`getprosol 1H P1 xW`** - Sets pulse and power, inserting previously determined value P1 with the appropriate power value.
* **`stop`** - Stops the measurement process.
* **`pulse <x>W`** - Recalculates the pulse for `<x> Watt`.

