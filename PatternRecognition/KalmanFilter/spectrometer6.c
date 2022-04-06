#include<iostream>
#include<algorithm>
#include<cstring>
#include<string>
#include<vector>
#include<cmath>
#include "TRandom3.h"
#include "TAxis.h"
#include "TH1.h"
#include "TRandom.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TFrame.h"
#include "TMatrixD.h"
#include "TROOT.h"

using namespace std;
 // Demonstrate track fit method for a simple example of horizontal tracks
 // passing 4 or 6 pixel tracking planes along x, each measuring coordinates (y,z).
 // A spectrometer magnet is inserted the middle of the telescope.
 //Everything is in a Helium bag  

  // y is up
  // x=0, y=0, z=0 at the first plane.
  // dy/dx = 0 at the first plane.

  // here are the planes for a choice of 4 planes with distBetweenPlanes=10.:
  //  I             I    magnet   I             I
  // 0cm--------- 10cm-----------20cm----------30cm---------->x-axis

  //RUN CONFIGURATION

  TRandom3 rdm;
  const int numberOfEvents=5000;        //number of events to be simulated   
  const int numberOfPlanes=   2;        //number of tracking planes on each side of magnet
  const float Cut1=          8.;        // cut on chisquared for first 3 hits
  const float Cut2=          8.;        // cut on chisquared for next hits
  const float Cut3= (4.*numberOfPlanes-5.)*2.5; // cut on total chisquared
  const float beamMomentum=    0.05;    // GeV

  //SPECTROMETER DESCRIPTION

  const float spectrometerLength=30.;   //(cm)
  const float distBetweenPlanes= spectrometerLength/(2.*numberOfPlanes-1.);
  const double pixelSize=  0.002;       // (cm)
  const double resolution=  0.0006;     //measurement resolution (cm)
  const float tailAmplitude=   0.1;     //probability of badly measured hit
  const float tailWidth=   0.0018;      //resolution of badly measured hit (cm)

// The multiple scattering times momentum per plane is estimated as follows
// Rl 50mu Si = 5.3e-4, Rl 50cm He Rl 8.8e-5
// multScattAngle=0.0175*sqrt(Rl)*(1+0.125*log(10Rl)/log(10))/sqrt(2)

  const double multScattAngle= 0.0002;  // effective theta0*E(GeV) (mult scatt) per plane
  const double thetaxz=        0.0;     // incident track angle in the xz plane

 
  // There is an adjustable threshold with which we can get the noise occupancy
  // as low is 10^-7, at a cost in the hit efficiency
  const float noiseOccupancy=  0.00001;  // noise probability in readout time window
  const float hitEfficiency =  0.97;    // probability for a track to make a hit
                                        //  assume: noise=0.000001 eff=0.93
                                        //                0.00001  eff=0.97
                                        //                0.0001   eff=0.98
                                        //                0.001    eff=0.995


  const int nparameters=         5;    // IMPORTANT: set equal to 5 if the field is on to check momentum.

  const float integralBdL=     0.5;    // Tesla*cm
  const float magLength=       10.;    // cm
  double xHits[2*numberOfPlanes];    // Distances (x) from first plane
  double ySize[2*numberOfPlanes];         // Half height of chip
  double zSize[2*numberOfPlanes];         // Half width of chip

  //RECONSTRUCTION DATA
  vector<double> yHits[2*numberOfPlanes];   //Measurement coordinates (y) of hits
  vector<double> zHits[2*numberOfPlanes];   //Measurement coordinates (z) of hits
  vector<float> tracks[15];                 //Info about each reconstructed track
