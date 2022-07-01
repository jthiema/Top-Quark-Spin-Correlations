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

# Step 8 RECO hists
hleppt = ROOT.TH1D('lep_pt', 'lep_pt', 1200, 0, 1200)
hlepeta = ROOT.TH1D('lep_eta', 'lep_eta', 1200, -2*np.pi, 2*np.pi)
hlepphi = ROOT.TH1D('lep_phi', 'lep_phi', 1200, -2*np.pi, 2*np.pi)

haleppt = ROOT.TH1D('alep_pt', 'alep_pt', 1200, 0, 1200)
halepeta = ROOT.TH1D('alep_eta', 'alep_eta', 1200, -2*np.pi, 2*np.pi)
halepphi = ROOT.TH1D('alep_phi', 'alep_phi', 1200, -2*np.pi, 2*np.pi)

hmetpt = ROOT.TH1D('met_pt', 'met_pt', 1200, 0, 1200)
hmetphi = ROOT.TH1D('met_phi', 'met_phi', 1200, -2*np.pi, 2*np.pi)

hbpt = ROOT.TH1D('b_pt', 'b_pt', 1200, 0, 1200)
hbeta = ROOT.TH1D('b_eta', 'b_eta', 1200, -2*np.pi, 2*np.pi)
hbphi = ROOT.TH1D('b_phi', 'b_phi', 1200, -2*np.pi, 2*np.pi)

habpt = ROOT.TH1D('ab_pt', 'ab_pt', 1200, 0, 1200)
habeta = ROOT.TH1D('ab_eta', 'ab_eta', 1200, -2*np.pi, 2*np.pi)
habphi = ROOT.TH1D('ab_phi', 'ab_phi', 1200, -2*np.pi, 2*np.pi)

hneupt = ROOT.TH1D('neu_pt', 'neu_pt', 1200, 0, 1200)
hneueta = ROOT.TH1D('neu_eta', 'neu_eta', 1200, -2*np.pi, 2*np.pi)
hneuphi = ROOT.TH1D('neu_phi', 'neu_phi', 1200, -2*np.pi, 2*np.pi)

haneupt = ROOT.TH1D('aneu_pt', 'aneu_pt', 1200, 0, 1200)
haneueta = ROOT.TH1D('aneu_eta', 'aneu_eta', 1200, -2*np.pi, 2*np.pi)
haneuphi = ROOT.TH1D('aneu_phi', 'aneu_phi', 1200, -2*np.pi, 2*np.pi)

htpt = ROOT.TH1D('t_pt', 't_pt', 1200, 0, 1200)
hteta = ROOT.TH1D('t_eta', 't_eta', 1200, -2*np.pi, 2*np.pi)
htphi = ROOT.TH1D('t_phi', 't_phi', 1200, -2*np.pi, 2*np.pi)

hatpt = ROOT.TH1D('at_pt', 'at_pt', 1200, 0, 1200)
hateta = ROOT.TH1D('at_eta', 'at_eta', 1200, -2*np.pi, 2*np.pi)
hatphi = ROOT.TH1D('at_phi', 'at_phi', 1200, -2*np.pi, 2*np.pi)

htatmass = ROOT.TH1D('tat_mass', 'tat_mass', 1200, 0, 1200)

hckk = ROOT.TH1D("ckk", "ckk", 1200, -1, 1)
hcrr = ROOT.TH1D("crr", "crr", 1200, -1, 1)
hcnn = ROOT.TH1D("cnn", "cnn", 1200, -1, 1)

hcrk = ROOT.TH1D("crk", "crk", 1200, -1, 1)
hckr = ROOT.TH1D("ckr", "ckr", 1200, -1, 1)

hcPrk = ROOT.TH1D("cP_rk", "cP_rk", 1200, -1, 1)
hcMrk = ROOT.TH1D("cM_rk", "cM_rk", 1200, -1, 1)

hchel = ROOT.TH1D("c_hel", "c_hel", 1200, -1, 1)

