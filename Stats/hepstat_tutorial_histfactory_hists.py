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

import os, sys
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
# if len(sys.argv)>1: mass = int(sys.argv[1])

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
#   [RooStats::HistFactory::Sample](https://root.cern.ch/doc/v606/classRooStats_1_1HistFactory_1_1Sample.html#abc13f0d4bc554b73bdb5fd3eb3a6672b)(std::string Name, std::string HistoName, std::string InputFile, std::string HistoPath="")
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
background.AddOverallSys( "bkg_norm_uncertainty", 0.90, 1.10)
#  [RooStats::HistFactory::Sample::AddHistoSys](https://root.cern.ch/doc/v606/classRooStats_1_1HistFactory_1_1Sample.html#af6f7abaad023353f47f63c8db6f39af0) (std::string Name, std::string HistoNameLow, std::string HistoFileLow, std::string HistoPathLow, std::string HistoNameHigh, std::string HistoFileHigh, std::string HistoPathHigh)
background.AddHistoSys("background_shape", "bkg_up", inputhist, "", "bkg_dn", inputhist, "")

# Add the bkg sample to the Channel
chan.AddSample( background )

# Add the Channel to the Meas
meas.AddChannel(chan)

# Collect the histograms from their files, print some output, 
meas.CollectHistograms()
meas.PrintTree()

# Make the workspace!
# -----------------------
hist2workspace = R.RooStats.HistFactory.HistoToWorkspaceFactoryFast(meas)
ws = hist2workspace.MakeSingleChannelModel(meas, chan)

# Write to a file
ws.SetName("myws")
ws.Print("t")
ws.writeToFile("test_hf_ws_{}.root".format(mass))

