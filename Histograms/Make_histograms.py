import sys
import math
import ROOT
import uproot
import operator
import argparse
import numpy as np
from array import array
from datetime import datetime

def ifOk(var_check) :
    if math.isfinite(var_check) :
        vOk = var_check
    else :
        vOk = -999999.
    return vOk

#====INSTRUCTIONS PLEASE READ====

#input should be a path to the foldwer where
#all of the files after top reco are
#they should be in the format of topreco_*.root
#for this to work

#output should be a root file, youre choice on
#path and naming

#EXAMPLE
#python Top_Reco/concatandplot.py -i ~/Data/toprecooutput/ -o ~/Data/ttbarplots.root

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Input delphes minitrees file')
parser.add_argument('-o', '--output', help='Output file location')

args = parser.parse_args()
inputFile = args.input
outputFile = args.output

opfile = ROOT.TFile(outputFile, 'recreate')

# Step 0 All GEN hists
step0 = uproot.open(inputFile)['Step0']

# items we need from Make_minitrees.py 
#    gen_top_pt_arr_0      = array('f', [0.])
#    gen_top_eta_arr_0     = array('f', [0.])
#    gen_top_phi_arr_0     = array('f', [0.])
#    gen_top_mass_arr_0     = array('f', [0.])
#    gen_top_status_arr_0  = array('f', [0.])
#
#    gen_atop_pt_arr_0     = array('f', [0.])
#    gen_atop_eta_arr_0    = array('f', [0.])
#    gen_atop_phi_arr_0    = array('f', [0.])
#    gen_atop_mass_arr_0    = array('f', [0.])
#    gen_atop_status_arr_0  = array('f', [0.])
#
#    gen_b_pt_arr_0      = array('f', [0.])
#    gen_b_eta_arr_0     = array('f', [0.])
#    gen_b_phi_arr_0     = array('f', [0.])
#    gen_b_mass_arr_0     = array('f', [0.])
#    gen_b_status_arr_0  = array('f', [0.])
#
#    gen_ab_pt_arr_0     = array('f', [0.])
#    gen_ab_eta_arr_0    = array('f', [0.])
#    gen_ab_phi_arr_0    = array('f', [0.])
#    gen_ab_mass_arr_0    = array('f', [0.])
#    gen_ab_status_arr_0  = array('f', [0.])
#
#    gen_lep_pt_arr_0      = array('f', [0.])
#    gen_lep_eta_arr_0     = array('f', [0.])
#    gen_lep_phi_arr_0     = array('f', [0.])
#    gen_lep_mass_arr_0     = array('f', [0.])
#    gen_lep_pdgid_arr_0  = array('f', [0.])
#    gen_lep_status_arr_0  = array('f', [0.])
#
#    gen_alep_pt_arr_0     = array('f', [0.])
#    gen_alep_eta_arr_0    = array('f', [0.])
#    gen_alep_phi_arr_0    = array('f', [0.])
#    gen_alep_mass_arr_0    = array('f', [0.])
#    gen_alep_pdgid_arr_0 = array('f', [0.])
#    gen_alep_status_arr_0  = array('f', [0.])
#
#    gen_lep_nearest_pt_arr_0      = array('f', [0.])
#    gen_lep_nearest_eta_arr_0     = array('f', [0.])
#    gen_lep_nearest_phi_arr_0     = array('f', [0.])
#    gen_lep_nearest_mass_arr_0     = array('f', [0.])
#    gen_lep_nearest_pdgid_arr_0  = array('f', [0.])
#    gen_lep_nearest_status_arr_0  = array('f', [0.])
#
#    gen_alep_nearest_pt_arr_0     = array('f', [0.])
#    gen_alep_nearest_eta_arr_0    = array('f', [0.])
#    gen_alep_nearest_phi_arr_0    = array('f', [0.])
#    gen_alep_nearest_mass_arr_0    = array('f', [0.])
#    gen_alep_nearest_pdgid_arr_0 = array('f', [0.])
#    gen_alep_nearest_status_arr_0  = array('f', [0.])
#
#    gen_neu_pt_arr_0      = array('f', [0.])
#    gen_neu_eta_arr_0     = array('f', [0.])
#    gen_neu_phi_arr_0     = array('f', [0.])
#    gen_neu_mass_arr_0     = array('f', [0.])
#    gen_neu_pdgid_arr_0  = array('f', [0.])
#    gen_neu_status_arr_0  = array('f', [0.])
#
#    gen_aneu_pt_arr_0     = array('f', [0.])
#    gen_aneu_eta_arr_0    = array('f', [0.])
#    gen_aneu_phi_arr_0    = array('f', [0.])
#    gen_aneu_mass_arr_0    = array('f', [0.])
#    gen_aneu_pdgid_arr_0 = array('f', [0.])
#    gen_aneu_status_arr_0  = array('f', [0.])
#
#    gen_met_pt_arr_0     = array('f', [0.])
#    gen_met_phi_arr_0    = array('f', [0.])

step0_hleppt = ROOT.TH1D('all_gen_lep_pt', 'all_gen_lep_pt', 30, 0, 1200)
step0_hlepeta = ROOT.TH1D('all_gen_lep_eta', 'all_gen_lep_eta', 30, -7, 7)
step0_hlepphi = ROOT.TH1D('all_gen_lep_phi', 'all_gen_lep_phi', 30, -np.pi, np.pi)
step0_haleppt = ROOT.TH1D('all_gen_alep_pt', 'all_gen_alep_pt', 30, 0, 1200)
step0_halepeta = ROOT.TH1D('all_gen_alep_eta', 'all_gen_alep_eta', 30, -7, 7)
step0_halepphi = ROOT.TH1D('all_gen_alep_phi', 'all_gen_alep_phi', 30, -np.pi, np.pi)
step0_hmetpt = ROOT.TH1D('all_gen_met_pt', 'all_gen_met_pt', 30, 0, 1200)
step0_hmetphi = ROOT.TH1D('all_gen_met_phi', 'all_gen_met_phi', 30, -np.pi, np.pi)
step0_htpt = ROOT.TH1D('all_gen_t_pt', 'all_gen_t_pt', 30, 0, 1200)
step0_hteta = ROOT.TH1D('all_gen_t_eta', 'all_gen_t_eta', 30, -7, 7)
step0_htphi = ROOT.TH1D('all_gen_t_phi', 'all_gen_t_phi', 30, -np.pi, np.pi)
step0_hatpt = ROOT.TH1D('all_gen_at_pt', 'all_gen_at_pt', 30, 0, 1200)
step0_hateta = ROOT.TH1D('all_gen_at_eta', 'all_gen_at_eta', 30, -7, 7)
step0_hatphi = ROOT.TH1D('all_gen_at_phi', 'all_gen_at_phi', 30, -np.pi, np.pi)
step0_hbpt = ROOT.TH1D('all_gen_b_pt', 'all_gen_b_pt', 30, 0, 1200)
step0_hbeta = ROOT.TH1D('all_gen_b_eta', 'all_gen_b_eta', 30, -7, 7)
step0_hbphi = ROOT.TH1D('all_gen_b_phi', 'all_gen_b_phi', 30, -np.pi, np.pi)
step0_habpt = ROOT.TH1D('all_gen_ab_pt', 'all_gen_ab_pt', 30, 0, 1200)
step0_habeta = ROOT.TH1D('all_gen_ab_eta', 'all_gen_ab_eta', 30, -7, 7)
step0_habphi = ROOT.TH1D('all_gen_ab_phi', 'all_gen_ab_phi', 30, -np.pi, np.pi)
step0_hneupt = ROOT.TH1D('all_gen_neu_pt', 'all_gen_neu_pt', 30, 0, 1200)
step0_hneueta = ROOT.TH1D('all_gen_neu_eta', 'all_gen_neu_eta', 30, -7, 7)
step0_hneuphi = ROOT.TH1D('all_gen_neu_phi', 'all_gen_neu_phi', 30, -np.pi, np.pi)
step0_haneupt = ROOT.TH1D('all_gen_aneu_pt', 'all_gen_aneu_pt', 30, 0, 1200)
step0_haneueta = ROOT.TH1D('all_gen_aneu_eta', 'all_gen_aneu_eta', 30, -7, 7)
step0_haneuphi = ROOT.TH1D('all_gen_aneu_phi', 'all_gen_aneu_phi', 30, -np.pi, np.pi)

