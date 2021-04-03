## \file
## \ingroup tutorial_pyroot
## \notebook
## Histfactory example. The model is basically the same as [hepstat_tutorial_roofit_extended.py](https://gitee.com/lailinxu/hepstat-tutorial/blob/master/Fitting/hepstat_tutorial_roofit_extended.py.nbconvert.ipynb): i.e, composite p.d.f with signal and background component
## ```
## pdf = n_bkg * bkg(x,a0,a1) + mu * n_sig * (f_sig1 * sig1(x,m,s1 + (1-f_sig1) * sig2(x,m,s2)))
## ```
##  with following objectives:
##  * Create a workspace using Workspace Factory
##  * Example operations at the workspace level
## 
## See also the example code [rf511_wsfactory_basic.py](https://root.cern/doc/master/rf511__wsfactory__basic_8py.html)
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

# Setup component pdfs
# ---------------------------------------

# Instantiate a workspace
w = R.RooWorkspace("w")

# Create pdf components
#   A single syntax exists to instantiate all RooFit pdf and function classes
#   ClassName::objectname(...) creates an instance of ClassName with the given object name (and identical title).
w.factory("Chebychev::bkg(x[0,10],{a0[0.5,0.,1],a1[-0.2,0.,1.]})")
w.factory("Gaussian::sig1(x,mean[5.],width1[0.5])")
w.factory("Gaussian::sig2(x,mean,width2[1.0])")

# Create the total model
w.factory("expr::sig2frac('1.-sig1frac',sig1frac[0.8,0,1.])")
w.factory("SUM::sig(sig1frac*sig1,sig2frac*sig2)")
w.factory("expr::S('mu_sig*nsig',mu_sig[1,0,10],nsig[500])")
w.factory("SUM::model(S*sig,nbkg[1000,0,1000]*bkg)")

x = w.var("x")
model = w.pdf("model")
model.Print()

# Generate pseudo data via sampling
data = model.generate(R.RooArgSet(x), 1000)


# Fit and plot model
# ---------------------------------------------------

myc = R.TCanvas("c", "c", 800, 600)
myc.SetFillColor(0)
myc.cd()

# Fit model to data
model.fitTo(data)

# Plot data and PDF overlaid
xframe = x.frame(R.RooFit.Title("Example of composite pdf=(sig1+sig2)+bkg"))
data.plotOn(xframe, R.RooFit.Name('Data'))
model.plotOn(xframe, R.RooFit.Name('Full_Model'), R.RooFit.LineColor(R.kBlue))
xframe.Draw()
ymax = xframe.GetMaximum()
xframe.SetMaximum(ymax*1.2)

xframe.Draw()

# Overlay teh bkg component
ras_bkg = R.RooArgSet(w.obj("bkg"))
model.plotOn(xframe, R.RooFit.Components(ras_bkg), R.RooFit.LineStyle(R.kDashed), R.RooFit.LineColor(R.kRed), R.RooFit.Name('Bkg'))
xframe.Draw()

# Overlay the signal components of model with a dotted line
ras_sig1 = R.RooArgSet(w.obj("sig1"))
model.plotOn(xframe, R.RooFit.Components(ras_sig1), R.RooFit.LineStyle(R.kDotted), R.RooFit.LineColor(R.kMagenta), R.RooFit.Name('Sig1'))
xframe.Draw()
ras_sig2 = R.RooArgSet(w.obj("sig2"))
model.plotOn(xframe, R.RooFit.Components(ras_sig2), R.RooFit.LineStyle(R.kDotted), R.RooFit.LineColor(R.kGreen+2), R.RooFit.Name('Sig2'))
xframe.Draw()

myc.Update()
myc.SaveAs("test_histfactory_1.png")


# Import the Model and Data to a workspace
# ---------------------------------------------------

w.Import(data, R.RooFit.Rename("ObsData"))

# Create the ModelConfig
mc=R.RooStats.ModelConfig("ModelConfig", w)
# Set up the Model
mc.SetPdf(w.pdf("model"))
mc.SetParametersOfInterest(w.var("mu_sig"))
mc.SetNuisanceParameters(R.RooArgSet(w.var("a0"), w.var("a1"), w.var("sig1frac"), w.var("nbkg")))
mc.SetObservables(w.var("x"))

mc.Print()

w.Import(mc)

# Take a peek at the workspac
w.Print("t")

# Write the workspace to a file
w.writeToFile("test_model_ws.root") 

# Questions:
# ---------------------------------------------------
# * What is inside this root file?
# * What can I do with it?
