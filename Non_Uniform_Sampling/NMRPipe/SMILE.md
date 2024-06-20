# SMILE reconstruction 

## General remarks

`NMRPipe` uses a single CPU core only. FT (and other linear transforations) do not consume memory. 

Reconstruction takes ... and consumes ... RAM. 

 

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

### SMILE 
Command reference: `nusPipe -fn SMILE -help` - see the output in [SMILE_ref.md](./nusPipe_SMILE_ref)

**Reconstruction and processing script**

Note how it writes out the data after each FT - this couls be optimized?

    set xP0 = -90
    nmrPrintf "Manual phase xP0: %.1f\n\n" $xP0


    xyz2pipe -in fid/test%04d.fid -x -verb \
    | nmrPipe -fn SOL \
    | nmrPipe -fn SP -off 0.5 -end 0.95 -pow 2 -elb 0.0 -glb 0.0 -c 0.5 \
    | nmrPipe -fn ZF -zf 1 -auto \
    | nmrPipe -fn FT \
    | nmrPipe -fn PS -p0 0.0 -p1 0.0 -di \
    | nmrPipe -fn EXT -x1 3% -xn 47% -sw \
    | pipe2xyz -out tmp/test%05d.ft1 -a -ov

    xyz2pipe -in tmp/test%05d.ft1 -x \
    | nusPipe -fn SMILE -nDim 4 -maxIter 10 -report 1 -sample nuslist \
                        -xApsod SP -xQ1 0.50 -xQ2 0.95 -xQ3 1 -xELB 0.0 -xGLB 0.0 \
                        -yApod SP -yQ1 0.50 -yQ2 0.95 -yQ3 1 -yELB 0.0 -yGLB 0.0 \
                        -zApod SP -zQ1 0.50 -zQ2 0.95 -zQ3 1 -zELB 0.0 -zGLB 0.0 \
                        -xT 160 -xP0 0.0 -xP1 0.0 \
                        -yT 160 -yP0 90.0 -yP1 180.0 \
                        -zT 400 -zP0 0.0 -zP1 0.0 \
    | pipe2xyz -out ft1/test%05d.ft1 -x -ov

    xyz2pipe -in ft1/test%05d.ft1 -x -verb \
    | nmrPipe -fn ZF -zf 1 -auto \
    | nmrPipe -fn FT \
    | nmrPipe -fn PS -p0 0.0 -p1 0.0 -di \
    | nmrPipe -fn TP \
    | nmrPipe -fn ZTP \
    | pipe2xyz -out ft2/test%05d.ft2 -a -ov

    xyz2pipe -in ft2/test%05d.ft2 -z -verb \
    | nmrPipe -fn POLY -auto \
    | nmrPipe -fn ZTP \
    | nmrPipe -fn SP -off 0.50 -end 0.95 -pow 1 -elb 0.0 -glb 0.0 -c 0.5 \
    | nmrPipe -fn ZF -zf 1 -auto \
    | nmrPipe -fn FT \
    | nmrPipe -fn PS -p0 0.0 -p1 0.0 -di \
    | nmrPipe -fn ZTP \
    | pipe2xyz -out ft3/test%05d.ft3 -x -ov

    xyz2pipe -in ft3/test%05d.ft3 -a -verb \
    | nmrPipe -fn SP -off 0.50 -end 0.95 -pow 1 -elb 0.0 -glb 0.0 -c 0.5 \
    | nmrPipe -fn ZF -zf 1 -auto \
    | nmrPipe -fn FT \
    | nmrPipe -fn PS -p0 0.0 -p1 0.0 -di \
    | pipe2xyz -out smile/test%04d.ft4 -a -ov

    echo "FT done."
    echo "Making projections"

    proj4D.tcl -in smile/test%03d.ft4 -sum -outDir ftproj_smile

    echo "Projection done."

**WARNING** I have a problem with memory consumption - is it leaking?!

