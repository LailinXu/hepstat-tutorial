## \file
## \ingroup tutorial_pyroot
## \notebook
## Histfactory example. 
##
##  with following objectives:
##  * Create a workspace using histograms
##  * Example operations at the workspace level
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

# Prepare input files
# =======================
inputhist = "data/h4l_toy_hists.root"
if not os.path.isfile(inputhist):
  print("Error! No input files found: {}".format(inputhist)) 
  pyhist = "hepstat_tutorial_genhists.py"
  if os.path.isfile(pyhist):
    cmd = "python3 {}".format(pyhist)
    os.system(cmd)

# Signal mass point
mass = 125

# Create a workspace
# =======================

# Create a Histfactory Measurement
# -----------------------

# First we set the Parameter of interest, and several constant parameters.
meas = R.RooStats.HistFactory.Measurement("meas", "meas")
meas.SetPOI("mu")

# Set the luminosity constant with a dummy uncertainty of 2%
meas.SetLumi( 1.0 )
meas.SetLumiRelErr( 0.02 )
meas.AddConstantParam("Lumi")

# Create a channel and set the measured value of data
chan = R.RooStats.HistFactory.Channel( "SR" )
chan.SetStatErrorConfig(0.05, "Poisson")
chan.SetData("obsData", inputhist)

# Create the signal sample and set its histogram
signal = R.RooStats.HistFactory.Sample( "signal", "sig_{}".format(mass), inputhist)

# Add the parmaeter of interest and a systematic and try to make intelligent choice of upper bound
signal.AddNormFactor( "mu", 1, 0, 3)

# Assign a dummy signal normalisation uncertainty (up, down with respect to the nominal)
signal.AddOverallSys( "signal_norm_uncertainty", 0.95, 1.05)

# Add the signal sample to the Channel
chan.AddSample( signal )

# Create the background sample and set its histogram
background = R.RooStats.HistFactory.Sample( "background", "bkg", inputhist )

# Add bkg systematics
background.AddHistoSys("background_shape", "bkg_up", inputhist, "", "bkg_dn", inputhist, "")

# Add the bkg sample to the Channel
chan.AddSample( background )

# Add the Channel to the Meas
meas.AddChannel(chan)

# Collect the histograms from their files, print some output, 
meas.PrintTree()

# Make workspace!
# -----------------------
hist2workspace = R.RooStats.HistFactory.HistoToWorkspaceFactoryFast(meas)
ws = hist2workspace.MakeSingleChannelModel(meas, chan)

ws.SetName("myws")
ws.writeToFile("test_hf_ws_{}.root".format(mass))

