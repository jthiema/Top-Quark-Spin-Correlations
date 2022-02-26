import ROOT
import uproot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Main function of the plotting step
#
# The major part of the code below is dedicated to define a nice-looking layout.
# The interesting part is the combination of the histograms to the QCD estimation.
# There, we take the data histogram from the control region and subtract all known
# processes defined in simulation and define the remaining part as QCD. Then,
# this shape is extrapolated into the signal region with a scale factor.

# Styles

def set_style() :
    ROOT.gStyle.SetOptStat(0)

    ROOT.gStyle.SetCanvasBorderMode(0)
    ROOT.gStyle.SetCanvasColor(ROOT.kWhite)
    ROOT.gStyle.SetCanvasDefH(600)
    ROOT.gStyle.SetCanvasDefW(600)
    ROOT.gStyle.SetCanvasDefX(0)
    ROOT.gStyle.SetCanvasDefY(0)

    ROOT.gStyle.SetPadTopMargin(0.08)
    ROOT.gStyle.SetPadBottomMargin(0.13)
    ROOT.gStyle.SetPadLeftMargin(0.16)
    ROOT.gStyle.SetPadRightMargin(0.05)

    ROOT.gStyle.SetHistLineColor(1)
    ROOT.gStyle.SetHistLineStyle(0)
    ROOT.gStyle.SetHistLineWidth(1)
    ROOT.gStyle.SetEndErrorSize(2)
    ROOT.gStyle.SetMarkerStyle(20)

    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetTitleFont(42)
    ROOT.gStyle.SetTitleColor(1)
    ROOT.gStyle.SetTitleTextColor(1)
    ROOT.gStyle.SetTitleFillColor(10)
    ROOT.gStyle.SetTitleFontSize(0.05)

    ROOT.gStyle.SetTitleColor(1, "XYZ")
    ROOT.gStyle.SetTitleFont(42, "XYZ")
    ROOT.gStyle.SetTitleSize(0.05, "XYZ")
    ROOT.gStyle.SetTitleXOffset(1.00)
    ROOT.gStyle.SetTitleYOffset(1.60)

    ROOT.gStyle.SetLabelColor(1, "XYZ")
    ROOT.gStyle.SetLabelFont(42, "XYZ")
    ROOT.gStyle.SetLabelOffset(0.007, "XYZ")
    ROOT.gStyle.SetLabelSize(0.04, "XYZ")

    ROOT.gStyle.SetAxisColor(1, "XYZ")
    ROOT.gStyle.SetStripDecimals(True)
    ROOT.gStyle.SetTickLength(0.03, "XYZ")
    ROOT.gStyle.SetNdivisions(510, "XYZ")
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)

    ROOT.gStyle.SetPaperSize(20., 20.)
    ROOT.gStyle.SetHatchesLineWidth(5)
    ROOT.gStyle.SetHatchesSpacing(0.05)

    ROOT.TGaxis.SetExponentOffset(-0.08, 0.01, "Y")


