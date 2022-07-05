#include <TH1F.h>
#include <TF1.h>
#include <TH2F.h>
#include <TGraphErrors.h>
#include <TGraphAsymmErrors.h>
#include <TFile.h>
#include <TTree.h>
#include <TBranch.h>
#include <TChain.h>
#include <TCanvas.h>
#include <iostream>
#include "TLorentzVector.h"
#include "TMath.h"
#include <vector>
#include <TLegend.h>
#include <TPaveText.h>
#include <TPaveStats.h>
#include "TStyle.h"
#include <string>
#include "TLatex.h"
#include "TPaveText.h"
#include "THStack.h"
#include <sstream>
#include <iomanip>
#include "Math/QuantFuncMathCore.h"

using namespace std;


// Code to make histograms for trigger efficiencies. To run in root:
// ex: root -l -b MkPlots.cc++(\"\")
// ex: root -l -b MkPlots.cc++'("")'

/// Functions

void setPad(TPad *p, bool hasGridX_ = true) {

  p->SetLeftMargin(0.12);
  p->SetRightMargin(0.05);
  p->SetBottomMargin(0.2);
  p->SetTopMargin(0.1);

  if (hasGridX_) p->SetGridx();
  p->SetGridy();
  p->SetTickx(1);
  p->SetTicky(1);

  p->Range(80,0.75,220,1.25);
  
  p->Draw();
  p->cd();

  gStyle->SetOptStat(0);
  gStyle->SetPaintTextFormat("3.3f");

}


void set2DPad(TPad *p) {

  p->SetLeftMargin(0.1);
  p->SetRightMargin(0.125);
  p->SetBottomMargin(0.15);
  p->SetTopMargin(0.1);
  p->SetTickx(1);
  p->SetTicky(1);
  p->Draw();
  p->cd();

  gStyle->SetOptStat(0);

}


void draw_FCC_ch() {

  TPaveText *pt_FCC = new TPaveText(0.13,0.9,0.23,1.0,"brNDC");
  pt_FCC->SetName("");
  pt_FCC->SetBorderSize(0);
  pt_FCC->SetFillStyle(0);
  pt_FCC->SetTextAlign(12);
  pt_FCC->SetTextFont(61);
  pt_FCC->SetTextSize(0.044);
  pt_FCC->AddText("FCC");
  pt_FCC->Draw("SAME"); 

  TPaveText *pt_Projected = new TPaveText(0.23,0.895,0.33,0.995,"brNDC");
  pt_Projected->SetName("");
  pt_Projected->SetBorderSize(0);
  pt_Projected->SetFillStyle(0);
  pt_Projected->SetTextAlign(12);
  pt_Projected->SetTextFont(52);
  pt_Projected->SetTextSize(0.04);
  pt_Projected->AddText("Projected");
  pt_Projected->Draw("SAME"); 

  TLatex tex_ch;
  tex_ch.SetTextAngle(0);
  tex_ch.SetTextColor(kBlack);
  tex_ch.SetTextAlign(31);
  tex_ch.SetTextSize(0.06);

  tex_ch.DrawLatexNDC(0.25,0.8,"e#mu");
 
}



void draw1DHists(TH1F *h1, TH1F *h2, string yAxisTitle_, double xMin_, double xMax_) {

  h1->SetLineWidth(2);
  h1->SetLineColor(kAzure);
  h1->SetMarkerStyle(20);
  h1->SetMarkerSize(1.2);
  h1->SetMarkerColor(kAzure);

  h1->GetXaxis()->SetLabelSize(0.);
  h1->GetYaxis()->SetLabelSize(0.03);
  h1->GetYaxis()->SetLabelOffset(0.01);

  h1->GetYaxis()->SetTitleSize(0.04);
  h1->GetYaxis()->SetTitleOffset(1.12);

  h1->GetYaxis()->SetTitle((yAxisTitle_).c_str());
  h1->GetXaxis()->SetLimits(xMin_, xMax_); 

  h1->Draw("");

  h2->SetLineWidth(2);
  h2->SetLineColor(kRed);
  h2->SetMarkerStyle(20);
  h2->SetMarkerSize(1.2);
  h2->SetMarkerColor(kRed);
  h2->Draw("SAME");

  TLegend *leg = new TLegend(0.68,0.78,0.93,0.88);  

  leg->AddEntry(h1,"Reco", "lep");
  leg->AddEntry(h2,"Gen", "lep");

  leg->SetBorderSize(0);
  leg->SetFillColor(0);
  leg->Draw("SAME");

  draw_FCC_ch();

}


void drawRatio(TH1F *h, string xAxisTitle_, double xMin_, double xMax_, string yAxisTitle_, double yMin_, double yMax_) {
  
  h->SetMinimum(yMin_); 
  h->SetMaximum(yMax_);
  h->GetXaxis()->SetLimits(xMin_, xMax_); 

  h->GetYaxis()->SetNdivisions(505);
  h->GetXaxis()->SetNdivisions(510);

  h->GetXaxis()->SetLabelSize(0.1);
  h->GetXaxis()->SetTitleSize(0.1);
  h->GetXaxis()->SetTitleOffset(0.95);

 
  h->GetXaxis()->SetTitle((xAxisTitle_).c_str());


  h->GetYaxis()->SetLabelSize(0.1);
  h->GetYaxis()->SetTitleSize(0.12);
  h->GetYaxis()->SetTitleOffset(0.37);
  h->GetYaxis()->SetTitle((yAxisTitle_).c_str());

  h->SetLineWidth(2);
  h->SetLineColor(kAzure);
  h->SetMarkerStyle(20);
  h->SetMarkerSize(1.2);
  h->SetMarkerColor(kAzure);
  h->Draw("");
 

}


