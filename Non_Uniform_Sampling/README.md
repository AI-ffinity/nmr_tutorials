# Manuals

* [SMILE](./NMRPipe/SMILE.md)
* IST 
	* [TopSpin](TOPSPIN/NUS_reconstruction/NUS_reconstruction.md) 
	* [Pipe](./NMRPipe/IST.md) 
	* [hmsIST scripts](./NMRPipe/hmsIST_no_pipe.md)
*  SSA


# Algorithm comparison

For processing of 3D spectra, one can afford to chose just about any reconstruction program without focussing on the implementation details. However for 4D, it is important that the method not only produces high quality frequency-domain data, but is also implemented in the resourse efficient way.

Here we summarized strenths and pitfalls of several reconstruction methods we tried ourselves.


|   Method      |NMR Pipe-based| RAM consumption |  Advantages   |  Disadvantages|  Time of full reconstruction (Ubiquitin)  |
|---------------|-----------|-----|----------|---------------|---------------|
|  SMILE        | Yes | **Overly high** |   Supposed to be the fastest and the "best" performing method overall for solution data |  **Won't run due to the [memory leak]** on large spectra (about 40 Gb) (https://groups.io/g/nmrpipe/topic/smile_4d_runs_out_of_memory/106780340) |   NA            |
|TopSpin CS (MDD)| No |  Medium (?) |  Integrated into TopSpin, peak-shape agnostic |  No reconstructed 4D FID written, each change in phasing or window function needs the entire reconstruction repeated.   |    Several hours (including the FT)       |
| hmsIST_4D.com        | Yes | Minimal | Peak-shape agnostic; integrated into NMR Pipe GUI    | Utterly inefficient use of the disc space ( 700+ Gb per spectrum); poorly documented  |         |
| hmsIST        | Yes | ~50 GB |  Fast; Good with overlapped peaks       |  Script-based interface |         |
| SSA           | No | NA | Fast and rather simple to set up     |  Apparently more prone to miss peaks than IST implementations            |  Overnight       |


