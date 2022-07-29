void h2D_rvg_aneu_eta()
{
//=========Macro generated from canvas: c_2D_rvg_aneu_eta/
//=========  (Sat Jul 23 10:39:54 2022) by ROOT version 6.24/02
   TCanvas *c_2D_rvg_aneu_eta = new TCanvas("c_2D_rvg_aneu_eta", "",0,0,1200,800);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   c_2D_rvg_aneu_eta->Range(0,0,1,1);
   c_2D_rvg_aneu_eta->SetFillColor(0);
   c_2D_rvg_aneu_eta->SetBorderMode(0);
   c_2D_rvg_aneu_eta->SetBorderSize(2);
   c_2D_rvg_aneu_eta->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: p_2D_rvg_aneu_eta
   TPad *p_2D_rvg_aneu_eta = new TPad("p_2D_rvg_aneu_eta", "",0,0,1,1);
   p_2D_rvg_aneu_eta->Draw();
   p_2D_rvg_aneu_eta->cd();
   p_2D_rvg_aneu_eta->Range(-8.806452,-9.8,9.258065,8.866667);
   p_2D_rvg_aneu_eta->SetFillColor(0);
   p_2D_rvg_aneu_eta->SetBorderMode(0);
   p_2D_rvg_aneu_eta->SetBorderSize(2);
   p_2D_rvg_aneu_eta->SetTickx(1);
   p_2D_rvg_aneu_eta->SetTicky(1);
   p_2D_rvg_aneu_eta->SetRightMargin(0.125);
   p_2D_rvg_aneu_eta->SetBottomMargin(0.15);
   p_2D_rvg_aneu_eta->SetFrameBorderMode(0);
   p_2D_rvg_aneu_eta->SetFrameBorderMode(0);
   
   TH2D *rvg_aneu_eta = new TH2D("rvg_aneu_eta","reco vs gen aneu eta",50,-7,7,50,-7,7);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   rvg_aneu_eta->SetLineColor(ci);
   rvg_aneu_eta->GetXaxis()->SetTitle("Reco aNeu eta");
   rvg_aneu_eta->GetXaxis()->SetRange(1,2000);
   rvg_aneu_eta->GetXaxis()->SetLabelFont(42);
   rvg_aneu_eta->GetXaxis()->SetLabelOffset(0.01);
   rvg_aneu_eta->GetXaxis()->SetTitleOffset(1.3);
   rvg_aneu_eta->GetXaxis()->SetTitleFont(42);
   rvg_aneu_eta->GetYaxis()->SetTitle("Gen aNeu eta");
   rvg_aneu_eta->GetYaxis()->SetRange(1,2000);
   rvg_aneu_eta->GetYaxis()->SetLabelFont(42);
   rvg_aneu_eta->GetYaxis()->SetLabelOffset(0.01);
   rvg_aneu_eta->GetYaxis()->SetTitleOffset(1.3);
   rvg_aneu_eta->GetYaxis()->SetTitleFont(42);
   rvg_aneu_eta->GetZaxis()->SetLabelFont(42);
   rvg_aneu_eta->GetZaxis()->SetTitleOffset(1);
   rvg_aneu_eta->GetZaxis()->SetTitleFont(42);
   rvg_aneu_eta->Draw("colz");
   p_2D_rvg_aneu_eta->Modified();
   c_2D_rvg_aneu_eta->cd();
   c_2D_rvg_aneu_eta->Modified();
   c_2D_rvg_aneu_eta->cd();
   c_2D_rvg_aneu_eta->SetSelected(c_2D_rvg_aneu_eta);
}
