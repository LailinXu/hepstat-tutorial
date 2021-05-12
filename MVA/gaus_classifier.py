## \file
## \ingroup tutorial_tmva
## \notebook
## Gaussian classifier
##
## \macro_image
## \macro_output
## \macro_code
##
## \author Lailin XU

import os
from math import sqrt, pow, fabs, log, cos, sin, pi, atan, exp
from subprocess import call
import ROOT as R
R.gROOT.SetStyle("ATLAS")
R.gStyle.SetPalette(1)

# Optionally one can use numpy to get the covariance matrix easily
# import numpy as np 

# Read training data
# =====================

fname_tr = "class_data.root"
if not os.path.isfile(fname_tr):
    call(['curl', '-L', '-O', 'http://yliu.web.cern.ch/yliu/HLZ_logs/class_data.root'])
tfin_tr = R.TFile.Open(fname_tr, "READ")
tr_s = tfin_tr.Get("signal;1")
tr_b = tfin_tr.Get("background;1")

# Split events into training and testing

ns = tr_s.GetEntries()
nb = tr_b.GetEntries()
print("Number of events: signal {0}, bkg {1}\n".format(ns, nb))

l_tr_s, l_tr_b = [], []
l_test_s, l_test_b = [], []

# Do roration
doRotation = 1
ang = -atan(0.32)

def do_rotation(x, y, ang=pi/4.):
  
  yp = -sin(ang)*x + cos(ang)*y  
  xp = cos(ang)*x + sin(ang)*y  
  
  return (xp, yp)

# Helper func to loop trees
def read_tr(tr):

  # Split the data into training and testing
  l_tr, l_test = [], []

  ns = tr.GetEntries()
  print("[read_tr] {0}, Number of events: {1}".format(tr.GetName(), ns))
  # loop the tree 
  for i in range(ns):
    tr.GetEntry(i)
    if i%(int(ns*0.1)) == 0:
      print(" Events processed: ", i)

    x1 = tr.X1
    x2 = tr.X2
    if doRotation:
      (x1, x2) = do_rotation(x1, x2, ang)
      
    # training data
    if i%1000 == 0:
      l_tr.append([x1, x2])
    else:
    # testing data
      l_test.append([x1, x2])

  return [l_tr, l_test]

# Read signal events
[l_tr_s, l_test_s] = read_tr(tr_s)

# Read bkg events
[l_tr_b, l_test_b] = read_tr(tr_b)

# Helper function to get the mean and covariance
def get_stat(l_data=[]):

  # number of events
  N = float(len(l_data))
  if N<1: return

  # dimension
  if type(l_data[0])==list:
    nd = len(l_data[0])
  else: nd = 1

  # mean
  l_mean = [0]*nd

  l_tot = [0]*nd 
  for i, d in enumerate(l_data):
    if nd > 1:
      for j, x in enumerate(d):
        l_tot[j] += x
    else:
        l_tot[0] += d

  for j, x in enumerate(l_tot):
    l_mean[j] = x / N

  # covariance matrix
  m_cov = R.TMatrixD(nd, nd)
  for i, d in enumerate(l_data):
    # matrix elements
    if nd > 1:
      for j, x in enumerate(d):
        for k, y in enumerate(d):
          R.TMatrixDRow(m_cov, j)[k] += (x - l_mean[j]) * (y - l_mean[k])
    else:
          R.TMatrixDRow(m_cov, 0)[0] += (d - l_mean[0]) * (d - l_mean[0])

  if nd > 1:
    for j, x in enumerate(d):
      for k, y in enumerate(d):
        R.TMatrixDRow(m_cov, j)[k] /= (N-1)
  else:
        R.TMatrixDRow(m_cov, 0)[0] /= (N-1)
  
  print("mean: ", l_mean)
  print("cov: ")
  for j in range(nd):
    for k in range(nd):
      print("{0} {1}: {2}".format(j, k, R.TMatrixDRow(m_cov, j)[k]))
  print("cov determinant:", m_cov.Determinant())
  return [l_mean, m_cov]

# Helper function to print a matrx(m, n)
def print_matrix(m_cov, md, nd):

  for j in range(md):
    for k in range(nd):
      print("{0} {1}: {2}".format(j, k, R.TMatrixDRow(m_cov, j)[k]))

# Get the mean and covariance of the input data, for the signal and background, respectively
# ===========================

