## \file
## \ingroup tutorial_kalmanFilter
## \notebook
## Kalman Filter
##
## \macro_image
## \macro_output
## \macro_code
##
## \author Lailin XU

import os
from math import sqrt, fabs, tan, atan
import ROOT as R
import numpy as np
from numpy.linalg import inv

# A Tutorial of Kalman Filter for a testbeam experiment or fixed target experiment
# =================
# Modified from the code by the original author:  Peter Hansen, [link](https://indico.nbi.ku.dk/event/454/contributions/2087)
# Useful references:
# * [Track Reconstruction,  Peter Hansen Oct 2018 Tracking Lectures](https://indico.nbi.ku.dk/event/1090/sessions/2365/attachments/2696/3926/trackalgs2018.pdf)
# * [Straight line track reconstruction for the ATLAS IBL testbeam with the EUDET telescope](https://cds.cern.ch/record/1708349)
# 
# Demonstrate track fit method for a simple example of horizontal tracks
# passing 4 or 6 pixel tracking planes along x, each measuring coordinates (y,z).
# A spectrometer magnet is inserted the middle of the telescope.
# Everything is in a Helium bag  

# y is up
# x=0, y=0, z=0 at the first plane.
# dy/dx = 0 at the first plane.

# here are the planes for a choice of 4 planes with distBetweenPlanes=10.:
#
#  I             I    magnet   I             I
#
# 0cm--------- 10cm-----------20cm----------30cm---------->x-axis
#
# ![Detector setup](figs/spectrometer.png "Detector geometry")
#
# This tutorial has the following parts:
# * Generate toy events: a particle passes through the 4 detector planes and it would leave 4 true hits. But the following detector effects are considered in the simulation:
# ** Detector resolution (the measured hit position could be different than the true hit position, a Gaussian smearing is used to emulate this effect)
# ** Multi-scattering which could deviate the track from a straight line
# ** Detector efficiency (not 100%, i.e., a true hit might not be seen by the detector)
# ** Detector noise (apart from the true signal hits, random noise hits are added in each detector plane)
# * Track finding with the Kalman Filter
# ** Use hits from the first two planes as a track seed. All combinatorial track seeds are considered, including both true signal hits and noise hits.
# * Track fitting with a simple chi2 minimization

# Global settings and variables
# =================
## RUN CONFIGURATION
# =================

rdm = R.TRandom3()
numberOfEvents=1        #number of events to be simulated 
numberOfPlanes=   2        #number of tracking planes on each side of magnet
Cut1=          100.        # cut on chisquared for first 3 hits
Cut2=          100.        # cut on chisquared for next hits
Cut3= (4.*numberOfPlanes-5.)*2.5 # cut on total chisquared
beamMomentum=    0.05    # GeV

## SPECTROMETER DESCRIPTION
# =================
spectrometerLength=30.   #(cm)
distBetweenPlanes= spectrometerLength/(2.*numberOfPlanes-1.)
pixelSize=  0.002       # (cm)
resolution=  float(0.0006)     #measurement resolution (cm)
tailAmplitude=   0.1     #probability of badly measured hit
tailWidth=   0.0018      #resolution of badly measured hit (cm)

# The multiple scattering times momentum per plane is estimated as follows
# Rl 50mu Si = 5.3e-4, Rl 50cm He Rl 8.8e-5
# multScattAngle=0.0175*sqrt(Rl)*(1+0.125*log(10Rl)/log(10))/sqrt(2)

multScattAngle= 0.0002  # effective theta0*E(GeV) (mult scatt) per plane
thetaxz=        0.0     # incident track angle in the xz plane

# There is an adjustable threshold with which we can get the noise occupancy
# as low is 10^-7, at a cost in the hit efficiency

noiseOccupancy=  0.000005  # noise probability in readout time window
hitEfficiency =  0.97    # probability for a track to make a hit
                                        #  assume: noise=0.000001 eff=0.93
                                        #                0.00001  eff=0.97
                                        #                0.0001   eff=0.98
                                        #                0.001    eff=0.995

nparameters=         5    # IMPORTANT: set equal to 5 if the field is on to check momentum.

integralBdL=     0.5    # Tesla*cm
magLength=       10.    # cm

xHits=(2*numberOfPlanes)*[0.]    # Distances (x) from first plane
ySize=(2*numberOfPlanes)*[0.]         # Half height of chip
zSize=(2*numberOfPlanes)*[0.]         # Half width of chip

## RECONSTRUCTION DATA
# =================
yHits=(2*numberOfPlanes)*[[]]  # Measurement coordinates (y) of hits
zHits=(2*numberOfPlanes)*[[]]  # Measurement coordinates (z) of hits
tracks=15*[[]]                 # Info about each reconstructed track
#tracks[0] vector of z-intercept with plane 0
#tracks[1] vector of dz/dx at plane 0
#tracks[2] vector of y-intercept with plane 0
#tracks[3] vector of dy/dx at plane 0
#tracks[4] vector of 1/p
#tracks[5]-tracks[9] same, but truth
#tracks[10]-tracks[14] errors on the parameters
#Allthough there is room for 15 tracks,
#for now these vectors have only one element. Only one track allowed.

