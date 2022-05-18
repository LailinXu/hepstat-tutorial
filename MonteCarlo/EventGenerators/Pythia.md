# Tutorial on Pythia

## Introduction

From its [official website](https://pythia.org/):
> PYTHIA is a program for the generation of high-energy physics collision events, i.e. for the description of collisions at high energies between electrons, protons, photons
> and heavy nuclei. It contains theory and models for a number of physics aspects, including hard and soft interactions, parton distributions, initial- and final-state
> parton showers, multiparton interactions, fragmentation and decay. It is largely based on original research, but also borrows many formulae and other knowledge from the
> literature. As such it is categorized as a general purpose Monte Carlo event generator.


This tutorial has the following objectives:
* Basic usage of Pythia
* Use Pythia to generate MC events
* Use Pythia to do parton shower

## Useful resources

Many tutorials can be found online, with a few examples below:
* Pythia tutorial given at the [MC4BSM workshop at DESY 2013](http://www.phys.ufl.edu/~matchev/mc4bsm6/): https://indico.desy.de/event/7142/contributions/81399/attachments/54392/66223/pythia_tutorial.pdf, and a local copy [here](Pythia/pythia_tutorial.pdf)
* Pythia official [online manual](https://pythia.org/latest-manual/Welcome.html)

## Download and Installation

### Local installation

See the instruction in the official website
> Download and install PYTHIA 8.307

> To get going with the program, do the following (on a Linux or Mac OS X system):

> Download the file [pythia8307.tgz](https://pythia.org/download/pythia83/pythia8307.tgz) to a suitable location.

> Unzip and expand it with `tar xvfz pythia8307.tgz`.

> Move to the thus created `pythia8307` directory.

> Read the `README` file in it for installation instructions, and apply them. (If you are not going to link any external libraries, or have any other special demands, you only need to type make.)

> Move to the `examples` subdirectory and read the `README` file there for instructions how to do some test runs. (Again, if you do not link to external libraries, you only need to type `make mainNN` followed by `./mainNN > mainNN.log`, where `NN` is a two-digit number in the range 01 - 30.)

### Docker
As mentioned in the [MadGraph tutorial](MadGraph.md), the Mg5_aMC docker setup at Github: https://github.com/scailfin/MadGraph5_aMC-NLO already has Pythia included. One just needs to use the same Docker image for this tutorial

## First run of Pythia

For user applications, a steering macro (either in `C++` or `Python`) should be used. For a first run, here is a quick example: [mymain01.cc](Pythia/mymain01.cc) and [mymain01.py](Pythia/mymain01.py). The macro is used to generate charmonium states from $pp$ collisions at 8 TeV, and 100 events would be generated. A simple histogram is filled to plot the number of charged particles for all events.

### How to run

* Python
```
docker run --rm -it -v $PWD/mg5:/work -w /work  scailfin/madgraph5-amc-nlo:mg5_amc3.3.2  -c "python mymain01.py > main01_out_py.txt"
```

* C++

The code needs to be compiled first.
```
docker run --rm -it -v $PWD/pythia:/work -w /work  scailfin/madgraph5-amc-nlo:mg5_amc3.3.2  -c "g++ mymain01.cc -o mymain01 -I/usr/local/venv/include  -L/usr/local/venv/lib -lpythia8 -L -lboost_iostreams -L./ -lz -ldl; ./mymain01 > out_mymain01.txt"
```

### Walkthrough of the code
1. Initialization

```
#include "Pythia8/Pythia.h"
using namespace Pythia8;
  // Generator. Process selection. LHC initialization. Histogram.
  Pythia pythia;
```
2. Beam and process setup
```
  pythia.readString("Beams:eCM = 8000.");
  pythia.readString("HardQCD:all = on");
```
The default beam is proton beam. One can use different beams:
```
The PDG id code for the first incoming particle. Allowed codes include
2212 = p, -2212 = pbar,
2112 = n, -2112 = nbar,
211 = pi^+, -211 = pi^-, 111 = pi^0,
990 = Pomeron (used in diffractive machinery; here mainly for debug purposes),
22 = gamma (for gamma-gamma and gamma-hadron interactions, more info here),
11 = e^-, -11 = e^+,
13 = mu^-, -13 = mu^+,
and a few more leptons/neutrinos in a few combinations.
```

3. Phase space cuts (optional)
```
  pythia.readString("PhaseSpace:pTHatMin = 20.");
```

4. Initialize Pythia
  pythia.init();

During the event generation prcess, from the print out you would see the following listing about the beam and process setup:
```
 --------  PYTHIA Info Listing  ---------------------------------------- 
 
 Beam A: id =   2212, pz =  6.500e+03, e =  6.500e+03, m =  9.383e-01.
 Beam B: id =   2212, pz = -6.500e+03, e =  6.500e+03, m =  9.383e-01.

 In 1: id =   21, x =  1.496e-03, pdf =  2.827e+01 at Q2 =  1.562e+04.
 In 2: id =   21, x =  6.181e-02, pdf =  1.547e+00 at same Q2.

 Subprocess g g -> H (SM) with code 902 is 2 -> 1.
 It has sHat =  1.562e+04.
     alphaEM =  7.846e-03,  alphaS =  1.238e-01    at Q2 =  1.562e+04.

 Impact parameter b =  8.872e-01 gives enhancement factor =  9.001e-01.
 Max pT scale for MPI =  1.300e+04, ISR =  1.300e+04, FSR =  1.300e+04.
 Number of MPI =     2, ISR =     7, FSRproc =    29, FSRreson =     0.

 --------  End PYTHIA Info Listing  ------------------------------------
```

5. Book histograms (optional)
```
  Hist mult("charged multiplicity", 100, -0.5, 799.5);
```

6. Event loop
```
  // Begin event loop. Generate event. Skip if error. List first one.
  for (int iEvent = 0; iEvent < 100; ++iEvent) {
    if (!pythia.next()) continue;
```

During the run you may receive problem messages. These come in three kinds:
* a *warning* is a minor problem that is automatically fixed by the program, at least
approximately;
* an *error* is a bigger problem, that is normally still automatically fixed by the program,
by backing up and trying again;
* an *abort* is such a major problem that the current event could not be completed; in
such a rare case `pythia.next()` is false and the event should be skipped.

7. Loop particles in each event
```
    for (int i = 0; i < pythia.event.size(); ++i)
      if (pythia.event[i].isFinal() && pythia.event[i].isCharged())
```
These lines hence illustrate both how to loop over the particles in the event record and how
to access their properties. See the [online manual](https://pythia.org/latest-manual/Welcome.html) for more details about [particle properties](https://pythia.org/latest-manual/ParticleProperties.html#section3).

Thus `event[i]` is the i’th particle of the current event, and you may study its properties by using various `event[i].method()` possibilities.
During the event generation prcess, from the print out you would see the following listing:
```
 --------  PYTHIA Event Listing  (hard process)  -----------------------------------------------------------------------------------
 
    no         id  name            status     mothers   daughters     colours      p_x        p_y        p_z         e          m 
     0         90  (system)           -11     0     0     0     0     0     0      0.000      0.000      0.000  13000.000  13000.000
     1       2212  (p+)               -12     0     0     3     0     0     0      0.000      0.000   6500.000   6500.000      0.938
     2       2212  (p+)               -12     0     0     4     0     0     0      0.000      0.000  -6500.000   6500.000      0.938
     3         21  (g)                -21     1     0     5     0   101   102      0.000      0.000      9.723      9.723      0.000
     4         21  (g)                -21     2     0     5     0   102   101      0.000      0.000   -401.758    401.758      0.000
     5         25  (h0)               -22     3     4     6     7     0     0      0.000      0.000   -392.036    411.481    124.999
     6         22  gamma               23     5     0     0     0     0     0    -37.723    -11.082   -355.950    358.115      0.000
     7         22  gamma               23     5     0     0     0     0     0     37.723     11.082    -36.085     53.366      0.000
                                   Charge sum:  0.000           Momentum sum:      0.000      0.000   -392.036    411.481    124.999

 --------  End PYTHIA Event Listing  -----------------------------------------------------------------------------------------------
```
The `event.list()` listing provides the main properties of each particles, by column:
* `no`, the index number of the particle (i above);
* `id`, the PDG particle identity code (method id());
* `name`, a plaintext rendering of the particle name (method name()), within brackets for initial or intermediate particles and without for final-state ones;
* `status`, the reason why a new particle was added to the event record (method `status()`);
* `mothers` and `daughters`, documentation on the event history (methods `mother1()`, `mother2()`, `daughter1()` and `daughter2()`);
* `colours`, the colour flow of the process (methods `col()` and `acol()`);
* `p_x, p_y, p_z` and `e`, the components of the momentum four-vector (px, py, pz, E), in units of GeV with c = 1 (methods `px(), py(), pz()` and `e()`);
* `m`, the mass, in units as above (method `m()`).
For a complete description of these and other particle properites, please see the manaul.

## Tutorials

### $gg\to H$ event generation
See the Python macro [mymain02.py](Pythia/mymain02.py)

### Only parton showering
See the `C++` macro [mymain02.cc](Pythia/mymain02.cc)

```
docker run --rm -it -v $PWD/pythia:/work -w /work  scailfin/madgraph5-amc-nlo:mg5_amc3.3.2  -c "g++ mymain02.cc -o mymain02 -I/usr/local/venv/include  -L/usr/local/venv/lib -lpythia8 -L -lboost_iostreams -L./ -lz -ldl; ./mymain02 > out_mymain02.txt"
```

#### Interface to HepMC
To save the pythin event records to an output file, like HepMC.
See the `C++` macro [mymain03.cc](Pythia/mymain03.cc)
```
docker run --rm -it -v $PWD/pythia:/work -w /work  scailfin/madgraph5-amc-nlo:mg5_amc3.3.2  -c "g++ mymain03.cc -o mymain03 -I/usr/local/venv/include  -L/usr/local/venv/lib -lpythia8 -lHepMC -L -lboost_iostreams -L./ -lz -ldl; ./mymain03 > out_mymain03.txt"
```