void draw2DHists(TH2F *h, string multivariablesxAxisTitles_, string multivariablesyAxisTitles_) {

  gStyle->SetPalette(1);

  h->GetXaxis()->SetLabelFont(42);
  h->GetXaxis()->SetLabelSize(0.035);
  h->GetXaxis()->SetLabelOffset(0.01);
  h->GetXaxis()->SetTitleFont(42);
  h->GetXaxis()->SetTitleSize(0.035);
  h->GetXaxis()->SetTitleOffset(1.3);

  h->GetYaxis()->SetLabelFont(42);
  h->GetYaxis()->SetLabelSize(0.035);
  h->GetYaxis()->SetLabelOffset(0.01);
  h->GetYaxis()->SetTitleFont(42);
  h->GetYaxis()->SetTitleSize(0.035);
  h->GetYaxis()->SetTitleOffset(1.3);

  h->GetZaxis()->SetLabelFont(42);
  h->GetZaxis()->SetLabelSize(0.035);
  h->GetZaxis()->SetLabelOffset(0.005);
  h->GetZaxis()->SetTitleFont(42);
  h->GetZaxis()->SetTitleSize(0.035);

  h->GetXaxis()->SetTitle((multivariablesxAxisTitles_).c_str());
  h->GetYaxis()->SetTitle((multivariablesyAxisTitles_).c_str());

  //  h->Draw("colz TEXT");
  h->Draw("colz");

}



/// Main Function                                                                                                                                                               

void MkPlots(){

  TH1::SetDefaultSumw2();

  TFile* f_hists = new TFile("/depot/cms/top/miacobuc/hists.root","READ");

  string output_dir = "FinalPlots";
  system(("mkdir -p "+output_dir).c_str());

  TFile *output_hists = new TFile((output_dir+"/FinalPlots.root").c_str(),"RECREATE");

  vector<string> channels = {"emu"};

  vector<string> variables = {"t_pt"}; 
  vector<string> xAxisTitles = {"Top pT (GeV)"};
  vector<double> xMins = {0.};
  vector<double> xMaxs = {1200.};

  vector<string> multivariables = {"rvg_t_pt"} ;
  vector<string> multivariablesxAxisTitles = {"Reco Top pT (GeV)"};
  vector<string> multivariablesyAxisTitles = {"Gen Top pT (GeV)"};


  for (UInt_t i = 0; i < channels.size(); i++) {

    cout << channels[i] << endl;

    // To Make 1D Plots

    for (UInt_t j = 0; j < variables.size(); j++) {

        cout << variables[j] << endl;

	TH1F *h_Reco = (TH1F*)f_hists->Get((variables[j]).c_str());
	h_Reco->Sumw2();

	TH1F *h_Gen = (TH1F*)f_hists->Get(("gen_"+variables[j]).c_str());
	h_Gen->Sumw2();


	// To Get Ratio
	TH1F *h_Ratio = (TH1F*)h_Reco->Clone(("ratio_"+variables[j]).c_str());
	h_Ratio->Divide(h_Gen);

	h_Ratio->Write();

	TCanvas *c = new TCanvas(("c_"+variables[j]).c_str(), "", 1000., 1000.);
	TPad *p = new TPad(("p_"+variables[j]).c_str(), "", 0, 0.15, 1, 1.0); 
	setPad(p);
	draw1DHists(h_Reco,h_Gen,"Entries", xMins[j], xMaxs[j]);
	c->cd();
	TPad *p_ratio = new TPad(("p_ratio_"+variables[j]).c_str(), "", 0, 0.05, 1, 0.3);  
	setPad(p_ratio, false);
	drawRatio(h_Ratio, xAxisTitles[j], xMins[j], xMaxs[j], "Reco/Gen", 0.5, 1.5);
	
	c->SaveAs((output_dir+"/h_"+variables[j]+".pdf").c_str());      
	c->SaveAs((output_dir+"/h_"+variables[j]+".C").c_str());      
	
	c->Write();

    }

    // To Make 2D Plots

    for (UInt_t j = 0; j < multivariables.size(); j++) {
	
	TH2F *h2D_RecovGen = (TH2F*)f_hists->Get((multivariables[j]).c_str());

	TCanvas *c_2D = new TCanvas(("c_2D_"+multivariables[j]).c_str(), "", 1200., 800.);
	TPad *p_2D = new TPad(("p_2D_"+multivariables[j]).c_str(), "", 0, 0, 1, 1); 
	set2DPad(p_2D);
	draw2DHists(h2D_RecovGen, multivariablesxAxisTitles[j], multivariablesyAxisTitles[j]);
	h2D_RecovGen->Write();

	c_2D->SaveAs((output_dir+"/h2D_"+multivariables[j]+".pdf").c_str());
	c_2D->SaveAs((output_dir+"/h2D_"+multivariables[j]+".C").c_str());
  
	c_2D->Write();

    }


  }

  output_hists->Close();

}