isNoise=(2*numberOfPlanes)*[0.] # MC truth flag for each hit

debug=False                       #debug flag
firstDebugEvent=0
lastDebugEvent=20

# counts
numberOfReconstructedTracks=0
numberOfGoodReconstructedTracks=0
nTotalHits=                 0
nNoiseHitsOnTrack=          0
numberOfInefficientTracks=0
numberOfRejectedTracks=0
numberOfGoodRejectedTracks=0

# Book histograms
fout2 = R.TFile("kf_result.root", "RECREATE")
h1 = R.TH1F("h1","y0 residuals",100,-.005,.005)
h2 = R.TH1F("h2","z0 residuals",100,-.005,.005)
h3 = R.TH1F("h3","ty residuals",100,-.025,.025)
h4 = R.TH1F("h4","tz residuals",100,-.025,.025)
h5 = R.TH1F("h5","1/p residuals",100,-1./beamMomentum,1./beamMomentum)
h6 = R.TH1F("h6","y0 pull",100,-10.,10.)
h7 = R.TH1F("h7","z0 pull",100,-10.,10.)
h8 = R.TH1F("h8"," ty pull ",100,-10.,10.)
h9 = R.TH1F("h9"," tz pull ",100,-10.,10.)
h10 = R.TH1F("h10"," 1/p pull ",100,-10.,10.)
h11 = R.TH1F("h11"," z chisquared at plane 2 ",80,0.,24.)
h12 = R.TH1F("h12"," z chisquared at plane 3 ",80,0.,24.)
h13 = R.TH1F("h13"," total chisquared ",80,0.,24.)
h14 = R.TH1F("h14"," total chisquared ",80,0.,24.)
h15 = R.TH1F("h15"," z chisquared at plane 4",80,0.,24.)
h16 = R.TH1F("h16"," z chisquared at plane 5",80,0.,24.)

# Event simulation
# =================
## Generate hits in detector planes
#
# propagate from one plane to the next in a field free region (a simple straight line)
def propagateStraight(firstplane, nextY, nextZ, nextdYdX, nextdZdX):
  
  for j in range(firstplane, firstplane+numberOfPlanes):
    if(debug): print(" propagating track. Now at plane ", j)
    nh=0
    y,z,r=0.,0.,0.

    # track impact in first plane
    if j==firstplane:  
      y=nextY
      z=nextZ
    else:
    # track impact in first plane
      nextY+=distBetweenPlanes*nextdYdX
      nextZ+=distBetweenPlanes*nextdZdX
      y=nextY
      z=nextZ
    
    # add multiple scattering      
    r=rdm.Gaus()/beamMomentum
    nextdYdX+=(r*multScattAngle)           # update angle due to MS
    r=rdm.Gaus()/beamMomentum
    nextdZdX+=(r*multScattAngle)           # update angle due to MS
    if(debug): print(" track y z at plane ", j, " ", y, " ", z, " angles " , nextdYdX, " ", nextdZdX)
    
    # To take into account the detector efficiency
    r=rdm.Uniform()
 
    # If this gives a hit
    if (r<hitEfficiency and fabs(nextY)<ySize[j] and fabs(nextZ)<zSize[j]): 
      # then smear y impact by resolution
      r1=rdm.Gaus()
      y+=r1*resolution                     

      # sometimes give extra smear
      r1=rdm.Uniform()                     
      if(r1<tailAmplitude):
        # extra smear (resolution tail)
        r2=rdm.Gaus()
        y+=r2*tailWidth                        

      # then smear z impact by resolution
      r3=rdm.Gaus()
      z+=r3*resolution
      # do we need extra smear?
      r3=rdm.Uniform()                      
      if(r3<tailAmplitude):
        # extra smear (resolution tail)
        r2=rdm.Gaus()
        z+=r2*tailWidth                       

      # update vector of y coords in plane j
      yHits[j].append(y)
      # update vector of z coords in plane j
      zHits[j].append(z)

      if(debug): print(" hit ", nh, " at plane ", j, " y " , y , " z " , z , " expect y z ", nextY , " " , nextZ)

      # update noise flag
      isNoise[j].append(0) 
      nh+=1

    # add noise to 500x500 pixel area ( around real hit )
    noise=rdm.Poisson(250000*noiseOccupancy)
    if(noise>0):
      for k in range(noise):
        r=rdm.Uniform()                  # placement of noise hit
        ynoise= y+(r-0.5)*(500.*pixelSize)
        r=rdm.Uniform()
        znoise= z+(r-0.5)*(500.*pixelSize)

        yHits[j].append(ynoise)          # update vector of y coords
        zHits[j].append(znoise)          # update vector of z coords
        isNoise[j].append(1)             # update truth flag
        nh+=1

  return [nextY, nextZ, nextdYdX, nextdZdX]
 
