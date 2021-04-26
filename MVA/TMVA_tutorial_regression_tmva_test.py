## \file
## \ingroup tutorial_tmva
## \notebook
## TMVA example, for regression
##  with following objectives:
##  * Test a BDT with TMVA
##
## \macro_image
## \macro_output
## \macro_code
##
## \author Lailin XU

from ROOT import TMVA, TFile, TTree, TCut, TH1F, TCanvas, gROOT, TLegend
from subprocess import call
from os.path import isfile
 
gROOT.SetStyle("ATLAS")
 
outfileName = 'TMVA_tutorial_reg_1.root'
tfin = TFile.Open(outfileName, 'READ')

# Helper function to fill histograms
def fill_hists(tr, tag):
  nevents = tr.GetEntries()

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
  hname="BDTG_{0}".format(tag)
  h4 = TH1F(hname, hname, nbins, xmin, xmax)
  h4.Sumw2()
  
  for i in range(nevents):
    tr.GetEntry(i)
 
    mtt_truth = tr.mtt_truth     
    # mtt_reco = tr.mtt_reco     
    BDT = tr.BDT     
    BDTG = tr.BDTG     
    h1.Fill(mtt_truth)
    # h2.Fill(mtt_reco)
    h3.Fill(BDT)
    h4.Fill(BDTG)
    
  return [h1, h2, h3, h4]

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

# Fill histograms
tr_train = tfin.Get("dataset/TrainTree")
h_train = fill_hists(tr_train, "train")

tr_test = tfin.Get("dataset/TestTree")
h_test = fill_hists(tr_test, "test")

# Plotting
myc = TCanvas("c", "c", 800, 600)
myc.SetFillColor(0)
myc.cd()

# Train vs Test
# ===============
# BDT
h1 = norm_hists(h_train[2])
h1.GetXaxis().SetTitle("BDT Regression m_{t#bar{t}} [GeV]")
h1.GetYaxis().SetTitle("A.U.")
h1.Draw()
h2 = norm_hists(h_test[2])
h2.SetLineColor(2)
h2.SetMarkerColor(2)
h2.Draw("same")

# Draw legends
lIy = 0.92
lg = TLegend(0.60, lIy-0.25, 0.85, lIy)
lg.SetBorderSize(0)
lg.SetFillStyle(0)
lg.SetTextFont(42)
lg.SetTextSize(0.04)
lg.AddEntry(h1, "Training", "l")
lg.AddEntry(h2, "Testing", "l")
lg.Draw()

myc.Draw()
myc.SaveAs("TMVA_tutorial_reg_test_1.png")

# BDTG
h1 = norm_hists(h_train[3])
h1.GetXaxis().SetTitle("BDTG Regression m_{t#bar{t}} [GeV]")
h1.GetYaxis().SetTitle("A.U.")
h1.Draw()
h2 = norm_hists(h_test[3])
h2.SetLineColor(2)
h2.SetMarkerColor(2)
h2.Draw("same")

# Draw legends
lIy = 0.92
lg = TLegend(0.60, lIy-0.25, 0.85, lIy)
lg.SetBorderSize(0)
lg.SetFillStyle(0)
lg.SetTextFont(42)
lg.SetTextSize(0.04)
lg.AddEntry(h1, "Training", "l")
lg.AddEntry(h2, "Testing", "l")
lg.Draw()

myc.Draw()
myc.SaveAs("TMVA_tutorial_reg_test_2.png")


# Regression vs Target
h1 = norm_hists(h_train[2])
h1.GetXaxis().SetTitle("m_{t#bar{t}} [GeV]")
h1.GetYaxis().SetTitle("A.U.")
h1.Draw()
h2 = norm_hists(h_train[3])
h2.SetLineColor(2)
h2.SetMarkerColor(2)
h2.Draw("same")
h3 = norm_hists(h_train[0])
h3.SetLineColor(4)
h3.SetMarkerColor(4)
h3.Draw("same")

# Draw legends
lIy = 0.92
lg = TLegend(0.60, lIy-0.25, 0.85, lIy)
lg.SetBorderSize(0)
lg.SetFillStyle(0)
lg.SetTextFont(42)
lg.SetTextSize(0.04)
lg.AddEntry(h1, "Regression BDT", "l")
lg.AddEntry(h2, "Regression BDTG", "l")
lg.AddEntry(h3, "Target", "l")
lg.Draw()

myc.Draw()
myc.SaveAs("TMVA_tutorial_reg_test_3.png")