for i in range(len(step0['gen_lep_pt_0'].array())):
    step0_hleppt.Fill(step0['gen_lep_pt_0'].array()[i]) 
    step0_hlepeta.Fill(step0['gen_lep_eta_0'].array()[i]) 
    step0_hlepphi.Fill(step0['gen_lep_phi_0'].array()[i]) 
    step0_haleppt.Fill(step0['gen_alep_pt_0'].array()[i]) 
    step0_halepeta.Fill(step0['gen_alep_eta_0'].array()[i]) 
    step0_halepphi.Fill(step0['gen_alep_phi_0'].array()[i]) 
    step0_hmetpt.Fill(step0['gen_met_pt_0'].array()[i]) 
    step0_hmetphi.Fill(step0['gen_met_phi_0'].array()[i]) 
    step0_htpt.Fill(step0['gen_top_pt_0'].array()[i]) 
    step0_hteta.Fill(step0['gen_top_eta_0'].array()[i]) 
    step0_htphi.Fill(step0['gen_top_phi_0'].array()[i]) 
    step0_hatpt.Fill(step0['gen_atop_pt_0'].array()[i]) 
    step0_hateta.Fill(step0['gen_atop_eta_0'].array()[i]) 
    step0_hatphi.Fill(step0['gen_atop_phi_0'].array()[i]) 
    step0_hbpt.Fill(step0['gen_b_pt_0'].array()[i]) 
    step0_hbeta.Fill(step0['gen_b_eta_0'].array()[i]) 
    step0_hbphi.Fill(step0['gen_b_phi_0'].array()[i]) 
    step0_habpt.Fill(step0['gen_ab_pt_0'].array()[i]) 
    step0_habeta.Fill(step0['gen_ab_eta_0'].array()[i]) 
    step0_habphi.Fill(step0['gen_ab_phi_0'].array()[i]) 
    step0_hneupt.Fill(step0['gen_neu_pt_0'].array()[i]) 
    step0_hneueta.Fill(step0['gen_neu_eta_0'].array()[i]) 
    step0_hneuphi.Fill(step0['gen_neu_phi_0'].array()[i]) 
    step0_haneupt.Fill(step0['gen_aneu_pt_0'].array()[i]) 
    step0_haneueta.Fill(step0['gen_aneu_eta_0'].array()[i]) 
    step0_haneuphi.Fill(step0['gen_aneu_phi_0'].array()[i]) 

# Step 8 RECO hists

hleppt = ROOT.TH1D('lep_pt', 'lep_pt', 30, 0, 1200)
hlepeta = ROOT.TH1D('lep_eta', 'lep_eta', 30, -7, 7)
hlepphi = ROOT.TH1D('lep_phi', 'lep_phi', 30, -np.pi, np.pi)

haleppt = ROOT.TH1D('alep_pt', 'alep_pt', 30, 0, 1200)
halepeta = ROOT.TH1D('alep_eta', 'alep_eta', 30, -7, 7)
halepphi = ROOT.TH1D('alep_phi', 'alep_phi', 30, -np.pi, np.pi)

hmetpt = ROOT.TH1D('met_pt', 'met_pt', 30, 0, 1200)
hmetphi = ROOT.TH1D('met_phi', 'met_phi', 30, -np.pi, np.pi)

hbpt = ROOT.TH1D('b_pt', 'b_pt', 30, 0, 1200)
hbeta = ROOT.TH1D('b_eta', 'b_eta', 30, -7, 7)
hbphi = ROOT.TH1D('b_phi', 'b_phi', 30, -np.pi, np.pi)

habpt = ROOT.TH1D('ab_pt', 'ab_pt', 30, 0, 1200)
habeta = ROOT.TH1D('ab_eta', 'ab_eta', 30, -7, 7)
habphi = ROOT.TH1D('ab_phi', 'ab_phi', 30, -np.pi, np.pi)

hneupt = ROOT.TH1D('neu_pt', 'neu_pt', 30, 0, 1200)
hneueta = ROOT.TH1D('neu_eta', 'neu_eta', 30, -7, 7)
hneuphi = ROOT.TH1D('neu_phi', 'neu_phi', 30, -np.pi, np.pi)

haneupt = ROOT.TH1D('aneu_pt', 'aneu_pt', 30, 0, 1200)
haneueta = ROOT.TH1D('aneu_eta', 'aneu_eta', 30, -7, 7)
haneuphi = ROOT.TH1D('aneu_phi', 'aneu_phi', 30, -np.pi, np.pi)

htpt = ROOT.TH1D('t_pt', 't_pt', 30, 0, 1200)
hteta = ROOT.TH1D('t_eta', 't_eta', 30, -7, 7)
htphi = ROOT.TH1D('t_phi', 't_phi', 30, -np.pi, np.pi)
htrap = ROOT.TH1D("t_rap", "t_rap", 30, -7, 7)

hatpt = ROOT.TH1D('at_pt', 'at_pt', 30, 0, 1200)
hateta = ROOT.TH1D('at_eta', 'at_eta', 30, -7, 7)
hatphi = ROOT.TH1D('at_phi', 'at_phi', 30, -np.pi, np.pi)
hatrap = ROOT.TH1D("at_rap", "at_rap", 30, -7, 7)

htatmass = ROOT.TH1D('tat_mass', 'tat_mass', 30, 0, 1200)
htatpt = ROOT.TH1D("tat_pt", "tat_pt", 30, 0 ,1200)
htateta = ROOT.TH1D("tat_eta", "tat_eta", 30, -7 ,7)
htatphi = ROOT.TH1D("tat_phi", "tat_phi", 30, -np.pi, np.pi)
htatrap = ROOT.TH1D("tat_rap", "tat_rap", 30, -7, 7)

hckk = ROOT.TH1D("ckk", "ckk", 30, -1, 1)
hcrr = ROOT.TH1D("crr", "crr", 30, -1, 1)
hcnn = ROOT.TH1D("cnn", "cnn", 30, -1, 1)

hcrk = ROOT.TH1D("crk", "crk", 30, -1, 1)
hckr = ROOT.TH1D("ckr", "ckr", 30, -1, 1)

hcPrk = ROOT.TH1D("cP_rk", "cP_rk", 30, -1, 1)
hcMrk = ROOT.TH1D("cM_rk", "cM_rk", 30, -1, 1)

hchel = ROOT.TH1D("c_hel", "c_hel", 30, -1, 1)

hlldeta = ROOT.TH1D("ll_deta", "ll_deta", 30, 0 ,7)
hlldphi = ROOT.TH1D("ll_dphi", "ll_dphi", 30, 0 ,np.pi)
hlldr = ROOT.TH1D("ll_dr", "ll_dr", 30, 0, 7)