## Simulate the whole track 
#
# (straight tracks hiting plans before the magnet, then through the magnent, then straight tracks through the plans after the magnet)
def propagateTrack():

  # start at plane 0
  nextY=0.
  nextdYdX=0.
  nextZ=0.
  nextdZdX=thetaxz

  # propagate track through the planes before the magnet
  [nextY, nextZ, nextdYdX, nextdZdX] = propagateStraight(0,nextY,nextZ,nextdYdX,nextdZdX)

  #Trace through magnet (to a good approximation),
  dtheta=0.003*integralBdL/beamMomentum
  #from plane 1 to the magnet center
  nextY+=(nextdYdX*distBetweenPlanes/2.)             
  ang=atan(nextdYdX)+dtheta
  #and on to the next plane
  nextY+=(tan(ang)*distBetweenPlanes/2.)             

  # update angle
  nextdYdX=tan(ang)                                  
  nextZ+=(distBetweenPlanes*nextdZdX)

  # propagate track through the planes after the magnet
  [nextY, nextZ, nextdYdX, nextdZdX] = propagateStraight(numberOfPlanes,nextY,nextZ,nextdYdX,nextdZdX)
  
# Kalman Filter
# =================

#### Predict and Update (in a local plane)
# 
# State vetector a the detector plane $k$ (in the $x-z$ cooridinate system): 
# $$
# x_k = \begin{pmatrix}
# z \\
# dz/dx
# \end{pmatrix}
# $$
#
# Propagation from the detector plane $k-1$ to the plane $k$:
# $$
# x_k = F_k x_{k-1}
# $$
# In our case, the propagation matrix $F_k$ is very simple (and the same for all planes, assuming no magnet)
# $$
# F_k = F_z \equiv \begin{pmatrix}
# 1 & d \\
# 0 & 1
# \end{pmatrix}
# $$
# So that the propagation is
# $$
# x_k = F_k x_{k-1} = \begin{pmatrix}
# 1 & d \\
# 0 & 1 
# \end{pmatrix}
# \begin{pmatrix}
# z_{k-1} \\
# (\frac{dz}{dx})_{k-1}
# \end{pmatrix}
# $$
# where $d$ is the distance between the two planes.
#
# To take into account the multi-scattering effect, one can add a noise term $\omega$ to the state vector:
# $$
# x_k = F_k x_{k-1} + \omega
# $$
# with $E(\omega)=0$ and the covariance matrix
# $$
# cov(\omega) = Q_z \equiv \begin{pmatrix}
# \theta_{MS}^2 d^2  &  \theta_{MS}^2 d \\
#  \theta_{MS}^2 d   &  \theta_{MS} 
# \end{pmatrix}
# $$
# where $\theta_{MS}$ is the average multi-scattering angle.
#
# Project the state vector $x_k$ to get the measurement $m_k$:
# $$
# m_k = H x_k + \epsilon
# $$
# where $H$ is the projection matrix with a simple form
# $$
# H = \begin{pmatrix}
# 1 & 0 \\
# 0 & 1 
# \end{pmatrix}
# $$
# and $\epsilon$ is the measurement uncertainty with $E(\epsilon)=0$ and a covariance matrix:
# $$
# cov(\epsilon) = \begin{pmatrix}
# \sigma^2 & 0 \\
# 0 & 0
# \end{pmatrix}
# $$
# where $\sigma$ is the detector resolution (we can only measure the hit position, not the direction).
#
#### Prediction:
#
# $$
# \tilde{x}_{k|k-1} = F_k \tilde{x}_{k-1} \\
# C_{k|k-1} = F_k^{T} C_{k-1} F_k + Q_k = F_z^T C_{k-1} F_z + Q_z \\
# $$
# $$
# C_{k-1} = \begin{pmatrix}
# \sigma^2 & \sigma^2/d \\
# \sigma^2/d & 2\sigma^2/d^2
# \end{pmatrix}
# $$
# 
#### Update:
#
# the weighted average of the measurement and the prediction.
# $$
# \tilde{x}_{k|k} = (W_{k|k-1} + W_m)^{-1} ( W_{k|k-1} \tilde{x}_{k|k-1} + W_m x_m) \\
# x_m = H^T m_k \\
# $$
# with weight matrices:
# $$
# W_m = cov(\epsilon)^{-1}
# $$
# $$
# W_{k|k-1} = C_{k|k-1}^{-1}
# $$