# Signal
print("\n======= Look at signal events")
[l_tr_s_mean, m_tr_s_cov] = get_stat(l_tr_s)
# Cross-check with numpy
# l_tr_s_x1 = [ x[0] for i,x in enumerate(l_tr_s) ]
# l_tr_s_x2 = [ x[1] for i,x in enumerate(l_tr_s) ]
# print("\ncov for training signal:")
# a_cov_tr_s = np.cov(l_tr_s_x1, l_tr_s_x2)
# print(a_cov_tr_s)
# rho_s = np.corrcoef(l_tr_s_x1, l_tr_s_x2)
# print("correlation: ", rho_s)

print("\ninversion:")
m_tr_s_cov_d = 0
m_tr_s_icov = R.TMatrixD(m_tr_s_cov)
m_tr_s_icov.Invert(m_tr_s_cov_d)
print_matrix(m_tr_s_icov, 2, 2)

# print("inversion from numpy:")
# a_icov_tr_s = np.linalg.inv(a_cov_tr_s)
# print(a_icov_tr_s)

# Background
print("\n======= Look at bkg events")
[l_tr_b_mean, m_tr_b_cov] = get_stat(l_tr_b)
# Cross-check with numpy
# l_tr_b_x1 = [ x[0] for i,x in enumerate(l_tr_b) ]
# l_tr_b_x2 = [ x[1] for i,x in enumerate(l_tr_b) ]
# print("\ncov for training bkg:")
# a_cov_tr_b = np.cov(l_tr_b_x1, l_tr_b_x2)
# print(a_cov_tr_b)
# rho_b = np.corrcoef(l_tr_b_x1, l_tr_b_x2)
# print("correlation: ", rho_b)

print("\ninversion:")
m_tr_b_cov_d = 0
m_tr_b_icov = R.TMatrixD(m_tr_b_cov)
m_tr_b_icov.Invert(m_tr_b_cov_d)
print_matrix(m_tr_b_icov, 2, 2)

# print("inversion from numpy:")
# a_icov_tr_b = np.linalg.inv(a_cov_tr_b)
# print(a_icov_tr_b)

# Plotting
# =====================
myc = R.TCanvas("c", "c", 800, 600)
myc.SetFillColor(0)

nbinsx, xmin, xmax = 200, -20, 20
nbinsy, ymin, ymax = 100, -10, 10
hname = "training_sig"
h_s = R.TH2F(hname, hname, nbinsx, xmin, xmax, nbinsy, ymin, ymax)
h_s.SetMarkerColor(2)
hname = "training_bkg"
h_b = R.TH2F(hname, hname, nbinsx, xmin, xmax, nbinsy, ymin, ymax)
h_b.SetMarkerColor(4)

for i in range(len(l_tr_s)):
  [x, y] = l_tr_s[i]
  h_s.Fill(x, y)
for i in range(len(l_tr_b)):
  [x, y] = l_tr_b[i]
  h_b.Fill(x, y)

h_s.Draw()
h_b.Draw("same")

myc.Update()
myc.Draw()
myc.SaveAs("gaus_test_0_doRotation{0}.png".format(doRotation))

h_s.Draw("colz")
h_b.Draw("colz same")

myc.Draw()
myc.SaveAs("gaus_test_1_doRotation{0}.png".format(doRotation))


# Overlay the multi-Gaussian PDF

# Helper function for 2D Gaussian
def gaus_2d(x, par):

  if len(x)<2 or len(par)<3: 
    print("[gaus_2d]: requirs 2D data, and 3 parameters")
    return 0

  # 2D Gaussian
  nd = 2
  # Mean
  mean = [par[0], par[1]]
  # Covariance matrix 
  cov = R.TMatrixD(nd, nd)
  ipar = 0
  for j in range(nd):
    for k in range(nd):
      R.TMatrixDRow(cov, j)[k] = par[ipar + 2]
      ipar += 1

  # Correlation
  sx = R.TMatrixDRow(cov, 0)[0]
  sy = R.TMatrixDRow(cov, 1)[1]

  sxy = R.TMatrixDRow(cov, 0)[1]
  rho = sxy / sqrt(sx*sy)

  if fabs(rho)==1:
    print("[gaus_2d]: error rho = ", rho)
    return 1

  # Build the multi-Gaussian
  m_x = R.TMatrixD(nd, 1)
  for i in range(nd):
    R.TMatrixDRow(m_x, i)[0] = x[i] - mean[i]

  m_x_t = R.TMatrixD(m_x)
  m_x_t.T()

  cov_d = 0
  icov = R.TMatrixD(cov)
  icov.Invert(cov_d)
  cov_d = cov.Determinant()
  icov_d = icov.Determinant()

  r = 0
  # r = (m_x_t * icov) * m_x
  for i in range(nd):
    for j in range(nd):
      r += R.TMatrixDRow(m_x_t, 0)[j] * R.TMatrixDRow(icov, i)[j] * R.TMatrixDRow(m_x, i)[0]

  # y = 1./(2*pi* sx * sy * sqrt(1. - pow(rho, 2))) * exp( - 1./(2*(1. - pow(rho, 2))) * ( pow(x[0]/sx, 2) + pow(x[1]/sy, 2) - 2*rho*x[0]*x[1]/(sx*sy) ) )
  y = 1./(2*pi * sqrt(cov_d)) * exp( -0.5* r ) 

  return y

