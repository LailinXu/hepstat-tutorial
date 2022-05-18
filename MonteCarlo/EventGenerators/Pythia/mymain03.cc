// main01.cc is a part of the PYTHIA event generator.
// Copyright (C) 2019 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// Keywords: basic usage; LHEF event showering


#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/HepMC2.h"
using namespace Pythia8;
int main() {
  // Set up generation

  // Interface for conversion from Pythia8::Event to HepMC event.
  HepMC::Pythia8ToHepMC ToHepMC;

  // Specify file where HepMC events will be stored.
  HepMC::IO_GenEvent ascii_io("ggH_4l.hepmc", std::ios::out);

  // Declare Pythia object
  Pythia pythia;
  // Beam info in LHEF.
  pythia.readString("Beams:frameType = 4"); 
  // Input LHE file path (ggH production)
  pythia.readString("Beams:LHEF = unweighted_ggH_events.lhe.gz");
  // Let Pythia decay the Higgs boson
  pythia.readString("25:onMode = off");
  // Only turn on H->ZZ 
  pythia.readString("25:onIfMatch = 23 23");
  // Only turn on Z->ee/mm
  pythia.readString("23:onMode = off");
  pythia.readString("23:mMin = 2.0");
  pythia.readString("23:onIfMatch = 11 11");
  pythia.readString("23:onIfMatch = 13 13");
  // Initialize; incoming pp beams is default.
  pythia.init(); 

  Hist mult("charged multiplicity", 10, -0.5, 9.5);
  // Begin event loop. Generate event. Skip if error. List first one.
  for (int iEvent = 0; iEvent < 100; ++iEvent) {
    if (!pythia.next()) continue;
    // Find number of all final charged particles and fill histogram.
    int nCharged = 0;
    for (int i = 0; i < pythia.event.size(); ++i)
      if (pythia.event[i].isFinal() && (abs(pythia.event[i].id())==11 || abs(pythia.event[i].id())==13) )
        ++nCharged;
    mult.fill( nCharged );
  
    // Construct new empty HepMC event and fill it.
    // Units will be as chosen for HepMC build, but can be changed
    // by arguments, e.g. GenEvt( HepMC::Units::GEV, HepMC::Units::MM)
    HepMC::GenEvent* hepmcevt = new HepMC::GenEvent();
    ToHepMC.fill_next_event( pythia, hepmcevt );

    // Write the HepMC event to file. Done with it.
    ascii_io << hepmcevt;
    delete hepmcevt;
  // End of event loop. Statistics. Histogram. Done.
  }
  pythia.stat();
  cout << mult;

  // Plotting
  HistPlot hpl( "numlep"); 
  hpl.frame( "numlep", "number of leptons", "nL", "Events");
  hpl.add(mult);
  hpl.plot();

  return 0;
}