def kalmanFilter(p1, ihit, z, C):
  # Propagates a track candidate from detector plane p1-1 to detector plane p1
  # as a straight line in x-z (the non-bending plane)
  # updates the track parameters and their error matrix in x-z
  # returns the chisquared at detector plane p1 for hit number ihit in this plane

  import ROOT as R
 
  s2=resolution*resolution
  #use here a fixed momentum estimate
  pinv = 1./beamMomentum 
  #average multiple scattering angle
  t0=multScattAngle*pinv 
  #propagator F to next plane
  Fz = np.zeros(shape=(2,2))
  FTz = np.zeros(shape=(2,2))
  Fz[0][0]=1
  Fz[0][1]=distBetweenPlanes
  Fz[1][0]=0
  Fz[1][1]=0

  #the transpose of F
  FTz=np.transpose(Fz)

  #multiple scattering contribution to covariance of extrapolation
  Qz = np.zeros(shape=(2,2))

  Qz[0][0]=t0*t0*distBetweenPlanes*distBetweenPlanes
  Qz[0][1]=t0*t0*distBetweenPlanes
  Qz[1][0]=t0*t0*distBetweenPlanes
  Qz[1][1]=t0*t0

  #covariance of extrapolation
  #Cpz = Fz*C*FTz+Qz
  Cpz = np.dot(np.dot(Fz, C), FTz)+Qz

  #predicted state at next plane
  zpred = np.zeros(shape=(2,1))
  #zpred = Fz*z
  zpred = np.dot(Fz, z)

  #covariance matrix of updated state 
  # covariance of the prediction
  Cinv = np.zeros(shape=(2,2))
  # covariance of the measurement
  Minv = np.zeros(shape=(2,2))
  Minv[0][0]=1./s2
  #add weights
  Cinv = inv(Cpz) + Minv 
  C=inv(Cinv)

  #updated track state, use the weighted average of the measurement and the prediction.
  # Note that An equivalent way is to use the Kalman gain matrix K
  znew = np.zeros(shape=(2,1))
  #new z weighted by 1/s2
  znew[0][0] = zHits[p1][ihit]/s2
  znew[1][0]=0.
  #add predicted z - remember Cpz is inverted
  #z=C*(Cpz*zpred + znew)   
  z=np.dot(C, (np.dot(Cpz, zpred) + znew))   

  #the residual and the chisquared (the returned float)
  r =(zHits[p1][ihit]-zpred[0][0])
  #covariance matrix of the residual
  R = s2 + Cpz[0][0]
  chi2=r*r/R
  return [chi2, zpred, z, C]

## Global Chi2 (the whole track)

def globalChi2(ihits, x, C):
  #global chi2-fit to x-y hits in 2*numberOfPlanes pixel planes 
  #nparameters=4 indicates that the field is off

  pinv=1./beamMomentum
  # d(momentum)/d(tan(delta_theta))
  dpdt=0.003*integralBdL 
  # MS angle using an estimated 1/p
  t0=multScattAngle*pinv 
  t2=t0*t0
  s2=resolution*resolution
  d2=distBetweenPlanes*distBetweenPlanes
  # number of pixel planes
  nplane=2*numberOfPlanes 
  # 2 times that (z and y measurements)
  ndim=4*numberOfPlanes   
  #
  # The column vector of the measurements
  # - first the nplane z measurements, then the nplane y measurements 
  m = np.zeros(shape=(ndim,1))
  for i in range(nplane):
    m[i][0] = zHits[i][ihits[i]]
    m[i+nplane][0] = yHits[i][ihits[i]]

  #
  # The Covariance matrix of the measurements, including MS induced correlations
  V = np.zeros(shape=(ndim,ndim))

  V[0][0] = s2
  V[nplane][nplane] = s2

  for i in range(1, nplane):
    for j in range(i, nplane):
       V[i][j] = V[i-1][j-1] + i*j*t2*d2
       V[i+nplane][j+nplane] = V[i][j]

       if(j>i):
         V[j][i] = V[i][j]
         V[j+nplane][i+nplane] = V[j][i]

  #
  # The track state vector is defined as
  # x = (z0, z', y0, y', 1/p) with
  # track impact z0, y0 and slopes z'=dz/dx and y'=dy/dx all given at plane 0
  #
  # H projects the track state vector on the measurement base
  H = np.zeros(shape=(ndim,nparameters))

  for i in range(nplane):
    j=i+nplane
    H[i][0]=1
    H[j][2]=1
    H[i][1]=i*distBetweenPlanes
    H[j][3]=i*distBetweenPlanes

    if(i>numberOfPlanes-1 and nparameters>4): H[j][4]=dpdt*distBetweenPlanes*(0.5+i-numberOfPlanes)
  
  HT=np.transpose(H)
  #
  # Now do the linear chi2 fit
  # chi2 = (m - H*x)^T V^-1 (m - H*x)
  # In linear case, the solution is x_fit = (H^T V^-1 H)^-1 H^T V^-1 m
  # see p54 of the [slides by Peter Hansen](https://indico.nbi.ku.dk/event/1090/sessions/2365/attachments/2696/3926/trackalgs2018.pdf)
  #
  #Ctmp=HT*inv(V)*H
  Ctmp=np.dot(np.dot(HT, inv(V)), H)
  C=inv(Ctmp)
  # V is now inverse
  # C is now the covariance matrix of the fitted track state

  # x is the fitted track state vector
  #x = C*HT*V*m
  x = np.dot(np.dot(C, HT), np.dot(V, m))

  # R is the residual vector
  #R=m-H*x
  R=m-np.dot(H, x)
  RT=np.transpose(R)
 
  #Chi2=RT*V*R
  Chi2=np.dot(np.dot(RT, V), R)
  if(debug): print("  chi2 ", Chi2[0][0])
  # Return chi2 for ndim-nparameters d.o.f.
  return [Chi2[0][0], x, C]


# Reconstruct one track in 4 planes
# =================

