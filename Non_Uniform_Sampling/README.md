---
title: "NUS reconstruction algorithms"
permalink: /Non_Uniform_Sampling/
layout: default
---

# NUS reconstruction algorithms

* [SMILE](./NMRPipe/SMILE.md)
* IST 
	* [TopSpin](../TOPSPIN/NUS_reconstruction/) 
	* [Pipe](./NMRPipe/IST.md) 
	* [hmsIST scripts](./NMRPipe/hmsIST_no_pipe.md)
*  SSA
	* [Detailed reconstruction tutorial](SSA/Full_NUS_Reconstruction_Tutorial.md)
 	* [Quick start](./SSA/Quick_NUS_Reconstruction_Tutorial.md)

## Comparison

For processing of 3D spectra, one can afford to choose just about any reconstruction program without focusing on the implementation details. However for 4D, it is important that the method not only produces high quality frequency-domain data, but is also implemented in the resource efficient way.

Here we summarize the strengths and pitfalls of several reconstruction methods we tested ourselves.


|   Method      |NMR Pipe-based| RAM consumption |  Advantages   |  Disadvantages|  Time of full reconstruction (Ubiquitin)  |
|---------------|-----------|-----|----------|---------------|---------------|
|  SMILE        | Yes | **Overly high** |   Supposed to be the fastest and the "best" performing method overall for solution data |  **Won't run due to the [memory leak]** on large spectra (about 40 Gb) (https://groups.io/g/nmrpipe/topic/smile_4d_runs_out_of_memory/106780340) |   NA            |
|TopSpin CS (MDD)| No |  Medium (?) |  Integrated into TopSpin, peak-shape agnostic |  No reconstructed 4D FID written, each change in phasing or window function needs the entire reconstruction repeated.   |    Several hours (including the FT)       |
| hmsIST_4D.com        | Yes | Minimal | Peak-shape agnostic; integrated into NMR Pipe GUI    | Utterly inefficient use of the disk space ( 700+ Gb per spectrum); poorly documented  |         |
| hmsIST        | Yes | ~50 GB |  Fast; Good with overlapped peaks       |  Script-based interface |         |
| SSA           | No | NA | Fast and rather simple to set up     |  Apparently more prone to miss peaks than IST implementations            |  Overnight       |