# Signal 
npar = 6 # mean: 2; cov: 2*2
g_s = R.TF2("gaus_s", gaus_2d, xmin, xmax, ymin, ymax, npar)
g_s.SetParameter(0, l_tr_s_mean[0])
g_s.SetParameter(1, l_tr_s_mean[1])
g_s.SetParameter(2, R.TMatrixDRow(m_tr_s_cov, 0)[0])
g_s.SetParameter(3, R.TMatrixDRow(m_tr_s_cov, 0)[1])
g_s.SetParameter(4, R.TMatrixDRow(m_tr_s_cov, 1)[0])
g_s.SetParameter(5, R.TMatrixDRow(m_tr_s_cov, 1)[1])

myc.Clear()
h_s.GetXaxis().SetRangeUser(-5, 5)
h_s.GetYaxis().SetRangeUser(-5, 5)
if doRotation:
  h_s.GetXaxis().SetTitle("X1'")
  h_s.GetYaxis().SetTitle("X2'")
else:
  h_s.GetXaxis().SetTitle("X1")
  h_s.GetYaxis().SetTitle("X2")

h_s.Draw("colz")
g_s.Draw("cont1 same")

myc.Draw()
myc.SaveAs("gaus_test_2_doRotation{0}.png".format(doRotation))

# Background
npar = 6 # mean: 2; cov: 2*2
g_b = R.TF2("gaus_b", gaus_2d, xmin, xmax, ymin, ymax, npar)
g_b.SetParameter(0, l_tr_b_mean[0])
g_b.SetParameter(1, l_tr_b_mean[1])
g_b.SetParameter(2, R.TMatrixDRow(m_tr_b_cov, 0)[0])
g_b.SetParameter(3, R.TMatrixDRow(m_tr_b_cov, 0)[1])
g_b.SetParameter(4, R.TMatrixDRow(m_tr_b_cov, 1)[0])
g_b.SetParameter(5, R.TMatrixDRow(m_tr_b_cov, 1)[1])

myc.Clear()
h_b.Draw("colz")
g_b.Draw("cont1 same")

myc.Draw()
myc.SaveAs("gaus_test_3_doRotation{0}.png".format(doRotation))


# Gaussian classifier
# =====================

def r_gaus(l_x=[], mean_s=[], cov_s=None, mean_b=[], cov_b=None, l_pi=[]):
  
  nd = len(l_x)
 
  # Signal 
  m_x_s = R.TMatrixD(nd, 1)
  for i in range(nd):
    R.TMatrixDRow(m_x_s, i)[0] = l_x[i] - mean_s[i]

  m_x_s_t = R.TMatrixD(m_x_s)
  m_x_s_t.T()

  cov_s_d = 0
  icov_s = R.TMatrixD(cov_s)
  icov_s.Invert(cov_s_d)
  cov_s_d = cov_s.Determinant()
  icov_s_d = icov_s.Determinant()

  r_s = 0
  # r_s = (m_x_s_t * icov_s) * m_x_s
  for i in range(nd):
    for j in range(nd):
      r_s += R.TMatrixDRow(m_x_s_t, 0)[j] * R.TMatrixDRow(icov_s, i)[j] * R.TMatrixDRow(m_x_s, i)[0]
  
  # Background
  m_x_b = R.TMatrixD(nd, 1)
  for i in range(nd):
    R.TMatrixDRow(m_x_b, i)[0] = l_x[i] - mean_b[i]
  
  m_x_b_t = R.TMatrixD(m_x_b)
  m_x_b_t.T()

  cov_b_d = 0
  icov_b = R.TMatrixD(cov_b)
  icov_b.Invert(cov_b_d)
  cov_b_d = cov_b.Determinant()
  icov_b_d = icov_b.Determinant()

  r_b = 0
  # r_b = m_x_b_t * icov_b * m_x_b
  for i in range(nd):
    for j in range(nd):
      r_b += R.TMatrixDRow(m_x_b_t, 0)[j] * R.TMatrixDRow(icov_b, i)[j] * R.TMatrixDRow(m_x_b, i)[0]

  # Classification
  y = 0
 
  if r_s < r_b + 2*log(l_pi[0]/l_pi[1]) + log(cov_b_d/cov_s_d): y = 1.

  return y