## Plotting
#
# Draw hits in the x-z plane
ch = R.TCanvas("chits","Hits",50,50,800,600)
ch.GetFrame().SetFillColor(0)
ch.GetFrame().SetBorderSize(20)

gr_xz_sig = None
gr_xz_noise = None
list_gr_trks=[]

def drawHits(evtIndex):
  
  global gr_xz_sig, gr_xz_noise
  nhitsAll, nhitsSig, nhitsNoise=0, 0, 0
  for j in range(2*numberOfPlanes):
    nHits=len(yHits[j])
    nhitsAll += nHits
    for k in range(nHits):
      if(isNoise[j][k]): nhitsNoise+=1

  nhitsSig = nhitsAll - nhitsNoise
  # Signal hits
  gr_xz_sig = R.TGraph(nhitsSig)
  gr_xz_sig.SetMarkerStyle(20)
  # Noise hits
  gr_xz_noise = R.TGraph(nhitsNoise)
  gr_xz_noise.SetMarkerStyle(24)

  # Loop all hits
  isig, inoise=0, 0
  for j in range(2*numberOfPlanes):
    nHits=len(yHits[j])
    for k in range(nHits):
      if(isNoise[j][k]):
        gr_xz_noise.SetPoint(inoise, xHits[j], zHits[j][k])
        inoise+=1
      else:  
        gr_xz_sig.SetPoint(isig, xHits[j], zHits[j][k])
        isig+=1

  ch.cd()
  htmp=ch.DrawFrame(-5, -1, 45, 1.2)
  htmp.GetXaxis().SetTitle("X [cm]")
  htmp.GetYaxis().SetTitle("Z [cm]")
  gr_xz_sig.Draw("P") 
  gr_xz_noise.Draw("Psame") 

  leg = R.TLegend(0.6, 0.7, 0.9, 0.9)
  leg.SetFillColor(R.kWhite)
  leg.SetBorderSize(0)
  leg.SetTextSize(0.040)
  leg.AddEntry(gr_xz_sig, "Signal hits", "p")
  leg.AddEntry(gr_xz_noise, "Noise hits", "p")
  leg.Draw()

  ch.Draw()

  fout2.cd()
  ch.SaveAs("event_"+str(i)+".png")
  ch.Write("event_"+str(i))
 
# Draw hits of the track candidate found by the Kalman Filter
def showKFposterior(evtIndex, zHitsKF, zHitsKFpred, totchi2_KF, totchi2_KFfit, itrk):

  nhits = 2*numberOfPlanes
  gr_kf = R.TGraph(nhits)
  gr_kf_pred = R.TGraph(nhits)
  ic = R.kMagenta + itrk
  gr_kf.SetMarkerColor(ic)
  gr_kf.SetLineColor(ic)
  gr_kf.SetMarkerStyle(29)
  gr_kf_pred.SetMarkerColor(ic)
  gr_kf_pred.SetLineColor(ic)
  gr_kf_pred.SetMarkerStyle(34)

  # Loop all hits
  ih=0
  for j in range(2*numberOfPlanes):
    gr_kf.SetPoint(ih, xHits[j], zHitsKF[j])
    gr_kf_pred.SetPoint(ih, xHits[j], zHitsKFpred[j])
    ih+=1

  ch.cd()
  gr_kf.Draw("Pcsame") 
  gr_kf_pred.Draw("Pcsame") 

  leg = R.TLegend(0.6, 0.7, 0.9, 0.9)
  leg.SetFillColor(R.kWhite)
  leg.SetBorderSize(0)
  leg.SetTextSize(0.040)
  leg.AddEntry(gr_xz_sig, "Signal hits", "p")
  leg.AddEntry(gr_xz_noise, "Noise hits", "p")
  leg.AddEntry(gr_kf_pred, "Predicted hits (Kalman)", "pl")
  leg.AddEntry(gr_kf, "Updated hits (Kalman)", "pl")
  leg.Draw()

  tl=R.TPaveText(0.6, 0.6, 0.9, 0.7, "NDC")
  tl.SetFillColor(R.kWhite)
  tl.SetBorderSize(0)
  tl.SetTextSize(0.04)
  tl.AddText("#chi^{{2}} (Kalman)= {:.3e}".format(totchi2_KF))
  tl.AddText("#chi^{{2}} (fit)= {:.3e}".format(totchi2_KFfit))
  tl.Draw()

  ch.Draw()

  fout2.cd()
  ch.SaveAs("event_"+str(i)+"_trk_"+str(itrk)+".png")
  ch.Write("event_"+str(i)+"_trk_"+str(itrk))

## Reconstruction (track finding with the Kalman Filter, then Track Fitting)