# Step 8 GEN hists
hgenleppt = ROOT.TH1D('gen_lep_pt', 'gen_lep_pt', 30, 0, 1200)
hgenlepeta = ROOT.TH1D('gen_lep_eta', 'gen_lep_eta', 30, -7, 7)
hgenlepphi = ROOT.TH1D('gen_lep_phi', 'gen_lep_phi', 30, -np.pi, np.pi)

hgenaleppt = ROOT.TH1D('gen_alep_pt', 'gen_alep_pt', 30, 0, 1200)
hgenalepeta = ROOT.TH1D('gen_alep_eta', 'gen_alep_eta', 30, -7, 7)
hgenalepphi = ROOT.TH1D('gen_alep_phi', 'gen_alep_phi', 30, -np.pi, np.pi)

hgenmetpt = ROOT.TH1D('gen_met_pt', 'gen_met_pt', 30, 0, 1200)
hgenmetphi = ROOT.TH1D('gen_met_phi', 'gen_met_phi', 30, -np.pi, np.pi)

hgenbpt = ROOT.TH1D('gen_b_pt', 'gen_b_pt', 30, 0, 1200)
hgenbeta = ROOT.TH1D('gen_b_eta', 'gen_b_eta', 30, -7, 7)
hgenbphi = ROOT.TH1D('gen_b_phi', 'gen_b_phi', 30, -np.pi, np.pi)

hgenabpt = ROOT.TH1D('gen_ab_pt', 'gen_ab_pt', 30, 0, 1200)
hgenabeta = ROOT.TH1D('gen_ab_eta', 'gen_ab_eta', 30, -7, 7)
hgenabphi = ROOT.TH1D('gen_ab_phi', 'gen_ab_phi', 30, -np.pi, np.pi)

hgenneupt = ROOT.TH1D('gen_neu_pt', 'gen_neu_pt', 30, 0, 1200)
hgenneueta = ROOT.TH1D('gen_neu_eta', 'gen_neu_eta', 30, -7, 7)
hgenneuphi = ROOT.TH1D('gen_neu_phi', 'gen_neu_phi', 30, -np.pi, np.pi)

hgenaneupt = ROOT.TH1D('gen_aneu_pt', 'gen_aneu_pt', 30, 0, 1200)
hgenaneueta = ROOT.TH1D('gen_aneu_eta', 'gen_aneu_eta', 30, -7, 7)
hgenaneuphi = ROOT.TH1D('gen_aneu_phi', 'gen_aneu_phi', 30, -np.pi, np.pi)

hgentpt = ROOT.TH1D('gen_t_pt', 'gen_t_pt', 30, 0, 1200)
hgenteta = ROOT.TH1D('gen_t_eta', 'gen_t_eta', 30, -7, 7)
hgentphi = ROOT.TH1D('gen_t_phi', 'gen_t_phi', 30, -np.pi, np.pi)
hgentrap = ROOT.TH1D("gen_t_rap", "gen_t_rap", 30, -7, 7)

hgenatpt = ROOT.TH1D('gen_at_pt', 'gen_at_pt', 30, 0, 1200)
hgenateta = ROOT.TH1D('gen_at_eta', 'gen_at_eta', 30, -7, 7)
hgenatphi = ROOT.TH1D('gen_at_phi', 'gen_at_phi', 30, -np.pi, np.pi)
hgenatrap = ROOT.TH1D("gen_at_rap", "gen_at_rap", 30, -7, 7)

hgentatmass = ROOT.TH1D('gen_tat_mass', 'gen_tat_mass', 30, 0, 1200)
hgentatpt = ROOT.TH1D("gen_tat_pt", "gen_tat_pt", 30, 0 ,1200)
hgentateta = ROOT.TH1D("gen_tat_eta", "gen_tat_eta", 30, -7 ,7)
hgentatphi = ROOT.TH1D("gen_tat_phi", "gen_tat_phi", 30, -np.pi, np.pi)
hgentatrap = ROOT.TH1D("gen_tat_rap", "gen_tat_rap", 30, -7, 7)

hgenckk = ROOT.TH1D("gen_ckk", "gen_ckk", 30, -1, 1)
hgencrr = ROOT.TH1D("gen_crr", "gen_crr", 30, -1, 1)
hgencnn = ROOT.TH1D("gen_cnn", "gen_cnn", 30, -1, 1)

hgencrk = ROOT.TH1D("gen_crk", "gen_crk", 30, -1, 1)
hgenckr = ROOT.TH1D("gen_ckr", "gen_ckr", 30, -1, 1)

hgencPrk = ROOT.TH1D("gen_cP_rk", "gen_cP_rk", 30, -1, 1)
hgencMrk = ROOT.TH1D("gen_cM_rk", "gen_cM_rk", 30, -1, 1)

hgenchel = ROOT.TH1D("gen_c_hel", "gen_c_hel", 30, -1, 1)

hgenlldeta = ROOT.TH1D("gen_ll_deta", "gen_ll_deta", 30, 0 ,7)
hgenlldphi = ROOT.TH1D("gen_ll_dphi", "gen_ll_dphi", 30, 0 ,np.pi)
hgenlldr = ROOT.TH1D("gen_ll_dr", "gen_ll_dr", 30, 0, 7)

#htestdphi = ROOT.TH1D("test_ll_dphi", "test_ll_dphi", 30, 0 ,np.pi)
#hgentestdphi = ROOT.TH1D("gen_test_ll_dphi", "gen_test_ll_dphi", 30, 0 ,np.pi)

#2D hists

hrvgleppt = ROOT.TH2D('rvg_lep_pt', 'reco vs gen lep pt', 30, 0, 30, 30, 0, 1200)
hrvglepeta = ROOT.TH2D('rvg_lep_eta', 'reco vs gen lep eta', 30, -7, 7, 30, -7, 7)
hrvglepphi = ROOT.TH2D('rvg_lep_phi', 'reco vs gen lep phi', 30, -np.pi, np.pi, 30, -np.pi, np.pi)

hrvgaleppt = ROOT.TH2D('rvg_alep_pt', 'reco vs gen alep pt', 30, 0, 30, 30, 0, 1200)
hrvgalepeta = ROOT.TH2D('rvg_alep_eta', 'reco vs gen alep eta', 30, -7, 7, 30, -7, 7)
hrvgalepphi = ROOT.TH2D('rvg_alep_phi', 'reco vs gen alep phi', 30, -np.pi, np.pi, 30, -np.pi, np.pi)

hrvgmetpt = ROOT.TH2D('rvg_met_pt', 'reco vs gen met pt', 30, 0, 30, 30, 0, 1200)
hrvgmetphi = ROOT.TH2D('rvg_met_phi', 'reco vs gen met phi', 30, -np.pi, np.pi, 30, -np.pi, np.pi)

hrvgbpt = ROOT.TH2D('rvg_b_pt', 'reco vs gen b pt', 30, 0, 30, 30, 0, 1200)
hrvgbeta = ROOT.TH2D('rvg_b_eta', 'reco vs gen b eta', 30, -7, 7, 30, -7, 7)
hrvgbphi = ROOT.TH2D('rvg_b_phi', 'reco vs gen b phi', 30, -np.pi, np.pi, 30, -np.pi, np.pi)

hrvgabpt = ROOT.TH2D('rvg_ab_pt', 'reco vs gen ab pt', 30, 0, 30, 30, 0, 1200)
hrvgabeta = ROOT.TH2D('rvg_ab_eta', 'reco vs gen ab eta', 30, -7, 7, 30, -7, 7)
hrvgabphi = ROOT.TH2D('rvg_ab_phi', 'reco vs gen ab phi', 30, -np.pi, np.pi, 30, -np.pi, np.pi)

