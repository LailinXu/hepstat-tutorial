## \file
## \ingroup tutorial_tmva
## \notebook
## TMVA example, for regression
##  with following objectives:
##  * Train a BDT with TMVA
##
## \macro_image
## \macro_output
## \macro_code
##
## \author Lailin XU
## Modified from [RegressionKeras.py](https://root.cern/doc/master/RegressionKeras_8py.html) and [TMVARegression.C](https://root.cern/doc/master/TMVARegression_8C.html)

from ROOT import TMVA, TFile, TTree, TCut
from subprocess import call
from os.path import isfile
 
# Setup TMVA
TMVA.Tools.Instance()
(TMVA.gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 5 
 
outfileName = 'TMVA_tutorial_reg_1.root'
output = TFile.Open(outfileName, 'RECREATE')
factory = TMVA.Factory('TMVARegression', output, '!V:!Silent:Color:DrawProgressBar:Transformations=D,G:AnalysisType=Regression')
 
# Load data
trfile = "SM_ttbar.root"
if not isfile('tmva_reg_example.root'):
    call(['curl', '-L', '-O', 'http://root.cern.ch/files/tmva_reg_example.root'])
 
data = TFile.Open(trfile)
if not data:
  print("Error! file not opened", trfile)
trname = "tree"
tree = data.Get(trname)
 
dataloader = TMVA.DataLoader('dataset')
for branch in tree.GetListOfBranches():
    name = branch.GetName()
    if not 'mtt' in name:
        dataloader.AddVariable(name)
dataloader.AddTarget('mtt_truth')
 
dataloader.AddRegressionTree(tree, 1.0)
dataloader.PrepareTrainingAndTestTree(TCut(''), 'nTrain_Regression=10000:SplitMode=Random:NormMode=NumEvents:!V')
 
# Generate model
 
# BDT
factory.BookMethod( dataloader,  TMVA.Types.kBDT, "BDT",
  "!H:!V:NTrees=100:MinNodeSize=1.0%:BoostType=AdaBoostR2:SeparationType=RegressionVariance:nCuts=20:PruneMethod=CostComplexity:PruneStrength=30" )
factory.BookMethod( dataloader,  TMVA.Types.kBDT, "BDTG",
  "!H:!V:NTrees=2000::BoostType=Grad:Shrinkage=0.1:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=3:MaxDepth=4" )

# Neural network (MLP)
#factory.BookMethod( dataloader,  TMVA.Types.kMLP, "MLP",
  #"!H:!V:VarTransform=Norm:NeuronType=tanh:NCycles=20000:HiddenLayers=N+20:TestRate=6:TrainingMethod=BFGS:Sampling=0.3:SamplingEpoch=0.8:ConvergenceImprove=1e-6:ConvergenceTests=15:!UseRegulator" )
 
# Run TMVA
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

output.Close()
