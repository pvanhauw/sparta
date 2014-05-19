/* ----------------------------------------------------------------------
   SPARTA - Stochastic PArallel Rarefied-gas Time-accurate Analyzer
   http://sparta.sandia.gov
   Steve Plimpton, sjplimp@sandia.gov, Michael Gallis, magalli@sandia.gov
   Sandia National Laboratories

   Copyright (2014) Sandia Corporation.  Under the terms of Contract
   DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains
   certain rights in this software.  This software is distributed under 
   the GNU General Public License.

   See the README file in the top-level SPARTA directory.
------------------------------------------------------------------------- */

#ifdef DUMP_CLASS

DumpStyle(image,DumpImage)

#else

#ifndef SPARTA_DUMP_IMAGE_H
#define SPARTA_DUMP_IMAGE_H

#include "dump_particle.h"

namespace SPARTA_NS {

class DumpImage : public DumpParticle {
 public:
  DumpImage(class SPARTA *, int, char**);
  ~DumpImage();

 private:
  int filetype;
  class Image *image;              // class that renders the images

  char *thetastr,*phistr;          // variables for view theta,phi
  int thetavar,phivar;             // index to theta,phi vars
  int cflag;                       // static/dynamic box center
  double cx,cy,cz;                 // fractional box center
  char *cxstr,*cystr,*czstr;       // variables for box center
  int cxvar,cyvar,czvar;           // index to box center vars
  char *upxstr,*upystr,*upzstr;    // view up vector variables
  int upxvar,upyvar,upzvar;        // index to up vector vars
  char *zoomstr,*perspstr;         // view zoom and perspective variables
  int zoomvar,perspvar;            // index to zoom,persp vars
  int boxflag,axesflag;            // 0/1 for draw box and axes
  double boxdiam,axeslen,axesdiam; // params for drawing box and axes
  double *boxcolor;                // colors for drawing box/grid/surf lines

  int viewflag;                    // overall view is static or dynamic

  // particle drawing

  int particleflag;                // 0/1 for draw particles
  int pcolor;                      // color of parts = TYPE, PROC, ATTRIBUTE
  int pdiam;                       // diam of partciles = TYPE, ATTRIBUTE
  double pdiamvalue;               // particle diameter value

  double **pcolortype;             // per-type particle colors
  double *pdiamtype;               // per-type particle diameters
  double *pcolorproc;              // particle color for me

  // grid drawing

  int gridflag;                    // 0/1 for draw entire grid cells
  int gcolor;                      // color of grid cells = PROC, ATTRIBUTE
  int gridwhich;                   // COMPUTE, FIX, VARIABLE for ATTRIBUTE
  char *idgrid;                    // ID of compute, fix, variable
  int gridindex;                   // index of compute, fix, variable
  int gridcol;                     // column of compute/fix array, 0 for vector

  double *gcolorproc;              // grid color for me

  // grid plane drawing

  int gridxflag,gridyflag;
  int gridzflag;                   // 0/1 for draw grid cell planes in xyz
  double gridxcoord,gridycoord;
  double gridzcoord;               // coordinate of plane
  int gxcolor,gycolor,gzcolor;     // color of planes = PROC, ATTRIBUTE
  int gridxwhich,gridywhich;
  int gridzwhich;                  // COMPUTE, FIX, VARIABLE for ATTRIBUTE
  char *idgridx,*idgridy,*idgridz; // ID of compute, fix, variable
  int gridxindex,gridyindex;
  int gridzindex;                  // index of compute, fix, variable
  int gridxcol,gridycol,gridzcol;  // column of compute/fix array, 0 vor vector

  // grid line drawing, for volume and planes

  int glineflag;                   // 0/1 for draw grid cell lines
  double glinediam;                // diameter of lines
  double *glinecolor;              // color of lines

  // surf drawing

  int surfflag;                    // 0/1 for draw surf elements
  int scolor;                      // color of surfs = ONE, PROC, ATTRIBUTE
  double *surfcolorone;            // ONE color of surfs
  double sdiamvalue;               // surf diameter for 2d lines
  int surfwhich;                   // COMPUTE, FIX, VARIABLE for ATTRIBUTE
  char *idsurf;                    // ID of compute, fix, variable
  int surfindex;                   // index of compute, fix, variable
  int surfcol;                     // column of compute/fix array, 0 vor vector

  double *scolorproc;              // surf color for me

  // surf line drawing

  int slineflag;                   // 0/1 for draw surf lines
  double slinediam;                // diameter of lines
  double *slinecolor;              // color of lines

  // methods

  void init_style();
  int modify_param(int, char **);
  void write();

  void box_center();
  void view_params();
  void box_bounds();

  void create_image();
};

}

#endif
#endif

/* ERROR/WARNING messages:

E: Invalid dump image filename

The file produced by dump image cannot be binary and must
be for a single processor.

E: Support for writing images in JPEG format not included

LAMMPS was not built with the -DLAMMPS_JPEG switch in the Makefile.

E: Support for writing images in PNG format not included

LAMMPS was not built with the -DLAMMPS_PNG switch in the Makefile.

E: Illegal ... command

Self-explanatory.  Check the input script syntax and compare to the
documentation for the command.  You can use -echo screen as a
command-line option when running LAMMPS to see the offending line.

E: Invalid dump image theta value

Theta must be between 0.0 and 180.0 inclusive.

E: Dump image persp option is not yet supported

Self-explanatory.

E: Dump image cannot use grid and gridx/gridy/gridz

UNDOCUMENTED

E: Dump image requires one snapshot per file

Use a "*" in the filename.

E: Variable name for dump image theta does not exist

Self-explanatory.

E: Variable for dump image theta is invalid style

Must be an equal-style variable.

E: Variable name for dump image phi does not exist

Self-explanatory.

E: Variable for dump image phi is invalid style

Must be an equal-style variable.

E: Variable name for dump image center does not exist

Self-explanatory.

E: Variable for dump image center is invalid style

Must be an equal-style variable.

E: Variable name for dump image zoom does not exist

Self-explanatory.

E: Variable for dump image zoom is invalid style

Must be an equal-style variable.

E: Variable name for dump image persp does not exist

Self-explanatory.

E: Variable for dump image persp is invalid style

Must be an equal-style variable.

E: Could not find dump image compute ID

UNDOCUMENTED

E: Could not find dump image fix ID

UNDOCUMENTED

E: Invalid color map min/max values

The min/max values are not consistent with either each other or
with values in the color map.

E: Invalid dump image zoom value

Zoom value must be > 0.0.

E: Invalid dump image persp value

Persp value must be >= 0.0.

E: Invalid color in dump_modify command

The specified color name was not in the list of recognized colors.
See the dump_modify doc page.

*/
