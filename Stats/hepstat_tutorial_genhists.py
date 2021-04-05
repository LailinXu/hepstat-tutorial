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
# Number of toy events to obtain the signal/bkg distributions (only to get the shape)
nbins = 25
nevents = 100000
# Number of toy events for the background
nbkg_exp = 100
mHs = [120., 125., 130., 135., 140., 145., 150.]
# Gaussian
for mH in mHs:
  x = R.RooRealVar("x", "x", 110, 160)

  mean = R.RooRealVar("mean", "mean of gaussians", mH)
  wH = mH*0.01
  sigma = R.RooRealVar("sigma", "width of gaussians", wH)

  sig = R.RooGaussian("sig", "Signal", x, mean, sigma)

  # Generate pseudo data via sampling
  data = sig.generate(R.RooArgSet(x), nevents)
  x.setBins(nbins)
  hname = "sig_{:d}".format(int(mH))
  dh = R.RooDataHist(hname, hname, R.RooArgSet(x), data).createHistogram(hname, x)
  dh.Scale(1./(dh.Integral()))
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
data = bkg.generate(R.RooArgSet(x), nevents)
x.setBins(nbins)
hname = "bkg"
dh = R.RooDataHist(hname, hname, R.RooArgSet(x), data).createHistogram(hname, x)
nint = dh.Integral()
dh.Scale(nbkg_exp/nint)
dh.SetName(hname)

# Toy observed data
# ----------------
data_obs = bkg.generate(R.RooArgSet(x), nbkg_exp)
x.setBins(nbins)
hname = "obsData"
dh_obs = R.RooDataHist(hname, hname, R.RooArgSet(x), data_obs).createHistogram(hname, x)
dh_obs.SetName(hname)


# Background variations
# ----------------
# Variation up
a0 = R.RooRealVar("a0", "a0", p0*1.02)
a1 = R.RooRealVar("a1", "a1", p1*0.99)
bkg = R.RooPolynomial("bkg_up", "Background", x, R.RooArgList(a0, a1))

# Generate pseudo data via sampling
data = bkg.generate(R.RooArgSet(x), nevents)
x.setBins(nbins)
hname = "bkg_up"
dh_up = R.RooDataHist(hname, hname, R.RooArgSet(x), data).createHistogram(hname, x)
dh_up.Scale(nbkg_exp/nint)
dh_up.SetName(hname)

# Variation up
a0 = R.RooRealVar("a0", "a0", p0*0.98)
a1 = R.RooRealVar("a1", "a1", p1*1.01)
bkg = R.RooPolynomial("bkg_dn", "Background", x, R.RooArgList(a0, a1))

# Generate pseudo data via sampling
data = bkg.generate(R.RooArgSet(x), nevents)
x.setBins(nbins)
hname = "bkg_dn"
dh_dn = R.RooDataHist(hname, hname, R.RooArgSet(x), data).createHistogram(hname, x)
dh_dn.Scale(nbkg_exp/nint)
dh_dn.SetName(hname)

tfout.cd()
dh_obs.Write()
dh.Write()
dh_up.Write()
dh_dn.Write()

tfout.Close()

