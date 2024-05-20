# Extraction of 1D cross-sections and 2D planes from 4D
Open the raw 4D and issue `qsin 100 999`. This will extract the 1D cross-section at bin (findex) No. 100 and will save it to a new folder named 999. 

To extract a 2D plane from the raw 4D issue `rser2d`. You will be prompted to select the two axes, and the plane number, and a new EXPNO where the new ser file will be saved. Once the 2D plane is extracted
issue `xfb` for automated FT and NUS reconstruction.


Divide by 2 all 4 dimensions in the SI row before doing NUS reconstruction with `frnd 0`. this way it will be faster.
In STSI row at HN dimension write SI/2 and click enter. It removes the 5-0 ppm Region where only water protons occur.