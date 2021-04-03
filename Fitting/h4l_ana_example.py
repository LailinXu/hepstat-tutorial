## \file
## \ingroup tutorial_pyroot
## \notebook
## Fit example.
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

# Open the root file, which contains a simple TTree
fname = "mc_160155.ggH125_ZZ4lep.root"
tfin = R.TFile.Open(fname, "READ")
tr = tfin.Get("mini")

nevents = tr.GetEntries()
print("Num. of events in file {0}: {1}".format(nevents, fname))

hname = "m4l"
nbins, xmin, xmax = 100, 110, 130
h_m4l = R.TH1F(hname, hname, nbins, xmin, xmax)
h_m4l.Sumw2()

# Unbinned data
r_m4l = R.RooRealVar("obs_m4l", "obs_m4l", xmin, xmax)
data_unbinned = R.RooDataSet("ds", "ds", R.RooArgSet(r_m4l))

# Loop all events
nevt_max = min(nevents, 1000)
for ie in range(nevt_max):
  tr.GetEntry(ie)

  # Event weight
  wt = tr.mcWeight
  
  # 4-momentum of leptons
  tlz_leps = []
  for il in range(len(tr.lep_pt)):    
    tlz_l = R.TLorentzVector()
    tlz_l.SetPtEtaPhiE(tr.lep_pt[il], tr.lep_eta[il], tr.lep_phi[il], tr.lep_E[il])

    tlz_leps.append(tlz_l)

  tlz_4l = R.TLorentzVector()
  for tlz in tlz_leps: tlz_4l += tlz

  # the invariant mass
  m4l = tlz_4l.M()*1e-3 # MeV -> GeV
  h_m4l.Fill(m4l, wt)

  r_m4l.setVal(m4l)
  data_unbinned.add(R.RooArgSet(r_m4l))

data_unbinned.Print()

# Plotting
myc = R.TCanvas("c", "c", 800, 600)
myc.SetFillColor(0)

myc.cd()
h_m4l.Draw()
myc.Draw()
myc.SaveAs("m4l_test.png")

tfin.Close()
