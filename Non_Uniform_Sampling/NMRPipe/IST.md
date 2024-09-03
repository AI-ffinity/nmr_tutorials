# IST reconstruction as implemented in NMR Pipe 

## General remarks

`NMRPipe` uses a single CPU core only. FT (and other linear transforations) do not consume memory. 

Reconstruction takes *2 h 40 m X 2 (at least)* and consumes almost no RAM. 

 

# Example: Ubiquitin (AIffinity pulse sequence)

With the default parameters

## Step 1: convert the file



    #!/bin/csh

    time

    nusExpand.tcl -mode bruker -sampleCount 3500 -avg -off 0 \
     -in ./ser -out ./ser_full -sample ./nuslist

    bruk2pipe -verb -in ./ser_full \
      -bad 0.0 -ext -aswap -AMX -decim 2800 -dspfvs 20 -grpdly 68  \
      -xN              1024  -yN               160  -zN               160  -aN               400  \
      -xT               512  -yT                80  -zT                80  -aT               200  \
      -xMODE            DQD  -yMODE        Complex  -zMODE        Complex  -aMODE        Complex  \
      -xSW         7142.857  -ySW         1411.433  -zSW         8756.567  -aSW         7142.857  \
      -xOBS         600.053  -yOBS          60.810  -zOBS         150.889  -aOBS         600.054  \
      -xCAR           4.771  -yCAR         120.169  -zCAR          41.847  -aCAR           6.737  \
      -xLAB              HN  -yLAB             15N  -zLAB             13C  -aLAB              1H  \
      -ndim               4  -aq2D         Complex                         \
    | nmrPipe -fn MULT -c 2.50000e+02 \
    | pipe2xyz -x -out ./fid/test%04d.fid -ov

    ### This mask creation may be not necessary - check that!
    xyz2pipe -in ./fid/test%04d.fid -noWr \
    | nusExpand.tcl -mask -noexpand -mode pipe -sampleCount 3500 -avg -off 0 \
      -in stdin -out ./mask/test%04d.fid -sample ./nuslist

    echo "Done."

    time

## Step 2: Check the settings without reconstruction

> @TODO: how to know the region for sure in NMRPipe?!
> @TODO: how to process 1 FID / 1 plane / 1 cube to test something?

1. Check the segment of the direct dimension you want to process - this is crusial for the processing time! 
	> Thus, only the FT of the entire spectrum takes longer than an hour while the segment of 20% of the direct dimension takees only 12 minutes!
2. This code auto-phases; but just in case, call the auto-phase command separately and compare with the phase correction coefficients for our 2D planes:


	nmrPrintf "Auto-Phase ...\n\n"
	set xP0 = (`basicAutoPhase.com -in fid/test%04d.fid -apxP1 0.0 -apyP0 0.0 -apyP1 0.0 -apyFTARG None -apOrd 0`)
	nmrPrintf "Auto-Phase xP0: %.1f\n\n" $xP0


### Doing actual fourier transform in the indirect dimensions