def reco4(ibest, xbest, Cbest):

  chi2min=10000000.
  itrk = 0 # counter
  # First loop over the hits in the first plane
  # =======================================================================
  for i0 in range(len(yHits[0])):
 
    # skip hit in first plane if it is outside the beam profile
    if(fabs(yHits[0][i0])>4.*pixelSize): continue
    allsignal= not isNoise[0][i0]

    # loop over the hits in the second plane
    # =====================================================================
    for i1 in range(len(yHits[1])):

      s2=resolution*resolution
      allsignal= allsignal and (not isNoise[1][i1])
      # Use hits in the first two planes as the track seed
      #consider the xz plane - a non-bending plane
      #track state at plane 1
      z = np.zeros(shape=(2,1))
      zpred = np.zeros(shape=(2,1))
      z[0][0] = zHits[1][i1]
      z[1][0] = (zHits[1][i1]-zHits[0][i0])/distBetweenPlanes
      #its covariance
      Cz = np.zeros(shape=(2,2))
      Cz[0][0] = s2
      Cz[0][1] = s2/distBetweenPlanes
      Cz[1][0] = Cz[0][1]
      Cz[1][1] = 2*s2/distBetweenPlanes/distBetweenPlanes

      # total chi2 of the track found by the Kalman Filter
      totchi2_KF = 0
  
      # loop over hits in the third plane
      #===========================================================
      for i2 in range(len(yHits[2])):

        # Kalman Filter to extend the track to the 3rd plane
        [chi2, zpred, z, Cz] = kalmanFilter(2,i2,z,Cz)

        allsignal=allsignal and (not isNoise[2][i2])
        if(allsignal): h11.Fill(chi2)

        if(chi2 > Cut1): continue
        z2 = z
        z2pred = zpred
        totchi2_KF += chi2
   
        #loop over hits in the fourth plane
        #====================================================================================
        for i3 in range(len(yHits[3])):

          # Kalman Filter to extend the track to the 4th plane
          [chi2, zpred, z, Cz] = kalmanFilter(3,i3,z,Cz)

          allsignal=allsignal and (not isNoise[3][i3])
          if(allsignal): h12.Fill(chi2)

          if(chi2 >Cut2): continue
          z3 = z
          z3pred = zpred
          totchi2_KF += chi2

          # now we have a track candidate, move to the track fitting part

          # make a global chi2 fit and store only the best track
          # ===============================================================================
          x = np.zeros(shape=(5,1))
          C = np.zeros(shape=(5,5))
          x[4][0] = 1./beamMomentum #use here a fixed momentum estimate
          ihits=[i0,i1,i2,i3]
          [chi2, x, C] = globalChi2(ihits,x,C)

          if(chi2<chi2min):
            ibest[0]=i0
            ibest[1]=i1
            ibest[2]=i2
            ibest[3]=i3
            xbest=x
            Cbest=C
            chi2min=chi2

          # visualize
          zHitsKF=[zHits[0][i1], zHits[1][i2], z2[0][0], z3[0][0]]
          zHitsKFpred=[zHits[0][i1], zHits[1][i2], z2pred[0][0], z3pred[0][0]]
          print('zHitsKF:', zHitsKF)
          showKFposterior(i, zHitsKF, zHitsKFpred, totchi2_KF, chi2, itrk)
          itrk += 1

  return [chi2min, xbest, Cbest]

# Store tracks
# =================
def storeTrack(ibest, xbest, Cbest):
  #
  #fitted z intercept at plane 0
  tracks[0].append(xbest[0])  
  if(debug): print(" z0 ", tracks[0][0])
  #fitted z slope at plane 0
  tracks[1].append(xbest[1]) 
  if(debug): print(" dz/dx " , tracks[1][0] )
  #y intercept at plane 0
  tracks[2].append(yHits[0][ibest[0]]) 
  if(debug): print(" y0 " , tracks[2][0] )
  tracks[3].append( (yHits[1][ibest[1]]-yHits[0][ibest[0]])/distBetweenPlanes )
  if(debug): print(" dy/dx " , tracks[3][0] )
  #charge/momentum
  tracks[4].append(xbest[4])   
  if(debug): print(" 1/p " , tracks[4][0] )
  #truth
  tracks[5].append(0.)
  tracks[6].append(thetaxz)
  tracks[7].append(0.)
  tracks[8].append(0.)
  tracks[9].append(1/beamMomentum)
  #errors
  tracks[10].append(sqrt( Cbest[0] ))
  if(debug): print(" Dz0 " , tracks[10][0] )
  tracks[11].append(sqrt( Cbest[5+1] ))
  if(debug): print(" Ddz/dx " , tracks[11][0] )
  tracks[12].append(sqrt( Cbest[2*5+2]))
  if(debug): print(" Dy0 " , tracks[12][0] )
  tracks[13].append(sqrt(Cbest[3*5+3]))
  if(debug): print(" Ddy/dx " , tracks[13][0] )
  tracks[14].append(sqrt( Cbest[4*5+4] ))
  if(debug): print(" D1/p " , tracks[14][0] )

  h1.Fill( tracks[2][0]-tracks[7][0] )
  h2.Fill( tracks[0][0]-tracks[5][0] )
  h3.Fill( tracks[3][0]-tracks[8][0] )
  h4.Fill( tracks[1][0]-tracks[6][0] )
  h5.Fill( tracks[4][0]-tracks[9][0] )
  h6.Fill( (tracks[2][0]-tracks[7][0])/tracks[12][0] )
  h7.Fill( (tracks[0][0]-tracks[5][0])/tracks[10][0] )
  h8.Fill( (tracks[3][0]-tracks[8][0])/tracks[13][0] )
  h9.Fill( (tracks[1][0]-tracks[6][0])/tracks[11][0] )
  h10.Fill( (tracks[4][0]-tracks[9][0])/tracks[14][0] )

