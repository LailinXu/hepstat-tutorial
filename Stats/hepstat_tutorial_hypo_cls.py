## \file
## \ingroup tutorial_pyroot
## \notebook
## RooStats example: compute the upper limit using Hypothesis Test Inversion (CLs Limits)
## The signal is a simple Gaussian and the background is a smoothly falling spectrum. 
## We need to perform the hypothesis test for different parameter of interest points and compute the corresponding p-values.
## Since we are interesting in computing a limit, the test null hypothesis, that we want to disprove, is the in this case the S+B model,
## while the alternate hypothesis is the B only model. *It is important to remember this, when we construct the hypothesis test calculator*.
## This is the opposite of the null hypothesis significance (p0) calculation.
##
##  Objectives of this tutorial are the following:
##  * Create the HypoTestInverter class and configure it
##  * Compute the CLs upper limits using the asymptotic formula
##  * Compute the CLs upper limits using the frequentist method (time consuming)
##
## \macro_image
## \macro_output
## \macro_code
##
## \author Lailin XU
## Based on the example [here](https://www.nikhef.nl/~vcroft/RooStats.html), and also [StandardHypoTestInvDemo.C](https://root.cern/doc/master/StandardHypoTestInvDemo_8C.html)

import os
# Import the ROOT libraries
import ROOT as R
from math import pow, sqrt, fabs
R.gROOT.SetStyle("ATLAS")

# Prepare the model
# =======================
# Signal mass point
mass = 125
# Worksapce
wsfile = "test_hf_ws_{}.root".format(mass)
if not os.path.isfile(wsfile):
  print("Error! No ws files found: {}".format(wsfile)) 
  pyhist = "hepstat_tutorial_histfactory_hists.py"
  if os.path.isfile(pyhist):
    cmd = "python3 {0} {1]".format(pyhist, mass)
    os.system(cmd)


# Open the workpace
tf = R.TFile.Open(wsfile, "READ")
w = tf.Get("myws")

# data
data = w.obj("obsData")

# The S+B model (Alternative hypo)
sbModel = w.obj("ModelConfig")
poi = sbModel.GetParametersOfInterest().first()
poi.setVal(1.)
poi.setRange(0, 20)
sbModel.SetSnapshot(R.RooArgSet(poi))

# PDF
pdf = sbModel.GetPdf()

# save snapshot before any fit has been done
params = pdf.getParameters(data)
snapshotName_init = "snapshot_paramsVals_initial"
w.saveSnapshot(snapshotName_init, params)

# The B model (Null hypo)
bModel = sbModel.Clone()
bModel.SetName("B_only_model")
poi.setVal(0)
bModel.SetSnapshot(R.RooArgSet(poi))

w.Print()

# Asymptotic calculator
# =======================
# NOTE here `null` is the S+B model, and the alternative is the B model, the one we want to disapprove
ac = R.RooStats.AsymptoticCalculator(data, bModel, sbModel)
ac.SetOneSided(True)

# HypoTestInverter
calc = R.RooStats.HypoTestInverter(ac)
# For 95% upper limits
calc.SetConfidenceLevel(0.95)

# for CLs
calc.UseCLs(True)
calc.SetVerbose(False)

# Get the hypo test result
r = calc.GetInterval()

med = r.GetExpectedUpperLimit(0)
m2 = r.GetExpectedUpperLimit(-2)
m1 = r.GetExpectedUpperLimit(-1)
p1 = r.GetExpectedUpperLimit(1)
p2 = r.GetExpectedUpperLimit(2)
# compute expected limit
print("Expected upper limits: " )
print(" expected limit (median) " , med)
print(" expected limit (-2 sig) " , m2)
print(" expected limit (-1 sig) " , m1)
print(" expected limit (+1 sig) " , p1)
print(" expected limit (+2 sig) " , p2)


# The frequentist appproach
# =======================
w.loadSnapshot(snapshotName_init)
poi.Print()
fc = R.RooStats.FrequentistCalculator(data, bModel, sbModel)
# null toys, alt toys
fc.SetToys(2500,1000)
# Test statistics: profile liekelihood
profll = R.RooStats.ProfileLikelihoodTestStat(sbModel.GetPdf())
profll.SetOneSided(True)

# Need to throw toys
toymcs = R.RooStats.ToyMCSampler(profll, 50)
if not sbModel.GetPdf().canBeExtended():
    toymcs.SetNEventsPerToy(1)
    print('\nAdjusting for non-extended formalism\n')

# HypoTestInverter
calc = R.RooStats.HypoTestInverter(fc)
calc.SetConfidenceLevel(0.95)

calc.UseCLs(True)
calc.SetVerbose(False)

# Set scan points and range
npoints = 10
poimin = poi.getMin()
poimax = poi.getMax()
calc.SetFixedScan(npoints,poimin,poimax)

# Get the hypo test result
r = calc.GetInterval()

med = r.GetExpectedUpperLimit(0)
m2 = r.GetExpectedUpperLimit(-2)
m1 = r.GetExpectedUpperLimit(-1)
p1 = r.GetExpectedUpperLimit(1)
p2 = r.GetExpectedUpperLimit(2)
# compute expected limit
print("Expected upper limits: " )
print(" expected limit (median) " , med)
print(" expected limit (-2 sig) " , m2)
print(" expected limit (-1 sig) " , m1)
print(" expected limit (+1 sig) " , p1)
print(" expected limit (+2 sig) " , p2)

# Plot the distributions of the test statistic
plot = R.RooStats.HypoTestInverterPlot("HTI_Result_Plot","HypoTest Scan Result",r)
c = R.TCanvas("HypoTestInverter Scan")
c.SetLogy(False)
plot.Draw("CLb 2CL")
c.Draw()

c.SaveAs("test_cls_1.png")
c.SaveAs("test_cls_1.root")