> ***Note 1***: the lines calling nmrPipe function `EXT`: they are responsible for cutting the dimensions.
> 
> Usage: see [nmrpipe reference page](https://www.nmrscience.com/ref/nmrpipe/)
> 
> Here, we define the region in percentage: 1-50% for the direct dimension going through 15N.
> 
> **Note 2**: To account for the 1-point delay in the ¹³C dimension, we include the line `| nmrPipe -fn CS -ls 20 -sw \` - where 20 is the number of points (read: 3D cubes) by which the axis needs to e shifted to the left.


	#!/bin/csh

	nmrPrintf "Auto-Phase ...\n\n"

	set xP0 = (`basicAutoPhase.com -in fid/test%04d.fid -apxP1 0.0 -apyP0 0.0 -apyP1 0.0 -apyFTARG None -apOrd 0`)

	nmrPrintf "Auto-Phase xP0: %.1f\n\n" $xP0

	xyz2pipe -in fid/test%04d.fid -x -verb \
	| nmrPipe -fn SOL \
	| nmrPipe -fn SP -off 0.5 -end 0.95 -pow 2 -elb 0.0 -glb 0.0 -c 0.5 \
	| nmrPipe -fn ZF -zf 1 -auto \
	| nmrPipe -fn FT \
	| nmrPipe -fn PS -p0 $xP0 -p1 0.0 -di \
	| nmrPipe -fn EXT -x1 1% -xn 50% -sw \
	| nmrPipe -fn TP \
	| nmrPipe -fn SP -off 0.50 -end 0.95 -pow 1 -elb 0.0 -glb 0.0 -c 0.5 \
	| nmrPipe -fn ZF -zf 1 -auto \
	| nmrPipe -fn FT \
	| nmrPipe -fn PS -p0 0.0 -p1 0.0 -di \
	| nmrPipe -fn TP \
	| nmrPipe -fn POLY -auto \
	| nmrPipe -fn ZTP \
	| nmrPipe -fn SP -off 0.50 -end 0.95 -pow 1 -elb 0.0 -glb 0.0 -c 0.5 \
	| nmrPipe -fn ZF -zf 1 -auto \
	| nmrPipe -fn FT \
	| nmrPipe  -fn CS -ls 20 -sw \
	| nmrPipe -fn PS -p0 0.0 -p1 0.0 -di \
	| nmrPipe -fn ZTP \
	| pipe2xyz -out ft3/test%05d.ft3 -x -ov

	xyz2pipe -in ft3/test%05d.ft3 -a -verb \
	| nmrPipe -fn SP -off 0.50 -end 0.95 -pow 1 -elb 0.0 -glb 0.0 -c 0.5 \
	| nmrPipe -fn ZF -zf 1 -auto \
	| nmrPipe -fn FT \
	| nmrPipe -fn PS -p0 0.0 -p1 0.0 -di \
	| pipe2xyz -out ft/test%03d.ft4 -a -ov

	echo "FT done."
	echo "Making projections"

	proj4D.tcl -in ft/test%03d.ft4 -axis -outDir ftproj

	echo "Projection done."

> FT of the **full** Ubq 4D takes approx. 1 hour
> FT + projections of the spectrum with 54% in the *direct* and 30-95% in the *indirect* ¹H dimension took ~25 minutes:
    
    real	50m18,008s
    user	21m17,213s
    sys	    29m27,771s
    
> ***Note 2***: do **not** use `basicFT4.com`! It generates an `nmr.com` with a lot of default actions that one might not like (for example, removing the `ft3` directory too early for troubleshooting). It sets default window functions to sine sqared in the direct and normal sine in the indirect dimensions. 
> You may specify the parameters you want as arguments - but then you do not need the function that creates this script! A separate explicit script is more readable!


### Clean-up:


	rm -rf fid mask ft3 
	
	
Making projections of the ENTIRE spectrum (full range of ppm in the direct dimension) takes 14 minutes on Atlas.


`615.093u 69.775s 13:47.19 82.7%	0+0k 3703120+9976io 13pf+0w`

> Spectrum of Ubiquitin can be somewhat legible even without NUS reconstruction, so with FT only! But most of the signals will be very weak. Projections are clear, but it's difficult to discern 4D peaks. 

## Step 3: NUS
    
### IST

Command: 

    ist4D.com –istMaxRes Auto \
    -in fid/test%04d.fid -mask mask/test%04d.fid -out ist/test%04d.ft3 \
    -xP0 -90 -xP1 0 -zP0 -90 -zP1 180 -xEXTX1 10.4ppm -xEXTXN 5.4ppm \
    -zFTARG alt

Unlike SMILE, the IST function does not generate any script. The prelimanary processing (FFT of the direcc dimension, 
reformatting, restructuring) takes *much* longer than in case of SMILE - more than an hour as opposed to a dozen minutes! 

See all availble options in the [command reference](./nusPipe_IST_4D_ref.md)

> **Warning**: Durnig processing, the intermediate file `ist_nuszf.fid` blows up *immensely* and can weight MORE THAN 350 GB - for 40 GB expanded FID!


