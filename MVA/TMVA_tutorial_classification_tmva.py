## \file
## \ingroup tutorial_tmva
## \notebook
## TMVA example, for classification
##  with following objectives:
##  * Train a BDT with TMVA
##
## \macro_image
## \macro_output
## \macro_code
##
## \author Lailin XU
## Modified from [ClassificationKeras.py](https://root.cern/doc/master/ClassificationKeras_8py.html) and [TMVAClassification.C](https://root.cern/doc/master/TMVAClassification_8C.html)

from ROOT import TMVA, TFile, TTree, TCut
from subprocess import call
from os.path import isfile
 
# Setup TMVA
# =======================
TMVA.Tools.Instance()
(TMVA.gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 5 
 
outfileName = 'TMVA_tutorial_cla_1.root'
output = TFile.Open(outfileName, 'RECREATE')
# Create the factory object. Later you can choose the methods whose performance you'd like to investigate. The factory is
#    the only TMVA object you have to interact with
#   
#    The first argument is the base of the name of all the weightfiles in the directory weight/
#    The second argument is the output file for the training results
factory = TMVA.Factory("TMVAClassification", output,
  "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification")
 
# Load data
# =======================
# Background
trfile_B = "example_data/SM_ttbar.root"
# Signal
trfile_S = "example_data/Zp1TeV_ttbar.root"
if not isfile('tmva_reg_example.root'):
    call(['curl', '-L', '-O', 'http://root.cern.ch/files/tmva_reg_example.root'])
 
data_B = TFile.Open(trfile_B)
data_S = TFile.Open(trfile_S)
trname = "tree"
tree_B = data_B.Get(trname)
tree_S = data_S.Get(trname)
 
dataloader = TMVA.DataLoader('dataset')
for branch in tree_S.GetListOfBranches():
    name = branch.GetName()
    if name not in ["mtt_truth", "weight", "nlep", "njets"]:
        dataloader.AddVariable(name)
 
# Add Signal and background trees
dataloader.AddSignalTree(tree_S, 1.0)
dataloader.AddBackgroundTree(tree_B, 1.0)

# Set individual event weights (the variables must exist in the original TTree)
# dataloader.SetSignalWeightExpression("weight")
# dataloader.SetBackgroundWeightExpression("weight")

# Tell the dataloader how to use the training and testing events
#
# If no numbers of events are given, half of the events in the tree are used
# for training, and the other half for testing:
#
#    dataloader->PrepareTrainingAndTestTree( mycut, "SplitMode=random:!V" );
#
# To also specify the number of testing events, use:
#
#    dataloader->PrepareTrainingAndTestTree( mycut,
#         "NSigTrain=3000:NBkgTrain=3000:NSigTest=3000:NBkgTest=3000:SplitMode=Random:!V" );
dataloader.PrepareTrainingAndTestTree(TCut(''), "nTrain_Signal=10000:nTrain_Background=10000:SplitMode=Random:NormMode=NumEvents:!V")
 
# Generate model
 
# BDT
factory.BookMethod( dataloader,  TMVA.Types.kBDT, "BDT",
  "!H:!V:NTrees=100:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20")
factory.BookMethod( dataloader,  TMVA.Types.kBDT, "BDTG",
  "!H:!V:NTrees=1000:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2")

 
# Run TMVA
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

output.Close()
