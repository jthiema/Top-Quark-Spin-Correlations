void h2D_rvg_neu_phi()
{
//=========Macro generated from canvas: c_2D_rvg_neu_phi/
//=========  (Thu Jul 21 14:33:20 2022) by ROOT version 6.24/02
   TCanvas *c_2D_rvg_neu_phi = new TCanvas("c_2D_rvg_neu_phi", "",0,0,1200,800);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   c_2D_rvg_neu_phi->Range(0,0,1,1);
   c_2D_rvg_neu_phi->SetFillColor(0);
   c_2D_rvg_neu_phi->SetBorderMode(0);
   c_2D_rvg_neu_phi->SetBorderSize(2);
   c_2D_rvg_neu_phi->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: p_2D_rvg_neu_phi
   TPad *p_2D_rvg_neu_phi = new TPad("p_2D_rvg_neu_phi", "",0,0,1,1);
   p_2D_rvg_neu_phi->Draw();
   p_2D_rvg_neu_phi->cd();
   p_2D_rvg_neu_phi->Range(-3.952326,-4.39823,4.15501,3.979351);
   p_2D_rvg_neu_phi->SetFillColor(0);
   p_2D_rvg_neu_phi->SetBorderMode(0);
   p_2D_rvg_neu_phi->SetBorderSize(2);
   p_2D_rvg_neu_phi->SetTickx(1);
   p_2D_rvg_neu_phi->SetTicky(1);
   p_2D_rvg_neu_phi->SetRightMargin(0.125);
   p_2D_rvg_neu_phi->SetBottomMargin(0.15);
   p_2D_rvg_neu_phi->SetFrameBorderMode(0);
   p_2D_rvg_neu_phi->SetFrameBorderMode(0);
   
   TH2D *rvg_neu_phi = new TH2D("rvg_neu_phi","reco vs gen neu phi",50,-3.141593,3.141593,50,-3.141593,3.141593);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   rvg_neu_phi->SetLineColor(ci);
   rvg_neu_phi->GetXaxis()->SetTitle("Reco Neu phi");
   rvg_neu_phi->GetXaxis()->SetRange(1,2000);
   rvg_neu_phi->GetXaxis()->SetLabelFont(42);
   rvg_neu_phi->GetXaxis()->SetLabelOffset(0.01);
   rvg_neu_phi->GetXaxis()->SetTitleOffset(1.3);
   rvg_neu_phi->GetXaxis()->SetTitleFont(42);
   rvg_neu_phi->GetYaxis()->SetTitle("Gen Neu phi");
   rvg_neu_phi->GetYaxis()->SetRange(1,2000);
   rvg_neu_phi->GetYaxis()->SetLabelFont(42);
   rvg_neu_phi->GetYaxis()->SetLabelOffset(0.01);
   rvg_neu_phi->GetYaxis()->SetTitleOffset(1.3);
   rvg_neu_phi->GetYaxis()->SetTitleFont(42);
   rvg_neu_phi->GetZaxis()->SetLabelFont(42);
   rvg_neu_phi->GetZaxis()->SetTitleOffset(1);
   rvg_neu_phi->GetZaxis()->SetTitleFont(42);
   rvg_neu_phi->Draw("colz");
   p_2D_rvg_neu_phi->Modified();
   c_2D_rvg_neu_phi->cd();
   c_2D_rvg_neu_phi->Modified();
   c_2D_rvg_neu_phi->cd();
   c_2D_rvg_neu_phi->SetSelected(c_2D_rvg_neu_phi);
}