def main() :
    # Specify the color for each process
    colors = {
            "ggH": ROOT.TColor.GetColor("#BF2229"),
            "qqH": ROOT.TColor.GetColor("#00A88F"),
            "TT" : ROOT.TColor.GetColor(155, 152, 204),
            "W"  : ROOT.TColor.GetColor(222, 90, 106),
            "QCD": ROOT.TColor.GetColor(250, 202, 255),
            "ZLL": ROOT.TColor.GetColor(100, 192, 232),
            "ZTT": ROOT.TColor.GetColor(248, 206, 104),
            }

    SUSY_pred = np.loadtxt('Mstop_175_mchi_10.txt')
    sat_pred  = np.loadtxt('singletop.txt')
    tt_pred   = np.loadtxt('ttbar.txt')
    st_pred   = np.loadtxt('singletop.txt')
    vv_pred   = np.loadtxt('vv.txt')

    nbins = 15
    vv_h_pred   = ROOT.TH1F('vv_h_pred'  , 'vv_h_pred'  , nbins, 0, 1)
    st_h_pred   = ROOT.TH1F('st_h_pred'  , 'st_h_pred'  , nbins, 0, 1)
    sat_h_pred  = ROOT.TH1F('sat_h_pred' , 'sat_h_pred' , nbins, 0, 1)
    tt_h_pred   = ROOT.TH1F('tt_h_pred'  , 'tt_h_pred'  , nbins, 0, 1)
    SUSY_h_pred = ROOT.TH1F('SUSY_h_pred', 'SUSY_h_pred', nbins, 0, 1)

    for i in range(len(vv_pred)) :
        vv_h_pred.Fill(vv_pred[i])

    for i in range(len(st_pred)) :
        st_h_pred.Fill(st_pred[i])

    for i in range(len(sat_pred)) :
        sat_h_pred.Fill(sat_pred[i])

    for i in range(len(tt_pred)) :
        tt_h_pred.Fill(tt_pred[i])

    for i in range(len(SUSY_pred)) :
        SUSY_h_pred.Fill(SUSY_pred[i])

    # Draw histograms
    lumi      = 3000
    scale_tt  = 16.1 * 2.32 * 1.702 
    tt_h_pred.Scale(scale_tt)

    scale_st  = 21.5
    st_h_pred.Scale(scale_st)

    scale_sat = 21.5
    sat_h_pred.Scale(scale_sat)

    scale_vv  = 0.22
    vv_h_pred.Scale(scale_vv)

    scale_SUSY=  21.95 * 1.17
    SUSY_h_pred.Scale(scale_SUSY)


    SUSY_h_pred.SetLineColor(colors["qqH"])
    SUSY_h_pred.SetLineWidth(3)

    ratio_min = 0.5
    ratio_max = 1.5

    xlow      = 0
    xhigh     = 1

    canv    = ROOT.TCanvas("", "", 1000, 1000)
    plotPad = ROOT.TPad("plotPad", "plotPad",  0.0, 0.28, 1, 1)  # Notthisone
    style   = set_style()

    #plotPad.DrawFrame(xlow, ylow, xhigh, yhigh)
    ROOT.gStyle.SetOptStat(0)
    plotPad.UseCurrentStyle()
    plotPad.Draw()
    plotPad.cd()

    # Set colors for the control plot
    for x, l in [(tt_h_pred, "W"), (st_h_pred, "ZTT"), (vv_h_pred, "ZLL") , (sat_h_pred, "ZTT")]:
        x.SetLineWidth(0)
        x.SetFillColor(colors[l])

    # Create histogram stack
    stack = ROOT.THStack("", "")
    for x in [vv_h_pred, st_h_pred, sat_h_pred, tt_h_pred, SUSY_h_pred]:
        stack.Add(x)

    plotPad.DrawFrame(xlow, 0, xhigh, stack.GetMaximum() * 1.3)
    stack.Draw("hist")

    stack.GetXaxis().SetTitle('Assigned Binary Probability')
    stack.GetYaxis().SetTitle("N_{Events} / bin")
    stack.SetMaximum(stack.GetMaximum() * 1.3)
    #stack.SetMinimum(0)
    #ROOT.gPad.SetLogy()

    # Add legend
    legend = ROOT.TLegend(0.6, 0.70, 0.9, 0.90)
    legend.SetNColumns(1)
    legend.AddEntry(tt_h_pred , "t#bar{t}", "f")
    legend.AddEntry(st_h_pred , "Single Top", "f")
    legend.AddEntry(vv_h_pred , "Diboson", "f")
    #legend.AddEntry(sat_h_pred, "Single Antitop", "f")
    legend.AddEntry(SUSY_h_pred, "m_{ #tilde{t}} = 175 GeV m_{#chi0} = 10 GeV", "l")
    legend.SetBorderSize(0)
    legend.Draw()

    # Add title
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.05)
    latex.SetTextFont(42)
    latex.DrawLatex(0.72, 0.935, "3000 fb^{{-1}} (14 TeV)".format(lumi))
    latex.DrawLatex(0.16, 0.935, "#bf{ CMS Projection}")
    ROOT.gStyle.SetLegendTextSize(0.03)

    ########################################
    # END UPPER PANEL, NOW ONTO RATIO
    ########################################


    hist1 = ROOT.TH1F('SM'       , 'SM'       , nbins, xlow, xhigh)
    hist2 = ROOT.TH1F('SM + SUSY', 'SM + SUSY', nbins, xlow, xhigh)

    for x in [vv_h_pred, st_h_pred, sat_h_pred, tt_h_pred]:
        hist1.Add(x)
        
    for x in [vv_h_pred, st_h_pred, sat_h_pred, tt_h_pred, SUSY_h_pred]:
        hist2.Add(x)

    canv.cd()  # returns to main canvas before defining pad2

    # Create ratio histogram
    h_ratio = hist2.Clone("h_ratio")
    h_ratio.SetLineColor(ROOT.kBlack)
    h_ratio.SetMarkerStyle(21)
    h_ratio.SetTitle("")
    h_ratio.SetMinimum(ratio_min)
    h_ratio.SetMaximum(ratio_max)

    # Set up plot for markers and errors
    #h_ratio.Sumw2()
    h_ratio.SetStats(0)
    h_ratio.Divide(hist1)

    h_ratio.GetYaxis().SetTitle("(SUSY + SM)/SM")

    h_ratio.GetXaxis().SetTitleFont(43)
    h_ratio.GetYaxis().SetTitleFont(43)
    h_ratio.GetXaxis().SetLabelFont(43)
    h_ratio.GetYaxis().SetLabelFont(43)
    h_ratio.GetXaxis().SetTitleSize(24)
    h_ratio.GetYaxis().SetTitleSize(30)
    h_ratio.GetXaxis().SetLabelSize(30)
    h_ratio.GetYaxis().SetLabelSize(30)

    h_ratio.GetXaxis().SetTitleOffset( 3.0 )
    h_ratio.GetYaxis().SetTitleOffset( 2.2 )

    h_ratio.GetXaxis().SetTickLength( 0.03*3 )
    h_ratio.GetYaxis().SetTickLength( 0.01*1 )

    h_ratio.GetYaxis().SetNdivisions(305)

    hline = ROOT.TLine(xlow, 1, xhigh, 1)
    hline.SetLineColor(ROOT.kBlue)

    pad2  = ROOT.TPad("pad2", "pad2", 0, 0.02, 1, 0.30)
    pad2.UseCurrentStyle()
    pad2.Draw()
    pad2.cd()
    h_ratio.Draw("0p")
    hline.Draw()

    canv.SaveAs("h_pred_175_10_ratio.pdf")

if __name__ == '__main__' :
    main()