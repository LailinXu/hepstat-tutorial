/// \file
/// \ingroup tutorial_fit
/// \notebook
/// example of fitting a 3D function
///
/// \macro_output
/// \macro_code
///
/// \author Lailin Xu


#include "TF3.h"
#include "TH3F.h"
#include "TError.h"

// Helper function to print a matrx(m, n)
void print_matrix(TMatrixD& m_cov, int md, int nd) {

  for(int j=0; j < md; j++) {
    for(int k=0; k < md; k++) {
      std::cout << j << " " << k << " " << TMatrixDRow(m_cov, j)[k] << std::endl;
    }
  }
}

// Helper function for 3D Gaussian
Double_t gaus_3d(Double_t *x, Double_t *par) {

  // 3D Gaussian
  const int nd = 3;

  // Mean
  // x1-x2, x1-x3, x2-x3
  Double_t mean[nd] = {par[0], par[1], par[2]};

  // Covariance matrix 
  //  sig1^2+sig2^2, sig1^2, sig2^2
  //  sig1^2, sig1^2+sig3^2, sig3^2
  //  sig2^2, sig3^2, sig2^2+sig3^2
  TMatrixD cov(nd, nd);
  TMatrixDRow(cov, 0)[0] = TMath::Power(par[3], 2) + TMath::Power(par[4], 2);
  TMatrixDRow(cov, 0)[1] = TMath::Power(par[3], 2);
  TMatrixDRow(cov, 0)[2] = TMath::Power(par[4], 2);
  TMatrixDRow(cov, 1)[0] = TMath::Power(par[3], 2);
  TMatrixDRow(cov, 1)[1] = TMath::Power(par[3], 2) + TMath::Power(par[5], 2);
  TMatrixDRow(cov, 1)[2] = TMath::Power(par[5], 2);
  TMatrixDRow(cov, 2)[0] = TMath::Power(par[4], 2);
  TMatrixDRow(cov, 2)[1] = TMath::Power(par[5], 2);
  TMatrixDRow(cov, 2)[2] = TMath::Power(par[4], 2) + TMath::Power(par[5], 2);

  // Build the multi-Gaussian
  TMatrixD m_x(nd, 1);
  for(int i=0; i<nd; i++) {
    TMatrixDRow(m_x, i)[0] = x[i] - mean[i];
  }

  TMatrixD m_x_t(m_x);
  m_x_t.T();
  
  Double_t cov_dr[nd];
  TMatrixD icov(cov);
  icov.Invert(cov_dr);
  Double_t cov_d = cov.Determinant();
  Double_t icov_d = icov.Determinant();

  Double_t r = 0;
  for(int i=0; i<nd; i++) {
    for(int j=0; j<nd; j++) {
      r += TMatrixDRow(m_x_t, 0)[j] * TMatrixDRow(icov, i)[j] * TMatrixDRow(m_x, i)[0];
    }
  }

  Double_t y = 1./(TMath::Power(2*TMath::Pi(), nd/2.) * TMath::Sqrt(cov_d)) * TMath::Exp( -0.5* r ) ;

  return y;
}