hrvgneupt = ROOT.TH2D('rvg_neu_pt', 'reco vs gen neu pt', 30, 0, 30, 30, 0, 1200)
hrvgneueta = ROOT.TH2D('rvg_neu_eta', 'reco vs gen neu eta', 30, -7, 7, 30, -7, 7)
hrvgneuphi = ROOT.TH2D('rvg_neu_phi', 'reco vs gen neu phi', 30, -np.pi, np.pi, 30, -np.pi, np.pi)

hrvganeupt = ROOT.TH2D('rvg_aneu_pt', 'reco vs gen aneu pt', 30, 0, 30, 30, 0, 1200)
hrvganeueta = ROOT.TH2D('rvg_aneu_eta', 'reco vs gen aneu eta', 30, -7, 7, 30, -7, 7)
hrvganeuphi = ROOT.TH2D('rvg_aneu_phi', 'reco vs gen aneu phi', 30, -np.pi, np.pi, 30, -np.pi, np.pi)

hrvgtpt = ROOT.TH2D('rvg_t_pt', 'reco vs gen t pt', 30, 0, 30, 30, 0, 1200)
hrvgteta = ROOT.TH2D('rvg_t_eta', 'reco vs gen t eta', 30, -7, 7, 30, -7, 7)
hrvgtphi = ROOT.TH2D('rvg_t_phi', 'reco vs gen t phi', 30, -np.pi, np.pi, 30, -np.pi, np.pi)
hrvgtrap = ROOT.TH2D('rvg_t_rap', 'reco vs gen t rap', 30, -7, 7, 30, -7, 7) 

hrvgatpt = ROOT.TH2D('rvg_at_pt', 'reco vs gen at pt', 30, 0, 30, 30, 0, 1200)
hrvgateta = ROOT.TH2D('rvg_at_eta', 'reco vs gen at eta', 30, -7, 7, 30, -7, 7)
hrvgatphi = ROOT.TH2D('rvg_at_phi', 'reco vs gen at phi', 30, -np.pi, np.pi, 30, -np.pi, np.pi)
hrvgatrap = ROOT.TH2D('rvg_at_rap', 'reco vs gen at rap', 30, -7, 7, 30, -7, 7)

hrvgtatm = ROOT.TH2D('rvg_tat_m', "reco vs gen tat mass", 30, 300, 30, 30, 300, 1400)
hrvgtatpt = ROOT.TH2D("rvg_tat_pt", "reco vs gen tat pt", 30, 0 ,30, 30, 0 ,1200)
hrvgtateta = ROOT.TH2D("rvg_tat_eta", "reco vs gen tat eta", 30, -7 ,7, 30, -7 ,7)
hrvgtatphi = ROOT.TH2D("rvg_tat_phi", "reco vs gen tat phi", 30, -np.pi, np.pi, 30, -np.pi, np.pi)
hrvgtatrap = ROOT.TH2D("rvg_tat_rap", "reco vs gen tat rap", 30, -7, 7, 30, -7, 7)

hrvgckk = ROOT.TH2D("rvg_ckk", "reco vs gen ckk", 30, -1, 1, 30, -1, 1)
hrvgcrr = ROOT.TH2D("rvg_crr", "reco vs gen crr", 30, -1, 1, 30, -1, 1)
hrvgcnn = ROOT.TH2D("rvg_cnn", "reco vs gen cnn", 30, -1, 1, 30, -1, 1)

hrvgcrk = ROOT.TH2D('rvg_crk', "reco vs gen crk", 30, -1, 1, 30, -1, 1)
hrvgckr = ROOT.TH2D('rvg_ckr', "reco vs gen ckr", 30, -1, 1, 30, -1, 1)

hrvgcPrk = ROOT.TH2D("rvg_cPrk", "reco vs gen cPrk", 30, -1, 1, 30, -1, 1)
hrvgcMrk = ROOT.TH2D("rvg_cMrk", "reco vs gen cMrk", 30, -1, 1, 30, -1, 1)

hrvgchel = ROOT.TH2D("rvg_c_hel", "reco vs gen c_hel", 30, -1, 1, 30, -1, 1)

hrvglldeta = ROOT.TH2D("rvg_ll_deta", "reco vs gen ll deta", 30, 0 ,7, 30, 0 ,7)
hrvglldphi = ROOT.TH2D("rvg_ll_dphi", "reco vs gen ll dphi", 30, 0 ,np.pi, 30, 0 ,np.pi)
hrvglldr = ROOT.TH2D("rvg_ll_dr", "reco vs gen ll dr", 30, 0, 7, 30, 0, 7)

# Step 7 hists

h_KinReco_d_angle_jet_step7 = ROOT.TH1D("KinReco_d_angle_jet_step7", ";#alpha, rad;Entries", 200, 0, 0.5 ) 
h_KinReco_d_angle_lep_step7 = ROOT.TH1D("KinReco_d_angle_lep_step7", ";#alpha, rad;Entries", 200, 0, 0.2 )
h_KinReco_fE_jet_step7 = ROOT.TH1D("KinReco_fE_jet_step7", "Jet Energy Correction Factor;#frac{E^{true}_{jet}}{E^{reco}_{jet}};Entries", 200, 0, 4 )
h_KinReco_fE_lep_step7 = ROOT.TH1D("KinReco_fE_lep_step7", "Lepton Energy Correction Factor;#frac{E^{true}_{lep}}{E^{reco}_{lep}};Entries", 200, 0.5, 2.5 )  
h_KinReco_mbl_true_step7  = ROOT.TH1D("KinReco_mbl_true_step7","mbl_true", 200, 0, 200 )

## STEP 8

fileptr = uproot.open(inputFile)['Step8']

t_pt     = fileptr['top_pt'].array()
t_phi    = fileptr['top_phi'].array()
t_eta    = fileptr['top_eta'].array()
t_rap    = fileptr['top_rapidity'].array()

tbar_pt  = fileptr['atop_pt'].array()
tbar_phi = fileptr['atop_phi'].array()
tbar_eta = fileptr['atop_eta'].array()
tbar_rap = fileptr['atop_rapidity'].array()

tt_mass  = fileptr['tt_mass'].array()
tt_pt = fileptr['tt_pt'].array()
tt_eta = fileptr['tt_eta'].array()
tt_phi = fileptr['tt_phi'].array()
tt_rap = fileptr['tt_rap'].array()

l_pt     = fileptr['lep_pt'].array()
l_phi    = fileptr['lep_phi'].array()
l_eta    = fileptr['lep_eta'].array()
l_mass   = fileptr['lep_mass'].array()

lbar_pt   = fileptr['alep_pt'].array()
lbar_phi  = fileptr['alep_phi'].array()
lbar_eta  = fileptr['alep_eta'].array()
lbar_mass = fileptr['alep_mass'].array()

gen_t_pt     = fileptr['gen_top_pt'].array()
gen_t_phi    = fileptr['gen_top_phi'].array()
gen_t_eta    = fileptr['gen_top_eta'].array()
gen_t_rap    = fileptr['gen_top_rapidity'].array()

gen_tbar_pt  = fileptr['gen_atop_pt'].array()
gen_tbar_phi = fileptr['gen_atop_phi'].array()
gen_tbar_eta = fileptr['gen_atop_eta'].array()
gen_tbar_rap = fileptr['gen_atop_rapidity'].array()

gen_tt_mass  = fileptr['gen_tt_mass'].array()
gen_tt_pt = fileptr['gen_tt_pt'].array()
gen_tt_eta = fileptr['gen_tt_eta'].array()
gen_tt_phi = fileptr['gen_tt_phi'].array()
gen_tt_rap = fileptr['gen_tt_rap'].array()

