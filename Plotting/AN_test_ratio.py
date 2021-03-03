import ROOT
import uproot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def setTDRStyle():
    import ROOT
    from ROOT import TStyle
    from ROOT import kWhite
    from ROOT import kTRUE

    tdrStyle = TStyle("tdrStyle", "Style for P-TDR")

    # For the canvas:
    tdrStyle.SetCanvasBorderMode(0)
    tdrStyle.SetCanvasColor(kWhite)
    # For the canvas:
    tdrStyle.SetCanvasBorderMode(0)
    tdrStyle.SetCanvasColor(kWhite)
    tdrStyle.SetCanvasDefH(800)  # Height of canvas
    tdrStyle.SetCanvasDefW(800)  # Width of canvas
    tdrStyle.SetCanvasDefX(0)  # POsition on screen
    tdrStyle.SetCanvasDefY(0)

    # For the Pad:
    tdrStyle.SetPadBorderMode(0)
    # tdrStyle->SetPadBorderSize(Width_t size = 1);
    tdrStyle.SetPadColor(kWhite)
    tdrStyle.SetPadGridX(0)
    tdrStyle.SetPadGridY(0)
    tdrStyle.SetGridColor(0)
    tdrStyle.SetGridStyle(3)
    tdrStyle.SetGridWidth(1)

    # For the frame:
    tdrStyle.SetFrameBorderMode(0)
    tdrStyle.SetFrameBorderSize(1)
    tdrStyle.SetFrameFillColor(0)
    tdrStyle.SetFrameFillStyle(0)
    tdrStyle.SetFrameLineColor(1)
    tdrStyle.SetFrameLineStyle(1)
    tdrStyle.SetFrameLineWidth(1)

    # For the histo:
    # tdrStyle->SetHistFillColor(1);
    # tdrStyle->SetHistFillStyle(0);
    tdrStyle.SetHistLineColor(1)
    tdrStyle.SetHistLineStyle(0)
    tdrStyle.SetHistLineWidth(3)
    # tdrStyle->SetLegoInnerR(Float_t rad = 0.5);
    # tdrStyle->SetNumberContours(Int_t number = 20);

    tdrStyle.SetEndErrorSize(2)
    #  tdrStyle->SetErrorMarker(20);
    tdrStyle.SetErrorX(0.)

    tdrStyle.SetMarkerStyle(20)
    tdrStyle.SetMarkerColor(1)
    # tdrStyle.SetMarkerSize(7)

    # For the fit/function:
    tdrStyle.SetOptFit(0)
    tdrStyle.SetFitFormat("5.4g")
    tdrStyle.SetFuncColor(2)
    tdrStyle.SetFuncStyle(1)
    tdrStyle.SetFuncWidth(1)

    # For the date:
    tdrStyle.SetOptDate(0)
    # tdrStyle->SetDateX(Float_t x = 0.01);
    # tdrStyle->SetDateY(Float_t y = 0.01);

    # For the statistics box:
    tdrStyle.SetOptFile(0)
    tdrStyle.SetOptStat(0)  # To display the mean and RMS:   SetOptStat("mr");
    tdrStyle.SetStatColor(kWhite)
    tdrStyle.SetStatFont(30)
    tdrStyle.SetStatFontSize(0.025)
    tdrStyle.SetStatTextColor(1)
    tdrStyle.SetStatFormat("6.4g")
    tdrStyle.SetStatBorderSize(1)
    tdrStyle.SetStatH(0.1)
    tdrStyle.SetStatW(0.15)
    # tdrStyle->SetStatStyle(Style_t style = 100.1);
    # tdrStyle->SetStatX(Float_t x = 0);
    # tdrStyle->SetStatY(Float_t y = 0);

    # Margins:
    tdrStyle.SetPadTopMargin(0.05)
    tdrStyle.SetPadBottomMargin(0.14)
    tdrStyle.SetPadLeftMargin(0.16)
    tdrStyle.SetPadRightMargin(0.05)

    # For the Global title:
    tdrStyle.SetOptTitle(0)
    tdrStyle.SetTitleFont(30)
    tdrStyle.SetTitleColor(1)
    tdrStyle.SetTitleTextColor(1)
    tdrStyle.SetTitleFillColor(10)
    tdrStyle.SetTitleFontSize(0.04)
    # tdrStyle->SetTitleH(0); # Set the height of the title box
    # tdrStyle->SetTitleW(0); # Set the width of the title box
    # tdrStyle->SetTitleX(0); # Set the position of the title box
    # tdrStyle->SetTitleY(0.985); # Set the position of the title box
    # tdrStyle->SetTitleStyle(Style_t style = 100.1);
    # tdrStyle->SetTitleBorderSize(2);

    # For the axis titles:
    tdrStyle.SetTitleColor(1, "XYZ")
    tdrStyle.SetTitleFont(42, "XYZ")
    tdrStyle.SetTitleSize(0.0475, "XYZ")
    # tdrStyle->SetTitleXSize(Float_t size = 0.02); # Another way to set the size?
    # tdrStyle->SetTitleYSize(Float_t size = 0.02);
    tdrStyle.SetTitleXOffset(1.3)
    tdrStyle.SetTitleYOffset(1.5)
    # tdrStyle->SetTitleOffset(1.1, "Y"); # Another way to set the Offset

    # For the axis labels:
    tdrStyle.SetLabelColor(1, "XYZ")
    tdrStyle.SetLabelFont(42, "XYZ")
    tdrStyle.SetLabelOffset(0.007, "XYZ")
    tdrStyle.SetLabelSize(0.05, "XYZ")

    # For the axis:
    tdrStyle.SetAxisColor(1, "XYZ")
    tdrStyle.SetStripDecimals(kTRUE)
    tdrStyle.SetTickLength(0.03, "XYZ")
    tdrStyle.SetNdivisions(408, "XYZ")

    # ~ tdrStyle->SetNdivisions(510, "XYZ");
    # To get tick marks on the opposite side of the frame
    tdrStyle.SetPadTickX(1)
    tdrStyle.SetPadTickY(1)

    # Change for log plots:
    tdrStyle.SetOptLogx(0)
    tdrStyle.SetOptLogy(0)
    tdrStyle.SetOptLogz(0)

    # Postscript options:
    tdrStyle.SetPaperSize(20., 20.)
    # tdrStyle->SetLineScalePS(Float_t scale = 3);
    # tdrStyle->SetLineStyleString(Int_t i, const char* text);
    # tdrStyle->SetHeaderPS(const char* header);
    # tdrStyle->SetTitlePS(const char* pstitle);

    # tdrStyle->SetBarOffset(Float_t baroff = 0.5);
    # tdrStyle->SetBarWidth(Float_t barwidth = 0.5);
    # tdrStyle->SetPaintTextFormat(const char* format = "g");
    tdrStyle.SetPalette(1)
    # tdrStyle->SetTimeOffset(Double_t toffset);
    # tdrStyle->SetHistMinimumZero(kTRUE);

    #ROOT.gROOT.ForceStyle()

    tdrStyle.cd()
    return tdrStyle


