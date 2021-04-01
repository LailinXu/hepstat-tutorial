# Tutorials for HEP data analysis

## References

### Statistics and data analysis
* [Statistics in Theory](https://indico.cern.ch/event/112319/session/1/contribution/41/material/slides/0.pdf) - a lecture by Bob Cousins
* [Statistical methods in LHC data analysis](http://indico.cern.ch/event/73545/) - Luca Lista

### ROOT and RooFit
* ROOT [Users Guides](https://root.cern/root/htmldoc/guides/users-guide/ROOTUsersGuide.html)
* ROOT Tutorials, 2015, https://twiki.cern.ch/twiki/bin/view/Main/ROOTRioTutorial 
* [RooFit reference slides](http://indico.in2p3.fr/materialDisplay.py?contribId=15&materialId=slides&confId=750) - by Wouter Verkerke, one of RooFit authors
* [RooFit tutorials](http://root.cern.ch/root/html/tutorials/roofit/index.html) - a set of working macros that showcase all major features of RooFit
* [RooStats Manual](https://twiki.cern.ch/twiki/pub/RooStats/WebHome/RooStats_UsersGuide.pdf) - concise, contains clear summary of statistics concepts and definitions
* [RooStats tutorial](http://indico.cern.ch/getFile.py/access?contribId=0&sessionId=1&resId=0&materialId=slides&confId=118720) - by Kyle Cranmer, one of the RooStats developers
* [RooStats tutorials](http://root.cern.ch/root/html/tutorials/roostats/index.html) - a set of working macros that showcase all major features of RooStats

### Schools
* INFN School Of Statistics, [2019](https://agenda.infn.it/event/16360/)
* IN2P3 School Of Statistics, [2021](https://indico.in2p3.fr/event/20220/timetable/)


## Preparation of the tutorials

You need `ROOT` (v6.22 or newer) and `python` installed for tutorials here. If you don't have them available, either from your local computer or a linux server, follow the instructions [here](README_pyroot.md) to install the `root` docker container.

The Jupyter setup is optional and if you are interested, you can find some intruction [here](README_jupyter.md) to set it up, or the docker setup in [the above instruction](README_pyroot.md#installation-of-jupyter_pyroot).

## Tutorials

### Parameter fitting in ROOT/RooFit

#### Hands-on 1: [Basic fitting](Fitting/hepstat_tutorial_fit.py.nbconvert.ipynb)

Fit example with `ROOT`, with following objectives:
 * Fit a histogram with a linear chi-squre fit, and compare results with by-hand calculations
 * Different fiting options
 * Compare chi-squre fit and likelihood fit

#### Hands-on 2: [Fitting with RooFit](Fitting/hepstat_tutorial_roofit.py.nbconvert.ipynb)

Fit examples with `RooFit`, composite p.d.f with signal and background component
```
pdf = f_bkg * bkg(x,a0,a1) + (1-fbkg) * (f_sig1 * sig1(x,m,s1 + (1-f_sig1) * sig2(x,m,s2)))
```
 with following objectives:
 * Construct a simple fit in RooFit and plot the NLL
 * Compare binned and unbinned fit results
 * Compare un-extended and extended likelihoof it

#### Hands-on 3: [Advanced fitting with RooFit](Fitting/hepstat_tutorial_roofit_extended.py.nbconvert.ipynb)

A bit advanced fit examples with `RooFit`, composite p.d.f with signal and background component, extended
```
pdf = n_bkg * bkg(x,a0,a1) + n_sig * (f_sig1 * sig1(x,m,s1 + (1-f_sig1) * sig2(x,m,s2)))
```
or using a signal strength
```
pdf = n_bkg * bkg(x,a0,a1) + mu * n_sig * (f_sig1 * sig1(x,m,s1 + (1-f_sig1) * sig2(x,m,s2)))
```
 with following objectives:
 * Compare plain likelihood fit and profile likelihood fit
 * Fit with nuisance parameters with constraints


#### Homework

Fit the Higgs peak in ATLAS H4l open "data": http://opendata.cern.ch/record/3823, MC: `gg->H->ZZ->4l` with mH = 125 GeV, for 2016 ATLAS open data release.
The (Monte Carlo) data is a Ttree with lepton four-vector informaiton available. Reconstruct the invariant mass of the four-lepton final state. An example code to process the TTree can be found [here](Fitting/h4l_ana_example.py). 

Tips and requirements:
* Construct a `S+B` model: S: signal, Gaussian, B: background, polynomial
* Restrict to the mass range of 110 GeV to 160 GeV
* Step 1: Fit the mass peak, compare binned and unbinned fit results
* Step 2: fix the mass peak and fit the signal and background yields



### Hypothesis test, Confidence intervals and Exclusion limits

To be added.