gen_l_pt     = fileptr['gen_lep_pt'].array()
gen_l_phi    = fileptr['gen_lep_phi'].array()
gen_l_eta    = fileptr['gen_lep_eta'].array()
gen_l_mass   = fileptr['gen_lep_mass'].array()

gen_lbar_pt   = fileptr['gen_alep_pt'].array()
gen_lbar_phi  = fileptr['gen_alep_phi'].array()
gen_lbar_eta  = fileptr['gen_alep_eta'].array()
gen_lbar_mass = fileptr['gen_alep_mass'].array()


for i in range(len(t_pt)):

    if (i % 12000 == 0):
        print('Processing event :: ' + str(i))
        now = datetime.now()  # Time keeping
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

    top = ROOT.TLorentzVector()
    atop = ROOT.TLorentzVector()
    lep = ROOT.TLorentzVector()
    alep = ROOT.TLorentzVector()

    gen_top = ROOT.TLorentzVector()
    gen_atop = ROOT.TLorentzVector()
    gen_lep = ROOT.TLorentzVector()
    gen_alep = ROOT.TLorentzVector()

    top.SetPtEtaPhiM(t_pt[i], t_rap[i], t_phi[i], 172.5)
    atop.SetPtEtaPhiM(tbar_pt[i], tbar_rap[i], tbar_phi[i], 172.5)  # Changed from eta to rap
    gen_top.SetPtEtaPhiM(gen_t_pt[i], gen_t_rap[i], gen_t_phi[i], 172.5)
    gen_atop.SetPtEtaPhiM(gen_tbar_pt[i], gen_tbar_rap[i], gen_tbar_phi[i], 172.5)

    lep.SetPtEtaPhiM(l_pt[i], l_eta[i], l_phi[i], l_mass[i])
    alep.SetPtEtaPhiM(lbar_pt[i], lbar_eta[i], lbar_phi[i], lbar_mass[i])
    gen_lep.SetPtEtaPhiM(gen_l_pt[i], gen_l_eta[i], gen_l_phi[i], gen_l_mass[i])
    gen_alep.SetPtEtaPhiM(gen_lbar_pt[i], gen_lbar_eta[i], gen_lbar_phi[i], gen_lbar_mass[i])

    # The various Bernreuther bases
    kBase = ROOT.TVector3()
    jBase = ROOT.TVector3()
    qBase = ROOT.TVector3()
    # rBase = ROOT.TVector3()
    # nBase = ROOT.TVector3()
    gen_kBase = ROOT.TVector3()
    gen_jBase = ROOT.TVector3()
    gen_qBase = ROOT.TVector3()

    # Beam unit vector
    p3_pPro = ROOT.TVector3(0., 0., 1.)
    gen_p3_pPro = ROOT.TVector3(0., 0., 1.)

    # The bases definition: Bernreuther spinMatrix 1508.05271
    p4_TT = top + atop
    b4_TT = ROOT.TVector3(-1. * p4_TT.BoostVector())

    b4_pTop = top
    b4_pTop.Boost(b4_TT)

    b4_aTop = atop
    b4_aTop.Boost(b4_TT)

    gen_p4_TT = gen_top + gen_atop
    gen_b4_TT = ROOT.TVector3(-1. * gen_p4_TT.BoostVector())

    gen_b4_pTop = gen_top
    gen_b4_pTop.Boost(gen_b4_TT)

    gen_b4_aTop = gen_atop
    gen_b4_aTop.Boost(gen_b4_TT)

    # Maybe need to be careful with the signs here ?? Check how the pairings are implemented in the FW

    ll_dEta = abs(ifOk(alep.Eta() - lep.Eta()))
    ll_dPhi = abs(ifOk(alep.DeltaPhi(lep)))
    ll_dR = abs(ifOk(alep.DeltaR(lep)))

    gen_ll_dEta = abs(ifOk(gen_alep.Eta() - gen_lep.Eta()))
    gen_ll_dPhi = abs(ifOk(gen_alep.DeltaPhi(gen_lep)))
    gen_ll_dR = abs(ifOk(gen_alep.DeltaR(gen_lep)))

    hlldeta.Fill(ll_dEta)
    hlldphi.Fill(ll_dPhi)
    hlldr.Fill(ll_dR)

    hgenlldeta.Fill(gen_ll_dEta)
    hgenlldphi.Fill(gen_ll_dPhi)
    hgenlldr.Fill(gen_ll_dR)

    b4_aLep = alep
    b4_aLep.Boost(b4_TT)
    b4_aLep.Boost(-1. * b4_pTop.BoostVector())

    b4_pLep = lep
    b4_pLep.Boost(b4_TT)
    b4_pLep.Boost(-1. * b4_aTop.BoostVector())

    gen_b4_aLep = gen_alep
    gen_b4_aLep.Boost(gen_b4_TT)
    gen_b4_aLep.Boost(-1. * gen_b4_pTop.BoostVector())

    gen_b4_pLep = gen_lep
    gen_b4_pLep.Boost(gen_b4_TT)
    gen_b4_pLep.Boost(-1. * gen_b4_aTop.BoostVector())

    # Calculating the top-beam angle for pTop only
    c_pTP = b4_pTop.Vect().Unit().Dot(p3_pPro)
    s_pTP = np.sqrt(1. - (c_pTP * c_pTP))

    gen_c_pTP = gen_b4_pTop.Vect().Unit().Dot(gen_p3_pPro)
    gen_s_pTP = np.sqrt(1. - (gen_c_pTP * gen_c_pTP))

    # The signs needed to account for Bose symmetry
    sY = 1. if (c_pTP >= 0.) else -1.
    sD = 1. if (abs(top.Rapidity()) >= abs(atop.Rapidity())) else -1.

    gen_sY = 1. if (gen_c_pTP >= 0.) else -1.
    gen_sD = 1. if (abs(gen_top.Rapidity()) >= abs(gen_atop.Rapidity())) else -1.

    # Define the base vectors a
    # j and q base are the k* and r* respectively
    # b is always -a

    kBase = b4_pTop.Vect().Unit()
    jBase = sD * kBase
    r_arr = (sY / s_pTP) * (p3_pPro - (c_pTP * kBase))  # Store in a temp np array since pyROOT typecasts automatically
    rBase = ROOT.TVector3(r_arr[0], r_arr[1], r_arr[2]).Unit()
    qBase = sD * rBase
    n_arr = (sY / s_pTP) * p3_pPro.Cross(kBase)  # Store in a temp np array since pyROOT typecasts automatically
    nBase = ROOT.TVector3(n_arr[0], n_arr[1], n_arr[2]).Unit()

    gen_kBase = gen_b4_pTop.Vect().Unit()
    gen_jBase = gen_sD * gen_kBase
    gen_r_arr = (gen_sY / gen_s_pTP) * (gen_p3_pPro - (gen_c_pTP * gen_kBase))  # Store in a temp np array since pyROOT typecasts automatically
    gen_rBase = ROOT.TVector3(gen_r_arr[0], gen_r_arr[1], gen_r_arr[2]).Unit()
    gen_qBase = gen_sD * gen_rBase
    gen_n_arr = (gen_sY / gen_s_pTP) * p3_pPro.Cross(gen_kBase)  # Store in a temp np array since pyROOT typecasts automatically
    gen_nBase = ROOT.TVector3(gen_n_arr[0], gen_n_arr[1], gen_n_arr[2]).Unit()

    # Find the relevant angles in these bases
    ck_aLep = b4_aLep.Vect().Unit().Dot(kBase)
    ck_pLep = b4_pLep.Vect().Unit().Dot(-1. * kBase)

    cj_aLep = b4_aLep.Vect().Unit().Dot(jBase)
    cj_pLep = b4_pLep.Vect().Unit().Dot(-1. * jBase)

    cr_aLep = b4_aLep.Vect().Unit().Dot(rBase)
    cr_pLep = b4_pLep.Vect().Unit().Dot(-1. * rBase)

    cq_aLep = b4_aLep.Vect().Unit().Dot(qBase)
    cq_pLep = b4_pLep.Vect().Unit().Dot(-1. * qBase)

    cn_aLep = b4_aLep.Vect().Unit().Dot(nBase)
    cn_pLep = b4_pLep.Vect().Unit().Dot(-1. * nBase)

    gen_ck_aLep = gen_b4_aLep.Vect().Unit().Dot(gen_kBase)
    gen_ck_pLep = gen_b4_pLep.Vect().Unit().Dot(-1. * gen_kBase)

    gen_cj_aLep = gen_b4_aLep.Vect().Unit().Dot(gen_jBase)
    gen_cj_pLep = gen_b4_pLep.Vect().Unit().Dot(-1. * gen_jBase)

    gen_cr_aLep = gen_b4_aLep.Vect().Unit().Dot(gen_rBase)
    gen_cr_pLep = gen_b4_pLep.Vect().Unit().Dot(-1. * gen_rBase)

    gen_cq_aLep = gen_b4_aLep.Vect().Unit().Dot(gen_qBase)
    gen_cq_pLep = gen_b4_pLep.Vect().Unit().Dot(-1. * gen_qBase)

    gen_cn_aLep = gen_b4_aLep.Vect().Unit().Dot(gen_nBase)
    gen_cn_pLep = gen_b4_pLep.Vect().Unit().Dot(-1. * gen_nBase)

    # Fill the raw angles into VarFloats
    b1k = ifOk(ck_aLep)
    b2k = ifOk(ck_pLep)

    b1j = ifOk(cj_aLep)
    b2j = ifOk(cj_pLep)

    b1r = ifOk(cr_aLep)
    b2r = ifOk(cr_pLep)

    b1q = ifOk(cq_aLep)
    b2q = ifOk(cq_pLep)

    b1n = ifOk(cn_aLep)
    b2n = ifOk(cn_pLep)

    gen_b1k = ifOk(gen_ck_aLep)
    gen_b2k = ifOk(gen_ck_pLep)

    gen_b1j = ifOk(gen_cj_aLep)
    gen_b2j = ifOk(gen_cj_pLep)

    gen_b1r = ifOk(gen_cr_aLep)
    gen_b2r = ifOk(gen_cr_pLep)

    gen_b1q = ifOk(gen_cq_aLep)
    gen_b2q = ifOk(gen_cq_pLep)

    gen_b1n = ifOk(gen_cn_aLep)
    gen_b2n = ifOk(gen_cn_pLep)

    # Now we can squeeze it all out based on table 5 page 16
    # The B1 ~ c_aLep, B2 ~ c_pLep sums

    bP_kk = ifOk(ck_aLep + ck_pLep)
    bM_kk = ifOk(ck_aLep - ck_pLep)

    bP_jj = ifOk(cj_aLep + cj_pLep)
    bM_jj = ifOk(cj_aLep - cj_pLep)

    bP_rr = ifOk(cr_aLep + cr_pLep)
    bM_rr = ifOk(cr_aLep - cr_pLep)

    bP_qq = ifOk(cq_aLep + cq_pLep)
    bM_qq = ifOk(cq_aLep - cq_pLep)

    bP_nn = ifOk(cn_aLep + cn_pLep)
    bM_nn = ifOk(cn_aLep - cn_pLep)

    gen_bP_kk = ifOk(gen_ck_aLep + gen_ck_pLep)
    gen_bM_kk = ifOk(gen_ck_aLep - gen_ck_pLep)

    gen_bP_jj = ifOk(gen_cj_aLep + gen_cj_pLep)
    gen_bM_jj = ifOk(gen_cj_aLep - gen_cj_pLep)

    gen_bP_rr = ifOk(gen_cr_aLep + gen_cr_pLep)
    gen_bM_rr = ifOk(gen_cr_aLep - gen_cr_pLep)

    gen_bP_qq = ifOk(gen_cq_aLep + gen_cq_pLep)
    gen_bM_qq = ifOk(gen_cq_aLep - gen_cq_pLep)

    gen_bP_nn = ifOk(gen_cn_aLep + gen_cn_pLep)
    gen_bM_nn = ifOk(gen_cn_aLep - gen_cn_pLep)

    # spinCorr coeff Cab = -9<cab>
    ckk = ifOk(ck_aLep * ck_pLep)
    crr = ifOk(cr_aLep * cr_pLep)
    cnn = ifOk(cn_aLep * cn_pLep)

    crk = cr_aLep * ck_pLep
    ckr = ck_aLep * cr_pLep

    cnr = cn_aLep * cr_pLep
    crn = cr_aLep * cn_pLep

    cnk = cn_aLep * ck_pLep
    ckn = ck_aLep * cn_pLep

    cP_rk = ifOk(crk + ckr)
    cM_rk = ifOk(crk - ckr)

    cP_nr = ifOk(cnr + crn)
    cM_nr = ifOk(cnr - crn)

    cP_nk = ifOk(cnk + ckn)
    cM_nk = ifOk(cnk - ckn)

    gen_ckk = ifOk(gen_ck_aLep * gen_ck_pLep)
    gen_crr = ifOk(gen_cr_aLep * gen_cr_pLep)
    gen_cnn = ifOk(gen_cn_aLep * gen_cn_pLep)

    gen_crk = gen_cr_aLep * gen_ck_pLep
    gen_ckr = gen_ck_aLep * gen_cr_pLep

    gen_cnr = gen_cn_aLep * gen_cr_pLep
    gen_crn = gen_cr_aLep * gen_cn_pLep

    gen_cnk = gen_cn_aLep * gen_ck_pLep
    gen_ckn = gen_ck_aLep * gen_cn_pLep

    gen_cP_rk = ifOk(gen_crk + gen_ckr)
    gen_cM_rk = ifOk(gen_crk - gen_ckr)

    gen_cP_nr = ifOk(gen_cnr + gen_crn)
    gen_cM_nr = ifOk(gen_cnr - gen_crn)

    gen_cP_nk = ifOk(gen_cnk + gen_ckn)
    gen_cM_nk = ifOk(gen_cnk - gen_ckn)

    # Find also the opening angles of the lepton

    cHel = ifOk(b4_aLep.Vect().Unit().Dot(b4_pLep.Vect().Unit()))

    #testdphi = abs(ifOk(b4_aLep.DeltaPhi(b4_pLep)))


    gen_cHel = ifOk(gen_b4_aLep.Vect().Unit().Dot(gen_b4_pLep.Vect().Unit()))

    #gentestdphi = abs(ifOk(gen_b4_aLep.DeltaPhi(gen_b4_pLep)))



    # Fill RECO

    hleppt.Fill(fileptr['lep_pt'].array()[i])
    hlepeta.Fill(fileptr['lep_eta'].array()[i])
    hlepphi.Fill(fileptr['lep_phi'].array()[i])

    haleppt.Fill(fileptr['alep_pt'].array()[i])
    halepeta.Fill(fileptr['alep_eta'].array()[i])
    halepphi.Fill(fileptr['alep_phi'].array()[i])

    hmetpt.Fill(fileptr['met_pt'].array()[i])
    hmetphi.Fill(fileptr['met_phi'].array()[i])

    hbpt.Fill(fileptr['b_pt'].array()[i])
    hbeta.Fill(fileptr['b_eta'].array()[i])
    hbphi.Fill(fileptr['b_phi'].array()[i])

    habpt.Fill(fileptr['ab_pt'].array()[i])
    habeta.Fill(fileptr['ab_eta'].array()[i])
    habphi.Fill(fileptr['ab_phi'].array()[i])

    hneupt.Fill(fileptr['neu_pt'].array()[i])
    hneueta.Fill(fileptr['neu_eta'].array()[i])
    hneuphi.Fill(fileptr['neu_phi'].array()[i])

    haneupt.Fill(fileptr['aneu_pt'].array()[i])
    haneueta.Fill(fileptr['aneu_eta'].array()[i])
    haneuphi.Fill(fileptr['aneu_phi'].array()[i])

    htpt.Fill(fileptr['top_pt'].array()[i])
    hteta.Fill(fileptr['top_eta'].array()[i])
    htphi.Fill(fileptr['top_phi'].array()[i])
    htrap.Fill(fileptr['top_rapidity'].array()[i])

    hatpt.Fill(fileptr['atop_pt'].array()[i])
    hateta.Fill(fileptr['atop_eta'].array()[i])
    hatphi.Fill(fileptr['atop_phi'].array()[i])
    hatrap.Fill(fileptr['atop_rapidity'].array()[i])

    htatmass.Fill(fileptr['tt_mass'].array()[i])
    htatpt.Fill(fileptr['tt_pt'].array()[i])
    htateta.Fill(fileptr['tt_eta'].array()[i])
    htatphi.Fill(fileptr['tt_phi'].array()[i])
    htatrap.Fill(fileptr['tt_rap'].array()[i])

    hckk.Fill(ckk)
    hcrr.Fill(crr)
    hcnn.Fill(cnn)

    hcrk.Fill(crk)
    hckr.Fill(ckr)

    hcPrk.Fill(cP_rk)
    hcMrk.Fill(cM_rk)
    
    hchel.Fill(cHel)



    # Fill GEN

    hgenleppt.Fill(fileptr['gen_lep_pt'].array()[i])
    hgenlepeta.Fill(fileptr['gen_lep_eta'].array()[i])
    hgenlepphi.Fill(fileptr['gen_lep_phi'].array()[i])

    hgenaleppt.Fill(fileptr['gen_alep_pt'].array()[i])
    hgenalepeta.Fill(fileptr['gen_alep_eta'].array()[i])
    hgenalepphi.Fill(fileptr['gen_alep_phi'].array()[i])

    hgenmetpt.Fill(fileptr['gen_met_pt'].array()[i])
    hgenmetphi.Fill(fileptr['gen_met_phi'].array()[i])

    hgenbpt.Fill(fileptr['gen_b_pt'].array()[i])
    hgenbeta.Fill(fileptr['gen_b_eta'].array()[i])
    hgenbphi.Fill(fileptr['gen_b_phi'].array()[i])

    hgenabpt.Fill(fileptr['gen_ab_pt'].array()[i])
    hgenabeta.Fill(fileptr['gen_ab_eta'].array()[i])
    hgenabphi.Fill(fileptr['gen_ab_phi'].array()[i])

    hgenneupt.Fill(fileptr['gen_neu_pt'].array()[i])
    hgenneueta.Fill(fileptr['gen_neu_eta'].array()[i])
    hgenneuphi.Fill(fileptr['gen_neu_phi'].array()[i])

    hgenaneupt.Fill(fileptr['gen_aneu_pt'].array()[i])
    hgenaneueta.Fill(fileptr['gen_aneu_eta'].array()[i])
    hgenaneuphi.Fill(fileptr['gen_aneu_phi'].array()[i])

    hgentpt.Fill(fileptr['gen_top_pt'].array()[i])
    hgenteta.Fill(fileptr['gen_top_eta'].array()[i])
    hgentphi.Fill(fileptr['gen_top_phi'].array()[i])
    hgentrap.Fill(fileptr['gen_top_rapidity'].array()[i])

    hgenatpt.Fill(fileptr['gen_atop_pt'].array()[i])
    hgenateta.Fill(fileptr['gen_atop_eta'].array()[i])
    hgenatphi.Fill(fileptr['gen_atop_phi'].array()[i])
    hgenatrap.Fill(fileptr['gen_atop_rapidity'].array()[i])

    hgentatmass.Fill(fileptr['gen_tt_mass'].array()[i])
    hgentatpt.Fill(fileptr['gen_tt_pt'].array()[i])
    hgentateta.Fill(fileptr['gen_tt_eta'].array()[i])
    hgentatphi.Fill(fileptr['gen_tt_phi'].array()[i])
    hgentatrap.Fill(fileptr['gen_tt_rap'].array()[i])

    hgenckk.Fill(gen_ckk)
    hgencrr.Fill(gen_crr)
    hgencnn.Fill(gen_cnn)

    hgencrk.Fill(gen_crk)
    hgenckr.Fill(gen_ckr)

    hgencPrk.Fill(gen_cP_rk)
    hgencMrk.Fill(gen_cM_rk)

    hgenchel.Fill(gen_cHel)




    #htestdphi.Fill(testdphi)
    #hgentestdphi.Fill(gentestdphi)

    # Fill RECO vs GEN

    hrvgleppt.Fill(fileptr['lep_pt'].array()[i], fileptr['gen_lep_pt'].array()[i])
    hrvglepeta.Fill(fileptr['lep_eta'].array()[i], fileptr['gen_lep_eta'].array()[i])
    hrvglepphi.Fill(fileptr['lep_phi'].array()[i], fileptr['gen_lep_phi'].array()[i])

    hrvgaleppt.Fill(fileptr['alep_pt'].array()[i], fileptr['gen_alep_pt'].array()[i])
    hrvgalepeta.Fill(fileptr['alep_eta'].array()[i], fileptr['gen_alep_eta'].array()[i])
    hrvgalepphi.Fill(fileptr['alep_phi'].array()[i], fileptr['gen_alep_phi'].array()[i])

    hrvgmetpt.Fill(fileptr['met_pt'].array()[i], fileptr['gen_met_pt'].array()[i])
    hrvgmetphi.Fill(fileptr['met_phi'].array()[i], fileptr['gen_met_phi'].array()[i])

    hrvgbpt.Fill(fileptr['b_pt'].array()[i], fileptr['gen_b_pt'].array()[i])
    hrvgbeta.Fill(fileptr['b_eta'].array()[i], fileptr['gen_b_eta'].array()[i])
    hrvgbphi.Fill(fileptr['b_phi'].array()[i], fileptr['gen_b_phi'].array()[i])

    hrvgabpt.Fill(fileptr['ab_pt'].array()[i], fileptr['gen_ab_pt'].array()[i])
    hrvgabeta.Fill(fileptr['ab_eta'].array()[i], fileptr['gen_ab_eta'].array()[i])
    hrvgabphi.Fill(fileptr['ab_phi'].array()[i], fileptr['gen_ab_phi'].array()[i])

    hrvgtpt.Fill(t_pt[i], fileptr['gen_top_pt'].array()[i])
    hrvgteta.Fill(t_eta[i], fileptr['gen_top_eta'].array()[i])
    hrvgtphi.Fill(fileptr['top_phi'].array()[i], fileptr['gen_top_phi'].array()[i])
    hrvgtrap.Fill(fileptr['top_rapidity'].array()[i], fileptr['gen_top_rapidity'].array()[i])

    hrvgatpt.Fill(tbar_pt[i], fileptr['gen_atop_pt'].array()[i])
    hrvgateta.Fill(tbar_eta[i], fileptr['gen_atop_eta'].array()[i])
    hrvgatphi.Fill(fileptr['atop_phi'].array()[i], fileptr['gen_atop_phi'].array()[i])
    hrvgatrap.Fill(fileptr['atop_rapidity'].array()[i], fileptr['gen_atop_rapidity'].array()[i])

    hrvgtatm.Fill(tt_mass[i], fileptr['gen_tt_mass'].array()[i])
    hrvgtatpt.Fill(fileptr['tt_pt'].array()[i], fileptr['gen_tt_pt'].array()[i])
    hrvgtateta.Fill(fileptr['tt_eta'].array()[i], fileptr['gen_tt_eta'].array()[i])
    hrvgtatphi.Fill(fileptr['tt_phi'].array()[i], fileptr['gen_tt_phi'].array()[i])
    hrvgtatrap.Fill(fileptr['tt_rap'].array()[i], fileptr['gen_tt_rap'].array()[i])

    hrvgckk.Fill(ckk, gen_ckk)
    hrvgcrr.Fill(crr, gen_crr)
    hrvgcnn.Fill(cnn, gen_cnn)

    hrvgcrk.Fill(crk, gen_crk)
    hrvgckr.Fill(ckr, gen_ckr)

    hrvgcPrk.Fill(cP_rk, gen_cP_rk)
    hrvgcMrk.Fill(cM_rk, gen_cM_rk)

    hrvgchel.Fill(cHel, gen_cHel)
    
    hrvglldeta.Fill(ll_dEta, gen_ll_dEta)
    hrvglldphi.Fill(ll_dPhi, gen_ll_dPhi)
    hrvglldr.Fill(ll_dR, gen_ll_dR)


