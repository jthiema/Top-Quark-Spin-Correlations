void h2D_rvg_aneu_pt()
{
//=========Macro generated from canvas: c_2D_rvg_aneu_pt/
//=========  (Sat Jul  9 01:43:10 2022) by ROOT version 6.24/02
   TCanvas *c_2D_rvg_aneu_pt = new TCanvas("c_2D_rvg_aneu_pt", "",0,0,1200,800);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   c_2D_rvg_aneu_pt->Range(0,0,1,1);
   c_2D_rvg_aneu_pt->SetFillColor(0);
   c_2D_rvg_aneu_pt->SetBorderMode(0);
   c_2D_rvg_aneu_pt->SetBorderSize(2);
   c_2D_rvg_aneu_pt->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: p_2D_rvg_aneu_pt
   TPad *p_2D_rvg_aneu_pt = new TPad("p_2D_rvg_aneu_pt", "",0,0,1,1);
   p_2D_rvg_aneu_pt->Draw();
   p_2D_rvg_aneu_pt->cd();
   p_2D_rvg_aneu_pt->Range(-154.8387,-240,1393.548,1360);
   p_2D_rvg_aneu_pt->SetFillColor(0);
   p_2D_rvg_aneu_pt->SetBorderMode(0);
   p_2D_rvg_aneu_pt->SetBorderSize(2);
   p_2D_rvg_aneu_pt->SetTickx(1);
   p_2D_rvg_aneu_pt->SetTicky(1);
   p_2D_rvg_aneu_pt->SetRightMargin(0.125);
   p_2D_rvg_aneu_pt->SetBottomMargin(0.15);
   p_2D_rvg_aneu_pt->SetFrameBorderMode(0);
   p_2D_rvg_aneu_pt->SetFrameBorderMode(0);
   
   TH2D *rvg_aneu_pt = new TH2D("rvg_aneu_pt","reco vs gen aneu pt",1200,0,1200,1200,0,1200);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   rvg_aneu_pt->SetLineColor(ci);
   rvg_aneu_pt->GetXaxis()->SetTitle("Reco aNeu pT (GeV)");
   rvg_aneu_pt->GetXaxis()->SetLabelFont(42);
   rvg_aneu_pt->GetXaxis()->SetLabelOffset(0.01);
   rvg_aneu_pt->GetXaxis()->SetTitleOffset(1.3);
   rvg_aneu_pt->GetXaxis()->SetTitleFont(42);
   rvg_aneu_pt->GetYaxis()->SetTitle("Gen aNeu pT (GeV)");
   rvg_aneu_pt->GetYaxis()->SetLabelFont(42);
   rvg_aneu_pt->GetYaxis()->SetLabelOffset(0.01);
   rvg_aneu_pt->GetYaxis()->SetTitleOffset(1.3);
   rvg_aneu_pt->GetYaxis()->SetTitleFont(42);
   rvg_aneu_pt->GetZaxis()->SetLabelFont(42);
   rvg_aneu_pt->GetZaxis()->SetTitleOffset(1);
   rvg_aneu_pt->GetZaxis()->SetTitleFont(42);
   rvg_aneu_pt->Draw("colz");
   p_2D_rvg_aneu_pt->Modified();
   c_2D_rvg_aneu_pt->cd();
   c_2D_rvg_aneu_pt->Modified();
   c_2D_rvg_aneu_pt->cd();
   c_2D_rvg_aneu_pt->SetSelected(c_2D_rvg_aneu_pt);
}
