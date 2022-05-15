# Quick tutorials on MadGraph5_aMC@NLO

## Introduction

From its [official website](https://launchpad.net/mg5amcnlo): 
```
MadGraph5_aMC@NLO is a framework that aims at providing all the elements necessary for SM and BSM phenomenology, such as the computations of cross sections, the generation of hard events and their matching with event generators, and the use of a variety of tools relevant to event manipulation and analysis. Processes can be simulated to LO accuracy for any user-defined Lagrangian, an the NLO accuracy in the case of models that support this kind of calculations -- prominent among these are QCD and EW corrections to SM processes. Matrix elements at the tree- and one-loop-level can also be obtained.
```

## Useful resources

This tutorial has multiple sections:
From the [MadGraph Tutorial](https://gitlab.com/hepcedar/mcnet-schools/beijing-2021/-/tree/master/madgraph) of the [Beijing 2021 MCnet school](https://indico.ihep.ac.cn/event/11202/):

* [installation/basic command](https://gitlab.com/hepcedar/mcnet-schools/beijing-2021/-/tree/master/madgraph/installation)

* Learning MG5aMC: https://cp3.irmp.ucl.ac.be/projects/madgraph/attachment/wiki/Milan/Milan_tuto_I.2.pdf

* Loop-Induced: https://cp3.irmp.ucl.ac.be/projects/madgraph/attachment/wiki/Milan/Milan_tuto_loop.pdf

* NLO: https://cp3.irmp.ucl.ac.be/projects/madgraph/attachment/wiki/Milan/tutorial-unimi-2019-NLO.pdf

* Merging: https://cp3.irmp.ucl.ac.be/projects/madgraph/attachment/wiki/Milan/Milan_tuto_merging.pdf

If additional theory information are required please check:
https://cp3.irmp.ucl.ac.be/projects/madgraph/wiki/Milan

## Download and Installation

### Local installation

MadGraph5_aMC@NLO needs Python version 2.7 or 3.7 (or higher) ; gfortran/gcc 4.6 or higher is required for NLO calculations/simulations.

* Downlad MadGraph5_aMC@NLO from the website https://launchpad.net/mg5amcnlo, and pick the latest version

* unpack the directory: `tar -xzpvf MG5_aMC_vX.Y.Z.tar.gz`

* *no compilation is needed*

### Docker
Here is a nice Mg5_aMC docker setup at Github: https://github.com/scailfin/MadGraph5_aMC-NLO
It also contains many useful third-party pacages.

The Docker image contains:
* [MadGraph5_aMC@NLO](https://launchpad.net/mg5amcnlo) `v3.3.2`
* Python 3.9
* [HepMC2](http://hepmc.web.cern.ch/hepmc/) `v2.06.11`
* [LHAPDF](https://lhapdf.hepforge.org/) `v6.3.0`
* [FastJet](http://fastjet.fr/) `v3.3.4`
* [PYTHIA](http://home.thep.lu.se/~torbjorn/Pythia.html) `v8.244`
* [BOOST](https://www.boost.org/doc/libs/1_76_0/more/getting_started/unix-variants.html) `v1.76.0`

#### Installation

```
docker pull scailfin/madgraph5-amc-nlo:mg5_amc3.3.2
```

## First run of MG5_aMC

Mg5_aMC can be executed interactively (where you need to type commands and settings one by one and step by step) or in [batch mode](https://answers.launchpad.net/mg5amcnlo/+faq/2186) (where you can put all commands and settings in a plain txt file).
See MG5 tutorials for the syntax.

All FAQs here: https://answers.launchpad.net/mg5amcnlo/+faqs

### For local installation

* launch the executable `./bin/mg5_aMC`

* type `tutorial` and follow instruction

### For docker usage

* In commandline: `docker run --rm scailfin/madgraph5-amc-nlo:mg5_amc3.4.0 "mg5_aMC --help"`, this would print out help messages

* Interative mode: `docker run --rm -it -v $PWD/mg5:/work -w /work  scailfin/madgraph5-amc-nlo:mg5_amc3.3.2`, once you enter the commandline, type `mg5_amc`:

```
root@793a53c8e964:/work# mg5_aMC
************************************************************
*                                                          *
*                     W E L C O M E to                     *
*              M A D G R A P H 5 _ a M C @ N L O           *
*                                                          *
*                                                          *
*                 *                       *                *
*                   *        * *        *                  *
*                     * * * * 5 * * * *                    *
*                   *        * *        *                  *
*                 *                       *                *
*                                                          *
*         VERSION 3.3.2                 2022-03-18         *
*                                                          *
*    The MadGraph5_aMC@NLO Development Team - Find us at   *
*    https://server06.fynu.ucl.ac.be/projects/madgraph     *
*                            and                           *
*            http://amcatnlo.web.cern.ch/amcatnlo/         *
*                                                          *
*               Type 'help' for in-line help.              *
*           Type 'tutorial' to learn how MG5 works         *
*    Type 'tutorial aMCatNLO' to learn how aMC@NLO works   *
*    Type 'tutorial MadLoop' to learn how MadLoop works    *
*                                                          *
************************************************************
load MG5 configuration from ../usr/local/venv/MG5_aMC/input/mg5_configuration.txt 
set fastjet to fastjet-config
set ninja to /usr/local/venv/MG5_aMC/HEPTools/lib
set collier to /usr/local/venv/MG5_aMC/HEPTools/lib
set lhapdf to lhapdf-config
set lhapdf to lhapdf-config
Using default text editor "vi". Set another one in ./input/mg5_configuration.txt
No valid web browser found. Please set in ./input/mg5_configuration.txt
Loading default model: sm
INFO: Restrict model sm with file ../usr/local/venv/MG5_aMC/models/sm/restrict_default.dat . 
INFO: Run "set stdout_level DEBUG" before import for more information. 
INFO: Change particles name to pass to MG5 convention 
Defined multiparticle p = g u c d s u~ c~ d~ s~
Defined multiparticle j = g u c d s u~ c~ d~ s~
Defined multiparticle l+ = e+ mu+
Defined multiparticle l- = e- mu-
Defined multiparticle vl = ve vm vt
Defined multiparticle vl~ = ve~ vm~ vt~
Defined multiparticle all = g u c d s u~ c~ d~ s~ a ve vm vt e- mu- ve~ vm~ vt~ e+ mu+ t b t~ b~ z w+ h w- ta- ta+
MG5_aMC>
```

### Third-party packages

Some third-party packages can be installed using the MG5_aMC shell command `install`.


### Tutorials
#### $e^{0}e^{+} \to ZH$
#### $ gg \to H$ 