# Test
# =====================
print("\nTest classification: input signal ")
ntest_s = len(l_test_s)
ntest_s_good = 0
# Assuming equal signal and bkg
l_pi = [0.5]*2
for i in range(ntest_s):
  y = r_gaus(l_test_s[i], l_tr_s_mean, m_tr_s_cov, l_tr_b_mean, m_tr_b_cov, l_pi)
  if y == 1: ntest_s_good += 1

rate_s = ntest_s_good/ float(ntest_s)
print("Accuracy: {0} / {1} = {2}".format(ntest_s_good, ntest_s, rate_s))

print("\nTest classification: input bkg ")
ntest_b = len(l_test_b)
ntest_b_good = 0
for i in range(ntest_b):
  y = r_gaus(l_test_b[i], l_tr_s_mean, m_tr_s_cov, l_tr_b_mean, m_tr_b_cov, l_pi)
  if y == 1: ntest_b_good += 1

rate_b = ntest_b_good/ float(ntest_b)
print("Accuracy: {0} / {1} = {2}".format(ntest_b_good, ntest_b, rate_b))

# Application
# =====================
fname_d = "real_data.root"
if not os.path.isfile(fname_d):
    call(['curl', '-L', '-O', 'http://yliu.web.cern.ch/yliu/HLZ_logs/real_data.root'])
tfin_d = R.TFile.Open(fname_d, "READ")
tr_d = tfin_d.Get("data;2")

[l_tr_d, l_test_d] = read_tr(tr_d)
l_test_d.extend(l_tr_d)

hname = "data"
h_d = R.TH2F(hname, hname, nbinsx, xmin, xmax, nbinsy, ymin, ymax)
h_d.SetMarkerColor(1)
hname = "data_sig"
h_ds = R.TH2F(hname, hname, nbinsx, xmin, xmax, nbinsy, ymin, ymax)
h_ds.SetMarkerColor(2)
hname = "data_bkg"
h_db = R.TH2F(hname, hname, nbinsx, xmin, xmax, nbinsy, ymin, ymax)
h_db.SetMarkerColor(4)

print("\nTest classification: real data ")
ntest_d = len(l_test_d)
ntest_d_good = 0
for i in range(ntest_d):
  r = r_gaus(l_test_d[i], l_tr_s_mean, m_tr_s_cov, l_tr_b_mean, m_tr_b_cov, l_pi)

  [x, y] = l_test_d[i]

  if r == 1:
    ntest_d_good += 1
    h_ds.Fill(x, y)
  else:
    h_db.Fill(x, y)
  h_d.Fill(x, y)

rate_d = ntest_d_good/ float(ntest_d)
print("Estimated signal events: {0} / {1} = {2}".format(ntest_d_good, ntest_d, rate_d))

# Plot real data, training signal and bkg
h_s.Draw()
h_b.Draw("same")
h_d.Draw("same")

myc.Draw()
myc.SaveAs("gaus_test_4_doRotation{0}.png".format(doRotation))

# Apply the classifier to data
if doRotation:
  h_ds.GetXaxis().SetTitle("X1'")
  h_ds.GetYaxis().SetTitle("X2'")
else:
  h_ds.GetXaxis().SetTitle("X1")
  h_ds.GetYaxis().SetTitle("X2")

h_ds.Draw()
h_db.Draw("same")

myc.Draw()
myc.SaveAs("gaus_test_5_doRotation{0}.png".format(doRotation))

# Test a different signal/bkg ratio
h_ds.Clear()
h_db.Clear()
l_pi = [0.1, 0.9]
ntest_d = len(l_test_d)
ntest_d_good = 0
for i in range(ntest_d):
  r = r_gaus(l_test_d[i], l_tr_s_mean, m_tr_s_cov, l_tr_b_mean, m_tr_b_cov, l_pi)

  [x, y] = l_test_d[i]

  if r == 1:
    ntest_d_good += 1
    h_ds.Fill(x, y)
  else:
    h_db.Fill(x, y)

rate_d = ntest_d_good/ float(ntest_d)
print("Estimated signal events: {0} / {1} = {2}".format(ntest_d_good, ntest_d, rate_d))

# Apply the classifier to data
if doRotation:
  h_ds.GetXaxis().SetTitle("X1'")
  h_ds.GetYaxis().SetTitle("X2'")
else:
  h_ds.GetXaxis().SetTitle("X1")
  h_ds.GetYaxis().SetTitle("X2")

h_ds.Draw()
h_db.Draw("same")

myc.Draw()
myc.SaveAs("gaus_test_6_doRotation{0}.png".format(doRotation))

