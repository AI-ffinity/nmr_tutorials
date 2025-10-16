You can make educated guesses about where to expect folded or aliased peaks in NMR spectra based on the parameters such as `FnMODE`, `SW` (Spectral Width), `SW_h` (high-resolution spectral width, if applicable), `O1`, and `O2` (carrier frequencies for different dimensions in multidimensional NMR experiments). Here’s how you can estimate the likelihood and location of such peaks:

### Understanding Folding and Aliasing
1. **Folding** occurs when a frequency component outside the observed spectral width is reflected back into the spectrum at a position calculated by subtracting (or adding, depending on the direction of the fold) that frequency from the spectral width.
2. **Aliasing** is similar but typically occurs due to insufficient sampling rates (in digital systems, described by the Nyquist theorem), which isn't often the primary concern with modern NMR settings but can still be relevant in certain multidimensional experiments.

### Using Parameters to Predict Folded/Aliased Peaks
- **Spectral Width (`SW`)**: This parameter determines the frequency range covered by the spectrum. If the chemical shifts of the sample extend beyond the spectral width, peaks corresponding to these shifts will appear folded into the spectrum. You can expect folding to occur at:
  \[ \text{Folded Position} = \pm (\text{Chemical Shift} - \text{SW}) \]
  
- **High-Resolution Spectral Width (`SW_h`)**: In some cases, especially in higher-dimensional NMR spectroscopy, a separate high-resolution spectral width might be specified. If `SW_h` is smaller than `SW`, it can indicate more focused acquisition within a smaller range, potentially leading to more folding if not correctly adjusted.

- **Carrier Frequency (`O1`, `O2`)**: These parameters set the center of the spectral window for the respective dimensions in a multidimensional experiment. If the carrier frequencies are not properly centered on the region of interest, peaks may fold from one end of the spectrum to the other. The general position where you might expect folding based on the carrier frequency can be estimated by:
  \[ \text{Expected Folded Position} = \text{O1 (or O2)} \pm \frac{\text{SW}}{2} \]

- **`FnMODE`** and Processing Algorithms: Depending on the Fourier transform mode and other processing settings, the representation of the spectrum might vary, influencing how peaks are visualized. Certain `FnMODE` settings might inherently handle folding or employ different strategies for displaying out-of-range frequencies.

### Example Scenario
Suppose you are performing a 2D NMR experiment with the following settings:
- `SW` of 10 ppm on both dimensions
- `O1` set to 4.7 ppm and `O2` set to 110 ppm (typical for proton and carbon frequencies, respectively)
- You expect chemical shifts in your sample ranging from 0 to 12 ppm in the first dimension and 100 to 180 ppm in the second dimension.

Here, you can predict:
- Peaks around 11 and 12 ppm in the first dimension could potentially fold to about 1 ppm and 0 ppm (i.e., 10 - 1 = 9 and 10 - 2 = 8, mirrored to the lower end of the spectrum).
- In the second dimension, peaks above 120 ppm might start folding back, appearing near the lower end of the spectrum range set by `O2`.

### Recommendations
- **Simulation**: Use chemical prediction software (e.g. UCBshift, SHIFTX, etc.) to model how your spectra might look like. By loading them to Sparky you can identify the peaks in your real spectrum that are aliased or folded.

---

# Authors
- Thomas Evangelidis