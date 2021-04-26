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
* [HistFactory](https://cds.cern.ch/record/1456844)
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
* Step 1: Fit the mass peak, compare binned and unbinned fit results, using 20 and 500 events, respectively (four fits in total)
* Step 2: fix the mass peak and fit the signal and background yields

When the Higgs boson was discovered in 2012, there were about 20 events in the H4l channel within the mass range of 110 GeV to 160 GeV, see Fig.2 of the [ATLAS Higgs discovery paper](https://arxiv.org/abs/1207.7214). With LHC Run-2 data, there are about 500 events in this mass range, see Fig. 5 of https://arxiv.org/abs/2004.03447.


### Hypothesis test, Confidence intervals and Exclusion limits

#### Hands-on 4: [Histfactory example](Stats/hepstat_tutorial_histfactory.py.nbconvert.ipynb)

Create a [workspace](https://root.cern.ch/doc/master/classRooWorkspace.html) using [HistFactory](https://root.cern/doc/master/group__HistFactory.html). 

RooWorkspace is a persistable container for RooFit projects.
It can contain and own variables, p.d.f.s, functions and datasets. The entire RooWorkspace can be saved into a ROOT TFile and organises the consistent streaming of its contents without duplication.

`HistFactory` is a package that creates a RooFit probability density function from ROOT histograms of expected distributions and histograms that represent the +/- 1 sigma variations from systematic effects. The resulting probability density function, or a `RooWorkspace`, can then be used with any of the statistical tools provided within RooStats, such as the profile likelihood ratio, Feldman-Cousins, etc.

In this tutorial, the model is basically the same as [hepstat_tutorial_roofit_extended.py](https://gitee.com/lailinxu/hepstat-tutorial/blob/master/Fitting/hepstat_tutorial_roofit_extended.py.nbconvert.ipynb): i.e, composite p.d.f with signal and background component
```
pdf = n_bkg * bkg(x,a0,a1) + mu * n_sig * (f_sig1 * sig1(x,m,s1 + (1-f_sig1) * sig2(x,m,s2)))
```
 and our goals are the following:
 * Create a workspace using Workspace Factory
 * Example operations at the workspace level

#### Hands-on 5: [Build a workspace using histograms](Stats/hepstat_tutorial_histfactory_hists.py.nbconvert.ipynb)

In the above example ([Histfactory example](Stats/hepstat_tutorial_histfactory.py.nbconvert.ipynb)), a workspace is built using parametrized functions.  In reality, non-parametrized PDFs are more often being used, for example, from Monte Carlo simulations. In this example, we build a workspace using histograms, and we also show you how to include systematic uncertainties in the likelihood model. Our objectives are:
  * Create a workspace using histograms
  * Include systematic uncertainties

#### Hands-on 6: [Null hypothesis significance test](Stats/hepstat_tutorial_hypo_p0.py.nbconvert.ipynb)

`RooStats` example: compute the p0 and significance (Hypothesis Test) 
The signal is a simple Gaussian and the background is a smoothly falling spectrum. To estimate the significance,
we need to perform an hypothesis test. We want to disprove the null model, i.e the background only model against the alternate model,
the background plus the signal. In RooStats, we do this by defining two two ModelConfig objects, one for the null model
(the background only model in this case) and one for the alternate model (the signal plus background).

Objectives of this tutorial are the following:
 * Compute the null hypo significance using the Asymptotic calculator
 * Compute the significance by hand using the asymptotic formula
 * Compute the significance using frequentist method

#### Hands-on 7: [CLs upper limits](Stats/hepstat_tutorial_hypo_cls.py.nbconvert.ipynb)

Use the [StandardHypoTestInvDemo](https://root.cern/doc/master/StandardHypoTestInvDemo_8C.html) tutorial macro to perform an inverted hypothesis test for computing an interval (one-sided upper limits). This macro will perform a scan of the p-values for computing the upper limit. Both asymptotic and frequentist methos will be shown.

Objectives of this tutorial are the following:
* Create the HypoTestInverter class and configure it
* Compute the CLs upper limits using the asymptotic formula
* Compute the CLs upper limits using the frequentist method (time consuming)

#### Homework (Optional)
Use the workspaces created from [Build a workspace using histograms](Stats/hepstat_tutorial_histfactory_hists.py.nbconvert.ipynb):
 * Plot the p0 scan as a function of the signal mass
 * Plot the CLs upper limits as a function of the signal mass

### Machine learning: TMVA

#### Hands-on: Regression with BDT

 * [Training of BDT regression](MVA/TMVA_tutorial_regression_tmva.py.nbconvert.ipynb)
 * [Testing/validation](MVA/TMVA_tutorial_regression_tmva_test.py.nbconvert.ipynb)
 * [Application](MVA/TMVA_tutorial_regression_tmva_app.py.nbconvert.ipynb)

#### Hands-on: Classification with BDT

 * [Training of BDT classification](MVA/TMVA_tutorial_classification_tmva.py.ipynb)
 * [Testing/validation](MVA/TMVA_tutorial_classification_tmva_test.py.nbconvert.ipynb)
 * [Application](MVA/TMVA_tutorial_classification_tmva_app.py.nbconvert.ipynb)


### Machine learning: Artificial Neural Networks with PyTorch

Before you start this toturial, follow the instruction [here](README_pytorch.md) to set up the [PyTorch](https://pytorch.org/) docker environment.

#### Hands-on: Regression with ANN

 * [Regression](MVA/DNN_example.ipynb)

#### Hands-on: Classification with ANN

 * [Classification](MVA/DNN_example.ipynb)