# Step 8 GEN hists
hgenleppt = ROOT.TH1D('gen_lep_pt', 'gen_lep_pt', 1200, 0, 1200)
hgenlepeta = ROOT.TH1D('gen_lep_eta', 'gen_lep_eta', 1200, -2*np.pi, 2*np.pi)
hgenlepphi = ROOT.TH1D('gen_lep_phi', 'gen_lep_phi', 1200, -2*np.pi, 2*np.pi)

hgenaleppt = ROOT.TH1D('gen_alep_pt', 'gen_alep_pt', 1200, 0, 1200)
hgenalepeta = ROOT.TH1D('gen_alep_eta', 'gen_alep_eta', 1200, -2*np.pi, 2*np.pi)
hgenalepphi = ROOT.TH1D('gen_alep_phi', 'gen_alep_phi', 1200, -2*np.pi, 2*np.pi)

hgenmetpt = ROOT.TH1D('gen_met_pt', 'gen_met_pt', 1200, 0, 1200)
hgenmetphi = ROOT.TH1D('gen_met_phi', 'gen_met_phi', 1200, -2*np.pi, 2*np.pi)

hgenbpt = ROOT.TH1D('gen_b_pt', 'gen_b_pt', 1200, 0, 1200)
hgenbeta = ROOT.TH1D('gen_b_eta', 'gen_b_eta', 1200, -2*np.pi, 2*np.pi)
hgenbphi = ROOT.TH1D('gen_b_phi', 'gen_b_phi', 1200, -2*np.pi, 2*np.pi)

hgenabpt = ROOT.TH1D('gen_ab_pt', 'gen_ab_pt', 1200, 0, 1200)
hgenabeta = ROOT.TH1D('gen_ab_eta', 'gen_ab_eta', 1200, -2*np.pi, 2*np.pi)
hgenabphi = ROOT.TH1D('gen_ab_phi', 'gen_ab_phi', 1200, -2*np.pi, 2*np.pi)

hgenneupt = ROOT.TH1D('gen_neu_pt', 'gen_neu_pt', 1200, 0, 1200)
hgenneueta = ROOT.TH1D('gen_neu_eta', 'gen_neu_eta', 1200, -2*np.pi, 2*np.pi)
hgenneuphi = ROOT.TH1D('gen_neu_phi', 'gen_neu_phi', 1200, -2*np.pi, 2*np.pi)

hgenaneupt = ROOT.TH1D('gen_aneu_pt', 'gen_aneu_pt', 1200, 0, 1200)
hgenaneueta = ROOT.TH1D('gen_aneu_eta', 'gen_aneu_eta', 1200, -2*np.pi, 2*np.pi)
hgenaneuphi = ROOT.TH1D('gen_aneu_phi', 'gen_aneu_phi', 1200, -2*np.pi, 2*np.pi)

hgentpt = ROOT.TH1D('gen_t_pt', 'gen_t_pt', 1200, 0, 1200)
hgenteta = ROOT.TH1D('gen_t_eta', 'gen_t_eta', 1200, -2*np.pi, 2*np.pi)
hgentphi = ROOT.TH1D('gen_t_phi', 'gen_t_phi', 1200, -2*np.pi, 2*np.pi)

hgenatpt = ROOT.TH1D('gen_at_pt', 'gen_at_pt', 1200, 0, 1200)
hgenateta = ROOT.TH1D('gen_at_eta', 'gen_at_eta', 1200, -2*np.pi, 2*np.pi)
hgenatphi = ROOT.TH1D('gen_at_phi', 'gen_at_phi', 1200, -2*np.pi, 2*np.pi)

hgentatmass = ROOT.TH1D('gen_tat_mass', 'gen_tat_mass', 1200, 0, 1200)

hgenckk = ROOT.TH1D("gen_ckk", "gen_ckk", 1200, -1, 1)
hgencrr = ROOT.TH1D("gen_crr", "gen_crr", 1200, -1, 1)
hgencnn = ROOT.TH1D("gen_cnn", "gen_cnn", 1200, -1, 1)