//tracks[0] vector of z-intercept with plane 0
//tracks[1] vector of dz/dx at plane 0
//tracks[2] vector of y-intercept with plane 0
//tracks[3] vector of dy/dx at plane 0
//tracks[4] vector of 1/p
//tracks[5]-tracks[9] same, but truth
//tracks[10]-tracks[14] errors on the parameters
//Allthough there is room for 15 tracks,
//for now these vectors have only one element. Only one track allowed.

  vector<bool> isNoise[2*numberOfPlanes]; //MC truth flag for each hit

  bool debug=false;                       //debug flag
  int  firstDebugEvent=0;
  int  lastDebugEvent=20;  

  //counts
  int numberOfReconstructedTracks=0;
  int numberOfGoodReconstructedTracks=0;
  int nTotalHits=                 0;
  int nNoiseHitsOnTrack=          0;
  int numberOfInefficientTracks=0;
  int numberOfRejectedTracks=0;
  int numberOfGoodRejectedTracks=0;

  // Book histograms
  TH1F* h1 = new TH1F("h1","y0 residuals",100,-.005,.005);
  TH1F* h2 = new TH1F("h2","z0 residuals",100,-.005,.005);
  TH1F* h3 = new TH1F("h3","ty residuals",100,-.025,.025);
  TH1F* h4 = new TH1F("h4","tz residuals",100,-.025,.025);
  TH1F* h5 = new TH1F("h5","1/p residuals",100,-1./beamMomentum,1./beamMomentum);
  TH1F* h6 = new TH1F("h6","y0 pull",100,-10.,10.);
  TH1F* h7 = new TH1F("h7","z0 pull",100,-10.,10.);
  TH1F* h8 = new TH1F("h8"," ty pull ",100,-10.,10.);
  TH1F* h9 = new TH1F("h9"," tz pull ",100,-10.,10.);
  TH1F* h10 = new TH1F("h10"," 1/p pull ",100,-10.,10.);
  TH1F* h11 = new TH1F("h11"," z chisquared at plane 2 ",80,0.,24.);
  TH1F* h12 = new TH1F("h12"," z chisquared at plane 3 ",80,0.,24.);
  TH1F* h13 = new TH1F("h13"," total chisquared ",80,0.,24.);
  TH1F* h14 = new TH1F("h14"," total chisquared ",80,0.,24.);
  TH1F* h15 = new TH1F("h15"," z chisquared at plane 4",80,0.,24.);
  TH1F* h16 = new TH1F("h16"," z chisquared at plane 5",80,0.,24.);

//**********************************************************************
void propagateStraight(int firstplane, float& nextY, float& nextZ, float& nextdYdX, float& nextdZdX) { 
    //
    // propagate from one plane to the next in a field free region
    //-----------------------------------------------------------------------

    for(int j=firstplane; j<firstplane+numberOfPlanes; j++) {    
      if(debug) cout << " propagating track. Now at plane " << j << endl;
      int nh=0;
      float y,z,r;

      if(j==firstplane) {
        y=nextY;                            // track impact in first plane
        z=nextZ;                         
      }else{
      //extrapolate true track to next plane
        nextY+=distBetweenPlanes*nextdYdX;
        nextZ+=distBetweenPlanes*nextdZdX;
        y=nextY;                            // track impact in second plane
        z=nextZ;                         
      }
       //add multiple scattering
        r=rdm.Gaus()/beamMomentum;
        nextdYdX+=(r*multScattAngle);           // update angle due to MS
        r=rdm.Gaus()/beamMomentum;
        nextdZdX+=(r*multScattAngle);           // update angle due to MS
        if(debug) cout << " track y z at plane " << j << " "
                       << " " << y << " "
                       << z << " angles " << nextdYdX << " " << nextdZdX << endl;

        r=rdm.Uniform();

        // If this gives a hit
        if(r<hitEfficiency && fabs(nextY)<ySize[j] && fabs(nextZ)<zSize[j]) {
          float r1=rdm.Gaus();
          y+=r1*resolution;                     // then smear impact by resolution
          r1=rdm.Uniform();                     // sometimes give extra smear
          if(r1<tailAmplitude) {
            float r2=rdm.Gaus();
            y+=r2*tailWidth;                        // extra smear (resolution tail)
          }
          float r3=rdm.Gaus();
          z+=r3*resolution;                      // smear impact by resolution
          r3=rdm.Uniform();                      // do we need extra smear?
          if(r3<tailAmplitude) {
            float r2=rdm.Gaus();
            z+=r2*tailWidth;                       // extra smear (resolution tail)
          }


          yHits[j].push_back(y);                  // update vector of y coords in plane j
          zHits[j].push_back(z);                  // update vector of z coords in plane j
          if(debug) cout << " hit " << nh << " at plane " << j <<
	     	          " y " << y << " z " << z << " expect y z "
                              << nextY << " " << nextZ << endl;
        isNoise[j].push_back(false);            // update noise flag
        nh++;
      }

      // add noise to 500x500 pixel area ( around real hit )
      int noise=rdm.Poisson(250000*noiseOccupancy);
      if(noise>0) {
        for(int k=0;k<noise;k++) {
          r=rdm.Uniform();                  // placement of noise hit
          float ynoise= y+(r-0.5)*(500.*pixelSize);
          r=rdm.Uniform();
          float znoise= z+(r-0.5)*(500.*pixelSize);

          yHits[j].push_back(ynoise);          // update vector of y coords
          zHits[j].push_back(znoise);          // update vector of z coords
          isNoise[j].push_back(true);             // update truth flag
          nh++;
        }
      }

    }                                       //end plane simulation loop
}
//**********************************************************************
void propagateTrack() {
    //==========================================================================================
    // Simulate the event
    //==========================================================================================
    // start at plane 0
    float nextY=0.;
    float nextdYdX=0.;
    float nextZ=0.;
    float nextdZdX=thetaxz;

    // propagate track through the planes before the magnet
    propagateStraight(0,nextY,nextZ,nextdYdX,nextdZdX);

    //Trace through magnet (to a good approximation),
    float dtheta=0.003*integralBdL/beamMomentum;
    nextY+=(nextdYdX*distBetweenPlanes/2.);             //from plane 1 to the magnet center
    float ang=atan(nextdYdX)+dtheta;
    nextY+=(tan(ang)*distBetweenPlanes/2.);             //and on to the next plane
    nextdYdX=tan(ang);                                  // update angle
    nextZ+=(distBetweenPlanes*nextdZdX);
 
    // propagate track through the planes after the magnet
    propagateStraight(numberOfPlanes,nextY,nextZ,nextdYdX,nextdZdX);
}

