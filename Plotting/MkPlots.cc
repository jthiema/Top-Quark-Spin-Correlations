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

void setPad(TPad *p, bool hasGridX_ = true, bool uselogy = false) {

  if (uselogy) p->SetLogy();

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
  gStyle->SetOptTitle(0);
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
  gStyle->SetOptTitle(0);

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

  tex_ch.DrawLatexNDC(0.75,0.925,"e#mu");
 
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

  TLegend *leg = new TLegend(0.83,0.78,0.93,0.88);  

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

	if (multivariablesxAxisTitles_ == "leading lepton pT (GeV)")
	{
		float AxisMin = 1000000000;
		float AxisMax = 0.00;

		int nbins_X = h->GetXaxis()->GetNbins();
		int nbins_Y = h->GetYaxis()->GetNbins();

		for (Int_t nbin_X = 0; nbin_X < nbins_X; nbin_X++)
		{

			for (Int_t nbin_Y = 0; nbin_Y < nbins_Y; nbin_Y++)
			{

				double binContent = h->GetBinContent(nbin_X+1,nbin_Y+1);

				if (binContent < AxisMin && binContent > 0.0) AxisMin = binContent;
				if (binContent > AxisMax) AxisMax = binContent;

			}
		}

		h->SetMinimum(AxisMin);
		h->SetMaximum(AxisMax);
	}

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

void reBin1D(TH1F *hfirst, TH1F *hsecond, float tailstart, float targetquantity, TH1F* arr[])
{
	/*
	int minx = 0;
	int miny = 0;
	int maxx = 0;
	int maxy = 0;
	bool posx = false;
	bool posy = false;
	int nbins_X = hfirst->GetNbinsX();
	int nbins_Y = hsecond->GetNbinsX();
	for(int i = 1; i <= nbins_X; i++)
	{
		if(posx != true & hfirst->GetBinContent(i) > 0)
		{
			posx = true;
			minx = i;
		}
		else if(hfirst->GetBinContent(i) == 0)
		{
			posx = false;
			maxx = i - 1;
			break;
		}
		else if(i == nbins_X)
		{
			maxx = i;
		}
	}
	for(int i = 1; i <= nbins_Y; i++)
	{
		if(posy != true & hsecond->GetBinContent(i) > 0)
		{
			posy = true;
			miny = i;
		}
		else if(hsecond->GetBinContent(i) == 0)
		{
			posy = false;
			maxy = i - 1;
			break;
		}
		else if(i == nbins_Y)
		{
			maxy = i;
		}
	}
	int templower = min(minx, miny);
	int tempupper = max(maxx, maxy);
	hfirst->GetXaxis()->SetLimits(hfirst->GetBinLowEdge(templower), hfirst->GetBinLowEdge(tempupper) + hfirst->GetBinWidth(tempupper)); 
	hsecond->GetXaxis()->SetLimits(hfirst->GetBinLowEdge(templower), hfirst->GetBinLowEdge(tempupper) + hfirst->GetBinWidth(tempupper));
	*/
	
	float count = 0;
	int nbins = 0;
	int totbins = 0;
	
	//cout << "===" << endl;
	for(int i = 1; i < hfirst->GetBin(1000000); i++)
	{
		totbins++;
		//cout << to_string(hfirst->GetBinContent(i)) << endl;
		if(hfirst->GetBinContent(i) >= tailstart)
		{
			nbins++;
			count = 0;
			//cout << "-" << endl;
		}
		else if(hfirst->GetBinContent(i) < tailstart)
		{
			count += hfirst->GetBinContent(i);
			if(count >= targetquantity)
			{
				nbins++;
				count = 0;
			}
			else if(i == hfirst->GetBin(1000000) - 1)
			{
				nbins++;
				count = 0;
				//cout << "-" << endl;
			}
		}
	}
	
	cout << to_string(totbins) << endl;
	cout << to_string(nbins) << endl;
	//cout << "===" << endl;
	
	int currentbin = 1;
	double* newbins = new double[nbins + 1];
	int lowbin = -1;
	//newbins[0] = hfirst->GetBinLowEdge(0);
	//cout << to_string(hfirst->GetBinLowEdge(1)) << endl;
	//cout << "-" << endl;
	
	for(int i = 1; i < hfirst->GetBin(1000000); i++)
	{
		if(hfirst->GetBinContent(i) >= tailstart)
		{
			newbins[currentbin] = hfirst->GetBinLowEdge(i) + hfirst->GetBinWidth(i);
			currentbin++;
			count = 0;
			if(lowbin < 0)
			{
				lowbin = i;
			}
			//cout << to_string( hfirst->GetBinLowEdge(i) + hfirst->GetBinWidth(i)) << endl;
			//cout << "-" << endl;
		}
		else if(hfirst->GetBinContent(i) < tailstart)
		{
			count += hfirst->GetBinContent(i);
			if(count >= targetquantity)
			{
				newbins[currentbin] =  hfirst->GetBinLowEdge(i) + hfirst->GetBinWidth(i);
				currentbin++;
				count = 0;
				if(lowbin < 0)
				{
					lowbin = i;
				}
			}
			else if(i == hfirst->GetBin(1000000) - 1)
			{
				newbins[currentbin] =  hfirst->GetBinLowEdge(i) + hfirst->GetBinWidth(i);
				currentbin++;
				count = 0;
				if(lowbin < 0)
				{
					lowbin = i;
				}
				//cout << to_string( hfirst->GetBinLowEdge(i) + hfirst->GetBinWidth(i)) << endl;
				//cout << "-" << endl;
			}
		}
	}
	newbins[0] = hfirst->GetBinLowEdge(lowbin);
	arr[0] = (TH1F*)hfirst->Rebin(nbins, hfirst->GetTitle(), newbins);
	arr[1] = (TH1F*)hsecond->Rebin(nbins, hsecond->GetTitle(), newbins);
	
	
	
}



/// Main Function                                                                                                                                                               

void MkPlots(){

  TH1::SetDefaultSumw2();

  //TFile* f_hists = new TFile("~/hists.root","READ");
  TFile* f_hists = new TFile("/depot/cms/top/miacobuc/hists.root","READ");

  string output_dir = "FinalPlots";
  system(("mkdir -p "+output_dir).c_str());

  TFile *output_hists = new TFile((output_dir+"/FinalPlots.root").c_str(),"RECREATE");

  vector<string> channels = {"emu"};

  vector<string> variables = {
	  "lep_pt", "lep_eta", "lep_phi",
	  "alep_pt", "alep_eta", "alep_phi",
	  "met_pt", "met_phi",
	  "b_pt", "b_eta", "b_phi",
	  "ab_pt", "ab_eta", "ab_phi",
	  "neu_pt", "neu_eta", "neu_phi",
	  "aneu_pt", "aneu_eta", "aneu_phi",
	  "t_pt", "t_eta", "t_phi", "t_rap",
	  "at_pt", "at_eta", "at_phi", "at_rap",
	  "tat_mass", "tat_pt", "tat_eta", "tat_phi", "tat_rap",
	  "ckk", "crr", "cnn", "crk", "ckr",
	  "cP_rk", "cM_rk", "c_hel",
	  "ll_deta", "ll_dphi", "ll_dr"
	  }; 
  vector<string> xAxisTitles = {
	  "Lep pT (GeV)", "Lep eta", "Lep phi",
	  "aLep pT (GeV)", "aLep eta", "aLep phi",
	  "MET pT (GeV)", "MET phi",
	  "Bot pT (GeV)", "Bot eta", "Bot phi",
	  "aBot pT (GeV)", "aBot eta", "aBot phi",
	  "Neu pT (GeV)", "Neu eta", "Neu phi",
	  "aNeu pT (GeV)", "aNeu eta", "aNeu phi",
	  "Top pT (GeV)", "Top eta", "Top phi", "Top rapidity",
	  "aTop pT (GeV)", "aTop eta", "aTop phi", "aTop rapidity",
	  "Top aTop mass", "Top aTop pT (GeV)", "Top aTop eta", "Top aTop phi", "Top aTop rapidity",
	  "ckk", "crr", "cnn", "crk", "ckr",
	  "cP_rk", "cM_rk", "c_hel",
	  "ll deta", "ll dphi", "ll dr"
	  };
  //vector<double> xMins = {0.};
  //vector<double> xMaxs = {1200.};

  vector<string> multivariables = {
	  "rvg_lep_pt", "rvg_lep_eta", "rvg_lep_phi",
	  "rvg_alep_pt", "rvg_alep_eta", "rvg_alep_phi",
	  "rvg_met_pt", "rvg_met_phi",
	  "rvg_b_pt", "rvg_b_eta", "rvg_b_phi",
	  "rvg_ab_pt", "rvg_ab_eta", "rvg_ab_phi",
	  "rvg_neu_pt", "rvg_neu_eta", "rvg_neu_phi",
	  "rvg_aneu_pt", "rvg_aneu_eta", "rvg_aneu_phi",
	  "rvg_t_pt", "rvg_t_eta", "rvg_t_phi", "rvg_t_rap",
	  "rvg_at_pt", "rvg_at_eta", "rvg_at_phi", "rvg_at_rap",
	  "rvg_tat_m", "rvg_tat_pt", "rvg_tat_eta", "rvg_tat_phi", "rvg_tat_rap",
	  "rvg_ckk", "rvg_crr", "rvg_cnn", "rvg_crk", "rvg_ckr",
	  "rvg_cPrk", "rvg_cMrk", "rvg_c_hel",
	  "rvg_ll_deta", "rvg_ll_dphi", "rvg_ll_dr"
	  } ;
  vector<string> multivariablesxAxisTitles = {
	  "Reco Lep pT (GeV)", "Reco Lep eta", "Reco Lep phi",
	  "Reco aLep pT (GeV)", "Reco aLep eta", "Reco aLep phi",
	  "Reco MET pT (GeV)", "Reco MET phi",
	  "Reco Bot pT (GeV)", "Reco Bot eta", "Reco Bot phi",
	  "Reco aBot pT (GeV)", "Reco aBot eta", "Reco aBot phi",
	  "Reco Neu pT (GeV)", "Reco Neu eta", "Reco Neu phi",
	  "Reco aNeu pT (GeV)", "Reco aNeu eta", "Reco aNeu phi",
	  "Reco Top pT (GeV)", "Reco Top eta", "Reco Top phi", "Reco Top rapidity",
	  "Reco aTop pT (GeV)", "Reco aTop eta", "Reco aTop phi", "Reco aTop rapidity",
	  "Reco Top aTop mass", "Reco Top aTop pT (GeV)", "Reco Top aTop eta", "Reco Top aTop phi", "Reco Top aTop rapidity",
	  "Reco ckk", "Reco crr", "Reco cnn", "Reco crk", "Reco ckr",
	  "Reco cP_rk", "Reco cM_rk", "Reco c_hel",
	  "Reco ll deta", "Reco ll dphi", "Reco ll dr"
	  };
  vector<string> multivariablesyAxisTitles = {
	  "Gen Lep pT (GeV)", "Gen Lep eta", "Gen Lep phi",
	  "Gen aLep pT (GeV)", "Gen aLep eta", "Gen aLep phi",
	  "Gen MET pT (GeV)", "Gen MET phi",
	  "Gen Bot pT (GeV)", "Gen Bot eta", "Gen Bot phi",
	  "Gen aBot pT (GeV)", "Gen aBot eta", "Gen aBot phi",
	  "Gen Neu pT (GeV)", "Gen Neu eta", "Gen Neu phi",
	  "Gen aNeu pT (GeV)", "Gen aNeu eta", "Gen aNeu phi",
	  "Gen Top pT (GeV)", "Gen Top eta", "Gen Top phi", "Gen Top rapidity",
	  "Gen aTop pT (GeV)", "Gen aTop eta", "Gen aTop phi", "Gen aTop rapidity",
	  "Gen Top aTop mass", "Gen Top aTop pT (GeV)", "Gen Top aTop eta", "Gen Top aTop phi", "Gen Top aTop rapidity",
	  "Gen ckk", "Gen crr", "Gen cnn", "Gen crk", "Gen ckr",
	  "Gen cP_rk", "Gen cM_rk", "Gen c_hel",
	  "Gen ll deta", "Gen ll dphi", "Gen ll dr"
	  };
  vector<double> tailstarts = { //-1 for let it do its default -2 for off, other nums are actual inputs
	-2, -2, -2,
	-2, -2, -2,
	-2, -2,
	-2, -2, -2,
	-2, -2, -2,
	-2, -2, -2,
	-2, -2, -2,
	-2, -2, -2, -2,
	-2, -2, -2, -2,
	-2, -2, -2, -2, -2,
	-2, -2, -2, -2, -2,
	-2, -2, -2,
	-2, -2, -2,
	
  };
  
  vector<double> mininbin = { //-1 for default, other nums are actual inputs
	-1, -1, -1,
	-1, -1, -1,
	-1, -1,
	-1, -1, -1,
	-1, -1, -1,
	-1, -1, -1,
	-1, -1, -1,
	-1, -1, -1, -1,
	-1, -1, -1, -1,
	-1, -1, -1, -1, -1,
	-1, -1, -1, -1, -1,
	-1, -1, -1,
	-1, -1, -1
  };
  
  vector<int> prebinning = { // -1 for default, -2 for off, other nums for actual vals
	-1, -1, -1,  //lep pt,eta,phi
	-1, -1, -1,  //alep pt,eta,phi
	-1, -1,  //met pt,phi
	-1, -1, -1,  //bot pt,eta,phi
	-1, -1, -1,  //abot pt,eta,phi
	-1, -1, -1,  //neu pt,eta,phi
	-1, -1, -1,  //aneu pt,eta,phi
	-1, -1, -1, -1,  //top pt,eta,phi, rap
	-1, -1, -1, -1,  //atop pt,eta,phi, rap
	-1, -1, -1, -1, -1,  //top atop mass, pt, eta, phi, rap
	-1, -1, -1, -1, -1,  //ckk crr cnn crk ckr
	-1, -1, -1,  //cprk cmrk chel
	-1, -1, -1 //ll deta,dphi,dr
  };
  
  vector<bool> uselogforscale = {
	  true, false, false,
	  true, false, false,
	  true, false,
	  true, false, false,
	  true, false, false,
	  true, false, false,
	  true, false, false,
	  true, false, false, false,
	  true, false, false, false,
	  false, true, false, false, false,
	  false, false, false, false, false,
	  false, false, false,
	  false, false, false
  };

  for (UInt_t i = 0; i < channels.size(); i++) {

    cout << channels[i] << endl;

    // To Make 1D Plots

    for (UInt_t j = 0; j < variables.size(); j++) {

        cout << variables[j] << endl;

	
	


	TH1F *h_Reco = (TH1F*)f_hists->Get((variables[j]).c_str());
	TH1F *h_Gen = (TH1F*)f_hists->Get(("gen_"+variables[j]).c_str());
	
	h_Reco->Sumw2();
	h_Gen->Sumw2();
	
	
	//cout << to_string(h_Gen1->GetXaxis()->GetXmax()) << endl;
	
	
	if(prebinning[j] != -2)
	{
		if(prebinning[j] == -1)
		{
			prebinning[j] = 40;
		}
		h_Reco = (TH1F*)h_Reco->Rebin(prebinning[j], h_Reco->GetTitle());
		h_Gen = (TH1F*)h_Gen->Rebin(prebinning[j], h_Gen->GetTitle());
	}
	
	//BELOW
	//First arg is the hist that is checked and bins tailord for
	//Second arg is a second hist that will also be fit to the binning
	//Third arg is what max of entries qualifies as part of the tailord
	//Fourth arg is min entries the rebinning will try to put together, may overshoot i.e. arg 3 is 100 arg 4 is 300, 99 + 98 + 97 + 96 is > 300
	//Fifth arg is where the hists are stored in the end, can be retrieved easily such as h1 = arr[0]
	
	if(tailstarts[j] != -2) //nonuniform binning is not off
	{
		TH1F* arr[2];
		if(tailstarts[j] == -1)
		{
			tailstarts[j] = 300;
		}
		if(mininbin[j] == -1)
		{
			mininbin[j] = 1000000;
		}
		reBin1D(h_Reco, h_Gen, tailstarts[j], mininbin[j], arr);
		h_Reco = arr[0];
		h_Gen = arr[1];
		
		reBin1D(h_Gen, h_Reco, tailstarts[j], mininbin[j], arr);
		h_Reco = arr[1];
		h_Gen = arr[0];
	}
	
	
	
	
	

	
	
	
	
	


	// To Get Ratio
	TH1F *h_Ratio = (TH1F*)h_Reco->Clone(("ratio_"+variables[j]).c_str());
	h_Ratio->Divide(h_Gen);

	h_Ratio->Write();

	TCanvas *c = new TCanvas(("c_"+variables[j]).c_str(), "", 1000., 1000.);
	TPad *p = new TPad(("p_"+variables[j]).c_str(), "", 0, 0.15, 1, 1.0); 
	setPad(p, true, uselogforscale[j]);
	//draw1DHists(h_Reco,h_Gen,"Entries", xMins[j], xMaxs[j]);
	draw1DHists(h_Reco,h_Gen,"Entries", h_Reco->GetXaxis()->GetXmin(), h_Reco->GetXaxis()->GetXmax());
	c->cd();
	TPad *p_ratio = new TPad(("p_ratio_"+variables[j]).c_str(), "", 0, 0.05, 1, 0.3);  
	setPad(p_ratio, false);
	//drawRatio(h_Ratio, xAxisTitles[j], xMins[j], xMaxs[j], "Reco/Gen", 0.5, 2.5);
	drawRatio(h_Ratio, xAxisTitles[j], h_Reco->GetXaxis()->GetXmin(), h_Reco->GetXaxis()->GetXmax(), "Reco/Gen", 0.5, 2.5);
	
	c->SaveAs((output_dir+"/h_"+variables[j]+".pdf").c_str());      
	c->SaveAs((output_dir+"/h_"+variables[j]+".C").c_str());      
	
	c->Write();

    }

    // To Make 2D Plots

    for (UInt_t j = 0; j < multivariables.size(); j++) {
	
	TH2F *h2D_RecovGen = (TH2F*)f_hists->Get((multivariables[j]).c_str());
	if(prebinning[j] != -2)
	{
		if(prebinning[j] == -1)
		{
			prebinning[j] = 20;
		}
		h2D_RecovGen = (TH2F*)h2D_RecovGen->Rebin2D(prebinning[j], prebinning[j]);
	}

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


