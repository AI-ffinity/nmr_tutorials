# t1-Noise Removal

--------------------

t1-noise can be attenuated by subtracting a projection of the noise using the **t1away** program, which automates threshold determination and processing. 

### Steps for Removing t1-Noise:
1. **swap2d**: Swap the t1 and t2 axes.
2. **t1away**: Use a typical threshold of 5-30 for t2 noise. For NOESY spectra, use thresholds ≥80 for t1 noise removal.
3. **swap2d**: Swap the axes back.

This method effectively removes noise bands in processed 2D spectra. Below is the Topspin macro.


```
/****************************************************************/
/* t1away 08.02.2007 */
/****************************************************************/
/* Short Description : */
/* Processing AU program to remove t1-noise from 2D spectra */
/****************************************************************/
/* Keywords : */
/* 2D t1-noise processing */
/****************************************************************/
/* Description/Usage : */
/* t1noise subtraction, for magnitude or phase sensitive */
/* data. */
/* */
/* For each column in the 2D a threshold is determined */
/* under which X% of the data points lie. All data points */
/* are then reduced by this threshold, with the effect */
/* that t1-noise/ridges artefacts are attenuated (this is */
/* equivalent to raising the contour level in areas of */
/* bigger noise). */
/* */
/* The threshold % can be altered to increase or decrease */
/* the effect, for example: */
/* t1away (default threshold, set below = 80%) */
/* t1away 70 (less subtraction) */
/* t1away 90 (more subtraction) */
/* */
/* Typical use as part of 2D processing: */
/* xfb */
/* <phase, if required> */
/* abs2 */
/* abs1 */
/* t1away */
/* <sym or syma, for homonuclear 2D, if desired> */
/****************************************************************/
/* Author(s) : */
/* Name : Andrew Gibbs */
/* Organisation : Bruker UK */
/* Email : andrew.gibbs@bruker.co.uk */
/****************************************************************/
/* Name Date Modification: */
/* agi 070208 created */
/* agi 070920 correct typo for reading xdim in f1 */
/* meb 01252011 moddified for use with TS 3 */
/****************************************************************/
/*
$Id: $
*/
/*** default threshold ***/
#define DEFSCALE 80;
Shan, Wilson, and Kamaric. Supporting Information S81
long xdim_f2, xdim_f1;
long si_f2, si_f1;
long point;
long nsub_f2, nsub_f1;
long i,j,k,l;
long ioffset, joffset, koffset;
char inputpath[PATH_MAX];
FILE *input;
long *spec_sub, *spec_2d, *spec_1d, *data;
long fullsize;
long max;
long *pld, *pld1;
int scale;
int qcomp( void *, void *);
int parmode;
GETCURDATA
FETCHPAR("PARMODE", &parmode)
if (parmode != 1) STOPMSG("function active for 2D data only!")
/* see if user asked for different threshold */
if ( *cmd != '\0') scale = atoi(cmd);
else scale = DEFSCALE;
/* get size of data matrix */
FETCHPARS("SI", &si_f2)
FETCHPAR1S("SI", &si_f1)
FETCHPARS("XDIM", &xdim_f2)
FETCHPAR1S("XDIM", &xdim_f1)
fullsize = si_f2*si_f1;
/* allocate memory for data */
if ( ( spec_sub = (long *)malloc(sizeof(long) * fullsize) ) == NULL ||
 ( spec_2d = (long *)malloc(sizeof(long) * fullsize) ) == NULL ||
 ( spec_1d = (long *)malloc(sizeof(long) * si_f1) ) == NULL )
{
Proc_err(ERROR_OPT, "could not allocated memory for arrays" );
ABORT
}
/* path to displayed data */
strcpy(inputpath, PROCPATH("2rr"));
/* open data file for read */
if ( (input = fopen(inputpath, "r")) == NULL )
{
Proc_err(ERROR_OPT, "file access problem %s ", inputpath);
ABORT
}
/* read data into memory */
if (fread(spec_sub, sizeof(long), fullsize, input) != fullsize)
{
Proc_err(ERROR_OPT, "did not read %d data points?", fullsize);
ABORT
}
fclose(input);
/*** reorder data from submatrix format ***/
/* number of submatrix units in each dimension */
nsub_f2 = si_f2 / xdim_f2;
Shan, Wilson, and Kamaric. Supporting Information
S82
nsub_f1 = si_f1 / xdim_f1;
/* input point from datastream */
point = 0;
for ( i=0; i < nsub_f1; i++) {
 ioffset = i * xdim_f1 * si_f2;
 for ( j=0; j < nsub_f2; j++)

{
 joffset = j * xdim_f2 + ioffset;
 for ( k=0; k < xdim_f1; k++)

{
 koffset = k * si_f2 + joffset;
 for ( l=0; l < xdim_f2; l++)

{
 spec_2d[ l + koffset] = spec_sub[point++];

}

}

}
}
data=spec_2d;
/*** end of reorder
- spec_2d is in 'natural' format ****/
/* for each column */
for (i=0; i<si_f2; i++) {
pld = spec_2d+i
;
/* extract column to 1D, absolute value */
for (j=0; j<si_f1; j++) {
spec_1d[j] = abs(*pld);
pld += si_f2;
}
 /* sort data, then get intensity of scale%'th point */
qsort(spec_1d, si_f1, sizeof(long), qcomp);
max = spec_1d[(int)(si_f1*((float)scale/100.0))];
/* reduce data points according to threshold */
pld = spec_2d+i;
for (j=0; j<si_f1; j++) {
if (abs(*pld) < max) *pld = 0;
else if (*pld < 0) *pld += max;
else if (*pld > 0) *pld
-= max;
pld += si_f2
;
}
}
/* now order data back to submatrix format */
/* input point from datastream */
point = 0;
for ( i=0; i < nsub_f1; i++) {
 ioffset = i * xdim_f1 * si_f2;
 for ( j=0; j < nsub_f2; j++)

{
 joffset = j * xdim_f2 + ioffset;
 for ( k=0; k < xdim_f1; k++)

{
 koffset = k * si_f2 + joffset;
 for ( l=0; l < xdim_f2; l++)
Shan, Wilson, and Kamaric. Supporting Information S83
 {
 spec_sub[point++] = spec_2d[ l + koffset];
 }
 }
 }
}
/* write data back to file */
if ( (input = fopen(inputpath, "w")) == NULL )
{
Proc_err(ERROR_OPT, "file access problem writing to %s ", inputpath);
ABORT
}
if (fwrite(spec_sub, sizeof(long), fullsize, input) != fullsize)
{
Proc_err(ERROR_OPT, "did not write %d data points?", fullsize);
ABORT
}
fclose(input);
/* force a screen refresh */
VIEWDATA_SAMEWIN
QUIT
/* function for quick sort */
int qcomp(void *n1, void *n2)
{
return(*(int *)n1 - *(int *)n2);
}
```