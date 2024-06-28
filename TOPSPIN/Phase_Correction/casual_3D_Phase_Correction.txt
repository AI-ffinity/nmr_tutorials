# phase correction on a 3D spectrum (13C-edited NOESY)
- the vertical lines in the center of F2-F3 plane is the water. Pulse sequences are designed to be symmetrical, namely 
 the space before and after the water line to be the same. Note down the start and end position of the ROI 
(390-1990).
- open the raw 3D spectrum and issue `rser 1` followed by `qsin` and `fp`
- `.ph` to start manual phase correction on F1. Roughly you want the noise "baseline" to be horizontally aligned.
- once you find the optimal PHC0 and PHC1 values, save them to the raw 3D.
- open the raw 3D and issue `xfb` to create again the 2D projections. 
- If the spectrum looks half blue and half green, the in the raw 3D set PHC0 += 90 and repeat `xfb`.
- If you are satisfied, open the raw 3D and conduct Fourier transform with `ft3d`. In this case, the spectrum was
measure without NUS, so no NUS reconstructgion is needed.

# baseline correction on a 3D spectrum
- increase FID dimensions by x2, maximum x3 if for example the dimensions size is 60
- take the baseline as that you want to base it somewhere where you don't have peaks. Therefore in the proton dimension
 set ABSF1->9.0 ppm and ABSF2->-4.0 ppm
- Fourier transform with `ft3d`
- click on the "hill" icon, Contour level sign -> positive, Level increment -> 1.2, number of levels -> 30
- navigate in depth (F2) by clicking the "+" icon until you reach two overlapping peaks. Note down the plane No 
(e.g. 27/256). Do several iteration, each time trying different FID size, window function and linear prediction until
the peaks separate, then stop. don't do linear prediction on proton dimension because you acquire a lot of points, but 
you can do it in direct dimension. But don't overdo it!
- `tabs1` followed by `tabs3` for baseline correction in F1 and F3.