//*****************************************************************************************************
float kalmanFilter(int p1, int ihit, TMatrixD& z, TMatrixD& C) {
  // Propagates a track candidate from detector plane p1-1 to detector plane p1
  // as a straight line in x-z (the non-bending plane)
  // updates the track parameters and their error matrix in x-z
  // returns the chisquared at detector plane p1 for hit number ihit in this plane
 
        double s2=resolution*resolution;
        double pinv = 1./beamMomentum; //use here a fixed momentum estimate
  	double t0=multScattAngle*pinv; //average multiple scattering angle
	//propagator F to next plane
        TMatrixD Fz(2,2);
        TMatrixD FTz(2,2);
        Fz[0][0]=1;     
        Fz[0][1]=distBetweenPlanes;
        Fz[1][0]=0;     
        Fz[1][1]=1;

        FTz=Fz.T();  //the transpose of F
        Fz.T();

        //multiple scattering contribution to covariance of extrapolation
        TMatrixD Qz(2,2);

        Qz[0][0]=t0*t0*distBetweenPlanes*distBetweenPlanes;
        Qz[0][1]=t0*t0*distBetweenPlanes;
        Qz[1][0]=t0*t0*distBetweenPlanes;
        Qz[1][1]=t0*t0;

 	//covariance of extrapolation
        TMatrixD Cpz(2,2);
        Cpz = Fz*C*FTz+Qz;

        //predicted state at next plane
        TMatrixD zpred(2,1);
        zpred = Fz*z;

        //covariance matrix of updated state 
        TMatrixD Cinv(2,2);
        TMatrixD Minv(2,2);
        Minv.Zero();
        Minv[0][0]=1./s2;
        Cinv = Cpz.Invert() + Minv; //add weights
        C=Cinv.Invert();

        //updated track state
        TMatrixD znew(2,1);
        znew[0][0]=zHits[p1].at(ihit)/s2; //new z weighted by 1/s2
        znew[1][0]=0.;
        z=C*(Cpz*zpred + znew);   //add predicted z - remember Cpz is inverted
        Cpz.Invert();

        //the residual and the chisquared (the returned float)
        double r =(zHits[p1].at(ihit)-zpred[0][0]);
        double R = s2 + Cpz[0][0];
        float chi2=r*r/R;
        return chi2;
}