## STEP 7

fileptr = uproot.open(inputFile)['Step7']

gen_lep_pt = fileptr['gen_lep_pt'].array()
gen_lep_eta = fileptr['gen_lep_eta'].array()
gen_lep_phi = fileptr['gen_lep_phi'].array()
gen_lep_mass = fileptr['gen_lep_mass'].array()

gen_alep_pt = fileptr['gen_alep_pt'].array()
gen_alep_eta = fileptr['gen_alep_eta'].array()
gen_alep_phi = fileptr['gen_alep_phi'].array()
gen_alep_mass = fileptr['gen_alep_mass'].array()

gen_b_pt = fileptr['gen_b_pt'].array()
gen_b_eta = fileptr['gen_b_eta'].array()
gen_b_phi = fileptr['gen_b_phi'].array()
gen_b_mass = fileptr['gen_b_mass'].array()

gen_ab_pt = fileptr['gen_ab_pt'].array()
gen_ab_eta = fileptr['gen_ab_eta'].array()
gen_ab_phi = fileptr['gen_ab_phi'].array()
gen_ab_mass = fileptr['gen_ab_mass'].array()

lep_nearest_pt = fileptr['lep_nearest_pt'].array()
lep_nearest_eta = fileptr['lep_nearest_eta'].array()
lep_nearest_phi = fileptr['lep_nearest_phi'].array()
lep_nearest_mass = fileptr['lep_nearest_mass'].array()

