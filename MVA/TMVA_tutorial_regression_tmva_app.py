from ROOT import TMVA, TFile, TTree, TCut, TH1F, TCanvas, gROOT, TLegend
from subprocess import call
from os.path import isfile
from array import array
 
gROOT.SetStyle("ATLAS")

# Setup TMVA
TMVA.Tools.Instance()

# Reader
reader = TMVA.Reader("Color:!Silent")
 
# Inputs
# =============
# Load data
trfile = "SM_ttbar.root"
 
data = TFile.Open(trfile)
tree = data.Get('tree')
 
# Set input variables
branches = {}
for branch in tree.GetListOfBranches():
    branchName = branch.GetName()
    branches[branchName] = array('f', [-999])
    tree.SetBranchAddress(branchName, branches[branchName])
    if not 'mtt' in branchName:
        reader.AddVariable(branchName, branches[branchName])
 
# Book method(s)
# =============
# BDT
methodName = "BDT"
weightfile = 'dataset/weights/TMVARegression_{0}.weights.xml'.format(methodName)
reader.BookMVA( methodName, weightfile )

# Loop events
nevents = tree.GetEntries()

# Book histograms
tag = methodName
hname="mtt_truth_{0}".format(tag)
nbins, xmin, xmax=200, 0, 2000
h1 = TH1F(hname, hname, nbins, xmin, xmax)
h1.Sumw2()
hname="mtt_reco_{0}".format(tag)
h2 = TH1F(hname, hname, nbins, xmin, xmax)
h2.Sumw2()
hname="BDT_{0}".format(tag)
h3 = TH1F(hname, hname, nbins, xmin, xmax)
h3.Sumw2()

for i in range(nevents):
  tree.GetEntry(i)

  mtt_truth = tree.mtt_truth     
  mtt_reco = tree.mtt_reco     
  BDT = reader.EvaluateMVA(methodName)
  h1.Fill(mtt_truth)
  h2.Fill(mtt_reco)
  h3.Fill(BDT)

# Helper function to normalize hists
def norm_hists(h):

  h_new = h.Clone()
  hname = h.GetName() + "_normalized"
  h_new.SetName(hname)
  h_new.SetTitle(hname)
  ntot = h.Integral()
  if ntot!=0:
    h_new.Scale(1./ntot)

  return h_new

# Plotting
myc = TCanvas("c", "c", 800, 600)
myc.SetFillColor(0)
myc.cd()

# Train vs Test
nh1 = norm_hists(h1)
nh1.GetXaxis().SetTitle("m_{t#bar{t}} [GeV]")
nh1.GetYaxis().SetTitle("A.U.")
nh1.Draw()
nh2 = norm_hists(h2)
nh2.SetLineColor(2)
nh2.SetMarkerColor(2)
nh2.Draw("same")
nh3 = norm_hists(h3)
nh3.SetLineColor(4)
nh3.SetMarkerColor(4)
nh3.Draw("same")

ymin = 0
ymax = max(nh1.GetMaximum(), nh2.GetMaximum(), nh3.GetMaximum())
nh1.GetYaxis().SetRangeUser(ymin, ymax*1.2)

# Draw legends
lIy = 0.92
lg = TLegend(0.60, lIy-0.25, 0.85, lIy)
lg.SetBorderSize(0)
lg.SetFillStyle(0)
lg.SetTextFont(42)
lg.SetTextSize(0.04)
lg.AddEntry(nh1, "Truth", "l")
lg.AddEntry(nh2, "Reco", "l")
lg.AddEntry(nh3, "Regression", "l")
lg.Draw()

myc.Draw()
myc.SaveAs("TMVA_tutorial_reg_app_1.png")