void rpc_reso_fit() {
  gROOT->SetStyle("ATLAS");
  gStyle->SetPalette(1);

  TString pname = "gaus_3D_test_C";
  TFile *tfout = new TFile(pname + ".root", "RECREATE");

  
  // Plotting
  // =====================
  TCanvas *myc = new TCanvas("c", "c", 800, 600);
  myc->SetFillColor(0);
  
  int nbinsx=60, nbinsy=60, nbinsz=60;
  float xmin=-3, xmax=3;
  float ymin=-3, ymax=3;
  float zmin=-3, zmax=3;
  
  // Overlay the multi-Gaussian PDF
  
  
  // Fit
  int npar = 6; // mean: 3; sigma: 3
  TF3 *g_s = new TF3("gaus_s", gaus_3d, xmin, xmax, ymin, ymax, zmin, zmax, npar);
  g_s->SetParameter(0, 0.);
  g_s->SetParameter(1, 0.);
  g_s->SetParameter(2, 0.);
  g_s->SetParameter(3, 1.);
  g_s->SetParameter(4, 0.8);
  g_s->SetParameter(5, 1.2);
  
  TString hname = "3D";
  TH3F *h_s = new TH3F(hname, hname, nbinsx, xmin, xmax, nbinsy, ymin, ymax, nbinsz, zmin, zmax);
  h_s->FillRandom("gaus_s", 1000);
  
  h_s->GetXaxis()->SetRangeUser(-3, 3);
  h_s->GetYaxis()->SetRangeUser(-3, 3);
  h_s->GetZaxis()->SetRangeUser(-3, 3);
  h_s->GetXaxis()->SetTitle("X1");
  h_s->GetYaxis()->SetTitle("X2");
  h_s->GetZaxis()->SetTitle("X3");
  
  h_s->Draw("colz");
  
  myc->Draw();
  myc->SaveAs(pname+"_1.png");
  
  // Projection
  TH1F *hx = (TH1F*)h_s->ProjectionX();
  TH1F *hy = (TH1F*)h_s->ProjectionY();
  TH1F *hz = (TH1F*)h_s->ProjectionZ();
  
  // X-axis
  myc->Clear();
  hx->Draw();
  myc->Draw();
  myc->SaveAs(pname+"_1_X.png");
  
  // Y-axis
  myc->Clear();
  hy->Draw();
  myc->Draw();
  myc->SaveAs(pname+"_1_Y.png");
  
  // Z-axis
  myc->Clear();
  hz->Draw();
  myc->Draw();
  myc->SaveAs(pname+"_1_Z.png");
  
  // Fitting
  std::cout << "DefaultMinimizerAlgo: " << ROOT::Math::MinimizerOptions::DefaultMinimizerAlgo() << std::endl;
  std::cout << "DefaultMinimizerType: " << ROOT::Math::MinimizerOptions::DefaultMinimizerType() << std::endl;
  myc->Clear();

  myc->Clear();
  h_s->Draw();
  // Likelihood fit
  h_s->Fit("gaus_s", "L");
  // Least-square fit
  // h_s->Fit("gaus_s");
  
  myc->Draw();
  myc->SaveAs(pname+"_2.png");
  
  // Check the fit results, by converting TF3 to TH3
  g_s->SetNpx(nbinsx);
  g_s->SetNpy(nbinsy);
  g_s->SetNpz(nbinsz);
  int npx = g_s->GetNpx();
  int npy = g_s->GetNpy();
  int npz = g_s->GetNpz();
  std::cout << "npx: " << npx << " npy: " << npy << " npz: " << npz << std::endl;

  TH3F *hf = (TH3F*)g_s->CreateHistogram();

  for(int ix=1; ix < npx+1; ix++) {
    float vx = hf->GetXaxis()->GetBinCenter(ix);
    for(int iy=1; iy < npy+1; iy++) {
      float vy = hf->GetYaxis()->GetBinCenter(iy);
      for(int iz=1; iz < npz+1; iz++) {
        float vz = hf->GetZaxis()->GetBinCenter(iz);
        float vf = g_s->Eval(vx, vy, vz);
        hf->SetBinContent(ix, iy, iz, vf);
      }
    }
  }
      
  hf->Print();
  
  // Projection
  TH1F *hfx = (TH1F*)hf->ProjectionX();
  TH1F *hfy = (TH1F*)hf->ProjectionY();
  TH1F *hfz = (TH1F*)hf->ProjectionZ();
  
  // X-axis
  myc->Clear();
  // Normalization
  float intx = hx->Integral();
  hfx->Scale(intx/hfx->Integral());

  float ym0 = hx->GetMinimum();
  float ym1 = hx->GetMaximum();
  float ym2 = hfx->GetMaximum();
  if(ym1<ym2) ym1=ym2;
  hx->GetYaxis()->SetRangeUser(ym0, ym1*1.2);

  hx->Draw();
  hfx->SetLineColor(2);
  hfx->Draw("same");

  TLegend *lg = new TLegend(0.6, 0.7, 0.9, 0.9);
  lg->SetBorderSize(0);
  lg->SetFillStyle(0);
  lg->SetTextFont(42);
  lg->SetTextSize(0.04);
  lg->AddEntry(hx, "X1", "l");
  lg->AddEntry(hfx, "3D fit projection X", "l");
  lg->Draw();

  myc->Draw();
  myc->SaveAs(pname+"_1_X_fit.png");
  
  // Y-axis
  myc->Clear();
  // Normalization
  float inty = hy->Integral();
  hfy->Scale(inty/hfy->Integral());

  ym0 = hy->GetMinimum();
  ym1 = hy->GetMaximum();
  ym2 = hfy->GetMaximum();
  if(ym1<ym2) ym1=ym2;
  hy->GetYaxis()->SetRangeUser(ym0, ym1*1.2);

  hy->Draw();
  hfy->SetLineColor(2);
  hfy->Draw("same");

  lg->Clear();
  lg->AddEntry(hy, "X2", "l");
  lg->AddEntry(hfy, "3D fit projection Y", "l");
  lg->Draw();

  myc->Draw();
  myc->SaveAs(pname+"_1_Y_fit.png");
  
  // Z-axis
  myc->Clear();
  // Normalization
  float intz = hz->Integral();
  hfz->Scale(intz/hfz->Integral());

  ym0 = hz->GetMinimum();
  ym1 = hz->GetMaximum();
  ym2 = hfz->GetMaximum();
  if(ym1<ym2) ym1=ym2;
  hz->GetYaxis()->SetRangeUser(ym0, ym1*1.2);

  hz->Draw();
  hfz->SetLineColor(2);
  hfz->Draw("same");

  lg->Clear();
  lg->AddEntry(hz, "X3", "l");
  lg->AddEntry(hfz, "3D fit projection Z", "l");
  lg->Draw();

  myc->Draw();
  myc->SaveAs(pname+"_1_Z_fit.png");

  // Save files
  tfout->cd();
  h_s->Write();
  hx->Write();
  hy->Write();
  hz->Write();
  g_s->Write();
  hf->Write();
  hfx->Write();
  hfy->Write();
  hfz->Write();
  tfout->Close();
  
}
