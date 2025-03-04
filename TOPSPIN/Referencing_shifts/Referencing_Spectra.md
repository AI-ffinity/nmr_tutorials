# Referencing spectra in Topspin with BioTop (RECOMMENDED)

- Execute `biotop` to open the browser-window.
- Set correctly the measurement conditions, namely `Labeling`, `Solvent`, `Tube`, `Temperature`. You can also provide 
the FASTA sequence of the protein and BioTop will automatically calculate the `Molecular size`. However, MW doesn't 
have any effect on the shift of the axes during referencing.
- Once ready, click `Close` and execute the command `btproc biorefonly`.
- You are all set. The axes must have shifted - check it.

> BioTop fails to reference 4D spectra and their 2D projections. In that case you will use the 2D projections to align
the 4D spectrum to the HSQC spectrum(a) [during peak picking in POKY](../../SPARKY_and_POKY/old_Peak_picking_4D_spectrum).

-------------

# Calibrating (aka Referencing) Manually all your 2D, 3D, 4D Spectra in Topspin

> **Calibration** is the process of using a referenced spectrum (e.g. `1H-15N HSQC`) to reference another spectrum
(e.g. `4D HCNH NOESY`)

Select the common axes between your 2D spectra, which you will use as a reference, and the 3D and 4D. 
For example, for 15N-edited 3D NOESY -> F1: H, F2: N, F3: HN  and 4D HCNH NOESY -> F1: C, F2: HC, F3: N, F4: HN
I chose the F2-F3 and F3-F4, respectively, because they match with the dimensions of the reference 15N HSQC.
Create the N-HN positive projections to identify common peaks between the three spectra 
with strong signal, which we will use for calibration: `projplp 23 all all 23` in 15N-edited 3D NOESY 
and `projplp 34 all all 34` in 4D HCNH NOESY.
Go to the 15N HSQC, do `.pp` for manual peak picking, select the chosen reference peak, type `peaks`
and note down its coordinates in ppm. Then switch to the 3D spectrum, click on the "23" icon to display
the F2-F3 plan. Type .md and select and drag the 15N HSQC spectrum, select it at the left lower panel
and increase its contour levels in order to clearly see all the peaks as strong signals but without noise. 
Then select the 3D spectrum and start navigating through the F1 axis by left-clicking and dragging on the 
"up-down arrow". While you navigate some of the peaks that are present in the 15 HSQC will start appearing
as strong signals in the overlaid F2-F3 plane. Once you see the signal of the selected reference peak appearing
stop dragging, place your cursor at the center of the peak and note down its index(F1)
coordinate, not the actual ppm coordinate. Now click on the "return" icon to return to the F2-F3 plane
view of the 3D NOESY. Click on the "E" icon, select the "F2-F3" visible plane and put the index(F1)
you noted down at the text box right of it. Now you should see the reference peak with strong signal.
Zoom in and type `.cal`, left-mouse click at the center of the reference peak, and in the window that 
pops up copy the coordinates in ppm you noted down from the 15 HSQC. Once you click "OK", both the F2 and F3
axes of the 3D NOESY spectrum will be shifted accordingly.
Do the same with the `34` projection of the 4D NOESY to calibrate it.

------------------

# OBSOLETE TOPSPIN MACRO SCRIPTS
These Topspin AU programs calculate the 1H, 13C and 15N reference shifts according 
to Lit: Wishart D. S. et al.: J. Biomol. NMR 6(1995) 135-140.

- Unzip and copy these files to `/opt/topspin4.4.0/exp/stan/nmr/au/src/user`.

You can add these values to the `SR` field in PROCPARS before FT or NUS reconstruction
to be applied to the resulting spectrum.