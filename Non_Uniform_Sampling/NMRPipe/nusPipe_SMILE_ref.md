---
title: "nusPipe SMILE ref"
layout: default
---

`nusPipe -fn SMILE -help`

Output: 

    ** SMILE Plugin:  Version 2.1 Rev 2019.337.11.19 64-bit **
    ** NMRPipe System Version 8.9 Rev 2017.150.13.42 64-bit **

    SMILE: Sparse Multidimensional Iterative Lineshape Enhanced.
    Options:
     -nDim        dimCount   [0]         Number of Dimensions     (0 for Auto).
     -nThread     nThread    [0]         Number of Threads        (0 for Auto).
     -maxMem      maxMem     [0.0]       Max Allowed Memory in GB (0 for Auto).
     -pseudoND                           Pseudo nD data, n-1 dim spectral series.
    SMILE RQD mode for echo-antiEcho (Use -x... -y...):
     -xEA                                Use Echo-AntiEcho (RQD Data Only).
    NUS Sampling Schedule:
     -sample        sName    [None]      NUS Sampling Schedule File.
     -sampleCount   sCount   [Auto]      Number of Valid Samples Measured.
     -sampleReverse                      Reverse Axis Order in Sampling Schedule.
     -sampleAverage                      Average Duplicates in Sampling Schedule.
     -sampleOffset  sampOff  [0 0 ...]   Offset Subtracted from Schedule Values.
    Phase Correction (Use -x... -y...):
     -xP0         xP0        [0.0]       Zero Order Phase Correction.
     -xP1         xP1        [0.0]       First Order Phase Correction.
    Zero Fill Options (Use Only One; Use -x... -y...):
     -xzf         zfCount    [2]         Number of Times to Double Size.
     -xzfSize     zfSize     [0]         Size After Zero Fill.
    Fourier Transform Modes (Use -x... -y...):
     -xAlt                               Use Sign Alternation Before FT.
     -xNeg                               Negate Imaginaries Before FT.
    Options for CT Evolution and Acq Time Extension (Use -x... -y...):
     -xCT         xCT        [0]         Number of Data Points Collected in CT.
     -xT          xT         [0]         Size extended (0 for 50% Extension).
    Apodization Parameters (Use -x... -y...):
     -xApod       xApodFunc  [SP]        Window Function: EM GM SP.
     -xQ1         xQ1        [0.50]      Window Function Parameter Q1.
     -xQ2         xQ2        [0.98]      Window Function Parameter Q2.
     -xQ3         xQ3        [1.00]      Window Function Parameter Q3.
    Composite Window Options, for SP Only (Use -x... -y...):
     -xELB        xElbHz     [0.0]       Exponential, Hz.
     -xGLB        xGlbHz     [0.0]       Gaussian, Hz.
     -xGOFF       xGOff      [0.0]       Gauss Offset, 0 to 1.
    Lineshape Simulation Parameters for Obtaining Linewidth-R2 Relationship:
     -minTDL      minTDL     [0.25]      Min TD Length (Tacq/max(T2)) for LW sim.
     -maxTDL      maxTDL     [4.00]      Max TD Length (Tacq/min(T2)) for LW sim.
    Options for unresolved scalar couplings (Use -x... -y...):
     -xJ                     [0.0]       Size of the unresolved J coupling;
    Options for Signal Detection, Reconstruction, and SMILE Termination:
     -sigma       sigma      [0.0]       Noise in the Data (0 for Auto Estimate).
     -nSigma      nSigma     [5.0]       Noise Factor for the Signal Cutoff.
     -thresh      thresh     [0.80]      Threshold for Signal Detection.
     -maxNPks     maxNPks    [0]         Max Number of Peaks (0 for Auto).
     -fraction    fraction   [1.00]      Fraction of Signals to be Reconstructed.
     -maxIter     maxIter    [800]       Max Number of Iterations.
     -maxTime     maxTime    [0.0]       Max Wall Time (hours) for the SMILE job.
    Options for Output Control:
     -scaling     scaling    [0.0]       Signal Downscaling Factor (0 for Auto).
     -log         logName    [smile.log] Log File Name
     -report      verbose    [0]         Report Level:
                                         0=No Report
                                         1=Output SMILE info (stderr & smile.log)
                                         2=More SMILE info on stderr
    Notes:
     1. Important options are -sample -xP0... -xP1...
     2. Auto setting for -nThread is Max(1, Number_of_Logical_Cores/2).
     3. Auto setting for -maxMem is 80% of the physical memory.
     4. When -xzf ... is used, zero fill size is rounded to a power of two.
        if a specific size is required, use -xzfSize ... instead.
     5. Use -xAlt ... if sign alternation is needed for FT of the given dimension.
     6. Use -xNeg ... if negation of imaginaries is needed for FT of the given dimension.
     7. Options -xAlt and -xNeg can be used together if needed.
     8. When setting an explicit value for -xT to perform extrapolation, use a value
        which is larger than the original time-domain size of the given dimension.
     9. Use the same -scaling value for spectra in a series, such as relaxation data.
