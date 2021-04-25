from ROOT import TMVA, TFile, TTree, TCut
from subprocess import call
from os.path import isfile
 
# Setup TMVA
TMVA.Tools.Instance()
(TMVA.gConfig().GetVariablePlotting()).fMaxNumOfAllowedVariablesForScatterPlots = 5 
 
outfileName = 'TMVA_tutorial_reg_1.root'
output = TFile.Open(outfileName, 'RECREATE')
factory = TMVA.Factory('TMVARegression', output,
        '!V:!Silent:Color:DrawProgressBar:Transformations=D,G:AnalysisType=Regression')
 
# Load data
trfile = "SM_ttbar.root"
if not isfile('tmva_reg_example.root'):
    call(['curl', '-L', '-O', 'http://root.cern.ch/files/tmva_reg_example.root'])
 
data = TFile.Open(trfile)
tree = data.Get('tree')
 
dataloader = TMVA.DataLoader('dataset')
for branch in tree.GetListOfBranches():
    name = branch.GetName()
    if not 'mtt' in name:
        dataloader.AddVariable(name)
dataloader.AddTarget('mtt_truth')
 
dataloader.AddRegressionTree(tree, 1.0)
dataloader.PrepareTrainingAndTestTree(TCut(''),
        'nTrain_Regression=4000:SplitMode=Random:NormMode=NumEvents:!V')
 
# Generate model
 
# BDT
factory.BookMethod( dataloader,  TMVA.Types.kBDT, "BDT",
  "!H:!V:NTrees=100:MinNodeSize=1.0%:BoostType=AdaBoostR2:SeparationType=RegressionVariance:nCuts=20:PruneMethod=CostComplexity:PruneStrength=30" )
 
# Run TMVA
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

output.Close()

# Launch the gui for the root macros
TMVA.TMVARegGui(outfileName)
