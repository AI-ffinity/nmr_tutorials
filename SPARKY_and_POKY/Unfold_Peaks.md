# Theory

**The peaks appear aliased/folded when** the frequency of a peak exceeds the Nyquist limit for the spectral window which is being observed. 
In the indirect dimensions, the spectral width is defined by the acquisition time (**SOME GOOD REFERENCE**), which is always limited by the available spectrometer time. 
The spectrometer time is expensive, which is one of the reasons to limit spectral width. (Another reason is the range of frequencies which can be hit by pulses). 

**The limit in spectral width is essentially the same as undersampling??**
If there are signals of a higher frequency than the maximum frequency sampled, the spectrometer “sees” their frequencies as if they were within the window by mirroring it, so it appears as a lower frequency within the observed range. 

The influence of the sampling rate is demonstrated in [this video by Zach Star](https://www.youtube.com/watch?v=Jv5FU8oUWEY)

**For nD NMR spectroscopy, this means** that peaks outside the detectable spectral window in any dimension will appear as "folded" or "aliased" peaks within the window. 
Folding in multiple dimensions, like in 2D or 3D NMR, can make spectra more complex, as folded signals from outside the spectral range appear within it, sometimes creating overlap with peaks from within the window. This folding or aliasing can complicate interpretation but may also be useful for spectral compression when controlled.

**There is a slight difference in terms "folded" and "aliased" peaks.** "Aliased" peaks typically refer to signals that appear within the observed spectral range due to frequency mirroring from outside the Nyquist range, whereas "folded" peaks are those that are mirrored back into the spectral window, 
often referring specifically to how they "fold" over the Nyquist frequency. In essence, while "aliasing" describes the appearance of an incorrect frequency, "folding" often refers to the mirroring effect specifically.

* Happens only in the indirect dimension: spectral width and sampling rate in the direct dimension is always enough - **is that still true for ultra-high fields like 1.2GHz???** 

## Phase of the folded peaks. 

**The sign of the folded peaks depends on the acquisition mode.**

In *Echo-antiecho* mode, the aliased signals will appear inverted. 

In *States-TPPI* the folded signals will have the same phase.

*States* and *TPPI* acquisition modes are inferior to *States-TPPI* and are not used in the modern NMR spectroscopy.


In the 3D spectrum, where one indirect dimension is recorded as _Echo-Antiecho_ and the other as _States-TPPI_, 
the folded signals will appear **WHAT PHASE?????**

For more details on the acquisition modes see _J. Keeler, Understanding NMR Spectroscopy, Chapter 8.12._ 

The additional factor influencing the phase of the folded signals is their offset from the carrier - 
i.e. how far they are from the middle of the spectrum. This is mostly and especially relevant for the carbon nuclei, 
which have a particularly wide spread of frequencies. 
The excitation pulses which are commonly used in the pulse sequence to target carbon nuclei affect only a narrow width 
around the frequency of the pulse in the "clean" way.
> A 90 degree pulse at 120 ppm will flip the magnetization vector of the carbons at 170 ppm for roughly 90 degrees, 
> but the 30-ppm-carbons will flip to only 40 degrees. *The numbers here are not accurate. The flip angle depends on the 
> amplitude and duration of the pulse. A precise calculation is quite simple but falls out of scope of this tutorial.*

## How to identify aliased peaks?

The most easy method to identify folded and aliased peaks is *experimental*, 
by recording a 2D with different spectrum widths. The peaks that change their positions are the aliased ones.  
* If the experimental evidence is not available, one has to resort to predictions. You may use the SHIFTX2 or UCBSHIFT plugins 
of POKY to obtain them. 
* **Hint about the antiphase**: happens if there are CO resonances. 
Phase distortion happens because the peaks are so far away that only specifically designed pulse sequences can cover the entire 
frequency range of 200 ppm from aliphatic to carbonyl carbons. (On the typical spectrometers 600+ MHz)
* Sign inversion - ???

The heatmaps below show the chemical shift distribution based on a dataset of nearly 4M peaks. 
If any peaks appear outside the shaded areas, they are likely to be aliased.   

| Hn / N plane                                                 | Hc/C plane                                                     |
|--------------------------------------------------------------|----------------------------------------------------------------|
| ![Peak Likelihood HN](./images/CS-distribution-HN-plane.png) | ![Peak Likelihood HcC](./images/CS-distribution-HcC-plane.png) |
  
Below are examples of the 13C-HSQC spectra with aliased peaks (in yellow boxes)

| Protein 1                                          | Protein 2                         |
|----------------------------------------------------|------------------------------------------------------|
| ![13C-HSQC-ac1](./images/13C-HSQC-ac1-aliased.png) | ![13C-HSQC-sy15](./images/13C-HSQC-sy15-aliased.png) |
 
# Unaliasing peaks in POKY
  
* When you use restricted peak picking (`kr`), POKY will automatically check for possible aliased peaks.
If the spectrum width of the source 2D is larger than that of the nD (n=[3,4]), than
POKY will find and mark the peaks in the 3D as aliased.

----------------------------

# LEGACY 


## Unfold peaks in the HC-C dimensions
* overlay the 2D HC-C projection of the 4D HCNH NOESY spectrum with the 13C HSQC spectrum
, as described in another tutorial.
* Identify peaks that are folded or aliased. You may use the SHIFTX2 or UCBSHIFT plugins 
of POKY to obtain the CS prediction and from the infer which peaks are folded/aliased.
* Open the 4D HCNH NOESY spectrum and the 15N HSQC and align them using `yt`.

Then you have two options to proceed.

### OPTION 1
* select all peaks in the 15N HSQC
* Switch to the 4D, type , activate the "peak" radio button.
* Type `ps` to enable viewing all peaks on all the visible planes.
* type `vd` to open the "View Depth" window, and set the visible planes at the N and HN 
dimensions to 999999. Now you should see all peaks of all spin systems of the 4D on the
HC-C plane.
* The peak locations should match those in the 2D HC-C projection. So you already know
which of them require unfolding/unaliasing. You can unalias them by a1,A1,a2,A2, etc.
as described in another tutorial.

### OPTION 2
