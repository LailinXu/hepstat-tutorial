## \file
## \ingroup tutorial_tmva
## \notebook
## TMVA example, for regression. The input data is a simple TTree file, which containts the needed input variables.
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
# ==================
TMVA.Tools.Instance()
(TMVA.gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 5 
 
# Create a new root output file
outfileName = 'TMVA_tutorial_reg_1.root'
output = TFile.Open(outfileName, 'RECREATE')

# Create the factory object. Later you can choose the methods whose performance you'd like to investigate. The factory will
# then run the performance analysis for you.
#
# The first argument is the base of the name of all the weightfiles in the directory weight/
#
# The second argument is the output file for the training results
factory = TMVA.Factory('TMVARegression', output, '!V:!Silent:Color:DrawProgressBar:Transformations=D,G:AnalysisType=Regression')
 
# Load data
trfile = "example_data/SM_ttbar.root"
if not isfile(trfile):
    call(['curl', '-L', '-O', 'https://gitee.com/lailinxu/hepstat-tutorial/raw/master/MVA/example_data/{0}'.format(trfile)])

# Get the tree file 
data = TFile.Open(trfile)
if not data:
  print("Error! file not opened", trfile)
trname = "tree"
tree = data.Get(trname)
 
# Define the input variables that shall be used for the MVA training
dataloader = TMVA.DataLoader('dataset')
for branch in tree.GetListOfBranches():
    name = branch.GetName()
    if not 'mtt' in name:
        dataloader.AddVariable(name)

# Add the variable carrying the regression target
dataloader.AddTarget('mtt_truth')
 
# Register the regression tree
dataloader.AddRegressionTree(tree, 1.0)

# Apply some cuts
# Set the number of events for training, and use all remaining events in the trees after training for testing

# If no numbers of events are given, half of the events in the tree are used for training, and the other half for testing:
#
#     dataloader->PrepareTrainingAndTestTree( mycut, "SplitMode=random:!V" );
dataloader.PrepareTrainingAndTestTree(TCut(''), 'nTrain_Regression=10000:SplitMode=Random:NormMode=NumEvents:!V')
 
# Generate model
# =============
# Book MVA methods 
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
