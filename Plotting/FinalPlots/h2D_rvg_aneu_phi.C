void h2D_rvg_aneu_phi()
{
//=========Macro generated from canvas: c_2D_rvg_aneu_phi/
//=========  (Wed Jul 13 12:22:19 2022) by ROOT version 6.24/02
   TCanvas *c_2D_rvg_aneu_phi = new TCanvas("c_2D_rvg_aneu_phi", "",0,0,1200,800);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   c_2D_rvg_aneu_phi->Range(0,0,1,1);
   c_2D_rvg_aneu_phi->SetFillColor(0);
   c_2D_rvg_aneu_phi->SetBorderMode(0);
   c_2D_rvg_aneu_phi->SetBorderSize(2);
   c_2D_rvg_aneu_phi->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: p_2D_rvg_aneu_phi
   TPad *p_2D_rvg_aneu_phi = new TPad("p_2D_rvg_aneu_phi", "",0,0,1,1);
   p_2D_rvg_aneu_phi->Draw();
   p_2D_rvg_aneu_phi->cd();
   p_2D_rvg_aneu_phi->Range(-7.904653,-8.79646,8.310019,7.958701);
   p_2D_rvg_aneu_phi->SetFillColor(0);
   p_2D_rvg_aneu_phi->SetBorderMode(0);
   p_2D_rvg_aneu_phi->SetBorderSize(2);
   p_2D_rvg_aneu_phi->SetTickx(1);
   p_2D_rvg_aneu_phi->SetTicky(1);
   p_2D_rvg_aneu_phi->SetRightMargin(0.125);
   p_2D_rvg_aneu_phi->SetBottomMargin(0.15);
   p_2D_rvg_aneu_phi->SetFrameBorderMode(0);
   p_2D_rvg_aneu_phi->SetFrameBorderMode(0);
   
   TH2D *rvg_aneu_phi = new TH2D("rvg_aneu_phi","reco vs gen aneu phi",50,-6.283185,6.283185,50,-6.283185,6.283185);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   rvg_aneu_phi->SetLineColor(ci);
   rvg_aneu_phi->GetXaxis()->SetTitle("Reco aNeu phi");
   rvg_aneu_phi->GetXaxis()->SetRange(1,1200);
   rvg_aneu_phi->GetXaxis()->SetLabelFont(42);
   rvg_aneu_phi->GetXaxis()->SetLabelOffset(0.01);
   rvg_aneu_phi->GetXaxis()->SetTitleOffset(1.3);
   rvg_aneu_phi->GetXaxis()->SetTitleFont(42);
   rvg_aneu_phi->GetYaxis()->SetTitle("Gen aNeu phi");
   rvg_aneu_phi->GetYaxis()->SetRange(1,1200);
   rvg_aneu_phi->GetYaxis()->SetLabelFont(42);
   rvg_aneu_phi->GetYaxis()->SetLabelOffset(0.01);
   rvg_aneu_phi->GetYaxis()->SetTitleOffset(1.3);
   rvg_aneu_phi->GetYaxis()->SetTitleFont(42);
   rvg_aneu_phi->GetZaxis()->SetLabelFont(42);
   rvg_aneu_phi->GetZaxis()->SetTitleOffset(1);
   rvg_aneu_phi->GetZaxis()->SetTitleFont(42);
   rvg_aneu_phi->Draw("colz");
   p_2D_rvg_aneu_phi->Modified();
   c_2D_rvg_aneu_phi->cd();
   c_2D_rvg_aneu_phi->Modified();
   c_2D_rvg_aneu_phi->cd();
   c_2D_rvg_aneu_phi->SetSelected(c_2D_rvg_aneu_phi);
}
