## \file
## \ingroup tutorial_pyroot
## \notebook
## Fit example.
##
## \macro_image
## \macro_output
## \macro_code
##
## \author Lailin XU

# Import the ROOT libraries
import ROOT as R
R.gROOT.SetStyle("ATLAS")

# Generate some toy data, assuming the model is y = m*x + b. Then define a histogram to save the data.
m = 11.
b = 2.5
bin0, bin1=0, 5
nbins = bin1-bin0

fl = R.TF1("flinear", "pol1", bin0, bin1)
fl.SetParameters(0, b)
fl.SetParameters(1, m)

hname = "test_data"
hd = R.TH1F(hname, hname, nbins, bin0, bin1)
hd.Sumw2()
hd.FillRandom("flinear", 200) 
#hd.FillRandom("flinear", 20) 

myc = R.TCanvas("c", "c", 800, 600)
myc.SetFillColor(0)

myc.cd()
hd.Draw()
myc.Draw()

# Do a fitting. By default ROOT uses Chi-square fit
my1 = R.TF1("myFunc1", "pol1", bin0, bin1)
my1.SetLineColor(4)

frp1 = hd.Fit("myFunc1", "S")
myc.Update()
myc.SaveAs("test_fitting_1.png")

# Now do a likelihood fit

my2 = R.TF1("myFunc2", "pol1", bin0, bin1)
my2.SetLineColor(2)
frp2 = hd.Fit("myFunc2", "LS")
my1.Draw("same")
myc.Update()
myc.SaveAs("test_fitting_2.png")

myc.Clear()
frp2.Print("V")
gr=R.TGraph()
smin, smax=0, 4
fr2=R.TFitResult(frp2.Get())
fr2.Print()
fr2.Scan(0, gr, smin, smax)
gr.Draw()
gr.Print()
myc.Draw()

myc.SaveAs("test_fitting_3.png")