alep_nearest_pt = fileptr['alep_nearest_pt'].array()
alep_nearest_eta = fileptr['alep_nearest_eta'].array()
alep_nearest_phi = fileptr['alep_nearest_phi'].array()
alep_nearest_mass = fileptr['alep_nearest_mass'].array()

bjet_nearest_pt = fileptr['bjet_nearest_pt'].array()
bjet_nearest_eta = fileptr['bjet_nearest_eta'].array()
bjet_nearest_phi = fileptr['bjet_nearest_phi'].array()
bjet_nearest_mass = fileptr['bjet_nearest_mass'].array()

abjet_nearest_pt = fileptr['abjet_nearest_pt'].array()
abjet_nearest_eta = fileptr['abjet_nearest_eta'].array()
abjet_nearest_phi = fileptr['abjet_nearest_phi'].array()
abjet_nearest_mass = fileptr['abjet_nearest_mass'].array()


for i in range(len(fileptr['lep_nearest_pt'].array())):

    gen_lep_4vec  = ROOT.TLorentzVector()
    gen_alep_4vec = ROOT.TLorentzVector()

    gen_lep_4vec.SetPtEtaPhiM(gen_lep_pt[i] , gen_lep_eta[i] , gen_lep_phi[i] , gen_lep_mass[i])
    gen_alep_4vec.SetPtEtaPhiM(gen_alep_pt[i] , gen_alep_eta[i] , gen_alep_phi[i] , gen_alep_mass[i])

    gen_b_4vec  = ROOT.TLorentzVector()
    gen_ab_4vec = ROOT.TLorentzVector()

    gen_b_4vec.SetPtEtaPhiM(gen_b_pt[i] , gen_b_eta[i] , gen_b_phi[i] , gen_b_mass[i])
    gen_ab_4vec.SetPtEtaPhiM(gen_ab_pt[i] , gen_ab_eta[i] , gen_ab_phi[i] , gen_ab_mass[i])

    lep_nearest_4vec  = ROOT.TLorentzVector()
    alep_nearest_4vec = ROOT.TLorentzVector()

    lep_nearest_4vec.SetPtEtaPhiM(lep_nearest_pt[i] , lep_nearest_eta[i] , lep_nearest_phi[i] , lep_nearest_mass[i])
    alep_nearest_4vec.SetPtEtaPhiM(alep_nearest_pt[i] , alep_nearest_eta[i] , alep_nearest_phi[i] , alep_nearest_mass[i])

    bjet_nearest_4vec  = ROOT.TLorentzVector()
    abjet_nearest_4vec = ROOT.TLorentzVector()

    bjet_nearest_4vec.SetPtEtaPhiM(bjet_nearest_pt[i] , bjet_nearest_eta[i] , bjet_nearest_phi[i] , bjet_nearest_mass[i])
    abjet_nearest_4vec.SetPtEtaPhiM(abjet_nearest_pt[i] , abjet_nearest_eta[i] , abjet_nearest_phi[i] , abjet_nearest_mass[i])

    
    h_KinReco_fE_jet_step7.Fill(gen_b_4vec.E()/bjet_nearest_4vec.E())
    h_KinReco_fE_jet_step7.Fill(gen_ab_4vec.E()/abjet_nearest_4vec.E())

    h_KinReco_fE_lep_step7.Fill(gen_lep_4vec.E()/lep_nearest_4vec.E())
    h_KinReco_fE_lep_step7.Fill(gen_alep_4vec.E()/alep_nearest_4vec.E())


    h_KinReco_d_angle_jet_step7.Fill(gen_b_4vec.Angle(bjet_nearest_4vec.Vect()))
    h_KinReco_d_angle_jet_step7.Fill(gen_ab_4vec.Angle(abjet_nearest_4vec.Vect()))

    h_KinReco_d_angle_lep_step7.Fill(gen_lep_4vec.Angle(lep_nearest_4vec.Vect()))
    h_KinReco_d_angle_lep_step7.Fill(gen_alep_4vec.Angle(alep_nearest_4vec.Vect()))

    h_KinReco_mbl_true_step7.Fill((gen_alep_4vec + gen_b_4vec).M())
    h_KinReco_mbl_true_step7.Fill((gen_lep_4vec + gen_ab_4vec).M())
    
   

opfile.Write()
opfile.Close()
