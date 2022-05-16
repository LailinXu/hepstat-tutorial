# Quick tutorials on MadGraph5_aMC@NLO

## Introduction

From its [official website](https://launchpad.net/mg5amcnlo): 
> MadGraph5_aMC@NLO is a framework that aims at providing all the elements necessary for SM and BSM phenomenology, such as the computations of cross sections,
> the generation of hard events and their matching with event generators, and the use of a variety of tools relevant to event manipulation and analysis.
> Processes can be simulated to LO accuracy for any user-defined Lagrangian, an the NLO accuracy in the case of models that support this kind of calculations
> -- prominent among these are QCD and EW corrections to SM processes. Matrix elements at the tree- and one-loop-level can also be obtained.

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
#### Drell-Yan $ pp \to \ell^{+} \ell^{-}$
Process card: [proc_DrellYan.dat](EventGenerators/MadGraph/proc_DrellYan.dat)

* Import the theory model (the [FeynRules](https://feynrules.irmp.ucl.ac.be/) UFO model), which is the Standard Model in this case
```
import model sm
```
One can also import any other UFO theory models, like SUSY or Dark Matter models, which can be found at, or ask your theory friends to write an UFO model for you.

* Define particles (or alias)
```
define p = g u c d s u~ c~ d~ s~
define j = g u c d s u~ c~ d~ s~
define l+ = e+ mu+
define l- = e- mu-
define vl = ve vm vt
define vl~ = ve~ vm~ vt~
```
The particle names are defined by the UFO model. Here we don't do any thing but just to define some alias to help simply the later process

* Define the physics process: `generate` + `[process name]`. The `process name` has to be valid and follow the Madgraph syntax. 
```
generate p p > l+ l-
```
here `p p` are initial states, and each `p` includes all possible particles `g u c d s u~ c~ d~ s~` as indicated by the definition above `define p = g u c d s u~ c~ d~ s~`; and `l+ l-` are final states, again `l+` is defined as `define l+ = e+ mu+`. If you don't want to include certain inistiate states or final states, you can change the particle definition in the previous step.

After this step, MadGraph would automatically check and producess all possible Feynman diagrams:
```
MG5_aMC>generate p p > l+ l-
8 processes with 16 diagrams generated in 0.456 s
Total: 8 processes with 16 diagrams
```
if we modify the process slightly to `p p > z > l+ l-`:
```
MG5_aMC>generate p p > z > l+ l-
8 processes with 8 diagrams generated in 0.438 s
Total: 8 processes with 8 diagrams
```
you can see the number of diagrams is reduced. This is due to the MadGraph syntax: by adding `> z` it actually requires a s-channel `Z` boson, otherwise it would include both `Z` boson processes and virtual photon processes (and the interference effect).

* Generate codes for matrix element calculations `output [output_directory_name]`. MadGraph would then produce codes for real calculations.
```
output test_ggH
INFO: initialize a new directory: test_ggH 
INFO: remove old information in test_ggH 
INFO: Organizing processes into subprocess groups 
INFO: Generating Helas calls for process: g g > h WEIGHTED<=4 [ noborn = QCD ] QCD^2<=4 
INFO: Processing color information for loop process: g g > h [ noborn = QCD ] QCD^2<=4 
INFO: Creating color matrix  loop process: g g > h WEIGHTED<=4 [ noborn = QCD ] QCD^2<=4 
INFO: Creating files in directory /work/test_ggH/SubProcesses/PV0_0_1_gg_h 
INFO: Computing diagram color coefficients 
INFO: Drawing loop Feynman diagrams for Process: g g > h WEIGHTED<=4 [ noborn = QCD ] QCD^2<=4 
INFO: Creating files in directory P0_gg_h 
INFO: Generating Feynman diagrams for Process: g g > h WEIGHTED<=4 [ noborn = QCD ] QCD^2<=4 
INFO: Finding symmetric diagrams for subprocess group gg_h 
Generated helas calls for 1 subprocesses (4 diagrams) in 0.121 s
ALOHA: aloha starts to compute helicity amplitudes
ALOHA: aloha creates 7 routines in  1.543 s
save configuration file to /work/test_ggH/Cards/me5_configuration.txt
INFO: Use Fortran compiler /usr/bin/gfortran 
INFO: Use c++ compiler g++ 
INFO: Generate jpeg diagrams 
INFO: Generate web pages 
Output to directory /work/test_ggH done.
Type "launch" to generate events from this process, or see
/work/test_ggH/README
Run "open index.html" to see more information about this process.
```

The output directory should have something like the following:
<pre>
<b>Cards</b>               <b>HTML</b>                README              <b>Source</b>              TemplateVersion.txt crossx.html         <b>lib</b>
<b>Events</b>              MGMEVersion.txt     README.systematics  <b>SubProcesses</b>        </b>bin</b>                 index.html
</pre>

It is always a good idea to check the generated Feynman diagrams, to see if they are expected. The automatically generated diagrams can be found under `SubProcesses/P1_*`, for example:
```
ls mg5/test_ee_Z2/SubProcesses/P1_ll_ll/matrix*jpg
mg5/test_ee_Z2/SubProcesses/P1_ll_ll/matrix11.jpg
```

* Launch the matrix element calculations `launch`. You would be prompted to ask to modify some settings:
```
Do you want to edit a card (press enter to bypass editing)?
/------------------------------------------------------------\
|  1. param         : param_card.dat                         |
|  2. run           : run_card.dat                           |
|  3. pythia8       : pythia8_card.dat                       |
|  4. MadLoopParams : MadLoopParams.dat                      |
\------------------------------------------------------------/
```

    * `param_card.dat`: change parameters for the model, like couplings, masses and widths of particles, etc

    * `run_card.dat`: change settings to control the process related calculations, like beam energies, PDF set, generator cuts, etc

    * other cards that are related to third-party packages, like `pythia8_card.dat` etc.

After finishing the settings, MadGraph would compile the source codes and run the calculation and event generation:
```
Generating 1000 events with run name run_01
survey  run_01 
INFO: compile directory 
Not able to open file /work/test_eeZH2/crossx.html since no program configured.Please set one in ./input/mg5_configuration.txt
compile Source Directory
Using random number seed offset = 21
INFO: Running Survey 
Creating Jobs
Working on SubProcesses
INFO: Compiling for process 1/1. 
INFO:     P1_ll_zh  
INFO:     P1_ll_zh  
INFO:  Idle: 1,  Running: 0,  Completed: 0 [ current time: 08h05 ] 
INFO:  Idle: 0,  Running: 0,  Completed: 1 [  1.7s  ] 
INFO:  Idle: 0,  Running: 0,  Completed: 1 [  1.7s  ] 
INFO: End survey 
```

* Results and outputs
After the above steps, MadGraph would calculate the cross-section and generate matrix-element events. The former can be found either from the printout message or from the `crossx.html` in the output directory. The latter can be found under the `Event` directory.

    * Cross-section
```
  === Results Summary for run: run_01 tag: tag_1 ===

     Cumulative sequential time for this run: 1m57s
     Cross-section :   19.1 +- 0.05824 pb
     Nb of events :  1000
```

    * Events. 
```
ls mg5/test_ggH/Events/run_01 
run_01_tag_1_banner.txt       tag_1_djrs.dat                tag_1_pythia8.cmd             tag_1_pythia8_events.hepmc.gz
run_shower.sh                 tag_1_pts.dat                 tag_1_pythia8.log             unweighted_events.lhe.gz
```

    The `unweighted_events.lhe.gz` file is the [Les Houches event (LHE)](https://arxiv.org/abs/hep-ph/0609017) file, which is basically an xml file and it contains the four-momentum of initial state and final state particles. 

    1. The header part (between `<header>` and `</header>`) also contains all the MadGraph settings mentioned above (`run_card` and `parameter_card`).


    2. The `init` part contains information about the beam energy, PDF set and cross-section
```
<init>
2212 2212 6.500000e+03 6.500000e+03 0 0 247000 247000 -4 1
1.909900e+01 5.823500e-02 1.909900e+01 0
<generator name='MadGraph5_aMC@NLO' version='3.3.2'>please cite 1405.0301 </generator>
</init>
```

    3. The `event` part contains all generated events. Each block of `<event>` and `</event>` is for one single event:
```
<event>
 3      0 +1.9099000e+01 6.25000000e+01 7.54677100e-03 1.38763000e-01
       21 -1    0    0  502  501 +0.0000000000e+00 +0.0000000000e+00 +4.9741077198e+02 4.9741077198e+02 0.0000000000e+00 0.0000e+00 1.0000e+00
       21 -1    0    0  501  502 -0.0000000000e+00 -0.0000000000e+00 -7.8531672815e+00 7.8531672815e+00 0.0000000000e+00 0.0000e+00 1.0000e+00
       25  1    1    2    0    0 +0.0000000000e+00 +0.0000000000e+00 +4.8955760470e+02 5.0526393926e+02 1.2500000000e+02 0.0000e+00 0.0000e+00
</event>
```

    Here `3` means the event has 3 particles, showing in the 3 lines below. Each line is for one particle, which has information about the PDG ID, particle index and the four-momentum (`px, py, pz, E, mass`) and spin.


#### $ gg \to H$ 

Process card: [proc_ggH.dat](EventGenerators/MadGraph/proc_ggH.dat)

#### $e^{0}e^{+} \to ZH$

Process card: [proc_ee_ZH.dat](EventGenerators/MadGraph/proc_ee_ZH.dat)

See the reference [2108.10261](https://arxiv.org/pdf/2108.10261.pdf) for the calcuation of lepton collisions in MadGraph.
