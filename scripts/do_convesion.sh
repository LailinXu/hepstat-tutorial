#!/bin/bash

cvcode=/Users/lailinxu/Local/Work/USTC/Teaching/2021Spring/HEPstat/Hands-on/converttonotebook.py
incode=/Users/lailinxu/Local/Work/USTC/Teaching/2021Spring/HEPstat/Hands-on/test/hepstat_tutorial_fit.py 
outdir=/Users/lailinxu/Local/Work/USTC/Teaching/2021Spring/HEPstat/Hands-on/test/

if [ $# -ge 1 ]; then
  incode=${1}
  incode=$(pwd)/${incode}
fi

python3 ${cvcode} ${incode} ${outdir}