# Main Program
# =================
# geometry
for i in range(2*numberOfPlanes):
  xHits[i]=distBetweenPlanes*i
  ySize[i]=1.
  if(i>numberOfPlanes-1): ySize[i]=2.
  zSize[i]=1.

#-----------------------------------------------------------------------
# Loop over numberOfEvents
#

for i in range(numberOfEvents):

  if(i > firstDebugEvent-1 ): debug=True
  if(i > lastDebugEvent ): debug=False

  # New event
  if (debug): print(" new event " )

  # reset input and output data buffers
  for j in range(15): tracks[j]=[]
  for j in range(2*numberOfPlanes):
    yHits[j]=[]
    zHits[j]=[]
    isNoise[j]=[]
  
  #========================================================================================
  # Simulate the event
  propagateTrack()

  #========================================================================================
  # Reconstruct the event
  #
  # ---------------------------------------------------------------------------------------
  # Pattern recognition and fit
  #========================================================================================
  #
  reject=False
  # first count number of hits in each plane
  nRealHits=0
  for j in range(2*numberOfPlanes):
    nHits=len(yHits[j])
    for k in range(nHits):
      if(not isNoise[j][k]):
        nRealHits+=1
        break
    nTotalHits+=nHits
    #all the planes must fire
    if(nHits<1): reject=True           
    if (debug): print(" plane " , j , " nHits " , nHits , " nRealHits " , nRealHits )

  if(reject):
    numberOfInefficientTracks+=1
    continue

  # visualize the hits
  drawHits(i)

  if(debug): print(" start reconstruction" )

  # number of accepted track candidates.
  ntracks=0           
  xbest=np.zeros(shape=(5,1))
  Cbest=np.zeros(shape=(5,5))
  ibest=(2*numberOfPlanes)*[0.]

  #Consider all possible combinations of hits to find best combination in xz
  #Only one track is reconstructed and it must have hits in all planes
  chi2min=100000000.
  if(numberOfPlanes>2):
    #chi2min=reco6(ibest,xbest,Cbest)
    continue
  else:
    [chi2min, xbest, Cbest]=reco4(ibest,xbest,Cbest)

  #fout2.cd()
  #ch.Write("event_"+str(i))

  # Reject event if best track not good enough
  if(chi2min>Cut3):
    numberOfRejectedTracks+=1
    if(nRealHits>2*numberOfPlanes-1): numberOfGoodRejectedTracks+=1
    if(debug): print(" best track rejected chi2= " , chi2min )
    continue
  
  h13.Fill(chi2min)

  # Repeat the fit for the selected track (using the measured momentum now)
  [chi2, dummp_x, dummy_C]= globalChi2(ibest,xbest,Cbest)
  h14.Fill(chi2)

  allsignal= True
  for j in range(2*numberOfPlanes): allsignal=allsignal and (not isNoise[j][ibest[j]])

  if(debug):
    if(allsignal):
      print(" Noiseless track selected   chi2 " , chi2 )
    else:
      print(" Noisy track selected   chi2 " , chi2 )

  #Store the track
  p = 5*[0.]
  ep = (5*5)*[0.]
  for ipar in range(5):
    p[ipar]=xbest[ipar][0]
    for jpar in range(5): ep[ipar*5+jpar]=Cbest[ipar][jpar]

  storeTrack(ibest,p,ep)

  ntracks+=1
  numberOfReconstructedTracks+=1          

  if(allsignal): numberOfGoodReconstructedTracks+=1
  for j in range(2*numberOfPlanes):
    if(isNoise[j][ibest[j]]): nNoiseHitsOnTrack+=1
    #flag the hits as used (change the coordinate to out of the detector range)
    yHits[j][ibest[j]]=ySize[j]+1.

#
print(" Generated Tracks " , numberOfEvents )
print(" Reconstructed Tracks " , numberOfReconstructedTracks )
print(" Reconstructed Tracks without noise hits " , numberOfGoodReconstructedTracks )
print(" Tracks lost due to missing hit " , numberOfInefficientTracks )
print(" Tracks lost to quality cuts " , numberOfRejectedTracks )
print(" Tracks with no noise hits lost to quality cuts " , numberOfGoodRejectedTracks )
print(" Total hits " , nTotalHits )
print(" Used noise hits  " , nNoiseHitsOnTrack )
print(" Hits per track is always " , 2*numberOfPlanes )

#
# Plot the results (fit parameter - truth),
#      the pulls ( (fit parameter - truth)/ parameter error )
#      and the chisquared (hit-fit)^2/hit error^2.

R.gStyle.SetOptFit(1011)
R.gStyle.SetErrorX(0)