Colsole output (execution aborted): 
    
    ekaterina@atlas:/home2/ekaterina/NUSdata/Ubiquitin_4D_2022_07/101$ time ./smile_ft4d.com 
    Manual phase xP0: -90.0


    SMILE. Version 2.1 Rev 2019.337.11.19 64-bit
    SMILE. Initializing SMILE Workspace.
    SMILE Error: insufficient memory left.
    SMILE Error initializing SMILE structure.
    NMRPipe Error in function initialization.
    NMRPipe Aborting with null header.
    Pipe2XYZ ETEST error 2.
    Pipe2XYZ Error setting file parameters.
    Pipe2XYZ Status: 2
    NMRPipe Error Status: 1
    NMRPipe Function SMILE
    DATAIO SYSOPEN Error 2:
    File: ft1/test00001.ft1 Access: Read
    SYSOPEN Message: No such file or directory
    XYZ2Pipe Error getting file list;
    Check for valid input name or template.
    Check that input data exists.
    XYZ2Pipe Aborting with null header.
    XYZ2Pipe Status: 1
    NMRPipe Error while reading header.
    NMRPipe Aborting with null header.
    NMRPipe Error Status: 2
    NMRPipe Function ZF
    NMRPipe Error while reading header.
    NMRPipe Aborting with null header.
    NMRPipe Error while reading header.
    NMRPipe Aborting with null header.
    NMRPipe Error Status: 2
    NMRPipe Function FT
    NMRPipe Error Status: 2
    NMRPipe Function PS
    NMRPipe Error while reading header.
    NMRPipe Aborting with null header.
    NMRPipe Error Status: 2
    NMRPipe Error while reading header.
    NMRPipe Function TP YTP XY2YX
    NMRPipe Aborting with null header.
    NMRPipe Error Status: 2
    NMRPipe Function ZTP XYZ2ZYX
    Pipe2XYZ ETEST error 2.
    Pipe2XYZ Error setting file parameters.
    Pipe2XYZ Status: 2
    DATAIO SYSOPEN Error 2:
    File: ft2/test00001.ft2 Access: Read
    SYSOPEN Message: No such file or directory
    XYZ2Pipe Error getting file list;
    Check for valid input name or template.
    Check that input data exists.
    XYZ2Pipe Aborting with null header.
    XYZ2Pipe Status: 1
    NMRPipe Error while reading header.
    NMRPipe Aborting with null header.
    NMRPipe Error Status: 2
    NMRPipe Function POLY
    NMRPipe Error while reading header.
    NMRPipe Aborting with null header.
    NMRPipe Error Status: 2
    NMRPipe Function ZTP XYZ2ZYX
    NMRPipe Error while reading header.
    NMRPipe Aborting with null header.
    NMRPipe Error Status: 2
    NMRPipe Function SP SINE
    NMRPipe Error while reading header.
    NMRPipe Aborting with null header.
    NMRPipe Error Status: 2
    NMRPipe Function ZF
    NMRPipe Error while reading header.
    NMRPipe Aborting with null header.
    NMRPipe Error Status: 2
    NMRPipe Function FT
    NMRPipe Error while reading header.
    NMRPipe Aborting with null header.
    NMRPipe Error Status: 2
    NMRPipe Function PS
    NMRPipe Error while reading header.
    NMRPipe Aborting with null header.
    NMRPipe Error Status: 2
    NMRPipe Function ZTP XYZ2ZYX
    Pipe2XYZ ETEST error 2.
    Pipe2XYZ Error setting file parameters.
    Pipe2XYZ Status: 2
    XYZ2Pipe Partition: Plane 1 to 256 of 256
    ^C Plane:  32 of 256 Z:   1 of 256


    real	3m37,566s
    user	0m11,319s
    sys	2m21,240s
    ekaterina@atlas:/home2/ekaterina/NUSdata/Ubiquitin_4D_2022_07/101$ 
    
    
### IST

Command: 

    ist4D.com –istMaxRes Auto \
    -in fid/test%04d.fid -mask mask/test%04d.fid -out ist/test%04d.ft3 \
    -xP0 -90 -xP1 0 -zP0 -90 -zP1 180 -xEXTX1 10.4ppm -xEXTXN 5.4ppm \
    -zFTARG alt



