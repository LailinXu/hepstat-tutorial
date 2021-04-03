## \file
## \ingroup tutorial_pyroot
## \notebook
##
## Generate some histograms
##   * Signal samples with different mass points, assuming Gaussian shapes
##   * Background samples: nominal and up/down variations, a simple ploynomial
##
## \macro_image
## \macro_output
## \macro_code
##
## \author Lailin XU

import os
# Import the ROOT libraries
import ROOT as R
from math import pow, sqrt
R.gROOT.SetStyle("ATLAS")

odir = "data"
if not os.path.isdir(odir): os.makedirs(odir)
tfout = R.TFile("data/h4l_toy_hists.root", "RECREATE")

# Signal samples
# ----------------
nevents = 100000
mHs = [120., 125., 130., 135., 140., 145., 150.]
# Gaussian
for mH in mHs:
  x = R.RooRealVar("x", "x", 110, 160)

  mean = R.RooRealVar("mean", "mean of gaussians", mH)
  wH = mH*0.01
  sigma = R.RooRealVar("sigma", "width of gaussians", wH)

  sig = R.RooGaussian("sig", "Signal", x, mean, sigma)

  # Generate pseudo data via sampling
  data = sig.generate(x, nevents)
  x.setBins(50)
  hname = "sig_{:d}".format(int(mH))
  dh = R.RooDataHist(hname, hname, R.RooArgSet(x), data).createHistogram(hname, x)
  dh.SetName(hname)

  tfout.cd()
  dh.Write()

# Nominal bkg
# ----------------
x = R.RooRealVar("x", "x", 110, 160)
p0 = 480.
p1 = -2.5
a0 = R.RooRealVar("a0", "a0", p0)
a1 = R.RooRealVar("a1", "a1", p1)
bkg = R.RooPolynomial("bkg", "Background", x, R.RooArgList(a0, a1))

# Generate pseudo data via sampling
data = bkg.generate(x, nevents)
data_obs = bkg.generate(x, nevents)
x.setBins(50)
hname = "bkg"
dh = R.RooDataHist(hname, hname, R.RooArgSet(x), data).createHistogram(hname, x)
dh.SetName(hname)

# Toy observed data
# ----------------
x.setBins(50)
hname = "obsData"
dh = R.RooDataHist(hname, hname, R.RooArgSet(x), data_obs).createHistogram(hname, x)
dh.SetName(hname)


# Background variations
# ----------------
# Variation up
a0 = R.RooRealVar("a0", "a0", p0*1.02)
a1 = R.RooRealVar("a1", "a1", p1*0.99)
bkg = R.RooPolynomial("bkg_up", "Background", x, R.RooArgList(a0, a1))

# Generate pseudo data via sampling
data = bkg.generate(x, nevents)
x.setBins(50)
hname = "bkg_up"
dh_up = R.RooDataHist(hname, hname, R.RooArgSet(x), data).createHistogram(hname, x)
dh_up.SetName(hname)

# Variation up
a0 = R.RooRealVar("a0", "a0", p0*0.98)
a1 = R.RooRealVar("a1", "a1", p1*1.01)
bkg = R.RooPolynomial("bkg_dn", "Background", x, R.RooArgList(a0, a1))

# Generate pseudo data via sampling
data = bkg.generate(x, nevents)
x.setBins(50)
hname = "bkg_dn"
dh_dn = R.RooDataHist(hname, hname, R.RooArgSet(x), data).createHistogram(hname, x)
dh_dn.SetName(hname)

tfout.cd()
dh.Write()
dh_up.Write()
dh_dn.Write()

tfout.Close()