def main():
   
    nbins = 15
    
    xlow  = 0
    ylow  = 0
    
    yhigh = 0.22
    xhigh = 4.2
    
    ratio_min = 0
    ratio_max = 1.5
    
    hist1 = ROOT.TH1F('Run 2 FS 13 TeV' , 'Run 2 FS 13 TeV', nbins, xlow, xhigh)
    hist2 = ROOT.TH1F('Delphes 14 TeV'  , 'Delphes 14 TeV' , nbins, xlow, xhigh)

    dR    = np.loadtxt('../txt_files/Delphes_dR_iso.txt')
    tt_dR = np.loadtxt('../txt_files/Run2_FS_dR_iso.txt')

    Delphes = np.histogram(dR   , bins=nbins)[0]
    Run2    = np.histogram(tt_dR, bins=nbins)[0]

    for i, j, k in zip(Run2, Delphes, range(1, nbins + 1)):
        hist1.SetBinContent(k, i)
        hist2.SetBinContent(k, j)

    canv    = ROOT.TCanvas("c1", "c1", 1100, 1100)
    plotPad = ROOT.TPad("plotPad", "plotPad", 0.0, 0.25, 1, 1)  # Notthisone
    style   = setTDRStyle()

    ROOT.gStyle.SetOptStat(0)
    plotPad.UseCurrentStyle()
    plotPad.Draw()
    plotPad.cd()

    hist1.SetLineColor(ROOT.kBlue)
    hist1.Scale(1./hist1.Integral())
    hist2.SetLineColor(ROOT.kRed)
    hist2.Scale(1./hist2.Integral())
    
    hist1.SetLineWidth(2)
    hist2.SetLineWidth(2)
    
    plotPad.DrawFrame(xlow, ylow, xhigh, yhigh, ";dR(lepton, jet); Arbitrary Units")
 
    ROOT.gStyle.SetOptFit(110)
    hist1.Draw('samehist')
    hist2.Draw('histsame')
    
    # Lumi and COM energy label
    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.041)
    latex.SetNDC(True)
    latex.DrawLatex(0.95, 0.96, "3000 fb^{-1} (14 TeV) ")
    
    # CMS
    latexCMS = ROOT.TLatex()
    latexCMS.SetTextFont(61)
    latexCMS.SetTextSize(0.055)
    latexCMS.SetNDC(True)
    latexCMS.DrawLatex(0.19, 0.88, "CMS")

    # Projection
    latexCMSExtra = ROOT.TLatex()
    latexCMSExtra.SetTextFont(42)
    latexCMSExtra.SetTextSize(0.035)
    latexCMSExtra.SetNDC(True)
    cmsExtra      = "Projection"
    latexCMSExtra.DrawLatex(0.19, 0.84, "%s" % (cmsExtra))

    # Legend
    leg = ROOT.TLegend(0.45, 0.72, 0.80, 0.92, "", "brNDC")
    leg.SetFillColor(10)
    leg.SetFillStyle(0)
    leg.SetLineColor(10)
    leg.SetShadowColor(0)
    leg.SetBorderSize(1)
    leg.SetTextFont(62)
    leg.AddEntry(hist1, "Run2 FS 13 TeV", "l")
    leg.AddEntry(hist2, "Delphes 14 TeV", "l")

    leg.Draw()

    canv.cd()  # returns to main canvas before defining pad2
    
    # Create ratio histogram
    h_ratio = hist1.Clone("h_ratio")
    h_ratio.SetLineColor(ROOT.kBlack)
    h_ratio.SetMarkerStyle(21)
    h_ratio.SetTitle("")
    h_ratio.SetMinimum(ratio_min)
    h_ratio.SetMaximum(ratio_max)
    
    # Set up plot for markers and errors
    h_ratio.Sumw2()
    h_ratio.SetStats(0)
    h_ratio.Divide(hist2)
    
    h_ratio.GetYaxis().SetTitle("Run2/Delphes")

    h_ratio.GetXaxis().SetTitleFont(43)
    h_ratio.GetYaxis().SetTitleFont(43)
    h_ratio.GetXaxis().SetLabelFont(43)
    h_ratio.GetYaxis().SetLabelFont(43)
    h_ratio.GetXaxis().SetTitleSize(24)
    h_ratio.GetYaxis().SetTitleSize(36)
    h_ratio.GetXaxis().SetLabelSize(40)
    h_ratio.GetYaxis().SetLabelSize(40)

    h_ratio.GetXaxis().SetTitleOffset( 3.2 )
    h_ratio.GetYaxis().SetTitleOffset( 2.2 )

    h_ratio.GetXaxis().SetTickLength( 0.03*3 )
    h_ratio.GetYaxis().SetTickLength( 0.01*1 )

    h_ratio.GetYaxis().SetNdivisions(305)

    hline = ROOT.TLine(xlow, 1, xhigh, 1)
    hline.SetLineColor(ROOT.kBlue)
    
    pad2  = ROOT.TPad("pad2", "pad2", 0, 0.02, 1, 0.25)
    pad2.UseCurrentStyle()
    pad2.Draw()
    pad2.cd()
    h_ratio.Draw("e0p")
    hline.Draw()
    canv.Draw()

    #canv.SaveAs('test.pdf')
    canv.SaveAs('AN_dR_post_selection.pdf')


main()