//*****************************************************************************************************
float globalChi2(int* ihits, TMatrixD& x, TMatrixD& C) {
  //global chi2-fit to x-y hits in 2*numberOfPlanes pixel planes 
  //nparameters=4 indicates that the field is off

  float pinv=1./beamMomentum;
  float  dpdt=0.003*integralBdL; // d(momentum)/d(tan(delta_theta))
  double t0=multScattAngle*pinv; // MS angle using an estimated 1/p
  double t2=t0*t0;
  double s2=resolution*resolution;
  double d2=distBetweenPlanes*distBetweenPlanes;
  const int nplane=2*numberOfPlanes; // number of pixel planes
  const int ndim=4*numberOfPlanes;   // 2 times that (z and y measurements)
  //
  // The column vector of the measurements
  // - first the nplane z measurements, then the nplane y measurements 
  TMatrixD m(ndim,1);
  for (int i=0 ;i<nplane;i++) {
    m[i][0]=zHits[i].at(ihits[i]);
    m[i+nplane][0]=yHits[i].at(ihits[i]);
    //cout << " z,y meas " << m[i][0] << " " << m[i+nplane][0] << endl;
  }

  //
  // The Covariance matrix of the measurements, including MS induced correlations
  TMatrixD V(ndim,ndim);

  V.Zero();
  V[0][0]=s2;
  V[nplane][nplane]=s2;
  //cout << " V meas " << 0 << " " << 0 << " " << V[0][0] << " " << V[nplane][nplane] << endl;
  for(int i=1; i<nplane; i++) {
    for(int j=i; j<nplane; j++) {
       V[i][j] = V[i-1][j-1] + i*j*t2*d2;
       V[i+nplane][j+nplane] = V[i][j];

       if(j>i) {
         V[j][i] = V[i][j];
         V[j+nplane][i+nplane] = V[j][i];
       }
       // cout << " V meas " << i << " " << j << " " << V[i][j] << " " << V[i+nplane][j+nplane] << endl;
    }
  }
  //
  // The track state vector is defined as
  // x = (z0, z', y0, y', 1/p) with
  // track impact z0, y0 and slopes z'=dz/dx and y'=dy/dx all given at plane 0
  //
  // H projects the track state vector on the measurement base
  TMatrixD H(ndim,nparameters);

  H.Zero();
  for(int i=0; i<nplane; i++) {
    int j=i+nplane;
    H[i][0]=1;
    H[j][2]=1;
    H[i][1]=i*distBetweenPlanes;
    H[j][3]=i*distBetweenPlanes;
    if(i>numberOfPlanes-1 && nparameters>4) H[j][4]=dpdt*distBetweenPlanes*(0.5+i-numberOfPlanes);
  }
  TMatrixD HT=H.T();
  H.T();
  //
  // Now do the linear chi2 fit
  C=HT*V.Invert()*H;
  C.Invert();
  // V is now inverse
  // C is now the covariance matrix of the fitted track state

  // x is the fitted track state vector
  x = C*HT*V*m;

  // R is the residual vector
  TMatrixD R=m-H*x;
  TMatrixD RT=R.T();
  R.T();
 
  TMatrixD Chi2=RT*V*R;
  if(debug) cout << "  chi2 " << Chi2[0][0] << endl;
  // Return chi2 for ndim-nparameters d.o.f.
  return Chi2[0][0];  
}

//**********************************************************************
float reco6(int* ibest,TMatrixD& xbest, TMatrixD& Cbest) {
    // =======================================================================
    //Reconstruct one track in 6 planes
    // =======================================================================

    float chi2min=10000000.;
    // loop over the hits in the first plane
    // =======================================================================
    for( int i0=0;i0< (int)yHits[0].size(); i0++) {
 
      // skip hit in first plane if it is outside the beam profile
      if(fabs(yHits[0].at(i0))>4.*pixelSize) continue;
      bool allsignal=!isNoise[0].at(i0);

      // loop over the hits in the second plane
      // =====================================================================
      for( int i1=0;i1< (int)yHits[1].size(); i1++) {

        double s2=resolution*resolution;
        allsignal= allsignal && !isNoise[1].at(i1);
	//consider the xz plane - a non-bending plane
        //track state at plane 1
        TMatrixD z(2,1);
        z[0][0]= zHits[1].at(i1);
        z[1][0]= (zHits[1].at(i1)-zHits[0].at(i0))/distBetweenPlanes ;
	//its covariance
        TMatrixD Cz(2,2);
        Cz[0][0]=s2;
        Cz[0][1]=s2/distBetweenPlanes;
        Cz[1][0]=Cz[0][1];
        Cz[1][1]=2*s2/distBetweenPlanes/distBetweenPlanes;


        // loop over hits in the third plane
        //===========================================================
        for( int i2=0;i2< (int)yHits[2].size(); i2++) {

	  float chi2 = kalmanFilter(2,i2,z,Cz);

          allsignal=allsignal && !isNoise[2].at(i2);
	  if(allsignal) h11->Fill(chi2);

 	  if(chi2 > Cut1) continue;


          //loop over hits in the fourth plane
          //====================================================================================
          for( int i3=0;i3< (int)yHits[3].size(); i3++) {

	    chi2 = kalmanFilter(3,i3,z,Cz);

            allsignal=allsignal && !isNoise[3].at(i3);
 	    if(allsignal) h12->Fill(chi2);

            if(chi2 >Cut2) continue;


            //loop over hits in the fifth plane
            //====================================================================================
            for( int i4=0;i4< (int)yHits[4].size(); i4++) {

	      chi2 = kalmanFilter(4,i4,z,Cz);

              allsignal=allsignal && !isNoise[4].at(i4);
	      if(allsignal)  h15->Fill(chi2);

              if(chi2 >Cut2) continue;

              //loop over hits in the sixth plane
              //====================================================================================
              for( int i5=0;i5< (int)yHits[5].size(); i5++) {

  	        chi2 = kalmanFilter(5,i5,z,Cz);

                allsignal=allsignal && !isNoise[5].at(i5);
	        if(allsignal) h16->Fill(chi2);

                if(chi2 >Cut2) continue;

	        // now we have a track candidate

	        // make a global chi2 fit and store only the best track
                // ===============================================================================
                TMatrixD x(5,1);
                TMatrixD C(5,5);
                x[4][0] = 1./beamMomentum; //use here a fixed momentum estimate
                int ihits[]={i0,i1,i2,i3,i4,i5};
                chi2= globalChi2(ihits,x,C);
                if(chi2<chi2min) {
                  ibest[0]=i0;
                  ibest[1]=i1;
                  ibest[2]=i2;
                  ibest[3]=i3;
                  ibest[4]=i4;
                  ibest[5]=i5;
                  xbest=x;
                  Cbest=C;
                  chi2min=chi2;
                }
 	      }
	    }
	  }
	}
      }
    }
    return chi2min;
}

