# NUS with hmsIST scripts - not using the implementation built into NMRPipe

The problem with IST in NMRPipe is that it generates a few VERY LARGE files in the process. While those can be deleted after successful reconstruction, it may become a big problem in the long run. 

Another shortcoming: the Pipe API requires not only conversion but also expansion of the NUS raw file, which takes not only disk space but time. 

hmsIST scripts do not generate that much garbare and conversion of the Bruker NUS data to the NMRPipe format takes seconds. With the GNU parallel script it can use all cores, unlike SMILE (?) or MDD on TopSpin. 

Shortcomings: 

* Quite slow, even with heavy parallelzation reconstruction alone takes ~6 hours 
    * 30 iterations, EXT 6-11 ppm (402 FIDs), 95% CPU utilization: **96 min**
* Licensing issues of the [GNU parallell](https://www.gnu.org/software/parallel/) script? 

> Note: hmsIST program still requires files that are processed in the direct dimension and written in the special format. 

# Workflow

Scripts can be taken from [Ekaterina's archive on GitHub](https://github.com/eburakova/hmsIST)
## Directory structure

<pre>-rwxr--r--  1 ekaterina ekaterina   12351 Jun 25 19:18 <font color="#26A269"><b>hmsIST_4D.com</b></font>*
-rwxr--r--  1 ekaterina ekaterina 1340491 Jan 27 13:42 <font color="#26A269"><b>istHMS</b></font>*
-rwxr--r--  1 ekaterina ekaterina  154824 Jan 27 13:42 <font color="#26A269"><b>parallel</b></font>*
-rwxr--r--  1 ekaterina ekaterina   47898 Jan 27 13:42 <font color="#26A269"><b>phf2pipe</b></font>*
-rwxr--r--  1 ekaterina ekaterina  254821 Jan 27 13:42 <font color="#26A269"><b>pipe2ucsf</b></font>*
-rwxr--r--  1 ekaterina ekaterina     466 Jun 25 19:18 <font color="#26A269"><b>runist_cluster</b></font>*
</pre>

## The `hmsIST_4D.com` script

Requires `runist_cluster` script (below).

> Put it into the parent directory of your experiments. Note down the EXPNO of the 4D data.

       
      #!/bin/csh
      
      cd ./101 # Change this the name of your EXPDIR
      
      date
      
      #=========================================================================================
      #
      #                                  CONFIG SECTION
      #
      #=========================================================================================
      
      set filename = ubq_hcnoesyhn4D
      
      #----------------------------------------------------------------------------------------
      #                                SetUp &  Reformatting 
      #----------------------------------------------------------------------------------------
      
      set nus_points = 3500  # This is the length of your NUS schedule
      
      # You can run the `bruker` NMR pipe script and take the parameters from that.
      # You can take the from TopSpin manually and assign to the variables, too. 
      
      # Spectral widths
      set ft4sw = 7142.857
      set ft3sw = 1411.433
      set ft2sw = 8756.567
      set ft1sw = 7142.857 
      
      # Carrier frequencies ("offsets")
      set ft4car = 4.7
      set ft3car = 120.1
      set ft2car = 41.0
      set ft1car = 4.7
      
      # Base frequencies 
      set ft4bf = 600.0528
      set ft3bf = 60.8025
      set ft2bf = 150.882
      set ft1bf = 600.0528
      
      ----------------------------------------------------------------------------------------
      #                                     Regular processing 
      #----------------------------------------------------------------------------------------
      
      # Zero fill
      set zf1 = 1024   # Zero-filling in the dir. dim.
      set zf2 = 128    # Zero-filling in the first indir. dim.
      set zf3 = 128    # Zero-filling in the second indir. dim.
      set zf4 = 128    # Zero-filling in the third indir. dim.
      
      # Phasing
      set f4ph0 = -90    # Direct dimension
      set f4ph1 = 0      # Direct dimension first order
      set f3ph0 = 0
      set f3ph1 = 0
      set f2ph0 = 0
      set f2ph1 = 0
      set f1ph0 = 0
      set f1ph1 = 0
      
      #----------------------------------------------------------------------------------------
      #                                    Navigation 
      #----------------------------------------------------------------------------------------
      
      if     ($1 == "fid")       goto FID       # Initial format conversion
      if     ($1 == "ft1phase")  goto FT1PHASE  # Optional: FT and phase check in the direct dimension
      if     ($1 == "ft1")       goto FT1       # FT in the direct dimension
      if     ($1 == "ist")       goto IST       # IST reconstruction
      if     ($1 == "pipe")      goto PH2PIPE   # Conversion
      
      goto DONE
      
      #----------------------------------------------------------------------------------------
      #                                    Reformatting 
      #----------------------------------------------------------------------------------------
      
      FID:
      
      # We are treating the experiment like a 3D
      
      rm -rf fid_hms
      mkdir fid_hms
      
      echo " Loading bruker FID starts here"
      
      bruk2pipe -verb -in ./ser                                                                        \
      -bad 0.0 -ext -aswap -AMX -decim 960 -dspfvs 20 -grpdly 68                                     \
      -xN              1024  -yN             8      -zN    $nus_points      -aN             0        \
      -xT               512  -yT             8      -zT    $nus_points      -aT             0        \
      -xMODE            DQD  -yMODE       Real      -zMODE        Real      -aMODE       Complex     \
      -xSW           $ft4sw  -ySW         $ft3sw    -zSW        $ft2sw      -aSW         $ft1sw      \
      -xOBS          $ft4bf  -yOBS        $ft3bf    -zOBS       $ft2bf      -aOBS        $ft1bf      \
      -xCAR          $ft4car -yCAR        $ft3car   -zCAR       $ft2car     -aCAR        $ft1car     \
      -xLAB              HN  -yLAB          N      -zLAB             C     -aLAB             Hh      \
      -ndim               3  -aq2D         States                                                    \
      -out ./fid_hms/fid_%04d.fid -verb -ov 
      
      echo " Loading bruker FID ends here"
      goto FT1PHASE
      
      #----------------------------------------------------------------------------------------
      #                   Optional: FT and phase check in the direct dimension
      #----------------------------------------------------------------------------------------
      
      FT1PHASE: 
      
      # Returns the data NOT suitable for reconstruction.
      
      rm -fr ft1_hms
      mkdir ft1_hms
      echo "check FT1 for phasing starts here"
      
      xyz2pipe -in ./fid/fid_%04d.fid -x                         \
      | nmrPipe  -fn ZF -size $zf1                               \
      #| nmrPipe  -fn EM -lb 20 -c 0.5                           \
      #| nmrPipe  -fn GM -g1 -20.0 -g3 0.01                      \
      | nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 2 -c 0.5         \
      | nmrPipe  -fn FT -auto -verb                              \
      | nmrPipe  -fn PS -p0 $f4ph0 -p1 $f4ph1 -di                \
      | nmrPipe  -fn POLY -auto -ord 4 -x1 100ppm -xn -100ppm    \
      | nmrPipe  -fn EXT -x1 11ppm -xn 6ppm -sw -round 2         \
      | pipe2xyz -ov -out ./ft1/fid_%04d.ft -x
      
      echo "check FT1 for phasing ends here"
      goto DONE
      
      #----------------------------------------------------------------------------------------
      #                               FT in the direct dimension 
      #----------------------------------------------------------------------------------------
      
      FT1: 
      
      # This file is for preparing the 3D files for NUS construction
      # format of the output file should be "phase increments time increments direct dimension". 
      # This is achieved by the following file. 
      # Till now we are treating the experiment file as 3D
      
      rm -fr ft1_ist
      mkdir ft1_ist
      
      xyz2pipe -in fid/fid_%04d.fid -x                        \
      | nmrPipe  -fn ZF -size $zf1                            \
      | nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 2 -c 0.5      \
      | nmrPipe  -fn FT   -auto -verb                         \
      | nmrPipe  -fn PS -p0 $f4ph0 -p1 $f4ph1 -di             \
      | nmrPipe  -fn EXT -x1 11ppm -xn 6ppm -sw -round 2      \
      | nmrPipe  -fn ZTP -verb                                \
      | pipe2xyz -ov -out ft1/fid_%04d.ft -y
      
      #goto ISTEST
      goto DONE
      
      #----------------------------------------------------------------------------------------
      #                                 The IST reconstruction 
      #----------------------------------------------------------------------------------------
      
      IST:
      
      # Calls GNU `parallel` script which distributes the jobs
      
      rm -fr ft1_ist
      mkdir ft1_ist
      
      echo 'The IST reconstruction starts here'
      
      pwd
      
      ./../parallel -j 95% './../runist_cluster {} > /dev/null; echo {}' ::: ./ft1/fid*.ft
      
      #goto DONE
      
      PH2PIPE: 
      
      xyz2pipe -in ft1/fid_%04d.phf | ./../phf2pipe -user 1 -xproj xa.ft1 -yproj ya.ft1 -zproj za.ft1 \
      | pipe2xyz -out ft1_pipe/fid_%04d.ft -ov 
      
      echo "IST reconstruction completed"
      
      goto DONE
      
      #----------------------------------------------------------------------------------------
      #                            Check phasing in the indirect dimensions 
      #----------------------------------------------------------------------------------------
      
      PROJPHASE:
      
      if ($2 == "first")  goto FIRST
      if ($2 == "second") goto SECOND
      if ($2 == "third")  goto THIRD
      
      FIRST: 
      
      rm -rf xa.ft2
      echo "Projection phasing in the first indirect dimension started "
      
      nmrPipe -in xa.ft1\
      | nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 2 -c 0.5        \
      | nmrPipe  -fn ZF -size 256                               \
      | nmrPipe  -fn FT -alt  -verb                             \
      | nmrPipe  -fn PS -p0 0 -p1 0 -di                         \
      -ov -out xa.ft2
      
      echo "Projection phasing in the first indirect dimension finished " 
      
      #goto DONE
      
      
      SECOND: 
      
      rm -rf ya.ft2
      
      echo "Projection phasing in the second indirect dimension started "
      
      nmrPipe -in ya.ft1\
      | nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 2 -c 0.5        \
      # | nmrPipe  -fn EM -lb 10                                 \ # Change the window function if needed
      | nmrPipe  -fn ZF -size 256                               \
      | nmrPipe  -fn FT -alt  -verb                             \
      | nmrPipe  -fn PS -p0 0 -p1 0 -di                         \
      -ov -out ya.ft2
      
      echo "Projection phasing in the second indirect dimension finished " 
      
      #goto DONE
      
      THIRD: 
      
      rm -rf za.ft2
      
      echo "Projection phasing in the third indirect dimension started "
      
      nmrPipe -in za.ft1\
      | nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 2 -c 0.5       \
      # | nmrPipe  -fn EM -lb 10                                \ # Change the window function if needed
      | nmrPipe  -fn ZF -size 256                              \
      | nmrPipe  -fn FT -alt  -verb                            \
      | nmrPipe  -fn PS -p0 0 -p1 0 -di                        \
      -ov -out za.ft2
      
      echo "Projection phasing in the third indirect dimension finished " 
      
      goto DONE
      
      #----------------------------------------------------------------------------------------
      #                            Full FT of the reconstructed data 
      #----------------------------------------------------------------------------------------
      
      FTALL:
      
      date
      
      rm -fr ft
      mkdir ft
      pwd
      echo "FT in all indirect dimensions starts here"
      
      xyz2pipe -in ./ft1_pipe/fid_%03d%03d.ft -x                \
      | nmrPipe  -fn ZF -size $zf2                              \
      | nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 2 -c 0.5        \
      #| nmrPipe  -fn EM -lb 20                                 \ # Change the window function if needed
      | nmrPipe  -fn FT  -alt  -verb                            \
      | nmrPipe  -fn PS -p0 $ft3ph0 -p1 $ft3ph0 -di             \
      | nmrPipe  -fn TP                                         \
      | nmrPipe  -fn ZF -size $zf3                              \
      | nmrPipe  -fn SP -off 0.5 -end 0.98 -pow 2 -c 0.5        \
      | nmrPipe  -fn FT -alt -verb                              \
      | nmrPipe  -fn PS -p0 $ft2ph0 -p1 $ft2ph0 -di             \
      | pipe2xyz -out ft/sp_%03d%03d.ft3 -y
      
      xyz2pipe -in ft/sp_%03d%03d.ft3 -z                        \
      | nmrPipe   -fn ZF -size $zf3                             \
      #| nmrPipe  -fn EM -lb 10                                 \ # Change the window function if needed
      | nmrPipe   -fn SP -off 0.5 -end 0.98 -pow 2 -c 0.5       \
      | nmrPipe   -fn FT -alt -verb                             \
      | nmrPipe   -fn PS -p0 $ft1ph0 -p1 $ft1ph0 -di            \
      | pipe2xyz -out ft/sp_%03d%03d.ft4 -z
      
      date
      
      rm -fr *dat
      # "-skylin for skyline projection"
      # "-sum for sum projection"
      # "-abs for absolution projection"
      proj4D.tcl -in ft/sp_%03d%03d.ft4 -skyline
      
      date
      
      #goto DONE
      
      #----------------------------------------------------------------------------------------
      #                             Obtaining single fileswith the spectrum
      #----------------------------------------------------------------------------------------
      
      
      UCSF:
      
      xyz2pipe -in ft/sp_%03d%03d.ft4 -x > $filename.ft   # NMRPipe format
      ./pipe2ucsf $filename.ft $filename.ucsf             # Spraky format
      
      goto DONE
      
      #=========================================================================================
      
      CLEAN:
      
      rm -rf fid
      rm -rf ft2
      rm -rf ft21
      rm -rf ft1_ist
      rm -rf ft
      rm -rf ft1
      #rm -rf hncocanh4d.ft 
      goto DONE
      
      #=========================================================================================
      DONE: 
      echo "Finished"
      
      #=========================================================================================

## `runist_cluster`

      
      #!/bin/csh 
      
      
      pwd 
      
      #set parameters here 
      
      set yn = 80
      set zn = 80
      set an = 200
      set niter = 30
      
      #nothing to change below
      
      set F = $1
      
      set in = $F:t
      set out = $F:t:r.phf
      
      set tst = $F:t:r.tst
      
      if ( -f ft1_ist/${tst} ) then
      echo $in $out 
      
      else
      
      touch ft1_ist/${tst}
      
      echo $in $out 
      
      ./../istHMS -dim 3 -ref 0 -user 1 -incr 1 -xN $yn -yN $zn -zN $an  \
        -itr $niter -verb 1 -ref 0 -vlist ./nuslist -i_mult 0.98 -e_mult 0.98 \
        < ./ft1/${in} >! ./ft1_ist/${out}


        