hgencrk = ROOT.TH1D("gen_crk", "gen_crk", 1200, -1, 1)
hgenckr = ROOT.TH1D("gen_ckr", "gen_ckr", 1200, -1, 1)

hgencPrk = ROOT.TH1D("gen_cP_rk", "gen_cP_rk", 1200, -1, 1)
hgencMrk = ROOT.TH1D("gen_cM_rk", "gen_cM_rk", 1200, -1, 1)

hgenchel = ROOT.TH1D("gen_c_hel", "gen_c_hel", 1200, -1, 1)

hrvgleppt = ROOT.TH2D('rvg_lep_pt', 'reco vs gen lep pt', 1200, 0, 1200, 1200, 0, 1200)
hrvglepeta = ROOT.TH2D('rvg_lep_eta', 'reco vs gen lep eta', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)
hrvglepphi = ROOT.TH2D('rvg_lep_phi', 'reco vs gen lep phi', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)

hrvgaleppt = ROOT.TH2D('rvg_alep_pt', 'reco vs gen alep pt', 1200, 0, 1200, 1200, 0, 1200)
hrvgalepeta = ROOT.TH2D('rvg_alep_eta', 'reco vs gen alep eta', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)
hrvgalepphi = ROOT.TH2D('rvg_alep_phi', 'reco vs gen alep phi', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)

hrvgmetpt = ROOT.TH2D('rvg_met_pt', 'reco vs gen met pt', 1200, 0, 1200, 1200, 0, 1200)
hrvgmetphi = ROOT.TH2D('rvg_met_phi', 'reco vs gen met phi', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)

hrvgbpt = ROOT.TH2D('rvg_b_pt', 'reco vs gen b pt', 1200, 0, 1200, 1200, 0, 1200)
hrvgbeta = ROOT.TH2D('rvg_b_eta', 'reco vs gen b eta', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)
hrvgbphi = ROOT.TH2D('rvg_b_phi', 'reco vs gen b phi', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)

hrvgabpt = ROOT.TH2D('rvg_ab_pt', 'reco vs gen ab pt', 1200, 0, 1200, 1200, 0, 1200)
hrvgabeta = ROOT.TH2D('rvg_ab_eta', 'reco vs gen ab eta', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)
hrvgabphi = ROOT.TH2D('rvg_ab_phi', 'reco vs gen ab phi', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)

hrvgneupt = ROOT.TH2D('rvg_neu_pt', 'reco vs gen neu pt', 1200, 0, 1200, 1200, 0, 1200)
hrvgneueta = ROOT.TH2D('rvg_neu_eta', 'reco vs gen neu eta', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)
hrvgneuphi = ROOT.TH2D('rvg_neu_phi', 'reco vs gen neu phi', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)

hrvganeupt = ROOT.TH2D('rvg_aneu_pt', 'reco vs gen aneu pt', 1200, 0, 1200, 1200, 0, 1200)
hrvganeueta = ROOT.TH2D('rvg_aneu_eta', 'reco vs gen aneu eta', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)
hrvganeuphi = ROOT.TH2D('rvg_aneu_phi', 'reco vs gen aneu phi', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)

hrvgtpt = ROOT.TH2D('rvg_t_pt', 'reco vs gen t pt', 1200, 0, 1200, 1200, 0, 1200)
hrvgteta = ROOT.TH2D('rvg_t_eta', 'reco vs gen t eta', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)
hrvgtphi = ROOT.TH2D('rvg_t_phi', 'reco vs gen t phi', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)

hrvgatpt = ROOT.TH2D('rvg_at_pt', 'reco vs gen at pt', 1200, 0, 1200, 1200, 0, 1200)
hrvgateta = ROOT.TH2D('rvg_at_eta', 'reco vs gen at eta', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)
hrvgatphi = ROOT.TH2D('rvg_at_phi', 'reco vs gen at phi', 1200, -2*np.pi, 2*np.pi, 1200, -2*np.pi, 2*np.pi)

