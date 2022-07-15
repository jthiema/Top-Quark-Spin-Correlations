void h2D_rvg_neu_pt()
{
//=========Macro generated from canvas: c_2D_rvg_neu_pt/
//=========  (Wed Jul 13 12:22:18 2022) by ROOT version 6.24/02
   TCanvas *c_2D_rvg_neu_pt = new TCanvas("c_2D_rvg_neu_pt", "",0,0,1200,800);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   c_2D_rvg_neu_pt->Range(0,0,1,1);
   c_2D_rvg_neu_pt->SetFillColor(0);
   c_2D_rvg_neu_pt->SetBorderMode(0);
   c_2D_rvg_neu_pt->SetBorderSize(2);
   c_2D_rvg_neu_pt->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: p_2D_rvg_neu_pt
   TPad *p_2D_rvg_neu_pt = new TPad("p_2D_rvg_neu_pt", "",0,0,1,1);
   p_2D_rvg_neu_pt->Draw();
   p_2D_rvg_neu_pt->cd();
   p_2D_rvg_neu_pt->Range(-154.8387,-240,1393.548,1360);
   p_2D_rvg_neu_pt->SetFillColor(0);
   p_2D_rvg_neu_pt->SetBorderMode(0);
   p_2D_rvg_neu_pt->SetBorderSize(2);
   p_2D_rvg_neu_pt->SetTickx(1);
   p_2D_rvg_neu_pt->SetTicky(1);
   p_2D_rvg_neu_pt->SetRightMargin(0.125);
   p_2D_rvg_neu_pt->SetBottomMargin(0.15);
   p_2D_rvg_neu_pt->SetFrameBorderMode(0);
   p_2D_rvg_neu_pt->SetFrameBorderMode(0);
   
   TH2D *rvg_neu_pt = new TH2D("rvg_neu_pt","reco vs gen neu pt",50,0,1200,50,0,1200);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   rvg_neu_pt->SetLineColor(ci);
   rvg_neu_pt->GetXaxis()->SetTitle("Reco Neu pT (GeV)");
   rvg_neu_pt->GetXaxis()->SetRange(1,1200);
   rvg_neu_pt->GetXaxis()->SetLabelFont(42);
   rvg_neu_pt->GetXaxis()->SetLabelOffset(0.01);
   rvg_neu_pt->GetXaxis()->SetTitleOffset(1.3);
   rvg_neu_pt->GetXaxis()->SetTitleFont(42);
   rvg_neu_pt->GetYaxis()->SetTitle("Gen Neu pT (GeV)");
   rvg_neu_pt->GetYaxis()->SetRange(1,1200);
   rvg_neu_pt->GetYaxis()->SetLabelFont(42);
   rvg_neu_pt->GetYaxis()->SetLabelOffset(0.01);
   rvg_neu_pt->GetYaxis()->SetTitleOffset(1.3);
   rvg_neu_pt->GetYaxis()->SetTitleFont(42);
   rvg_neu_pt->GetZaxis()->SetLabelFont(42);
   rvg_neu_pt->GetZaxis()->SetTitleOffset(1);
   rvg_neu_pt->GetZaxis()->SetTitleFont(42);
   rvg_neu_pt->Draw("colz");
   p_2D_rvg_neu_pt->Modified();
   c_2D_rvg_neu_pt->cd();
   c_2D_rvg_neu_pt->Modified();
   c_2D_rvg_neu_pt->cd();
   c_2D_rvg_neu_pt->SetSelected(c_2D_rvg_neu_pt);
}
