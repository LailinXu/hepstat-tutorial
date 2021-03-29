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
## Modified from [rf201_composite.py](https://root.cern/doc/master/rf201__composite_8py.html)

# Import the ROOT libraries
import ROOT as R
from math import pow, sqrt
R.gROOT.SetStyle("ATLAS")

# Setup component pdfs
# ---------------------------------------

# Declare observable x

#   [RooRealVar](https://root.cern.ch/doc/master/classRooRealVar.html) (const char *name, const char *title, Double_t minValue, Double_t maxValue, const char *unit="")
x = R.RooRealVar("x", "x", 0, 10)

# Create two Gaussian PDFs g1(x,mean1,sigma) anf g2(x,mean2,sigma) and
# their parameters
mean = R.RooRealVar("mean", "mean of gaussians", 5)
sigma1 = R.RooRealVar("sigma1", "width of gaussians", 0.5)
sigma2 = R.RooRealVar("sigma2", "width of gaussians", 1)

sig1 = R.RooGaussian("sig1", "Signal component 1", x, mean, sigma1)
sig2 = R.RooGaussian("sig2", "Signal component 2", x, mean, sigma2)

# Build Chebychev polynomial p.d.f.
a0 = R.RooRealVar("a0", "a0", 0.5, 0., 1.)
a1 = R.RooRealVar("a1", "a1", -0.2, 0., 1.)
bkg = R.RooChebychev("bkg", "Background", x, R.RooArgList(a0, a1))

# Full model: the total PDF
# ------------------------------------------
# Sum the signal components into a composite signal p.d.f.. Here we use [RooAddPdf](https://root.cern.ch/doc/master/classRooAddPdf.html)
#   RooAddPdf (const char *name, const char *title, const RooArgList &pdfList, const RooArgList &coefList, Bool_t recursiveFraction=kFALSE)
sig1frac = R.RooRealVar("sig1frac", "fraction of component 1 in signal", 0.8, 0., 1.)
sig = R.RooAddPdf("sig", "Signal", R.RooArgList(sig1, sig2), R.RooArgList(sig1frac))

# Sum the composite signal and background
bkgfrac = R.RooRealVar("bkgfrac", "fraction of background", 0.5, 0., 1.)
model = R.RooAddPdf("model", "g1+g2+a", R.RooArgList(bkg, sig), R.RooArgList(bkgfrac))

# A quick look at the model
model.Print()

# Sample, fit and plot model
# ---------------------------------------------------

myc = R.TCanvas("c", "c", 800, 600)
myc.SetFillColor(0)
myc.cd()

# Generate a toy data sample of 1000 events in x from model
data = model.generate(R.RooArgSet(x), 1000)

# Fit model to data
model.fitTo(data)

# Plot data and PDF overlaid
xframe = x.frame(R.RooFit.Title("Example of composite pdf=(sig1+sig2)+bkg"))
data.plotOn(xframe)
model.plotOn(xframe)
myc.Draw()

# Overlay the background component of model with a dashed line
ras_bkg = R.RooArgSet(bkg)
model.plotOn(xframe, R.RooFit.Components(ras_bkg), R.RooFit.LineStyle(R.kDashed))
myc.Draw()

# Overlay the background+sig2 components of model with a dotted line
ras_bkg_sig2 = R.RooArgSet(bkg, sig2)
model.plotOn(xframe, R.RooFit.Components(ras_bkg_sig2), R.RooFit.LineStyle(R.kDotted))
myc.Draw()

myc.SaveAs("test_roofit_1.png")
