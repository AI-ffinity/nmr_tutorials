# Unfold peaks in the HC-C dimensions
* overlay the 2D HC-C projection of the 4D HCNH NOESY spectrum with the 13C HSQC spectrum
, as described in another tutorial.
* Identify peaks that are folded or aliased. You may use the SHIFTX2 or UCBSHIFT plugins 
of POKY to obtain the CS prediction and from the infer which peaks are folded/aliased.
* Open the 4D HCNH NOESY spectrum and the 15N HSQC and align them using `yt`.

Then you have two options to proceed.

## OPTION 1
* select all peaks in the 15N HSQC
* Switch to the 4D, type , activate the "peak" radio button.
* Type `ps` to anable viewing all peaks on all the visible planes.
* type `vd` to open the "View Depth" window, and set the visible planes at the N and HN 
dimensions to 999999. Now you should see all peaks of all spin systems of the 4D on the
HC-C plane.
* The peak locations should match those in the 2D HC-C projection. So you already know
which of them require unfolding/unaliasing. You can unalias them by a1,A1,a2,A2, etc.
as described in another tutorial.

## OPTION 2
