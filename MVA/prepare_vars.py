#!/usr/bin/env python

import ROOT as R
from math import fabs

def loop_tr(infile=""):

  tfin=R.TFile(infile, "READ")
  tname="Delphes"
  tr=tfin.Get(tname)

  brs=[
  ]

  nevents = tr.GetEntries()
  tr.SetBranchStatus("*",1) #
  print("Nevents= ", nevents)

  for i in range(nevents):
    tr.GetEntry(i)

    l_wt=[]
    l_tlz_t = []

    # truth particles
    EntryFromBranch= tr.Event.GetEntries()
    for j in range(EntryFromBranch):
      wt=tr.GetLeaf("Event.Weight").GetValue(j)
      l_wt.append(wt)

    # truth particles
    EntryFromBranch= tr.Particle.GetEntries()
    for j in range(EntryFromBranch):
      PID=tr.GetLeaf("Particle.PID").GetValue(j)
      if fabs(PID)==6:
        d1=tr.GetLeaf("Particle.D1").GetValue(j) 
        d2=tr.GetLeaf("Particle.D2").GetValue(j) 
        pd1=tr.GetLeaf("Particle.PID").GetValue(int(d1))
        pd2=tr.GetLeaf("Particle.PID").GetValue(int(d2))
  
        if(fabs(pd1)==24 and fabs(pd2)==5) or (fabs(pd2)==24 and fabs(pd1)==5):
          tlz_t = R.TLorentzVector()
          Px=tr.GetLeaf("Particle.Px").GetValue(j)
          Py=tr.GetLeaf("Particle.Py").GetValue(j)
          Pz=tr.GetLeaf("Particle.Pz").GetValue(j)
          E=tr.GetLeaf("Particle.E").GetValue(j)
          tlz_t.SetPxPyPzE(Px, Py, Pz, E)
          l_tlz_t.append(tlz_t)

    """
    print(tr.Particle.Mass[0])
    np = len(tr.Particle.Mass)
    for jp in range(np):
      # Top-quraks
      if fabs(tr.Particle.PID[jp])== 6:
        d1 = tr.Particle.D1[jp]
        d2 = tr.Particle.D2[jp]
        if (fabs(tr.Particle.PID[d1]) == 24 and fabs(tr.Particle.PID[d2]) == 5) or (fabs(tr.Particle.PID[d2]) == 24 and fabs(tr.Particle.PID[d1]) == 5):
          tlz_t = R.TLorentzVector()
          tlz_t.SetPxPyPzE(tr.Particle.Px[jp], tr.Particle.Py[jp], tr.Particle.Pz[jp], tr.Particle.E[jp])
          l_tlz_t.append(tlz_t)
    """

    if len(l_tlz_t)==2:
      mtt = (l_tlz_t[0] + l_tlz_t[1]).M()
      print("mtt= {0}".format(mtt))
    else:
      print("ntops: ", len(l_tlz_t))


  tfin.Close()

if __name__ == "__main__":

  infile="../Gridpack/Zp1TeV_ttbar_inc_2lep_gridpack_evgen/Run_10/delphes_events.root"
  loop_tr(infile)
