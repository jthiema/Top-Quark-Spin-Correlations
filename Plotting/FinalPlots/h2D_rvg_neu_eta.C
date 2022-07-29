void h2D_rvg_neu_eta()
{
//=========Macro generated from canvas: c_2D_rvg_neu_eta/
//=========  (Sat Jul 23 10:39:54 2022) by ROOT version 6.24/02
   TCanvas *c_2D_rvg_neu_eta = new TCanvas("c_2D_rvg_neu_eta", "",0,0,1200,800);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   c_2D_rvg_neu_eta->Range(0,0,1,1);
   c_2D_rvg_neu_eta->SetFillColor(0);
   c_2D_rvg_neu_eta->SetBorderMode(0);
   c_2D_rvg_neu_eta->SetBorderSize(2);
   c_2D_rvg_neu_eta->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: p_2D_rvg_neu_eta
   TPad *p_2D_rvg_neu_eta = new TPad("p_2D_rvg_neu_eta", "",0,0,1,1);
   p_2D_rvg_neu_eta->Draw();
   p_2D_rvg_neu_eta->cd();
   p_2D_rvg_neu_eta->Range(-8.806452,-9.8,9.258065,8.866667);
   p_2D_rvg_neu_eta->SetFillColor(0);
   p_2D_rvg_neu_eta->SetBorderMode(0);
   p_2D_rvg_neu_eta->SetBorderSize(2);
   p_2D_rvg_neu_eta->SetTickx(1);
   p_2D_rvg_neu_eta->SetTicky(1);
   p_2D_rvg_neu_eta->SetRightMargin(0.125);
   p_2D_rvg_neu_eta->SetBottomMargin(0.15);
   p_2D_rvg_neu_eta->SetFrameBorderMode(0);
   p_2D_rvg_neu_eta->SetFrameBorderMode(0);
   
   TH2D *rvg_neu_eta = new TH2D("rvg_neu_eta","reco vs gen neu eta",50,-7,7,50,-7,7);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   rvg_neu_eta->SetLineColor(ci);
   rvg_neu_eta->GetXaxis()->SetTitle("Reco Neu eta");
   rvg_neu_eta->GetXaxis()->SetRange(1,2000);
   rvg_neu_eta->GetXaxis()->SetLabelFont(42);
   rvg_neu_eta->GetXaxis()->SetLabelOffset(0.01);
   rvg_neu_eta->GetXaxis()->SetTitleOffset(1.3);
   rvg_neu_eta->GetXaxis()->SetTitleFont(42);
   rvg_neu_eta->GetYaxis()->SetTitle("Gen Neu eta");
   rvg_neu_eta->GetYaxis()->SetRange(1,2000);
   rvg_neu_eta->GetYaxis()->SetLabelFont(42);
   rvg_neu_eta->GetYaxis()->SetLabelOffset(0.01);
   rvg_neu_eta->GetYaxis()->SetTitleOffset(1.3);
   rvg_neu_eta->GetYaxis()->SetTitleFont(42);
   rvg_neu_eta->GetZaxis()->SetLabelFont(42);
   rvg_neu_eta->GetZaxis()->SetTitleOffset(1);
   rvg_neu_eta->GetZaxis()->SetTitleFont(42);
   rvg_neu_eta->Draw("colz");
   p_2D_rvg_neu_eta->Modified();
   c_2D_rvg_neu_eta->cd();
   c_2D_rvg_neu_eta->Modified();
   c_2D_rvg_neu_eta->cd();
   c_2D_rvg_neu_eta->SetSelected(c_2D_rvg_neu_eta);
}
