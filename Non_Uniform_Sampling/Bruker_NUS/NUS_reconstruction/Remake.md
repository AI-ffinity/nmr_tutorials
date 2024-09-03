# General workflow

1. Copy the raw 4D spectrum in a new directory by executing `wrpa` command. This will make working with the 4D neat and safe. 
> [!NOTE]
> NUS spectra before reconstruction are not that heavy: usually under a Gb. 
2. If there were recorded test 2D **planes** (or 3D cubes) with **this exact** 4D pulse program, check their processing parameters:
    * Phasing in the direct and indirect dimensions
    * Window functions (rarely changes from default)
    * Baseline correction parameters (rarely changes from default)
    * Linear Prediction (LP), if you use it.
> [!TIP]
> Using linear prediction (LP) can enhance resolution, especially if the time domain (TD) values are small or if your FIDs are truncated. In TopSpin, you can use LP for improving resolution in particular dimensions during the Fourier Transform process by specifying the ME_mod and NCOEF parameters for those dimensions. Note that it may cause additional wiggles.
3. Note down the signal region in the direct dimension. It can be extracted either from the test planes or the 2D experiments (HSQC, TOCSY, etc). 
    * Go to the 2D experiment. Zoom in such that the signal-free regions are trimmed as much as possible. Issue the `.ftf2region STSR` command, it will prompt to  `Save display region to Parameters STSR\SI`.
    * Issue the `STSR` command. Note down the values for the direct dimension. Same with `STSI`
> [!TIP]
> Those values may be obtained manually: in the 1D or 2D spectrum, note the "col Index" (`16` on the screenshot). Save it into `STSR`. Move the coursor to the right and calculate the width of the dimension in points, save that number into `STSI`.   

![coursor_position](../../images/coursor_position.png)
    
> [!IMPORTANT]
> Make sure the spectrum windows of the 4D and the planes are the same. If they are not, the signal regions have to be adjusted manually. 
4. Go to the `NUS` section. Check that the NUS mode is `mdd` (default). Set the phasing of the indirect dimensions to the same values as in the `Phase` section (i.e. `PH0` and `PH1`). 
5. When everything is ready, issue 

    `ftnd 0 21234 dlp nusthreads 30`

* ` ftnd` will run the NUS reconstruction, followed by FT all directions, with the Window Multiplication (WM), baseline correction and the LP as specified in the PROCPARS. `0` stands for "all dimensions", `21234` stands for the procedure number?, `dlp` stands for the region truncation, `nusthreads 30` allocates 30 CPU cores for the process. 
> [!NOTE]
> Whereas NUS reconstruction is parallelized, FT stage uses only a single thread, therefore takes multiple hours.
6. *Optionally*: adjust baseline correction parameters and apply the automatic baseline correction to the whole reconstructed 4D spectrum by issuing `absnd`.
7. Evaluate the quality of the reconstructed spectrum by looking at the sum projections. You need to look at both positive and negative projections to identify the antiphase signals as well as the potentially misphased peaks. This is done by the command `projplp` and `projpln`. Run each and provide the parameters over the GUI or run the single lines such as `projplp 12 all all 21` 
    - `projplp` stands for positive projection; run `projpln` to get the negative one
    - `12` refers to keeping the first two dimensions (for standard Bruker HSQC NOESY, those are C and HC dimensions); that means, N (F3) and direct H (F4) will be summed up.
    - `all` indicates that all planes within these dimensions should be included.
    - `21` specifies the output PROCNO where the projection data will be stored. Adjust the PROCNO based on where you want to save the output.
8. Perform automatic baseline correction of the projections with `abs1` followed by `abs2`.
9. If the projections look good, evaluate the 4D spectrum. 
    * Perform a putative peak picking. For that, lower the countours such that the noise disappears, then issue `pp` and set the sensitivity to the lowest countour level. 
    
    ![alt text](../../images/peak_picking.png)
    * Jump to some position of the 4D which contains signals. For that, press the E button and give the plane numbers or the desired ppm.

    ![screenshot](../../images/navigation_4D.png)


9. If the phasing or other processing parameters are off, adjust them and repeat the reconstruction. If the projections looks good - congratulations!


# Examples

## Bruker 4D HCNH NOESY

The dimensions in the Bruker's 4D HCNH NOESY spectrum are F1: C; F2: HC; F3: N; F4: HN.


## Simple alerts
> [!NOTE]
> This is a note.

> [!TIP]
> This is a tip. (Supported since 14 Nov 2023)

> [!IMPORTANT]
> Crutial information comes here.

> [!CAUTION]
> Negative potential consequences of an action. (Supported since 14 Nov 2023)

> [!WARNING]
> Critical content comes here.
