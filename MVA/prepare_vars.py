#!/usr/bin/env python

import ROOT as R
import numpy as np
from math import fabs

def loop_tr(infile="", outfile="test.root"):

  # Input file
  tfin=R.TFile(infile, "READ")
  tname="Delphes"
  tr=tfin.Get(tname)

  # Output file 
  tfout=R.TFile(outfile, "RECREATE")
  trout = R.TTree("tree", "tutorial")

  mtt_truth = np.empty((1), dtype="float32")
  mtt_reco = np.empty((1), dtype="float32")
  o_tlz_l1 = R.TLorentzVector()
  o_tlz_l2 = R.TLorentzVector()
  o_tlz_j1 = R.TLorentzVector()
  o_tlz_j2 = R.TLorentzVector()
  o_tlz_j3 = R.TLorentzVector()
  o_tlz_l1_pt, o_tlz_l1_eta, o_tlz_l1_phi, o_tlz_l1_m = np.empty((1), dtype="float32"), np.empty((1), dtype="float32"), np.empty((1), dtype="float32"), np.empty((1), dtype="float32")
  o_tlz_l2_pt, o_tlz_l2_eta, o_tlz_l2_phi, o_tlz_l2_m = np.empty((1), dtype="float32"), np.empty((1), dtype="float32"), np.empty((1), dtype="float32"), np.empty((1), dtype="float32")
  o_tlz_j1_pt, o_tlz_j1_eta, o_tlz_j1_phi, o_tlz_j1_m = np.empty((1), dtype="float32"), np.empty((1), dtype="float32"), np.empty((1), dtype="float32"), np.empty((1), dtype="float32")
  o_tlz_j2_pt, o_tlz_j2_eta, o_tlz_j2_phi, o_tlz_j2_m = np.empty((1), dtype="float32"), np.empty((1), dtype="float32"), np.empty((1), dtype="float32"), np.empty((1), dtype="float32")
  o_tlz_j3_pt, o_tlz_j3_eta, o_tlz_j3_phi, o_tlz_j3_m = np.empty((1), dtype="float32"), np.empty((1), dtype="float32"), np.empty((1), dtype="float32"), np.empty((1), dtype="float32")
  nlep_good, njets_good=np.empty((1), dtype="float32"), np.empty((1), dtype="float32")
  met, met_phi = np.empty((1), dtype="float32"), np.empty((1), dtype="float32")
  
  trout.Branch("mtt_truth", mtt_truth, "mtt_truth/F")
  trout.Branch("mtt_reco", mtt_reco, "mtt_reco/F")
  trout.Branch("nlep", nlep_good, "nlep/I")
  trout.Branch("lep1_pt", o_tlz_l1_pt, "lep1_pt/F")
  trout.Branch("lep1_eta", o_tlz_l1_eta, "lep1_eta/F")
  trout.Branch("lep1_phi", o_tlz_l1_phi, "lep1_phi/F")
  trout.Branch("lep1_m", o_tlz_l1_m, "lep1_m/F")
  trout.Branch("lep2_pt", o_tlz_l1_pt, "lep2_pt/F")
  trout.Branch("lep2_eta", o_tlz_l1_eta, "lep2_eta/F")
  trout.Branch("lep2_phi", o_tlz_l1_phi, "lep2_phi/F")
  trout.Branch("lep2_m", o_tlz_l1_m, "lep2_m/F")
  trout.Branch("njets", njets_good, "njets/I")
  trout.Branch("jet1_pt", o_tlz_j1_pt, "jet1_pt/F")
  trout.Branch("jet1_eta", o_tlz_j1_eta, "jet1_eta/F")
  trout.Branch("jet1_phi", o_tlz_j1_phi, "jet1_phi/F")
  trout.Branch("jet1_m", o_tlz_j1_m, "jet1_m/F")
  trout.Branch("jet2_pt", o_tlz_j2_pt, "jet2_pt/F")
  trout.Branch("jet2_eta", o_tlz_j2_eta, "jet2_eta/F")
  trout.Branch("jet2_phi", o_tlz_j2_phi, "jet2_phi/F")
  trout.Branch("jet2_m", o_tlz_j2_m, "jet2_m/F")
  trout.Branch("jet3_pt", o_tlz_j3_pt, "jet3_pt/F")
  trout.Branch("jet3_eta", o_tlz_j3_eta, "jet3_eta/F")
  trout.Branch("jet3_phi", o_tlz_j3_phi, "jet3_phi/F")
  trout.Branch("jet3_m", o_tlz_j3_m, "jet3_m/F")
  trout.Branch("met", met, "met/F")
  trout.Branch("met_phi", met_phi, "met_phi/F")

  nevents = tr.GetEntries()
  tr.SetBranchStatus("*",1) #
  print("Nevents= ", nevents)

  for i in range(nevents):
    tr.GetEntry(i)

    l_wt=[]
    l_tlz_t = []

    # Event weights
    # ===========
    EntryFromBranch= tr.Event.GetEntries()
    for j in range(EntryFromBranch):
      wt=tr.GetLeaf("Event.Weight").GetValue(j)
      l_wt.append(wt)

    # Truth particles
    # ===========
    EntryFromBranch= tr.Particle.GetEntries()
    for j in range(EntryFromBranch):
      PID=tr.GetLeaf("Particle.PID").GetValue(j)
      if fabs(PID)==6:
        d1=tr.GetLeaf("Particle.D1").GetValue(j) 
        d2=tr.GetLeaf("Particle.D2").GetValue(j) 
        pd1=tr.GetLeaf("Particle.PID").GetValue(int(d1))
        pd2=tr.GetLeaf("Particle.PID").GetValue(int(d2))
        # Find the last top-quarks in the chain 
        if(fabs(pd1)==24 and fabs(pd2)==5) or (fabs(pd2)==24 and fabs(pd1)==5):
          tlz_t = R.TLorentzVector()
          Px=tr.GetLeaf("Particle.Px").GetValue(j)
          Py=tr.GetLeaf("Particle.Py").GetValue(j)
          Pz=tr.GetLeaf("Particle.Pz").GetValue(j)
          E=tr.GetLeaf("Particle.E").GetValue(j)
          tlz_t.SetPxPyPzE(Px, Py, Pz, E)
          l_tlz_t.append(tlz_t)

    # Particle level variables
    # ===========
    # Electrons
    EntryFromBranch= tr.Electron.GetEntries()
    l_tlz_el=[]
    pt_max_el1, j_el1 = 0, -1
    pt_max_el2, j_el2 = 0, -1
    for j in range(EntryFromBranch):
      pt=tr.GetLeaf("Electron.PT").GetValue(j)
      if pt > pt_max_el1:
        pt_max_el2 = pt_max_el1
        j_el2 = j_el1

        pt_max_el1 = pt
        j_el1 = j
      else:
        if pt > pt_max_el2:
          pt_max_el2 = pt
          j_el2 = j
    # Leading ones
    if j_el1 >=0:
      pt=tr.GetLeaf("Electron.PT").GetValue(j_el1)
      eta=tr.GetLeaf("Electron.Eta").GetValue(j_el1)
      phi=tr.GetLeaf("Electron.Phi").GetValue(j_el1)
      m=0.511E-3
      tlz_l = R.TLorentzVector()
      tlz_l.SetPtEtaPhiM(pt, eta, phi, m)
      l_tlz_el.append(tlz_l)
    if j_el2 >=0:
      pt=tr.GetLeaf("Electron.PT").GetValue(j_el2)
      eta=tr.GetLeaf("Electron.Eta").GetValue(j_el2)
      phi=tr.GetLeaf("Electron.Phi").GetValue(j_el2)
      m=0.511E-3
      tlz_l = R.TLorentzVector()
      tlz_l.SetPtEtaPhiM(pt, eta, phi, m)
      l_tlz_el.append(tlz_l)
      
    # Muons
    EntryFromBranch= tr.Muon.GetEntries()
    l_tlz_mu=[]
    pt_max_mu1, j_mu1 = 0, -1
    pt_max_mu2, j_mu2 = 0, -1
    for j in range(EntryFromBranch):
      pt=tr.GetLeaf("Muon.PT").GetValue(j)
      if pt > pt_max_mu1:
        pt_max_mu2 = pt_max_mu1
        j_mu2 = j_mu1

        pt_max_mu1 = pt
        j_mu1 = j
      else:
        if pt > pt_max_mu2:
          pt_max_mu2 = pt
          j_mu2 = j
    # Leading ones
    if j_mu1 >=0:
      pt=tr.GetLeaf("Muon.PT").GetValue(j_mu1)
      eta=tr.GetLeaf("Muon.Eta").GetValue(j_mu1)
      phi=tr.GetLeaf("Muon.Phi").GetValue(j_mu1)
      m=0.1057
      tlz_l = R.TLorentzVector()
      tlz_l.SetPtEtaPhiM(pt, eta, phi, m)
      l_tlz_mu.append(tlz_l)
    if j_mu2 >=0:
      pt=tr.GetLeaf("Muon.PT").GetValue(j_mu2)
      eta=tr.GetLeaf("Muon.Eta").GetValue(j_mu2)
      phi=tr.GetLeaf("Muon.Phi").GetValue(j_mu2)
      m=0.1057
      tlz_l = R.TLorentzVector()
      tlz_l.SetPtEtaPhiM(pt, eta, phi, m)
      l_tlz_mu.append(tlz_l)
      
    print("pt_max_el1: {0}, pt_max_el2: {1}, pt_max_mu1: {2}, pt_max_mu2: {3}".format(pt_max_el1, pt_max_el2, pt_max_mu1, pt_max_mu2))
    # Leptons
    l_tlz_lep = []
    # Order by pt
    dict_lep = {"El1": [pt_max_el1, j_el1], "El2": [pt_max_el2, j_el2],
                "Mu1": [pt_max_mu1, j_mu1], "Mu2": [pt_max_mu2, j_mu2],}
    dict_lep_sorted = sorted(dict_lep.items(), key=lambda x: x[1][0], reverse=True)  
    # Select leading ele/muons
    nel, nmu=0, 0
    for il in range(2):
     if dict_lep_sorted[il][0]=="El1" and pt_max_el1>0:
       l_tlz_lep.append(l_tlz_el[0])
       nel += 1
     if dict_lep_sorted[il][0]=="El2" and pt_max_el2>0:
       l_tlz_lep.append(l_tlz_el[1])
       nel += 1
     if dict_lep_sorted[il][0]=="Mu1" and pt_max_mu1>0:
       l_tlz_lep.append(l_tlz_mu[0])
       nmu += 1
     if dict_lep_sorted[il][0]=="Mu2" and pt_max_mu2>0:
       l_tlz_lep.append(l_tlz_mu[1])
       nmu += 1
    nlep_good[0] = nel+nmu

    # Jets
    EntryFromBranch= tr.Jet.GetEntries()
    l_tlz_jet=[]
    dict_jets = {}
    for j in range(EntryFromBranch):
      pt=tr.GetLeaf("Jet.PT").GetValue(j)
      dict_jets[j]=pt

    # Leading ones
    dict_jets_sorted = sorted(dict_jets.items(), key=lambda x: x[1], reverse=True)  
    njet = len(dict_jets_sorted)
    njets_good[0] = 0
    if njet >=2:
      njets_good[0] = min(3, njet)
      for j in range(njets_good[0]):
        j_jet = dict_jets_sorted[j][0]
        pt=tr.GetLeaf("Jet.PT").GetValue(j_jet)
        eta=tr.GetLeaf("Jet.Eta").GetValue(j_jet)
        phi=tr.GetLeaf("Jet.Phi").GetValue(j_jet)
        m=tr.GetLeaf("Jet.Mass").GetValue(j_jet)
        tlz_j = R.TLorentzVector()
        tlz_j.SetPtEtaPhiM(pt, eta, phi, m)
        l_tlz_jet.append(tlz_j)

    # Missing ET
    EntryFromBranch= tr.MissingET.GetEntries()
    for j in range(EntryFromBranch):
      met[0]=tr.GetLeaf("MissingET.MET").GetValue(j)
      met_phi[0]=tr.GetLeaf("MissingET.Phi").GetValue(j)



    if len(l_tlz_t)==2:
      mtt_truth[0] = (l_tlz_t[0] + l_tlz_t[1]).M()
    else:
      print("ntops: ", len(l_tlz_t))

    # Fill Output tree
    if nlep_good[0]>=2 and njets_good[0]>=2:
      o_tlz_l1 = l_tlz_lep[0]
      o_tlz_l2 = l_tlz_lep[1]
      o_tlz_j1 = l_tlz_jet[0]
      o_tlz_j2 = l_tlz_jet[1]
      o_tlz_j3 = R.TLorentzVector()
      if njets_good[0]>=3:
        o_tlz_j3 = l_tlz_jet[2]

      tlz_lljj = o_tlz_l1 + o_tlz_l2+ o_tlz_j1+ o_tlz_j2
      mtt_reco[0] = tlz_lljj.M()
      print("mtt= {0}, mtt_reco= {5}, nel= {1}, nmu= {2}, njet= {3}, met= {4}".format(mtt_truth[0], nel, nmu, njet, met[0], mtt_reco[0]))

      o_tlz_l1_pt[0] = o_tlz_l1.Pt()
      o_tlz_l1_eta[0] = o_tlz_l1.Eta()
      o_tlz_l1_phi[0] = o_tlz_l1.Phi()
      o_tlz_l1_m[0] = o_tlz_l1.M()
      o_tlz_l2_pt[0] = o_tlz_l2.Pt()
      o_tlz_l2_eta[0] = o_tlz_l2.Eta()
      o_tlz_l2_phi[0] = o_tlz_l2.Phi()
      o_tlz_l2_m[0] = o_tlz_l2.M()
      o_tlz_j1_pt[0] = o_tlz_j1.Pt()
      o_tlz_j1_eta[0] = o_tlz_j1.Eta()
      o_tlz_j1_phi[0] = o_tlz_j1.Phi()
      o_tlz_j1_m[0] = o_tlz_j1.M()
      o_tlz_j2_pt[0] = o_tlz_j2.Pt()
      o_tlz_j2_eta[0] = o_tlz_j2.Eta()
      o_tlz_j2_phi[0] = o_tlz_j2.Phi()
      o_tlz_j2_m[0] = o_tlz_j2.M()
      o_tlz_j3_pt[0] = o_tlz_j3.Pt()
      o_tlz_j3_eta[0] = o_tlz_j3.Eta()
      o_tlz_j3_phi[0] = o_tlz_j3.Phi()
      o_tlz_j3_m[0] = o_tlz_j3.M()

      trout.Fill()

  tfout.cd()
  trout.Write()
  tfout.Close()
  tfin.Close()

if __name__ == "__main__":

  infile="../Gridpack/Zp1TeV_ttbar_inc_2lep_gridpack_evgen/Run_10/delphes_events.root"
  outfile="test.root"
  loop_tr(infile, outfile)
