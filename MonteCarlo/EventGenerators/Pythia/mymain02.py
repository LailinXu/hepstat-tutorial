# main01.py is a part of the PYTHIA event generator.
# Copyright (C) 2019 Torbjorn Sjostrand.
# PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.

# Keywords: basic usage; charged multiplicity; python;

# This is a simple test program. It fits on one slide in a talk.  It
# studies the charged multiplicity distribution at the LHC.

# Modified by Matthew Feickert to be Python3 compliant and location independent

# Import the Pythia module
import pythia8

pythia = pythia8.Pythia()

# Process
## Higgs production
pythia.readString("HiggsSM:gg2H = on")
## Higgs decay
pythia.readString("25:onMode = off")
pythia.readString("25:onIfMatch = 22 22")
# Beam setup
## energy
pythia.readString("Beams:eCM = 13000")
## beam types:
"""
The PDG id code for the first incoming particle. Allowed codes include
2212 = p, -2212 = pbar,
2112 = n, -2112 = nbar,
211 = pi^+, -211 = pi^-, 111 = pi^0,
990 = Pomeron (used in diffractive machinery; here mainly for debug purposes),
22 = gamma (for gamma-gamma and gamma-hadron interactions, more info here),
11 = e^-, -11 = e^+,
13 = mu^-, -13 = mu^+,
and a few more leptons/neutrinos in a few combinations.
"""
pythia.readString("Beams:idA = 2212")
pythia.readString("Beams:idB = 2212")
# Phase space cuts
pythia.readString("PhaseSpace:mHatMin = 2.")
pythia.init()
# Histograms
h_m = pythia8.Hist( "Higgs mass spectrum", 100, 120., 130.) 
h_myy = pythia8.Hist( "gamgam mass spectrum", 100, 120., 130.) 
y1_pt = pythia8.Hist( "gam pt spectrum", 500, 0., 100.) 
# Begin event loop. Generate event. Skip if error. List first one.
for iEvent in range(0, 100):
    if not pythia.next():
        continue
    # Find number of all final charged particles and fill histogram.
    print("Evnet", iEvent)
    pty1=0
    pty2=0
    fvy1 = pythia8.Vec4()
    fvy2 = pythia8.Vec4()
    fvyy = pythia8.Vec4()
    for prt in pythia.event:
        if prt.statusAbs()==62 and prt.id()==25:
          print("Higgs mass", prt.m())
          h_m.fill(prt.m())
        if prt.isFinal() and prt.id()==22:
          if prt.pT() > pty1:
            pty1 = prt.pT()
            fvy1.px(prt.px())
            fvy1.py(prt.py())
            fvy1.pz(prt.pz())
            fvy1.e(prt.e())
          elif prt.pT() > pty2:
            pty2 = prt.pT()
            fvy2.px(prt.px())
            fvy2.py(prt.py())
            fvy2.pz(prt.pz())
            fvy2.e(prt.e())
    print("leading photon pt", pty1)
    y1_pt.fill(pty1)
    fvyy = fvy1 + fvy2
    h_myy.fill(fvyy.mCalc())
# End of event loop. Statistics. Histogram. Done.
pythia.stat()
print(h_m)
# Matplotlib output format
hpl = pythia8.HistPlot("hists_ggH")
hpl.frame( "h_m", "Higgs mass", "m_H [GeV]", "sigma")
hpl.add(h_m, '-')
hpl.plot()
hpl.frame( "h_myy", "DiPhoton mass", "m_yy [GeV]", "sigma")
hpl.add(h_myy, '-')
hpl.plot()
hpl.frame( "y1_pt", "Leading photon pt", "p_{y}^{T} [GeV]", "sigma")
hpl.add(y1_pt, '-')
hpl.plot()
