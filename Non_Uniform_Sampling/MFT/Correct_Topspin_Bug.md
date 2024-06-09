# Description of Topspin files

In Bruker NMR spectroscopy systems, various files are used to store acquisition parameters for experiments, including multidimensional NMR like a 4D HCNH NOESY. Each of these files contains specific sets of parameters that define how the NMR experiment is conducted, particularly concerning each dimension of the experiment. Here’s a breakdown of what each file generally contains:

1. **acqu** and **acqus**: 
   - **acqu**: This file is the primary acquisition parameter file for the first dimension (F1) and is readable in a plain text format. It contains parameters like the number of points in F1, spectral width, pulse sequences, and other details necessary for the acquisition.
   - **acqus**: Similar to `acqu`, but usually in a format that is system-readable (binary or encoded). It might also contain a complete set of parameters in a format used by the software for processing and display.

2. **acqu2** and **acqu2s**:
   - **acqu2**: Contains acquisition parameters specifically for the second dimension (F2) of the experiment. Parameters might include details like the number of scans, delay times, and specific settings for phase cycling or gradient pulses for that dimension.
   - **acqu2s**: The system-readable version of `acqu2`, containing the same information in a format suited for the system's processing requirements.

3. **acqu3** and **acqu3s**:
   - **acqu3**: Used for storing acquisition parameters for the third dimension (F3) of the experiment. This could include details similar to `acqu2` but tailored for the third dimension's specific needs.
   - **acqu3s**: The system-readable version of `acqu3`, again containing similar information in a format that the system requires for correct interpretation and use.

4. **acqu4** and **acqu4s**:
   - **acqu4**: Contains acquisition parameters for the fourth dimension (F4) of the experiment. As with the other acqu files, it holds parameters relevant to its specific dimension.
   - **acqu4s**: The system-readable version of `acqu4`, containing the information in a system-compatible format.

In summary, the files without the 's' (like `acqu`, `acqu2`, etc.) are generally human-readable and can be viewed with a standard text editor. They contain parameters set for each specific dimension of a multidimensional NMR experiment. The files with an 's' (like `acqus`, `acqu2s`, etc.) are system-readable versions of these parameter files, usually used directly by the TopSpin software for executing the NMR experiment and processing the data. These files ensure that the spectrometer operates correctly according to the specific requirements of each dimension in a multidimensional experiment.


## Below is an example `acqu3` file and explaination of its contents:

This file contains acquisition parameters specific to the third dimension (F3) of your 4D HCNH NOESY experiment.

1. **##TITLE, ##JCAMPDX, ##DATATYPE, ##NPOINTS, ##ORIGIN, ##OWNER**: These are metadata entries providing information about the file format, type of data, origin (Bruker BioSpin GmbH), and owner of the data.

2. **##$ACQT0**: Acquisition time zero correction in points. This adjusts for the delay from the actual start of signal acquisition.

3. **##$BF1 (Base Frequency)**: The base frequency for the first channel, expressed in MHz. This is the primary frequency setting for the channel of the spectrometer used to observe the nucleus in question. It serves as the foundational frequency setting for tuning the NMR spectrometer to the resonance frequency of the nucleus being observed, essential for accurate NMR measurements and for the system’s calibration.

4. **##$DE**: Digital resolution enhancement factor.

5. **##$DECIM**: Decimation rate used in the digital filter.

6. **##$DR**: Dynamic range of the receiver.

7. **##$FW**: Full width in Hz, possibly indicating the bandwidth of the receiver.

8. **##$FnILOOP**: Number of iterations in indirect detection loops.

9. **##$FnMODE (Fourier Transformation Mode)**: This parameter sets the mode of Fourier transformation used in processing the NMR data. Different modes can affect how the data is transformed from the time domain to the frequency domain and can include options for phase-sensitive detection, magnitude calculation, or complex data handling. Affects the way the NMR signal is processed and visualized, influencing the spectral phase and baseline qualities. Proper setting of FnMODE is crucial for obtaining high-quality, artifact-free spectra suitable for quantitative and qualitative analysis.