"""
c1 = R.TCanvas("c1"," intercept ",50,50,800,600)
c1.GetFrame().SetFillColor(0)
c1.GetFrame().SetBorderSize(20)
h1.SetMarkerColor(1)
h1.SetMarkerStyle(20)
h1.GetXaxis().SetTitle(" y0 residual (cm)")
h1.Draw("AP")
h1.Fit("gaus")
h1.Draw("same")

c2 = R.TCanvas("c2"," intercept ",70,70,800,600)
c2.GetFrame().SetFillColor(0)
c2.GetFrame().SetBorderSize(20)
h2.GetXaxis().SetTitle(" z0 residual (cm)")
h2.Draw("AP")
h2.Fit("gaus")
h2.Draw("same")

c3 = R.TCanvas("c3"," y slope ",80,80,800,600)
c3.GetFrame().SetFillColor(0)
c3.GetFrame().SetBorderSize(20)
h3.GetXaxis().SetTitle(" ty residual")
h3.Draw("AP")
h3.Fit("gaus")
h3.Draw("same")

c4 = R.TCanvas("c4"," z slope ",90,90,800,600)
c4.GetFrame().SetFillColor(0)
c4.GetFrame().SetBorderSize(20)
h4.GetXaxis().SetTitle(" tz residual")
h4.Draw("AP")
h4.Fit("gaus")
h4.Draw("same")
"""

c5 = R.TCanvas("c5","1/p",100,100,800,600)
c5.GetFrame().SetFillColor(0)
c5.GetFrame().SetBorderSize(20)
h5.GetXaxis().SetTitle("fitted 1/p residual GeV-1")
h5.Draw()
h5.Fit("gaus")
h5.Draw("same")


c6 = R.TCanvas("c6","y0 pull",120,120,800,600)
c6.GetFrame().SetFillColor(0)
c6.GetFrame().SetBorderSize(20)
h6.GetXaxis().SetTitle("y0 pull")
h6.Draw()
h6.Fit("gaus")
h6.Draw("same")
"""
c7 = R.TCanvas("c7","z0 pull",130,130,800,600)
c7.GetFrame().SetFillColor(0)
c7.GetFrame().SetBorderSize(20)
h7.GetXaxis().SetTitle("z0 pull")
h7.Draw()
h7.Fit("gaus")
h7.Draw("same")
"""
c8 = R.TCanvas("c8","y slope pull",140,140,800,600)
c8.GetFrame().SetFillColor(0)
c8.GetFrame().SetBorderSize(20)
h8.GetXaxis().SetTitle("y slope pull")
h8.Draw()
h8.Fit("gaus")
h8.Draw("same")

"""
c9 = R.TCanvas("c9","z slope pull ",140,140,800,600)
c9.GetFrame().SetFillColor(0)
c9.GetFrame().SetBorderSize(20)
h9.GetXaxis().SetTitle("z slope pull")
h9.Draw()
h9.Fit("gaus")
h9.Draw("same")
"""

c10 = R.TCanvas("c10"," 1/p pull",140,140,800,600)
c10.GetFrame().SetFillColor(0)
c10.GetFrame().SetBorderSize(20)
h10.GetXaxis().SetTitle(" 1/p pull")
h10.Draw()
h10.Fit("gaus")
h10.Draw("same")


c11 = R.TCanvas("c11"," chi2 ",150,150,800,600)
c11.GetFrame().SetFillColor(0)
c11.GetFrame().SetBorderSize(20)
h11.GetXaxis().SetTitle(" chi2(z) at plane 2")
h11.Draw()

"""
c15 = R.TCanvas("c15"," chi2 ",155,155,800,600)
c15.GetFrame().SetFillColor(0)
c15.GetFrame().SetBorderSize(20)
h15.GetXaxis().SetTitle(" chi2(z) at plane 4")
h15.Draw()

c12 = R.TCanvas("c12"," chi2 ",160,160,800,600)
c12.GetFrame().SetFillColor(0)
c12.GetFrame().SetBorderSize(20)
h12.GetXaxis().SetTitle(" chi2(z) at plane 3")
h12.Draw()

c16 = R.TCanvas("c16"," chi2 ",165,165,800,600)
c16.GetFrame().SetFillColor(0)
c16.GetFrame().SetBorderSize(20)
h16.GetXaxis().SetTitle(" chi2(z) at plane 5")
h16.Draw()
"""

c13 = R.TCanvas("c13"," chi2 ",170,170,800,600)
c13.GetFrame().SetFillColor(0)
c13.GetFrame().SetBorderSize(20)
h13.GetXaxis().SetTitle(" global chi2 with fixed MS error")
h13.Draw()

"""
c14 = R.TCanvas("c14"," chi2 ",180,180,800,600)
c14.GetFrame().SetFillColor(0)
c14.GetFrame().SetBorderSize(20)
h14.GetXaxis().SetTitle(" global chi2 with variable MS error")
h14.Draw()
"""

fout2.cd()
h1.Write()
h1.Write() 
h2.Write() 
h3.Write() 
h4.Write() 
h5.Write() 
h6.Write() 
h7.Write() 
h8.Write() 
h9.Write() 
h10.Write()
h11.Write()
h12.Write()
h13.Write()
h14.Write()
h15.Write()
h16.Write()
fout2.Close()
