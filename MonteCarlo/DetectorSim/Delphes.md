# Brief tutorial on fast detector simulation with Delphes

## Introduction
From its [official website](https://cp3.irmp.ucl.ac.be/projects/delphes): A framework for fast simulation of a generic collider experiment
> Delphes is a C++ framework, performing a fast multipurpose detector response simulation. The simulation includes a tracking system, embedded into a magnetic field,
> calorimeters and a muon system. The framework is interfaced to standard file formats (e.g. Les Houches Event File or HepMC) and outputs observables such as isolated leptons,
> missing transverse energy and collection of jets which can be used for dedicated analyses. The simulation of the detector response takes into account the effect of
> magnetic field, the granularity of the calorimeters and sub-detector resolutions.
> Visualisation of the final state particles is also built-in using the corresponding ROOT library.

It is widely used by theorists for phenomelogical studies to estimate the expected sensitivity of a given physics model in a given experiment.

The framework is hosted at github:  https://github.com/delphes/delphes

The objectives of this tutorial:
* Run a fast detector simulation (CEPC) with Delphes
* Physics analysis with the Delphes output

## Useful references

Tutorials: 
* 2020 Fermilab, https://indico.fnal.gov/event/45413/contributions/196321/attachments/135130/167579/ilc_tutorial2_potter.pdf
* 2016, https://www.tcm.phy.cam.ac.uk/~mjh261/pdfs/delphes.pdf
* 2015, https://indico.desy.de/event/11460/contributions/5483/attachments/3873/4481/Delphes_exercise_LB.pdf

## Download and Installation

### Local installation
See the instruction from the [official website](https://github.com/delphes/delphes#quick-start-with-delphes):
* Commands to get the code:
```
   wget http://cp3.irmp.ucl.ac.be/downloads/Delphes-3.5.0.tar.gz

   tar -zxf Delphes-3.5.0.tar.gz
```
* Commands to compile the code:
```
   cd Delphes-3.5.0

   make
```
* Finally, we can run Delphes:
```
   ./DelphesHepMC3
```
* Command line parameters:
```
   ./DelphesHepMC3 config_file output_file [input_file(s)]
     config_file - configuration file in Tcl format
     output_file - output file in ROOT format,
     input_file(s) - input file(s) in HepMC format,
     with no input_file, or when input_file is -, read standard input.
```

### Docker 
The docker image can be found at: https://hub.docker.com/r/scailfin/delphes-python-centos
```
docker pull scailfin/delphes-python-centos
```

## Tutorial
### CEPC

1. Download the detector description file for CEPC
```
wget https://raw.githubusercontent.com/delphes/delphes/master/cards/delphes_card_CEPC.tcl
```
Or download it from https://github.com/delphes/delphes/blob/master/cards/delphes_card_CEPC.tcl directly.

2. Prepare the input event file (HepMC)

This is usually the output file from Pythia. See the [Pythia tutorial]()

3. Run the Delphes simulation
```
docker run --rm -it -v $PWD/pythia:/work -w /work --platform linux/amd64 scailfin/delphes-python-centos:3.5.0-python3.9 -c "DelphesHepMC2 delphes_card_CEPC.tcl delphes_output_ggH_4l.root  ggH_4l.hepmc  > out_delphes_ggH_4l.txt"
```

### Physics analysis
The output file (a ROOT file) from Delphes simulation can be used for further physics analysis. The output is basically a simple ROOT TTree file.
Some examples and tutorials can be found at:
* Simple analysis using TTree::Draw: https://github.com/delphes/delphes#simple-analysis-using-ttreedraw
* Macro-based analysis: https://github.com/delphes/delphes#macro-based-analysis
