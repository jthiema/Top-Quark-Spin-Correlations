#include "TFile.h"
#include "TTree.h"
#include "TAttMarker.h"
#include <set>
#include <array>
#include <string>
#include <iostream>
#include <fstream>

void eff_lep_pt_cut(){
    
    gSystem->Exec("mkdir -p effvscut");
    
    TFile *minitree = new TFile("../HistogramOutput/histogram_TTJets_DiLept_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_200PU_1.root", "READ");
    
    TH1F *h_reco = (TH1F*) minitree->Get("lep_pt");
    TH1F *h_gen = (TH1F*) minitree->Get("gen_lep_pt_0"); 
    TH1F *h_ratio = (TH1F*) h_reco->Clone("rvg_lep_pt"); 
    h_ratio->Divide(h_gen); 
    
    TGraph *g_ratio = new TGraph(h_ratio->GetNbinsX());
    for (int i=0; i<=h_ratio->GetNbinsX(); i++){
        if (h_ratio->GetBinContent(i)!=0){
            g_ratio->SetPoint(i, h_ratio->GetBinCenter(i), h_ratio->GetBinContent(i));
        } else {
            continue; 
        }
    }
    
    cout << h_reco->Integral(h_reco->GetXaxis()->GetBinLowEdge(1), h_reco->GetXaxis()->GetBinUpEdge(h_reco->GetNbinsX())) << endl; 
    cout << h_gen->Integral(h_gen->GetXaxis()->GetBinLowEdge(1), h_gen->GetXaxis()->GetBinUpEdge(h_gen->GetNbinsX())) << endl;
    
    TCanvas *c1 = new TCanvas("c1","", 1500, 600);
    c1->Divide(2, 1); 
    c1->cd(1);
    h_reco->SetStats(0);
    h_reco->SetFillStyle(1); 
    h_reco->SetFillColor(kRed);
    h_reco->SetMarkerSize(5);
    h_gen->GetXaxis()->SetRangeUser(-200, 180);
    h_gen->GetXaxis()->SetTitle("Lepton P_{t} (GeV)");
    h_gen->GetYaxis()->SetTitle("Entires");
    h_gen->SetTitle("Lepton P_{T}"); 

    h_gen->SetStats(0);
    h_gen->SetMarkerSize(5);
    h_gen->SetLineColor(kBlue); 
    h_gen->GetXaxis()->SetRangeUser(-200, 180);
    h_gen->Draw("HIST"); 
    h_reco->Draw("HIST SAME"); 
    
 
    
    TLegend* l1 = new TLegend(0.8,0.8,0.6,0.9);
    l1->AddEntry(h_reco, "Reco"); 
    l1->AddEntry(h_gen, "Step0 Gen"); 
    l1->Draw("SAME");  

    c1->cd(2);
    h_ratio->SetStats(0);
    h_ratio->SetLineColor(kBlack); 
    h_ratio->GetXaxis()->SetRangeUser(-200, 180);
    h_ratio->GetYaxis()->SetTitle("Ratio");
    h_ratio->GetXaxis()->SetTitle("Lepton P_{t} (GeV)");
    h_ratio->SetTitle("Lepton P_{T} Reco vs. All Gen Ratio"); 
    h_ratio->Draw("HIST");
    g_ratio->SetMarkerColor(kBlack); 
    g_ratio->SetMarkerSize(25); 
    //g_ratio->Draw("PSAME"); 
    
    c1->SaveAs("effvscut/effvscut_reco_vs_allgen.png");
    minitree->Close(); 
    
    return 0;
}