// main01.cc is a part of the PYTHIA event generator.
// Copyright (C) 2019 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// Keywords: basic usage; LHEF event showering


#include "Pythia8/Pythia.h"
using namespace Pythia8;
int main() {
  // Set up generation

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

  Hist mult("charged multiplicity", 100, -0.5, 799.5);
  // Begin event loop. Generate event. Skip if error. List first one.
  for (int iEvent = 0; iEvent < 100; ++iEvent) {
    if (!pythia.next()) continue;
    // Find number of all final charged particles and fill histogram.
    int nCharged = 0;
    for (int i = 0; i < pythia.event.size(); ++i)
      if (pythia.event[i].isFinal() && (abs(pythia.event[i].id())==11 || abs(pythia.event[i].id())==13) )
        ++nCharged;
    mult.fill( nCharged );
  // End of event loop. Statistics. Histogram. Done.
  }
  pythia.stat();
  cout << mult;
  return 0;
}
