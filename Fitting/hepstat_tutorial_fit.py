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
from math import pow, sqrt
R.gROOT.SetStyle("ATLAS")

# Linear least square method
def lls(l_x=[], l_y=[], l_ye=[],):
  """
  A simple linear regression, y=m*x+b
  """
  sum_1, sum_x, sum_x2 = 0, 0, 0
  sum_xy, sum_y, sum_y2 = 0, 0, 0
  
  for i in range(len(l_x)):
    ye = l_ye[i]
    x = l_x[i]
    y = l_y[i]
    if ye ==0: continue # ignore empty bins
    sum_1 += pow(ye, -2)
    sum_x += x*pow(ye, -2)
    sum_y += y*pow(ye, -2)
    sum_x2 += pow(x/ye, 2)
    sum_xy += x*y*pow(ye, -2)
    sum_y2 += pow(y/ye, 2)

  m = (sum_1 * sum_xy - sum_x * sum_y) / (sum_1 * sum_x2 - pow(sum_x, 2))
  b = (sum_y * sum_x2 - sum_x * sum_xy) / (sum_1 * sum_x2 - pow(sum_x, 2))

  # Error
  v_m = sum_1 / (sum_1 * sum_x2 - pow(sum_x, 2))
  v_b = sum_x2 / (sum_1 * sum_x2 - pow(sum_x, 2))
  corr_mb0 = - sum_x / sqrt(sum_1 * sum_x2)

  # Error matrix
  mat = R.TMatrixD(2,2)
  R.TMatrixDRow(mat, 0)[0] = sum_x2
  R.TMatrixDRow(mat, 0)[1] = sum_x
  R.TMatrixDRow(mat, 1)[0] = sum_x
  R.TMatrixDRow(mat, 1)[1] = sum_1
  mat_inv = mat.Invert()
  e_m = sqrt(R.TMatrixDRow(mat_inv, 0)(0)) 
  e_b = sqrt(R.TMatrixDRow(mat_inv, 1)(1)) 
  corr_mb = (R.TMatrixDRow(mat_inv, 0)(1)) / (e_m*e_b) 

  print(sqrt(v_m), e_m, sqrt(v_b), e_b, corr_mb0, corr_mb)
  return [m, e_m, b, e_b, corr_mb]

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
hd.GetXaxis().SetTitle("x")
hd.GetYaxis().SetTitle("y")
hd.FillRandom("flinear", 200) 

myc = R.TCanvas("c", "c", 800, 600)
myc.SetFillColor(0)

myc.cd()
hd.Draw()
myc.Draw()

# Do a fitting. By default ROOT uses Chi-square fit
my1 = R.TF1("myFunc1", "pol1", bin0, bin1)
my1.SetLineColor(4)

frp1 = hd.Fit("myFunc1", "S")
frp1.Print("V")
myc.Update()
myc.Draw()
myc.SaveAs("test_fitting_1.png")

# Do a linear regression BY HAND
l_x, l_y, l_ye=[], [], []
for i in range(1, nbins+1):
  l_x.append(hd.GetBinCenter(i))
  l_y.append(hd.GetBinContent(i))
  l_ye.append(hd.GetBinError(i))

[est_m, est_err_m, est_b, est_err_b, est_corr_mb] = lls(l_x, l_y, l_ye)
print("\nInput [x]:", l_x)
print("Input [y]:", l_y)
print("Input [y_err]:", l_ye)
print("Estimated m (p1): {0} +/- {1}".format(est_m, est_err_m))
print("Estimated b (p0): {0} +/- {1}".format(est_b, est_err_b))
print("Estimated correlation (m, b): {0}\n\n".format(est_corr_mb))

# Now do a likelihood fit
my2 = R.TF1("myFunc2", "pol1", bin0, bin1)
my2.SetLineColor(2)
frp2 = hd.Fit("myFunc2", "LS")
my1.Draw("same")
myc.Update()
myc.Draw()
myc.SaveAs("test_fitting_2.png")

# Plot the NLL scan
myc.Clear()
frp2.Print("V")
gr=R.TGraph()
smin, smax=0, 4
fr2=R.TFitResult(frp2.Get())
fr2.Print()
fr2.Scan(0, gr, smin, smax)
gr.Draw()
gr.GetXaxis().SetTitle("#theta")
gr.GetYaxis().SetTitle("-2log(#lambda)")
myc.Draw()

myc.SaveAs("test_fitting_3.png")