htvgtatm = ROOT.TH2D('rvg_tat_m', "reco vs gen tat mass", 1400, 0, 1400, 1400, 0, 1400)

# Step 7 hists

h_KinReco_d_angle_jet_step7 = ROOT.TH1D("KinReco_d_angle_jet_step7", ";#alpha, rad;Entries", 200, 0, 0.5 ) 
h_KinReco_d_angle_lep_step7 = ROOT.TH1D("KinReco_d_angle_lep_step7", ";#alpha, rad;Entries", 200, 0, 0.2 )
h_KinReco_fE_jet_step7 = ROOT.TH1D("KinReco_fE_jet_step7", "Jet Energy Correction Factor;#frac{E^{true}_{jet}}{E^{reco}_{jet}};Entries", 100, 0, 4 )
h_KinReco_fE_lep_step7 = ROOT.TH1D("KinReco_fE_lep_step7", "Lepton Energy Correction Factor;#frac{E^{true}_{lep}}{E^{reco}_{lep}};Entries", 200, 0.5, 2.5 )  
h_KinReco_mbl_true_step7  = ROOT.TH1D("KinReco_mbl_true_step7","mbl_true", 100, 0, 180 )



## STEP 8

ptr = uproot.open(inputFile)
fileptr = ptr['Step8']

t_pt     = fileptr['top_pt'].array()
t_phi    = fileptr['top_phi'].array()
t_eta    = fileptr['top_eta'].array()
t_rap    = fileptr['top_rapidity'].array()

tbar_pt  = fileptr['atop_pt'].array()
tbar_phi = fileptr['atop_phi'].array()
tbar_eta = fileptr['atop_eta'].array()
tbar_rap = fileptr['atop_rapidity'].array()

tt_mass  = fileptr['tt_mass'].array()

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

gen_l_pt     = fileptr['gen_lep_pt'].array()
gen_l_phi    = fileptr['gen_lep_phi'].array()
gen_l_eta    = fileptr['gen_lep_eta'].array()
gen_l_mass   = fileptr['gen_lep_mass'].array()

gen_lbar_pt   = fileptr['gen_alep_pt'].array()
gen_lbar_phi  = fileptr['gen_alep_phi'].array()
gen_lbar_eta  = fileptr['gen_alep_eta'].array()
gen_lbar_mass = fileptr['gen_alep_mass'].array()


