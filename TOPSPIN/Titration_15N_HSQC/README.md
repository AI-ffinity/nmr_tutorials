`new` to create a new experiment and add the description.
`sx 1` to start the carousel with the sample to be inserted into the spectrometer.
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
