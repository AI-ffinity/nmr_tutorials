# NUS reconstruction of PaaR2 Protein

## Region of Interest (ROI)
HN (F4) : 6.3-10 ppm; 
HC (F1): -0.7 - 10.5 ppm;
keep F2 and F3 at full-length as they are saturated with peaks.

```shell
$ preprocSPARSE -nuft
preprocSPARSE.inp not found - creating, switching to interactive mode
experiment info: <4Dnoesy>, <noehcnhwg4d_nove_edited_av>, nmrsu@nmrpc8, Fri Nov 24 15:06:28 CET 2023, TopSpin 3.6.0
number of (NUS) dimensions: (3) 4
Number of INTerleaved components [1]: ? 
 using NINT=1
Pseudo-DIMension number [0]: ? 
 without pseudo-dim (PDIM=0)
NUS/RQD schedule [nuslist ]: ? 
 using NUS schedule in nuslist (3500*3)
 without RQD schedule
NUS density: 0.2734% (3500/1280000)
AQSEQ=0 (1234) => seq=1 2 3 4
changing dimension order to 1 4 3 2
CARrier frequency for dimension 1 (orig. 1, F4, 1H, 1024, DQD) [4.69999874 ppm]: ? 
 using CAR1=4.69999874 ppm
CARrier frequency for dimension 2 (orig. 2, F3, 15N, 28000, Complex) [117.00000000 ppm]: ? 
 using CAR2=117.00000000 ppm
CARrier frequency for dimension 3 (orig. 3, F2, 13C, 1, Complex) [39.00000000 ppm]: ? 
 using CAR3=39.00000000 ppm
CARrier frequency for dimension 4 (orig. 4, F1, 1H, 1, Complex) [4.69999874 ppm]: ? 
 using CAR4=4.69999874 ppm
Apodization POWer for dimension 1 (orig. 1, 1H) [2] ?
 using APOW1=2, sb_sign="-"
Apodization POWer for dimension 2 (orig. 2, 15N) [1] ?
 using APOW2=1, sb_sign=""
Apodization POWer for dimension 3 (orig. 3, 13C) [1] ?
 using APOW3=1, sb_sign=""
Apodization POWer for dimension 4 (orig. 4, 1H) [1] ?
 using APOW4=1, sb_sign=""
amount of Zero-Filling for dimension 1 (orig. 1, 1H) [1 1] ?
 using ZF1=1, ZFflag="-auto", ZFsize=1024
amount of Zero-Filling for dimension 2 (orig. 2, 15N) [1 0] ?
 using ZF2=1, ZFflag="", ZFsize=160
amount of Zero-Filling for dimension 3 (orig. 3, 13C) [1 0] ?
 using ZF3=1, ZFflag="", ZFsize=160
amount of Zero-Filling for dimension 4 (orig. 4, 1H) [1 0] ?
 using ZF4=1, ZFflag="", ZFsize=400
found flipped dim 2 (orig. 4)
found flipped dim 3 (orig. 3)
flags for dimension 2 (orig. 4, 1H) [SWAP=0 FLIP=1] ?
 using SWAP4=0, FLIP4=1 => FTflag4=" -neg"
flags for dimension 3 (orig. 3, 13C) [SWAP=0 FLIP=1] ?
 using SWAP3=0, FLIP3=1 => FTflag3=" -neg"
flags for dimension 4 (orig. 2, 15N) [SWAP=0 FLIP=0] ?
 using SWAP2=0, FLIP2=0 => FTflag2=""
Region Of Interest for dimension 1 (orig. 1, 1H) [10.7 -1.3 ppm]: ? 10.6 6.3
 using ROI1=10.6 6.3 ppm (4.3 ppm)
Region Of Interest for dimension 2 (orig. 2, 15N) [126.5 107.5 ppm]: ? 
 using ROI2=126.5 107.5 ppm (full ppm)
Region Of Interest for dimension 3 (orig. 3, 13C) [65.5 12.5 ppm]: ? 
 using ROI3=65.5 12.5 ppm (full ppm)
Region Of Interest for dimension 4 (orig. 4, 1H) [10.7 -1.3 ppm]: ? 9.4 -0.7
 using ROI4=9.4 -0.7 ppm (10.1 ppm)
P0 for dimension 1 [deg]: ?0
 using P01=0 deg

Bruker DMX --> NMRPipe Conversion.
Input File: Standard Input.
Output File: Standard Output.
2D Sizes: (886 Real+Imag)(2 Real+Imag)
Byte Swap Mode: OFF

Slice 2 of 2


NUFT preprocessing finished
Change to directory nuft/
Run ./proc.sh [nuft]
See the comments in proc.sh, make changes to parameters.txt, if necessary
Remove unnecessary files with ./remove.sh [all]
```

`cd nuft`

* Open `parameters.txt` and change `name 1H` to `name HN` and `name1 1H` to `name1 HC`.
* Set `phases2` to `0.0 180.0` for a 1-point delay in 13C.

* Open `proc.sh` and add `--limits=-0.7:10.5` to reconstructor4d to limit HC axis from -0.7 to 10.5 ppm. Also add `-j 8`
to both cleaner4d and reconstructor4d to use 8 CPU cores (increase it if you want).

`./fid2D.com` (ignore "using existing test.fid, remove it in case of problems" in the `proc.sh`; it always has a problem)

`./proc.sh FT` and review the projections in "roi_6.3_10.6-nuft/"

If they look alright run `./proc.sh NUFT` to conduct the full NUS-reconstruction

* If too few peaks are reconstructed:
    - In `nuft/proc.sh`, go to the line 28 with `cleaner4d` and add `-T 8` (equivalent to `--threshold=8` ). The default value is 10, so this would be a little tweak. Reconstruct again and see if it helps.
    - Another parameter to tweak is `-J 3.5` (`--joint-threshold=3.5`, defaults to 4.0) - this is the region (in some relative units) which is considered peak-free. It may help to detect overlapping peaks.



* Generate additional 2D HC-C projections from 4D spectrum:
   ```bash
   cd roi_6.3_10.6
   ucsfdata -p4 -o projection-1-2-3.ucsf spectrum.ucsf
   ucsfdata -p3 -o projection-1-2.ucsf projection-1-2-3.ucsf
   ```
* In Sparky, read the resulting projections and shift the C or HC axes as previously described.
* Overlay these projections on the HC-C HSQC (data/AIffinity_2024/13 in red/green). The projection from data/AIffinity_2024/12 
   will be in turquoise, with the AIffinity/101 projection in gold. Note that the missing part of AIffinity/101 (gold) 
   got shifted outside the HSQC window but the peaks there can be correctly handled with the peak aliasing feature in Sparky.
   
   
# Referencing
HC: 0.00577
13C: -16.41540
N: 0.01357
HN: -0.01376
