## \file
## \ingroup tutorial_pyroot
## \notebook
## Fit examples with RooFit, composite p.d.f with signal and background component
## ```
## pdf = f_bkg * bkg(x,a0,a1) + (1-fbkg) * (f_sig1 * sig1(x,m,s1 + (1-f_sig1) * sig2(x,m,s2)))
## ```
##  with following objectives:
##  * Construct a simple fit in RooFit and plot the NLL
##  * Compare binned and unbinned fit results
##  * Compare un-extended and extended likelihoof it
##  * Compare plain likelihood fit and profile likelihood fit
##  * Fit with nuisance parameters with constraints
##
## \macro_image
## \macro_output
## \macro_code
##
## \author Lailin XU

# Import the ROOT libraries
import ROOT as R
from math import pow, sqrt
R.gROOT.SetStyle("ATLAS")


