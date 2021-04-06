## \file
## \ingroup tutorial_pyroot
## \notebook
## RooStats example: compute the p0 and significance (Hypothesis Test) 
## The signal is a simple Gaussian and the background is a smoothly falling spectrum. To estimate the significance,
## we need to perform an hypothesis test. We want to disprove the null model, i.e the background only model against the alternate model,
## the background plus the signal. In RooStats, we do this by defining two two ModelConfig objects, one for the null model
## (the background only model in this case) and one for the alternate model (the signal plus background).
##
##  Objectives of this tutorial are the following:
##  * Compute the null hypo significance using the Asymptotic calculator
##  * Compute the significance by hand using the asymptotic formula
##  * Compute the significance using frequentist method
##  * Plot the p0 scan as a function of the signal mass
##
## \macro_image
## \macro_output
## \macro_code
##
## \author Lailin XU
## Based on the example [here](https://www.nikhef.nl/~vcroft/RooStats.html), and also [StandardFrequentistDiscovery.C](https://root.cern/doc/master/StandardFrequentistDiscovery_8C.html)

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
data = w.data("obsData")

# The S+B model (Alternative hypo)
sbModel = w.obj("ModelConfig")
poi = sbModel.GetParametersOfInterest().first()
poi.setVal(1.)
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
# The Asymptotic calculator it is based on the Profile Likelihood test statistics,
# We will do:
#  * create the AsymptoticCalculator class using the two models and the data set;
#  * run the test of hypothesis using the GetHypoTest function.
#  * Look at the result obtained as a HypoTestResult object
ac = R.RooStats.AsymptoticCalculator(data, sbModel, bModel)
ac.SetOneSidedDiscovery(True)

# Get the hypo test result
asResult = ac.GetHypoTest()
asResult.Print()
pvalue_as = asResult.NullPValue()

# By hand calculation
# =======================
w.loadSnapshot(snapshotName_init)
sbModel = w.obj("ModelConfig")
pdf = sbModel.GetPdf()
# Get the nuisance parameters and global observables
constrainedParams = sbModel.GetNuisanceParameters()
glbObs = sbModel.GetGlobalObservables()
# Create the neg-log-likelihood
nll_sb = pdf.createNLL(data, R.RooFit.Constrain(constrainedParams), R.RooFit.GlobalObservables(glbObs), R.RooFit.Offset(1),
                                       R.RooFit.NumCPU(2), R.RooFit.Optimize(2))
nllval = nll_sb.getVal()
print("Starting NLL value:", nllval)

# Do the minimization
minim = R.RooMinimizer(nll_sb)
strategy = R.Math.MinimizerOptions.DefaultStrategy()
minim.setStrategy(strategy)
minim.optimizeConst(2)
minimizer = R.Math.MinimizerOptions.DefaultMinimizerType()
algorithm = R.Math.MinimizerOptions.DefaultMinimizerAlgo()
print("\n =========== Unconditinal fit =========\n")
status = minim.minimize(minimizer, algorithm)

obs_nll_min = nll_sb.getVal()
reverse = (poi.getVal() < 0)

# Fix POI to 0 (B-only model) and do the minimization again
print("\n =========== Conditinal fit =========\n")
w.loadSnapshot(snapshotName_init)
poi.setVal(0)
poi.setConstant(1)

status = minim.minimize(minimizer, algorithm)

obs_nll_min_bkg = nll_sb.getVal()

# The asymptotic statistic: q0 = nll(b-only, mu=0) - nll(s+b)
# Significance: Z = sqrt( 2*q0 )
obs_q0 = 2*(obs_nll_min_bkg - obs_nll_min)
# Check the sign: excess or deficit? 
if reverse: obs_q0 = -obs_q0
sign = 0
if obs_q0!=0: sign = obs_q0 / fabs(obs_q0)
obs_sig = sign*sqrt(fabs(obs_q0));
print("\nUnconditional NLL value:", obs_nll_min)
print("Conditional NLL value:", obs_nll_min_bkg)
print("==> Asymmptotic signficance: ", obs_sig)

# The frequentist appproach
# =======================
w.loadSnapshot(snapshotName_init)
poi.Print()
fc = R.RooStats.FrequentistCalculator(data, sbModel, bModel)
# null toys, alt toys
fc.SetToys(2500,1000)
# Test statistics: profile liekelihood
profll = R.RooStats.ProfileLikelihoodTestStat(sbModel.GetPdf())
profll.SetOneSidedDiscovery(True)
profll.SetVarName("q_{0}/2")

# Need to throw toys
toymcs = R.RooStats.ToyMCSampler(profll, 50)
if not sbModel.GetPdf().canBeExtended():
    toymcs.SetNEventsPerToy(1)
    print('\nAdjusting for non-extended formalism\n')

# Run the test
fqResult = fc.GetHypoTest()
fqResult.Print()
fqResult.GetNullDistribution().SetTitle("b only")
fqResult.GetAltDistribution().SetTitle("s+b")
fqResult.Print()
pvalue_fq = fqResult.NullPValue()

# Plot the distributions of the test statistic
c = R.TCanvas()
plot = R.RooStats.HypoTestPlot(fqResult)
plot.SetLogYaxis(True)

# add chi2 to plot, to check the asymptotic behavior
nPOI = 1
fchi = R.TF1("f", "1*ROOT::Math::chisquared_pdf(2*x,{0},0)".format(nPOI), 0, 20)
fchi.SetLineColor(R.kBlack)
fchi.SetLineStyle(7)
plot.AddTF1(fchi, "#chi^{{2}}(2x,{0})".format(nPOI))
plot.Draw()
c.Draw()

c.SaveAs("test_p0_1.png")
c.SaveAs("test_p0_1.root")