10. **##$NUC1**: Observed nucleus in this dimension, which is carbon-13 (13C) for this parameter set.

11. **##$NusJSP, ##$NusT2, ##$NusTD**: Non-uniform sampling parameters that are specific to how data points are sampled and processed.

12. **##$O1 (Offset Frequency, aka Carrier Frequency)**: This is the offset frequency for the observed nucleus in the third dimension of your 4D experiment. It specifies the center of the frequency window around which the NMR spectrum is acquired. It is used to adjust the spectral position, ensuring that the spectral window is centered on the area of interest, which is crucial for observing specific resonances, especially when high precision is required in chemical shift measurements.

13. **##$ProjAngle**: Projection angle, likely relevant if there's any transformation or rotation of axes in the data processing or acquisition.

14. **##$SFO1 (Spectrometer Frequency for Observed Nucleus)**: This represents the spectrometer operating frequency for the observed nucleus, expressed in MHz. It is an important parameter that defines the absolute frequency setting of the NMR spectrometer for the nucleus being observed in this dimension. Influences how the frequency of NMR signals is calculated. Accurate SFO1 values are vital for precise chemical shift calculations and for comparisons between different spectra or different spectrometers.

15. **##$SW (Spectral Width)**: This parameter indicates the frequency range covered by the spectrum in Hz. It defines the maximum range of chemical shifts that can be observed from the center frequency set by the offset (##$O1). The spectral width determines how wide the frequency range is for the NMR acquisition. A smaller spectral width results in a higher digital resolution, assuming a constant number of data points, because the same number of points covers a narrower range of frequencies.

16. **##$SW_h (High-Resolution Spectral Width)**: High-resolution spectral width is typically used during the processing stage and may reflect an enhanced frequency range used for specific high-resolution techniques. This is not necessarily a direct acquisition parameter but may influence how the data is resampled or processed to achieve higher resolution in the frequency domain. The high-resolution spectral width might be utilized to adjust the resolution during processing or to set the parameters for zero-filling, which increases the number of points in the Fourier-transformed spectrum without increasing the actual information content. This can help in resolving closely spaced peaks more clearly.

17. **##$TD**: Total data points in this dimension of the experiment, defining the resolution in the frequency domain.

This file configures the settings for the third dimension of your 4D experiment, focusing on how the carbon-13 nucleus is observed and processed. Adjusting these parameters affects the resolution, sensitivity, and the range of chemical shifts that can be observed in your NMR experiments.

