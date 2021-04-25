#!/bin/bash

## to submit condor jobs for eft fit

BASEDIR=$(pwd)

## a text file, each line contains another text file, which
## is a list of EVNT files belonging to a given dataset
input_list_EVNT=$1 
## where truth_daod is saved
outdir=/usatlas/groups/bnl_local/lailinxu/Analysis/VLVL/MCProd/MadGraph/MVAInputs/Output

OUTPUTFOLDER="Delphes"
if [ $# -ge 2 ]; then
  OUTPUTFOLDER=$2
fi

TAG=v1
if [ $# -ge 2 ]; then
  TAG=$3
fi
QUEUE="longlunch" ## for lxplus, see https://twiki.cern.ch/twiki/bin/view/ABPComputing/LxbatchHTCondor#Queue_Flavours

DIR=$(pwd)

job="MVA"
condorInputFile="condorInputFile.${job}.${OUTPUTFOLDER}.${TAG}.txt"
condorRunFile="condorRunFile.${job}.${OUTPUTFOLDER}.${TAG}.sh"
condorSubmitFile="condorSubmit.${job}.${OUTPUTFOLDER}.${TAG}.sub"

if [ -f ${condorInputFile} ] || [ -f ${condorRunFile} ] || [ -f ${condorSubmitFile} ]; then
  echo " "
  echo "Submission files exist. Do you really want to overwrite them???"
  echo " "
  exit
fi


###################
#Make run file
###################
echo "#!/bin/bash
echo \$(hostname)
echo \$(pwd)

wdir=/tmp/\${USER}/
if [ ! -d \${wdir} ]; then
  mkdir \${wdir} -p
fi
cd \${wdir}

### ROOT
source /usatlas/groups/bnl_local/lailinxu/Analysis/VLVL/MCProd/MadGraph/Gridpack/setup.sh

# input file
input_evnt=\${1}
# output file
output=\${2}
# output destination
dest_dir=\${3}

pydir=/usatlas/groups/bnl_local/lailinxu/Analysis/VLVL/MCProd/MadGraph/MVAInputs

python \${pydir}/prepare_vars.py \${input_evnt} \${output}

# copy output
if [ -f \${output} ]; then
  cp \${output} \${dest_dir} -p
fi

"> $condorRunFile
chmod +x $condorRunFile


###################
#Make condor File
###################
logdir=log_${OUTPUTFOLDER}
if [ ! -d ${logdir} ]; then mkdir ${logdir}; fi

echo "Universe      = vanilla
getenv        = True
executable    = ${condorRunFile}
WhenToTransferOutput = ON_EXIT
#transfer_output_Files = ${OUTPUTFOLDER}
output        = log_${OUTPUTFOLDER}/log.\$(ClusterId).\$(ProcId).out
error         = log_${OUTPUTFOLDER}/log.\$(ClusterId).\$(ProcId).err
log           = log_${OUTPUTFOLDER}/log.\$(ClusterId).\$(ProcId).log

#+JobFlavour   = \"${QUEUE}\"
#+JobFlavour   = \"microcentury\"
#+JobFlavour   = \"longlunch\"
#+JobFlavour   = \"workday\"
#+JobFlavour   = \"tomorrow\"
#+JobFlavour   = \"testmatch\"

queue arguments from ${condorInputFile}
  "> $condorSubmitFile

###################
#Make input config file
###################
if [ -f $condorInputFile ]; then
  rm $condorInputFile
fi

#Loop over inputlist
## loop each dataset list

this_outpath=${outdir}/${OUTPUTFOLDER}
if [ ! -d ${this_outpath} ]; then mkdir ${this_outpath} -p; fi

for evnt in `less ${input_list_EVNT}`; do
  lname=`dirname ${evnt}`
  fname=`basename ${lname}`
  output=${OUTPUTFOLDER}_${fname}_tree.root
  echo "${evnt} ${output} ${this_outpath}" >> $condorInputFile
done


###################
#Submit 
###################
if [ -f ${condorSubmitFile} ]; then
  echo "Submit condor jobs ${condorSubmitFile}"
  condor_submit $condorSubmitFile
fi

