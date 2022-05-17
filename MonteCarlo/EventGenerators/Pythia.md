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