## Association Between ##$SW and ##$SW_h:
The association between these two values generally relates to how the raw data acquired with a spectral width (##$SW) is processed or interpolated to achieve a greater level of detail in the spectral display or analysis (##$SW_h). The high-resolution spectral width might be set to a higher value to provide a more detailed view of the spectrum after data processing techniques such as zero-filling or interpolation are applied.

Practical Example: If the original data is acquired with a spectral width of 58.033 Hz, processing it with a high-resolution spectral width of 8756.567 Hz could involve expanding the frequency axis in the final spectrum. This expansion doesn't increase the intrinsic resolution of the data collected but improves the appearance of the spectrum, making it easier to analyze and interpret, especially for complex mixtures or closely overlapping signals.
In summary, ##$SW_h may be used to refine the visualization and analysis of NMR data that is initially captured within the limits set by ##$SW, with both parameters playing pivotal roles in ensuring accurate spectral interpretation and detailed peak analysis.

# The Bug

2. **Correct Known TopSpin Bugs** related to badly writren O (offset values; aka CARrier frequencies) values :
   - For the 13C axis, change from 39.1096 ppm to 41 ppm.
   - For the HC axis, change from 6.666 ppm to 4.7 ppm.

   These corrections are included in the `preprocSPARSE.inp.1.5` file provided.
   
   - **How to calculate the correct 13C and HC CAR values and which version of Topspin generates this error?**

     **Answer:** The process involves some trial and error. Review all the SFO and BF values listed in the respective 
     acquisition files (acqu*) and try to determine which version of Topspin was used based on these values. 
     Additionally, other parameters, such as SW, might also be incorrect. The issue was initially reported a while ago, 
     and although Bruker has released about 2-3 patches to address it, the error still occurs randomly in various 
     versions, so there is no guaranteed way to predict which versions are error-free.


7. **Adjust the 13C Axis and Correct the TopSpin Bug**:

   - The **13C axis is folded by 1/4*SW** and relevant peaks are aliased. The amount of folding is also influenced by 
   the mentioned TopSpin bug. For a definition of "aliasing" and "folding" read [this](https://sites.google.com/site/ccpnwiki/home/documentation/ccpnmr-analysis/core-concepts/folding-and-aliasing).
   An example of spectrum aliasing-unaliasing can be found [here](https://sopnmr.blogspot.com/2016/04/aliasing.html).
   To match the 13C axis in the 4D NOESY with the 2D HC-C HSQC (`AIffinity/3/`), 
   shift the 13C axis in Sparky by this amount: `-(58.0333/4 + (41-39.1096)*2) = -18.289 ppm`. Fortunately, when 
   exporting the shifted peaks from Sparky to a Sparky list file, they preserve the corrected 13C coordinates. 
   The most correct approach would be to do "circular shift" on the raw 4D spectrum, to unfold aliased peaks, as 
   it's impractical to do CS on a finished 4D (~10GB size). But this cannot be done in SSA programs or in Sparky. 
   It is typically compensated by the peak aliasing feature in Sparky during peak picking/assignment. NMRPipe and 
   nmrglue have "circular shift" functions.
   
     - http://nmrwiki.org/wiki/index.php?title=CS_-_circular_shift_%28nmrPipe_function%29
   
     - https://nmrglue.readthedocs.io/en/latest/reference/generated/nmrglue.process.proc_base.cs.html

dimension 1 (HN):
BF1= 600.05
O1= 2820.235
SFO1= 600.052820235
SW= 11.9037139764792

dimension 4 (HC):
BF1= 600.05
O1= 4000
SFO1= 600.054
SW= 11.9037


CAR1 = ((SFO1-BF1)*1000000.0) / BF1

The error in the HC dimensions stems from the SFO1, which should have been 600.052820235, as the SFO1 of the HN dimension.

NOTE: I think that for every dimension, a calibration must be conducted starting from the BF[1-6] frequency (e.g. on the 600 MHz Bruker spectrometer, the BF1 of HN is 600.05) and reaching the optimum values for the spectroemter, which is the variable SFO[1-6] (e.g. on the 600 MHz Bruker spectrometer, the BF1 of HN is 600.052820235). If somebody asks "what is the spectrometer's magnetic field strenght" probably refers to the BF1 value for the HN proton, namely 600.05 MHz.


EXAMPLES FOR 13C dimension:
acqu:##$SFO2= 150.888879190413
acqus:##$SFO2= 150.888879190413
acqu3:##$SFO1= 150.88859396
acqu3s:##$SFO1= 150.88859396


acqu:##$BF2= 150.882693
acqu3:##$BF1= 150.882693
acqu3s:##$BF1= 150.882693
acqus:##$BF2= 150.882693

((SFO1-BF1)*1000000.0) / BF1 = 39.10958826814879 (wrong)
((SFO2-BF1)*1000000.0) / BF1 = 41.00000000012107 (correct)

Notice that the 13C nucleus is in dimension 2 in `acqus` file, as determined by `##$NUC2= <13C>`. The dimensions in this file are not associated with the axes of the 4D spectrum but to the elements 1H, 13C, 15N!
The `acqus` file contains the correct SFO values, unlike `acqu3` file, which corresponds to the C axis of the 4D HCNH NOESY spectrum, that contains wrong SFO value for the 13C nucleus.

# Conclusion
Try to match the SFO[1-9] values in the `acqu` file with the respective SFO[1-9] values in the `acqu[1-9]`. Beware that the `acqu` file contains the values of the elements 1H, 13C, 15N (e.g. one value for both HN and HC), while the `acqu[1-9]` files contain the values for one of the axes of the spectrum.

```shell
grep SFO acqu acqu[1-4]
grep BF acqu acqu[1-4]
```