//**********************************************************************
float reco4(int* ibest,TMatrixD& xbest, TMatrixD& Cbest) {
    // =======================================================================
    //Reconstruct one track in 4 planes
    // =======================================================================

    float chi2min=10000000.;
    // First loop over the hits in the first plane
    // =======================================================================
    for( int i0=0;i0< (int)yHits[0].size(); i0++) {
 
      // skip hit in first plane if it is outside the beam profile
      if(fabs(yHits[0].at(i0))>4.*pixelSize) continue;
      bool allsignal=!isNoise[0].at(i0);

      // loop over the hits in the second plane
      // =====================================================================
      for( int i1=0;i1< (int)yHits[1].size(); i1++) {

        double s2=resolution*resolution;
        allsignal= allsignal && !isNoise[1].at(i1);
	//consider the xz plane - a non-bending plane
        //track state at plane 1
        TMatrixD z(2,1);
        z[0][0]= zHits[1].at(i1);
        z[1][0]= (zHits[1].at(i1)-zHits[0].at(i0))/distBetweenPlanes ;
	//its covariance
        TMatrixD Cz(2,2);
        Cz[0][0]=s2;
        Cz[0][1]=s2/distBetweenPlanes;
        Cz[1][0]=Cz[0][1];
        Cz[1][1]=2*s2/distBetweenPlanes/distBetweenPlanes;


        // loop over hits in the third plane
        //===========================================================
        for( int i2=0;i2< (int)yHits[2].size(); i2++) {

	  float chi2 = kalmanFilter(2,i2,z,Cz);

          allsignal=allsignal && !isNoise[2].at(i2);
	  if(allsignal) h11->Fill(chi2);

 	  if(chi2 > Cut1) continue;


          //loop over hits in the fourth plane
          //====================================================================================
          for( int i3=0;i3< (int)yHits[3].size(); i3++) {


	    chi2 = kalmanFilter(3,i3,z,Cz);

            allsignal=allsignal && !isNoise[3].at(i3);
 	    if(allsignal) h12->Fill(chi2);

            if(chi2 >Cut2) continue;


 
	        // now we have a track candidate

	        // make a global chi2 fit and store only the best track
                // ===============================================================================
                TMatrixD x(5,1);
                TMatrixD C(5,5);
                x[4][0] = 1./beamMomentum; //use here a fixed momentum estimate
                int ihits[]={i0,i1,i2,i3};
                chi2= globalChi2(ihits,x,C);

                if(chi2<chi2min) {
                  ibest[0]=i0;
                  ibest[1]=i1;
                  ibest[2]=i2;
                  ibest[3]=i3;
                  xbest=x;
                  Cbest=C;
                  chi2min=chi2;
                }
	  }
	}
      }
    }
    return chi2min;
}
//*****************************************************************************************************
void storeTrack(int* ibest,float* xbest, float* Cbest){
         //
	  //Store track.
          tracks[0].push_back(xbest[0]);  //fitted z intercept at plane 0
          if(debug) cout << " z0 " << tracks[0].at(0) << endl;
          tracks[1].push_back(xbest[1]); //fitted z slope at plane 0
          if(debug) cout << " dz/dx " << tracks[1].at(0) << endl;
          tracks[2].push_back(yHits[0].at(ibest[0])); //y intercept at plane 0
          if(debug) cout << " y0 " << tracks[2].at(0) << endl;
          tracks[3].push_back( (yHits[1].at(ibest[1])-yHits[0].at(ibest[0]))/distBetweenPlanes );
          if(debug) cout << " dy/dx " << tracks[3].at(0) << endl;
	  tracks[4].push_back(xbest[4]);   //charge/momentum
          if(debug) cout << " 1/p " << tracks[4].at(0) << endl;
	  //truth
          tracks[5].push_back(0.);
          tracks[6].push_back(thetaxz);
          tracks[7].push_back(0.);
          tracks[8].push_back(0.);
          tracks[9].push_back(1/beamMomentum);
	  //errors
          tracks[10].push_back(sqrt( Cbest[0] ));
          if(debug) cout << " Dz0 " << tracks[10].at(0) << endl;
          tracks[11].push_back(sqrt( Cbest[5+1] ));
          if(debug) cout << " Ddz/dx " << tracks[11].at(0) << endl;
          tracks[12].push_back(sqrt( Cbest[2*5+2]));
          if(debug) cout << " Dy0 " << tracks[12].at(0) << endl;
          tracks[13].push_back(sqrt(Cbest[3*5+3]));
          if(debug) cout << " Ddy/dx " << tracks[13].at(0) << endl;
          tracks[14].push_back(sqrt( Cbest[4*5+4] ));
          if(debug) cout << " D1/p " << tracks[14].at(0) << endl;

	  h1->Fill( tracks[2].at(0)-tracks[7].at(0) );
	  h2->Fill( tracks[0].at(0)-tracks[5].at(0) );
	  h3->Fill( tracks[3].at(0)-tracks[8].at(0) );
	  h4->Fill( tracks[1].at(0)-tracks[6].at(0) );
	  h5->Fill( tracks[4].at(0)-tracks[9].at(0) );
	  h6->Fill( (tracks[2].at(0)-tracks[7].at(0))/tracks[12].at(0) );
	  h7->Fill( (tracks[0].at(0)-tracks[5].at(0))/tracks[10].at(0) );
	  h8->Fill( (tracks[3].at(0)-tracks[8].at(0))/tracks[13].at(0) );
	  h9->Fill( (tracks[1].at(0)-tracks[6].at(0))/tracks[11].at(0) );
	  h10->Fill( (tracks[4].at(0)-tracks[9].at(0))/tracks[14].at(0) );

}
//*********************************************************************************************
void doall() {

  // Main Program
  //

  // geometry
  for(int i=0; i<2*numberOfPlanes; i++) {
    xHits[i]=distBetweenPlanes*i;
    ySize[i]=1.;
    if(i>numberOfPlanes-1) ySize[i]=2.;
    zSize[i]=1.;
  }

  //-----------------------------------------------------------------------
  // Loop over numberOfEvents
  //

  for(int i=0; i<numberOfEvents; i++) {
  
    if(i > firstDebugEvent-1 ) debug=true;
    if(i > lastDebugEvent ) debug=false;

    // New event
    if (debug) cout << " new event " << endl;
    // reset input and output data buffers
    for (int j=0; j<15; j++) tracks[j].clear();
    for(int j=0; j<2*numberOfPlanes; j++) {
      yHits[j].clear();
      zHits[j].clear();
      isNoise[j].clear();
    }
    //========================================================================================
    // Simulate the event
    propagateTrack();

    //========================================================================================
    // Reconstruct the event
    //
    // ---------------------------------------------------------------------------------------
    // Pattern recognition and fit
    //========================================================================================
    //
    bool reject=false;
    // first count number of hits in each plane
    int nRealHits=0;
    for( int j=0; j<2*numberOfPlanes; j++) {
      int nHits=yHits[j].size();    
      for(int k=0; k<nHits; k++) {
        if(!isNoise[j].at(k)) {
	  nRealHits++;
          break;
        }
      }
      nTotalHits+=nHits;
      if(nHits<1) reject=true;           //all the planes must fire
      if (debug) cout << " plane " << j << " nHits " << nHits << " nRealHits " << nRealHits << endl;
    }

    if(reject) {
      numberOfInefficientTracks++;
      continue;
    }

    if(debug) cout << " start reconstruction" << endl;

    int ntracks=0;           // number of accepted track candidates.
    TMatrixD xbest(5,1);
    TMatrixD Cbest(5,5);
    int ibest[2*numberOfPlanes];

    //Consider all possible combinations of hits to find best combination in xz
    //Only one track is reconstructed and it must have hits in all planes
    float chi2min=100000000.;
    if(numberOfPlanes>2) {
      chi2min=reco6(ibest,xbest,Cbest);
    } else {
      chi2min=reco4(ibest,xbest,Cbest);
    }

    // Reject event if best track not good enough
    if(chi2min>Cut3)  {
      numberOfRejectedTracks++;
      if(nRealHits>2*numberOfPlanes-1) numberOfGoodRejectedTracks++;
      if(debug) cout << " best track rejected chi2= " << chi2min << endl;
      continue;
    }
    h13->Fill(chi2min);

    // Repeat the fit for the selected track (using the measured momentum now)
    float chi2= globalChi2(ibest,xbest,Cbest);
    h14->Fill(chi2);

    bool allsignal= true;
    for(int j=0; j<2*numberOfPlanes; j++) allsignal=allsignal && !isNoise[j].at(ibest[j]);

    if(debug) {
      if(allsignal) {
	cout << " Noiseless track selected   chi2 " << chi2 << endl;
      } else {
  	cout << " Noisy track selected   chi2 " << chi2 << endl;
      }
    }

//Store the track
    float p[5];
    float ep[5*5];
    for( int ipar=0; ipar<5; ipar++) {
      p[ipar]=xbest[ipar][0];
      for(int jpar=0; jpar<5; jpar++) ep[ipar*5+jpar]=Cbest[ipar][jpar];
    }
    storeTrack(ibest,p,ep);

    ntracks++;
    numberOfReconstructedTracks++;          

    if(allsignal) numberOfGoodReconstructedTracks++;
    for(int j=0; j<2*numberOfPlanes; j++) {
      if(isNoise[j].at(ibest[j])) nNoiseHitsOnTrack++;
      //flag the hits as used
      yHits[j][ibest[j]]=ySize[j]+1.;
    }
  }                                         // end event loop

  //
  cout << " Generated Tracks " << numberOfEvents << endl;
  cout << " Reconstructed Tracks " << numberOfReconstructedTracks << endl;
  cout << " Reconstructed Tracks without noise hits " << numberOfGoodReconstructedTracks << endl;
  cout << " Tracks lost due to missing hit " << numberOfInefficientTracks << endl;
  cout << " Tracks lost to quality cuts " << numberOfRejectedTracks << endl;
  cout << " Tracks with no noise hits lost to quality cuts " << numberOfGoodRejectedTracks << endl;
  cout << " Total hits " << nTotalHits << endl;
  cout << " Used noise hits  " << nNoiseHitsOnTrack << endl;
  cout << " Hits per track is always " << 2*numberOfPlanes << endl;

  //
  // Plot the results (fit parameter - truth),
  //      the pulls ( (fit parameter - truth)/ parameter error )
  //      and the chisquared (hit-fit)^2/hit error^2.

  gStyle->SetOptFit(1011);
  gStyle->SetErrorX(0);

  
   /*  
  TCanvas *c1 = new TCanvas("c1"," intercept ",50,50,800,600);
  c1->GetFrame()->SetFillColor(0);
  c1->GetFrame()->SetBorderSize(20);
  h1->SetMarkerColor(1);
  h1->SetMarkerStyle(20);
  h1->GetXaxis()->SetTitle(" y0 residual (cm)");
  h1->Draw("AP");
  h1->Fit("gaus");
  h1->Draw("same");

  TCanvas *c2 = new TCanvas("c2"," intercept ",70,70,800,600);
  c2->GetFrame()->SetFillColor(0);
  c2->GetFrame()->SetBorderSize(20);
  h2->GetXaxis()->SetTitle(" z0 residual (cm)");
  h2->Draw("AP");
  h2->Fit("gaus");
  h2->Draw("same");

  TCanvas *c3 = new TCanvas("c3"," y slope ",80,80,800,600);
  c3->GetFrame()->SetFillColor(0);
  c3->GetFrame()->SetBorderSize(20);
  h3->GetXaxis()->SetTitle(" ty residual");
  h3->Draw("AP");
  h3->Fit("gaus");
  h3->Draw("same");

 TCanvas *c4 = new TCanvas("c4"," z slope ",90,90,800,600);
  c4->GetFrame()->SetFillColor(0);
  c4->GetFrame()->SetBorderSize(20);
  h4->GetXaxis()->SetTitle(" tz residual");
  h4->Draw("AP");
  h4->Fit("gaus");
  h4->Draw("same");
  */

  TCanvas *c5 = new TCanvas("c5","1/p",100,100,800,600);
  c5->GetFrame()->SetFillColor(0);
  c5->GetFrame()->SetBorderSize(20);
  h5->GetXaxis()->SetTitle("fitted 1/p residual GeV-1");
  h5->Draw();
  h5->Fit("gaus");
  h5->Draw("same");


  TCanvas *c6 = new TCanvas("c6","y0 pull",120,120,800,600);
  c6->GetFrame()->SetFillColor(0);
  c6->GetFrame()->SetBorderSize(20);
  h6->GetXaxis()->SetTitle("y0 pull");
  h6->Draw();
  h6->Fit("gaus");
  h6->Draw("same");
  /*
  TCanvas *c7 = new TCanvas("c7","z0 pull",130,130,800,600);
  c7->GetFrame()->SetFillColor(0);
  c7->GetFrame()->SetBorderSize(20);
  h7->GetXaxis()->SetTitle("z0 pull");
  h7->Draw();
  h7->Fit("gaus");
  h7->Draw("same");
  */
  TCanvas *c8 = new TCanvas("c8","y slope pull",140,140,800,600);
  c8->GetFrame()->SetFillColor(0);
  c8->GetFrame()->SetBorderSize(20);
  h8->GetXaxis()->SetTitle("y slope pull");
  h8->Draw();
  h8->Fit("gaus");
  h8->Draw("same");

  /*
  TCanvas *c9 = new TCanvas("c9","z slope pull ",140,140,800,600);
  c9->GetFrame()->SetFillColor(0);
  c9->GetFrame()->SetBorderSize(20);
  h9->GetXaxis()->SetTitle("z slope pull");
  h9->Draw();
  h9->Fit("gaus");
  h9->Draw("same");
  */

  TCanvas *c10 = new TCanvas("c10"," 1/p pull",140,140,800,600);
  c10->GetFrame()->SetFillColor(0);
  c10->GetFrame()->SetBorderSize(20);
  h10->GetXaxis()->SetTitle(" 1/p pull");
  h10->Draw();
  h10->Fit("gaus");
  h10->Draw("same");


  TCanvas *c11 = new TCanvas("c11"," chi2 ",150,150,800,600);
  c11->GetFrame()->SetFillColor(0);
  c11->GetFrame()->SetBorderSize(20);
  h11->GetXaxis()->SetTitle(" chi2(z) at plane 2");
  h11->Draw();

  /*
  TCanvas *c15 = new TCanvas("c15"," chi2 ",155,155,800,600);
  c15->GetFrame()->SetFillColor(0);
  c15->GetFrame()->SetBorderSize(20);
  h15->GetXaxis()->SetTitle(" chi2(z) at plane 4");
  h15->Draw();

  TCanvas *c12 = new TCanvas("c12"," chi2 ",160,160,800,600);
  c12->GetFrame()->SetFillColor(0);
  c12->GetFrame()->SetBorderSize(20);
  h12->GetXaxis()->SetTitle(" chi2(z) at plane 3");
  h12->Draw();

  TCanvas *c16 = new TCanvas("c16"," chi2 ",165,165,800,600);
  c16->GetFrame()->SetFillColor(0);
  c16->GetFrame()->SetBorderSize(20);
  h16->GetXaxis()->SetTitle(" chi2(z) at plane 5");
  h16->Draw();
  */

  TCanvas *c13 = new TCanvas("c13"," chi2 ",170,170,800,600);
  c13->GetFrame()->SetFillColor(0);
  c13->GetFrame()->SetBorderSize(20);
  h13->GetXaxis()->SetTitle(" global chi2 with fixed MS error");
  h13->Draw();

  /*
TCanvas *c14 = new TCanvas("c14"," chi2 ",180,180,800,600);
  c14->GetFrame()->SetFillColor(0);
  c14->GetFrame()->SetBorderSize(20);
  h14->GetXaxis()->SetTitle(" global chi2 with variable MS error");
  h14->Draw();
  */

}




  
