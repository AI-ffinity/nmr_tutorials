`new` to create a new experiment and add the description.
`sx` or `ej` to eject current sample
`sx <position>` to start the carousel with the sample at position <position> to be inserted into the spectrometer.
`atma` to automatically tune and match 15N and 1H channels. Click the arrows to bring the well to the center at the 
vertical line.
`lock` select "H2O + D2O" from the list. it will measure a simple spectrum according to which it will adjust the 
frequency
`topshim gui` for automatic 1D shimming.
`p1`
`1 P1 1`
`zg` starts the experiment.
`new` to start new experiment
`p1`
`1 P1 1`
`zg` starts the experiment.
`stop`
`1 NS 1`
`d1`
`zg`
`efp` em+ft+pk; `em` exponentially multiply -> 1b is broadening, `ft` fourier transform 1D, `pk` apply phase 
correction -> apply phc0 and phc1 to spectrum
`1 RG 64` sets the values of ... gate to 64.

`pulsecal` calculates length of 90° hydrogen pulse p1 for 10W (as set in active experiment). We calculate this for each sample although the differences are small
depends more on the concentration of salt and temperature than the protein and ligand.
`pulse <x>W` re-calculates the pulse for <x> Watt, in our case 10.
open 1D experiment in folder praktikum
[new] l0 <Creates new experiment based on an active one
[getprosol 1H P(x)W] insert previously found value P1 with appropriate power value
[qfp] process the spectrum (macro for qsin, ft, pk)
open 2D experiment in folder praktikum
[new] creates new experiment based on an active one
[getprosol 1H P1 xW] insert previously found value P1 with appropriate power value
[zg] starts the experiment
[xfb] Fourier transform in both dimensions
[.ph] phase correction
[.md] multidisplay mode
`bas` baseline correction. Red is the baseline, blue is the spectrum, which is simplified. This is not related to field 
homogenity. We do this because automatic correction is imperfect.
`qfp` q ..., `ft` fourier transform 1D, `pk` apply phase correction.

## General Remarks:
* Water occurs at 4.7 ppm.
