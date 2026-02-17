---
title: "nusPipe IST 4D ref"
layout: default
---

`ist4D.com -help`

Output: 
        
        ist4D.com 2020.023.18.46
        Perform IST Recontruction of 4D Non-Uniformly Sampled (NUS) Data:
         -in   inName    [Auto]              Expanded Time-Domain Input.
         -mask maskName  [mask/mask%04d.fid] Corresponding Time-Domain Mask Input.
         -out  outName   [ist/test%04d.ft4]  IST Spectrum Output.
         -ft1  ft1Name   [None]              IST Interferogram Output (Sets -noapod).
         -nus                                Input is NUS (Default).
         -us                                 Input is Uniformly Sampled (US).
         -yz                                 Exchange Y-Axis and Z-Axis of Result.
         -ya                                 Exchange Y-Axis and A-Axis of Result.
        IST Parameters:
         -istMaxRes r [Auto]  Target Max in Residual, as % of Original Max (Or Auto).
         -istTMult  t [0.70]  Fraction for Threshold at Each Iteration
         -istCMult  c [0.30]  Fraction for Reducing Data Above Threshold.
         -istIter   n [2048]  Maximum Allowed Iterations.
         -mult      m [1.0]   Multiplication Factor for -istMaxRes Auto.
         -retain              Retain Original Time-Domain Data Points (Sets -noapod).
         -noretain            Replace Original Time-Domain Data Points (Default).
         -rist                Same as -retain Option.
         -pos                 Use All-Positive IST (No Negative Signals).
        Noise Estimate (Used Only for Statistic Reports):
         -noise     s [None]  Estimate of Noise in Spectrum.
        Processing Parameters (Use -x... -y... -z... -a...):
         -xSOL   sName   [NULL]       Solvent Function Name and Options (X-Axis Only).
         -xAPOD  aName   [SP]         Window Function Name.
         -xQ1    q1      [0.50]       Window Parameter Q1.
         -xQ2    q2      [0.95]       Window Parameter Q2.
         -xQ3    q3      [2]          Window Parameter Q3 (Default for -yQ3/-zQ3 is 1).
         -xELB   elb     [0.0]        Exponential Line Broaden, Hz.
         -xGLB   glb     [0.0]        Gaussian Line Broaden, Hz.
         -xGOFF  goff    [0.0]        Gaussian Center, 0.0 to 1.0.
         -xC1    c       [Auto]       First-Point Time-Domain Scale (0.5 1.0 Auto).
         -xP0    p0      [0.0]        Zero-Order Phase Correction.
         -xP1    p1      [0.0]        First Order Phase Correction.
         -xZFARG zfArgs  [zf=1,auto]  ZF (Zero Fill) Option.
         -xFTARG ftArg   [None]       FT (Fourier Transform) Options (None neg alt).
         -xEXTX1 x1      [0%]         Extract Range Start (X-Axis Only) (% Hz ppm pts).
         -xEXTXN xn      [100%]       Extract Range End   (X-Axis Only) (% Hz ppm pts).
         -apodDF                      Adjust Window Function for Digital Oversampling.
         -noapod                      No Apodization for Indirect Dimensions.
         -ssNMR                       Set Defaults for Solid-State NMR Data.
        Processing Parameters for X-Axis Only:
         -xBASEARG_INIT bArgs [NULL]  Baseline Correction Before Region Extraction.
         -xP0EXT        p0Ext [0.0]   Zero-Order Phase After Region Extraction.
         -xP1EXT        p1Ext [0.0]   First Order Phase After Region Extraction.
        NUS Zero-Fill Mode (Time-Domain Extrapolation by IST):
         -nusZF                       NUS Zero-Fill Extrapolation ON (Default).
         -nonusZF                     NUS Zero-Fill Extrapolation OFF.
         -yNUSZF  zfArgs  [zf=1]      Amount of Y-Axis NUS Zero-Fill Extrapolation.
         -zNUSZF  zfArgs  [zf=1]      Amount of Z-Axis NUS Zero-Fill Extrapolation.
         -aNUSZF  zfArgs  [zf=1]      Amount of A-Axis NUS Zero-Fill Extrapolation.
         -istName outName [ist/test%04d.ft4]  Overrides -out Setting.
        Baseline Correction Function Name and Options (Use -x... -y... -z...):
         -xBASEARG_FT1    [NULL]      Interferogram Baseline Correction (X-Axis Only).
         -xBASEARG        [NULL]      Spectrum Baseline Correction.
         -xBASEARG_FINAL  [NULL]      Baseline Correction for Final IST Result.
        Baseline Correction Applied to Final Residual:
         -rBASEARG        [POLY,auto,ord=0] Residual Baseline Correction.
        Other Options:
         -clean           Delete Intermediate Results (Default).
         -noclean         Retain Intermediate Results.
        echi: Command not found.
         -progress        Display Progress Bar Graphic.
         -yz              Move Z-Axis to Y-Axis of Result.
         -ya              Move A-Axis to Y-Axis of Result.

        Notes:
         1. Options -xSOL -xBASEARG_FT1 -xBASEARG and -xBASEARG_FINAL are expanded
            into NMRPipe processing function names and command line arguments.
            Options should contain no spaces. Flags are separated by commas, and
            values are given using = signs. For example, solvent filter:

              -xSOL     NULL            Becomes: nmrPipe -fn NULL (No Solvent Filter)
              -xSOL     SOL             Becomes: nmrPipe -fn SOL
              -xSOL     POLY,time       Becomes: nmrPipe -fn POLY -time

            For baseline correction:

              -xBASEARG NULL            Becomes: nmrPipe -fn NULL (No Correction)
              -xBASEARG POLY,auto,ord=0 Becomes: nmrPipe -fn POLY -auto -ord 0


         2. Options -xZFARG -xFTARG are expanded to command line arguments for ZF
            and FT, for example:

              -xZFARG zf=2,auto       Becomes: nmrPipe -fn ZF -zf 2 -auto
              -xFTARG neg             Becomes: nmrPipe -fn FT -neg
              -xFTARG neg,alt         Becomes: nmrPipe -fn FT -neg -alt

         3. When first-point time-domain scaling is set to Auto (-xC1 Auto etc),
            the scaling value will be set to 0.5 if the first-order phase correction
            for that dimension is 0+/-10 degrees, or to 1.0 otherwise.

         4. For applying NUS Zero Fill to conventional data, use -nusZF -mask Auto to
            automatically create mask data via the nusZF.com script.

         5. If the X-Axis label of the input spectrum starts with 'HN', default
            parameters will be adjusted as follows:

               -xSOL SOL -xBASEARG_FINAL POLY,auto -xEXTX1 3% -xEXTXN 47%

            Or when -nusZF -mask Auto is used for conventional data:

               -xSOL SOL -xBASEARG POLY,auto -xEXTX1 3% -xEXTXN 47%

         6. If the -ssNMR flag is used, default parameters will be:

               -xSOL NULL -xBASEARG NULL -xBASEARG_FINAL NULL

         7. Commonly, only region of interest, FT, and phase correction options need
            to be provided, and the convergence parameter can be set automatically.
            Include -nusZF if extrapolation during reconstruction is desired. Example:

            ist4D.com -xP0 -75 -xP1   0 -xEXTX1 10.4ppm -xEXTXN 5.4ppm \
                      -yP0 -90 -yP1 180 -zFTARG alt -aFTARG alt -nusZF

         8. To stop an IST calculation in progress:

               touch ist.stop

         9. See utility nusExpand.tcl for expanding time-domain NUS data and
            creating time-domain NUS schedule mask.
