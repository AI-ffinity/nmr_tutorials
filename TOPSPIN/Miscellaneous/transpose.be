/*****************************************************************/
/*   transpose.be                   30.10.2012                   */
/*****************************************************************/
/*   Short Description :                                         */
/*****************************************************************/
/*   Keywords :                                                  */
/*****************************************************************/
/*   Description/Usage :                                         */
/*****************************************************************/
/*   Author(s) :                                                 */
/*   Name            : Wolfgang Bermel                           */
/*   Organisation    : Bruker Analytik                           */
/*   Email           : wolfgang.bermel@bruker.de                 */
/*****************************************************************/
/*   Name            Date    Modification:                       */
/*   ber             121030  created from noxdim                 */
/*****************************************************************/
/*
$Id: $
*/


AUERR = transpose(curdat, cmd);
QUIT

#undef MASR
#undef SINO
#undef TILT


#include <pstruc.h>
#include <pstruc_all.h>
#include <lib/par.h>
#include <fcntl.h>
#include <limits.h>


static struct all_pars p_f1s =
#include <pinit_all.h>

static struct all_pars p_f2s =
#include <pinit_all.h>


int transpose(const char* curdat, const char* cmd)
{

char infile[PATH_MAX], outfile[PATH_MAX], path[PATH_MAX];

double sw_p2, sw_p1, sf2, sf1;

float axis_offs2, axis_offs1, sr2, sr1;

int i,j,k,m;
int byteorder, ret;
int si1, si2, xdim1, xdim2;
int *rowin, *rowout;
int *dbuf;

FILE *fpin, *fpout;


/***** get dataset and parameters *****/

GETCURDATA

FETCHPARS("SI",&si2);
FETCHPAR1S("SI",&si1);

FETCHPARS("BYTORDP",&byteorder);
FETCHPARS("XDIM",&xdim2);
FETCHPAR1S("XDIM",&xdim1);


/***** allocate memory *****/

if ( 2. * (double)si1 * (double)si2 * (double)sizeof(int) 
                                       >= 2. * 1024 * 1024* 1024 )
   {
   (void)sprintf(path,"amount of memory requested too large\n");
   STOPMSG(path);
   }


dbuf = malloc ( 2 * si1 * si2 * sizeof(int) );

if (dbuf == 0)
   {
   (void)sprintf(path,"cannot get enough mermory\n");
   STOPMSG(path);
   }


rowin   = dbuf;
rowout  = dbuf + si1*si2;


/***** read 2D *****/

(void)strcpy(infile, PROCPATH("2rr"));

fpin = fopen(infile,"rb");

if ( fpin == NULL )
   {
   (void)sprintf(path,"cannot open 2rr file: %s",infile);
   STOPMSG(path);
   }

(void)fclose(fpin);


fpin = fopen(infile,"rb");

fread(rowin,sizeof(int),si1*si2,fpin);
local_swap4(rowin,sizeof(int)*si1*si2,byteorder);

(void)fclose(fpin);


/*****  sort/transpose *****/

for (m=0; m < si1/xdim1; m++)
   {
   for (k=0; k < si2/xdim2; k++)
      {
      for (j=0; j < xdim1; j++)
         {
         for (i=0; i < xdim2; i++)
            {
            rowout[i*si1+j+k*si1*xdim2+m*xdim1] = rowin[i+j*xdim2+k*xdim2*xdim1+m*xdim1*si2];
            }
         }
      }
   }


/***** store 2D *****/

(void)strcpy(outfile, PROCPATH("2rr"));

fpout = fopen(outfile,"wb");

local_swap4(rowout,sizeof(int)*si1*si2,byteorder);
fwrite(rowout,sizeof(int),si1*si2,fpout);

(void)fclose(fpout);


/***** store parameters *****/

STOREPARS("SI", si1)
STOREPAR1S("SI", si2)
STOREPARS("XDIM", si1)
STOREPAR1S("XDIM", si2)


STOREPARS("BYTORDP",local_endian ());


/***** free memory *****/

free(dbuf);


/***** unlink files *****/

(void)strcpy(outfile, PROCPATH("2ir"));

if (!access(outfile, F_OK))
   {
   (void)unlink(outfile);
   }


(void)strcpy(outfile, PROCPATH("2ri"));

if (!access(outfile, F_OK))
   {
   (void)unlink(outfile);
   }


(void)strcpy(outfile, PROCPATH("2ii"));

if (!access(outfile, F_OK))
   {
   (void)unlink(outfile);
   }


/***** read axis parameters *****/

FETCHPARS("SF",&sf2);
FETCHPARS("SW_p",&sw_p2);
FETCHPARS("OFFSET",&axis_offs2);
FETCHPARS("SR",&sr2);

FETCHPAR1S("SF",&sf1);
FETCHPAR1S("SW_p",&sw_p1);
FETCHPAR1S("OFFSET",&axis_offs1);
FETCHPAR1S("SR",&sr1);


/***** swap axis parameters *****/

STOREPARS("SR",&sr1);
STOREPAR1S("SR",&sr2);


(void)strcpy(path, PROCPATH("proc2s"));

if ((ret = getpar(path, "$PROC", &p_f1s)) < 0)
   {
   Proc_err(DEF_ERR_OPT, "getpar failed on %s\n%s", path, par_err(ret));
   return -1;
   }


(void)strcpy(path, PROCPATH("procs"));

if ((ret = getpar(path, "$PROC", &p_f2s)) < 0)
   {
   Proc_err(DEF_ERR_OPT, "getpar failed on %s\n%s", path, par_err(ret));
   return -1;
   }


p_f1s.SF = sf2;
p_f1s.SW_p = sw_p2;
p_f1s.OFFSET = axis_offs2;
/*
p_f1s.SR = sr2;
*/

p_f2s.SF = sf1;
p_f2s.SW_p = sw_p1;
p_f2s.OFFSET = axis_offs1;
/*
p_f2s.SR = sr1;
*/


(void)strcpy(path, PROCPATH("proc2s"));

if ((ret = putpar(path, "$PROC", &p_f1s)) < 0)
   {
   Proc_err(DEF_ERR_OPT, "getpar failed on %s\n%s", path, par_err(ret));
   return -1;
   }


(void)strcpy(path, PROCPATH("procs"));

if ((ret = putpar(path, "$PROC", &p_f2s)) < 0)
   {
   Proc_err(DEF_ERR_OPT, "getpar failed on %s\n%s", path, par_err(ret));
   return -1;
   }


/***** view data *****/

VIEWDATA


Proc_err(ERROPT_AK_NO, "transpose finished");


return 0;
}