for i in range(len(t_pt)):

    if (i % 1000 == 0):
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
    ll_dEta = ifOk(b4_aLep.Eta() - b4_pLep.Eta())
    ll_dPhi = ifOk(b4_aLep.DeltaPhi(b4_pLep))
    ll_dR = ifOk(b4_aLep.DeltaR(b4_pLep))
    cHel = ifOk(b4_aLep.Vect().Unit().Dot(b4_pLep.Vect().Unit()))

    gen_ll_dEta = ifOk(gen_b4_aLep.Eta() - gen_b4_pLep.Eta())
    gen_ll_dPhi = ifOk(gen_b4_aLep.DeltaPhi(gen_b4_pLep))
    gen_ll_dR = ifOk(gen_b4_aLep.DeltaR(gen_b4_pLep))
    gen_cHel = ifOk(gen_b4_aLep.Vect().Unit().Dot(gen_b4_pLep.Vect().Unit()))



    # Fill RECO

    hleppt.Fill(fileptr['lep_pt'].array()[i])
    hlepeta.Fill(fileptr['lep_eta'].array()[i])
    hlepphi.Fill(fileptr['lep_phi'].array()[i])

    haleppt.Fill(fileptr['alep_pt'].array()[i])
    halepeta.Fill(fileptr['alep_eta'].array()[i])
    halepphi.Fill(fileptr['alep_phi'].array()[i])

    #hmetpt.Fill(fileptr['MET'].array()[i])
    #hmetphi.Fill(fileptr['MET_phi'].array()[i])

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

    hatpt.Fill(fileptr['atop_pt'].array()[i])
    hateta.Fill(fileptr['atop_eta'].array()[i])
    hatphi.Fill(fileptr['atop_phi'].array()[i])

    htatmass.Fill(fileptr['tt_mass'].array()[i])

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

    hgenatpt.Fill(fileptr['gen_atop_pt'].array()[i])
    hgenateta.Fill(fileptr['gen_atop_eta'].array()[i])
    hgenatphi.Fill(fileptr['gen_atop_phi'].array()[i])

    hgentatmass.Fill(fileptr['gen_tt_mass'].array()[i])

    hgenckk.Fill(gen_ckk)
    hgencrr.Fill(gen_crr)
    hgencnn.Fill(gen_cnn)

    hgencrk.Fill(gen_crk)
    hgenckr.Fill(gen_ckr)

    hgencPrk.Fill(gen_cP_rk)
    hgencMrk.Fill(gen_cM_rk)

    hgenchel.Fill(gen_cHel)

    # Fill RECO vs GEN

    hrvgleppt.Fill(fileptr['lep_pt'].array()[i], fileptr['gen_lep_pt'].array()[i])
    hrvglepeta.Fill(fileptr['lep_eta'].array()[i], fileptr['gen_lep_eta'].array()[i])
    hrvglepphi.Fill(fileptr['lep_phi'].array()[i], fileptr['gen_lep_phi'].array()[i])

    hrvgaleppt.Fill(fileptr['alep_pt'].array()[i], fileptr['gen_alep_pt'].array()[i])
    hrvgalepeta.Fill(fileptr['alep_eta'].array()[i], fileptr['gen_alep_eta'].array()[i])
    hrvgalepphi.Fill(fileptr['alep_phi'].array()[i], fileptr['gen_alep_phi'].array()[i])

    hrvgmetpt.Fill(ptr['Step7']['MET'].array()[i], fileptr['gen_met_pt'].array()[i])
    hrvgmetphi.Fill(ptr['Step7']['MET_phi'].array()[i], fileptr['gen_met_phi'].array()[i])

    hrvgbpt.Fill(fileptr['b_pt'].array()[i], fileptr['gen_b_pt'].array()[i])
    hrvgbeta.Fill(fileptr['b_eta'].array()[i], fileptr['gen_b_eta'].array()[i])
    hrvgbphi.Fill(fileptr['b_phi'].array()[i], fileptr['gen_b_phi'].array()[i])

    hrvgabpt.Fill(fileptr['ab_pt'].array()[i], fileptr['gen_ab_pt'].array()[i])
    hrvgabeta.Fill(fileptr['ab_eta'].array()[i], fileptr['gen_ab_eta'].array()[i])
    hrvgabphi.Fill(fileptr['ab_phi'].array()[i], fileptr['gen_ab_phi'].array()[i])

    hrvgtpt.Fill(t_pt[i], fileptr['gen_top_pt'].array()[i])
    hrvgteta.Fill(t_eta[i], fileptr['gen_top_eta'].array()[i])
    hrvgtphi.Fill(fileptr['top_phi'].array()[i], fileptr['gen_top_phi'].array()[i])

    hrvgatpt.Fill(tbar_pt[i], fileptr['gen_atop_pt'].array()[i])
    hrvgateta.Fill(tbar_eta[i], fileptr['gen_atop_eta'].array()[i])
    hrvgatphi.Fill(fileptr['atop_phi'].array()[i], fileptr['gen_atop_phi'].array()[i])

    htvgtatm.Fill(tt_mass[i], fileptr['gen_tt_mass'].array()[i])


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
    
    
    # Filling MET with Step7 because forgot to propagate to step 8
    
    hmetpt.Fill(fileptr['MET'].array()[i])
    hmetphi.Fill(fileptr['MET_phi'].array()[i])




opfile.Write()
opfile.Close()
