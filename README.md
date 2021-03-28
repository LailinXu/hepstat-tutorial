# Tutorials for HEP data analysis

## References

### Statistics and data analysis
* [Statistics in Theory](https://indico.cern.ch/event/112319/session/1/contribution/41/material/slides/0.pdf) - a lecture by Bob Cousins
* [Statistical methods in LHC data analysis](http://indico.cern.ch/event/73545/) - Luca Lista

### ROOT and RooFit
* ROOT Tutorials, 2015, https://twiki.cern.ch/twiki/bin/view/Main/ROOTRioTutorial 
* [RooFit reference slides](http://indico.in2p3.fr/materialDisplay.py?contribId=15&materialId=slides&confId=750) - by Wouter Verkerke, one of RooFit authors
* [RooFit tutorials](http://root.cern.ch/root/html/tutorials/roofit/index.html) - a set of working macros that showcase all major features of RooFit
* [RooStats Manual](https://twiki.cern.ch/twiki/pub/RooStats/WebHome/RooStats_UsersGuide.pdf) - concise, contains clear summary of statistics concepts and definitions
* [RooStats tutorial](http://indico.cern.ch/getFile.py/access?contribId=0&sessionId=1&resId=0&materialId=slides&confId=118720) - by Kyle Cranmer, one of the RooStats developers
* [RooStats tutorials](http://root.cern.ch/root/html/tutorials/roostats/index.html) - a set of working macros that showcase all major features of RooStats

### Schools
* INFN School Of Statistics, [2019](https://agenda.infn.it/event/16360/)
* IN2P3 School Of Statistics, [2021](https://indico.in2p3.fr/event/20220/timetable/)

## Jupyter Notebook

### Jupyter

Installation
```
pip3 install jupyter
```

### Convert `C` marcos or `pyroot` macros to notebooks

Here is a script [converttonotebook.py](https://github.com/root-project/root/blob/master/documentation/doxygen/converttonotebook.py) used to convert ROOT official tutorial codes to notebooks.

But it requires some header lines at the beginning of the macros:
```
/// \file
/// \ingroup tutorial_fit
/// \notebook
/// Simple fitting example (1-d histogram with an interpreted function)
///
/// \macro_image
/// \macro_output
/// \macro_code
///
/// \author XXX
```
or for pyroot
```
## \file
## \ingroup tutorial_pyroot
## \notebook
## Fit example.
##
## \macro_image
## \macro_output
## \macro_code
##
## \author XXX
```


