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
parser.add_argument('-i', '--input', help='Input delphes minitrees folder location')
parser.add_argument('-o', '--output', help='Output file location')

args = parser.parse_args()
inputFolder = args.input
outputFile = args.output

## STEP 8

fileptr = uproot.concatenate([inputFolder+'minitree_*.root:Step8'])
opfile = ROOT.TFile(outputFile, 'recreate')

t_pt     = fileptr['top_pt']
t_phi    = fileptr['top_phi']
t_eta    = fileptr['top_eta']
t_rap    = fileptr['top_rapidity']

tbar_pt  = fileptr['atop_pt']
tbar_phi = fileptr['atop_phi']
tbar_eta = fileptr['atop_eta']
tbar_rap = fileptr['atop_rapidity']

tt_mass  = fileptr['tt_mass']

l_pt     = fileptr['lep_pt']
l_phi    = fileptr['lep_phi']
l_eta    = fileptr['lep_eta']
l_mass   = fileptr['lep_mass']

lbar_pt   = fileptr['alep_pt']
lbar_phi  = fileptr['alep_phi']
lbar_eta  = fileptr['alep_eta']
lbar_mass = fileptr['alep_mass']

# The Bi's
h_b1k = []
h_b2k = []
h_b1j = []
h_b2j = []
h_b1r = []
h_b2r = []
h_b1q = []
h_b2q = []
h_b1n = []
h_b2n = []

h_bP_kk = []
h_bM_kk = []
h_bP_jj = []
h_bM_jj = []
h_bP_rr = []
h_bM_rr = []
h_bP_qq = []
h_bM_qq = []
h_bP_nn = []
h_bM_nn = []

# The Ci's
h_ckk = []
h_crr = []
h_cnn = []
h_crk = []
h_ckr = []
h_cnr = []
h_crn = []
h_cnk = []
h_ckn = []

h_cP_rk = []
h_cM_rk = []
h_cP_nr = []
h_cM_nr = []
h_cP_nk = []
h_cM_nk = []

# ll variables
h_ll_dphi = []
h_ll_deta = []
h_ll_dR   = []
h_c_hel   = []

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

    top.SetPtEtaPhiM(t_pt[i], t_rap[i], t_phi[i], 172.5)
    atop.SetPtEtaPhiM(tbar_pt[i], tbar_rap[i], tbar_phi[i], 172.5)  # Changed from eta to rap

    lep.SetPtEtaPhiM(l_pt[i], l_eta[i], l_phi[i], l_mass[i])
    alep.SetPtEtaPhiM(lbar_pt[i], lbar_eta[i], lbar_phi[i], lbar_mass[i])

    # The various Bernreuther bases
    kBase = ROOT.TVector3()
    jBase = ROOT.TVector3()
    qBase = ROOT.TVector3()
    # rBase = ROOT.TVector3()
    # nBase = ROOT.TVector3()

    # Beam unit vector
    p3_pPro = ROOT.TVector3(0., 0., 1.)

    # The bases definition: Bernreuther spinMatrix 1508.05271
    p4_TT = top + atop
    b4_TT = ROOT.TVector3(-1. * p4_TT.BoostVector())

    b4_pTop = top
    b4_pTop.Boost(b4_TT)

    b4_aTop = atop
    b4_aTop.Boost(b4_TT)

    # Maybe need to be careful with the signs here ?? Check how the pairings are implemented in the FW
    b4_aLep = alep
    b4_aLep.Boost(b4_TT)
    b4_aLep.Boost(-1. * b4_pTop.BoostVector())

    b4_pLep = lep
    b4_pLep.Boost(b4_TT)
    b4_pLep.Boost(-1. * b4_aTop.BoostVector())

    # Calculating the top-beam angle for pTop only
    c_pTP = b4_pTop.Vect().Unit().Dot(p3_pPro)
    s_pTP = np.sqrt(1. - (c_pTP * c_pTP))

    # The signs needed to account for Bose symmetry
    sY = 1. if (c_pTP >= 0.) else -1.
    sD = 1. if (abs(top.Rapidity()) >= abs(atop.Rapidity())) else -1.

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

    # Find also the opening angles of the lepton
    ll_dEta = ifOk(b4_aLep.Eta() - b4_pLep.Eta())
    ll_dPhi = ifOk(b4_aLep.DeltaPhi(b4_pLep))
    ll_dR = ifOk(b4_aLep.DeltaR(b4_pLep))
    cHel = ifOk(b4_aLep.Vect().Unit().Dot(b4_pLep.Vect().Unit()))

    # Fill the empty lists
    h_b1k.append(b1k)
    h_b2k.append(b2k)
    h_b1j.append(b1j)
    h_b2j.append(b2j)
    h_b1r.append(b1r)
    h_b2r.append(b2r)
    h_b1q.append(b1q)
    h_b2q.append(b2q)
    h_b1n.append(b1n)
    h_b2n.append(b2n)

    h_bP_kk.append(bP_kk)
    h_bM_kk.append(bM_kk)
    h_bP_jj.append(bP_jj)
    h_bM_jj.append(bM_jj)
    h_bP_rr.append(bP_rr)
    h_bM_rr.append(bM_rr)
    h_bP_qq.append(bP_qq)
    h_bM_qq.append(bM_qq)
    h_bP_nn.append(bP_nn)
    h_bM_nn.append(bM_nn)

    h_ckk.append(ckk)
    h_crr.append(crr)
    h_cnn.append(cnn)
    h_crk.append(crk)
    h_ckr.append(ckr)
    h_cnr.append(cnr)
    h_crn.append(crn)
    h_cnk.append(cnk)
    h_ckn.append(ckn)

    h_cP_rk.append(cP_rk)
    h_cM_rk.append(cM_rk)
    h_cP_nr.append(cP_nr)
    h_cM_nr.append(cM_nr)
    h_cP_nk.append(cP_nk)
    h_cM_nk.append(cM_nk)

    h_ll_dphi.append(ll_dPhi)
    h_ll_deta.append(ll_dEta)
    h_ll_dR.append(ll_dR)
    h_c_hel.append(cHel)


htptgtpt = ROOT.TH2D('t_pt_v_gen_t_pt', 'pt vs gen pt', 1200,0,1200, 1200,0,1200 )
htetagteta = ROOT.TH2D('t_eta_v_gen_t_eta', 'eta vs gen eta', 1200,-2*np.pi,2*np.pi, 1200,-2*np.pi,2*np.pi)
htbarptgtbarpt = ROOT.TH2D('tbar_pt_v_gen_tbar_pt', 'pt vs gen pt', 1200,0,1200, 1200,0,1200 )
htbaretagtbareta = ROOT.TH2D('tbar_eta_v_gen_tbar_eta', 'eta vs gen eta', 1200,-2*np.pi,2*np.pi, 1200,-2*np.pi,2*np.pi)
httmgttm = ROOT.TH2D('ttbarmass_v_gen_ttbarmass', "mass vs gen mass", 1400, 0, 1400, 1400, 0, 1400)

hckk = ROOT.TH1D("ckk", "ckk", 1200, -1, 1)
hcrr = ROOT.TH1D("crr", "crr", 1200, -1, 1)
hcnn = ROOT.TH1D("cnn", "cnn", 1200, -1, 1)

hcrk = ROOT.TH1D("crk", "crk", 1200, -1, 1)
hckr = ROOT.TH1D("ckr", "ckr", 1200, -1, 1)

hcPrk = ROOT.TH1D("cP_rk", "cP_rk", 1200, -1, 1)
hcMrk = ROOT.TH1D("cM_rk", "cM_rk", 1200, -1, 1)

hchel = ROOT.TH1D("c_hel", "c_hel", 1200, -1, 1)

for i in range(len(t_pt)):
    htptgtpt.Fill(t_pt[i], fileptr['gen_top_pt'][i])
    htetagteta.Fill(t_eta[i], fileptr['gen_top_eta'][i])
    htbarptgtbarpt.Fill(tbar_pt[i], fileptr['gen_atop_pt'][i])
    htbaretagtbareta.Fill(tbar_eta[i], fileptr['gen_atop_eta'][i])
    httmgttm.Fill(tt_mass[i], fileptr['gen_tt_mass'][i])

    hckk.Fill(h_ckk[i])
    hcrr.Fill(h_crr[i])
    hcnn.Fill(h_cnn[i])

    hcrk.Fill(h_crk[i])
    hckr.Fill(h_ckr[i])

    hcPrk.Fill(h_cP_rk[i])
    hcMrk.Fill(h_cM_rk[i])
    
    hchel.Fill(h_c_hel[i])

## STEP 7

fileptr = uproot.concatenate([inputFolder+'minitree_*.root:Step7'])


h_KinReco_d_angle_jet_step7 = ROOT.TH1D("KinReco_d_angle_jet_step7", ";#alpha, rad;Entries", 200, 0, 0.5 ) 
h_KinReco_d_angle_lep_step7 = ROOT.TH1D("KinReco_d_angle_lep_step7", ";#alpha, rad;Entries", 200, 0, 0.2 )
h_KinReco_fE_jet_step7 = ROOT.TH1D("KinReco_fE_jet_step7", "Jet Energy Correction Factor;#frac{E^{true}_{jet}}{E^{reco}_{jet}};Entries", 100, 0, 4 )
h_KinReco_fE_lep_step7 = ROOT.TH1D("KinReco_fE_lep_step7", "Lepton Energy Correction Factor;#frac{E^{true}_{lep}}{E^{reco}_{lep}};Entries", 200, 0.5, 2.5 )  
h_KinReco_mbl_true_step7  = ROOT.TH1D("KinReco_mbl_true_step7","mbl_true", 100, 0, 180 )

gen_lep_pt = fileptr['gen_lep_pt']
gen_lep_eta = fileptr['gen_lep_eta']
gen_lep_phi = fileptr['gen_lep_phi']
gen_lep_mass = fileptr['gen_lep_mass']

gen_alep_pt = fileptr['gen_alep_pt']
gen_alep_eta = fileptr['gen_alep_eta']
gen_alep_phi = fileptr['gen_alep_phi']
gen_alep_mass = fileptr['gen_alep_mass']

gen_b_pt = fileptr['gen_b_pt']
gen_b_eta = fileptr['gen_b_eta']
gen_b_phi = fileptr['gen_b_phi']
gen_b_mass = fileptr['gen_b_mass']

gen_ab_pt = fileptr['gen_ab_pt']
gen_ab_eta = fileptr['gen_ab_eta']
gen_ab_phi = fileptr['gen_ab_phi']
gen_ab_mass = fileptr['gen_ab_mass']
lep_pt = fileptr['lep_pt']
lep_eta = fileptr['lep_eta']
lep_phi = fileptr['lep_phi']
lep_mass = fileptr['lep_mass']

alep_pt = fileptr['alep_pt']
alep_eta = fileptr['alep_eta']
alep_phi = fileptr['alep_phi']
alep_mass = fileptr['alep_mass']

ljet_pt = fileptr['ljet_pt']
ljet_eta = fileptr['ljet_eta']
ljet_phi = fileptr['ljet_phi']
ljet_mass = fileptr['ljet_mass']

sljet_pt = fileptr['sljet_pt']
sljet_eta = fileptr['sljet_eta']
sljet_phi = fileptr['sljet_phi']
sljet_mass = fileptr['sljet_mass']


for i in range(len(fileptr['lep_pt'])):

    gen_lep_4vec  = ROOT.TLorentzVector()
    gen_alep_4vec = ROOT.TLorentzVector()

    gen_lep_4vec.SetPtEtaPhiM(gen_lep_pt[i] , gen_lep_eta[i] , gen_lep_phi[i] , gen_lep_mass[i])
    gen_alep_4vec.SetPtEtaPhiM(gen_alep_pt[i] , gen_alep_eta[i] , gen_alep_phi[i] , gen_alep_mass[i])

    gen_b_4vec  = ROOT.TLorentzVector()
    gen_ab_4vec = ROOT.TLorentzVector()

    gen_b_4vec.SetPtEtaPhiM(gen_b_pt[i] , gen_b_eta[i] , gen_b_phi[i] , gen_b_mass[i])
    gen_ab_4vec.SetPtEtaPhiM(gen_ab_pt[i] , gen_ab_eta[i] , gen_ab_phi[i] , gen_ab_mass[i])

    lep_4vec  = ROOT.TLorentzVector()
    alep_4vec = ROOT.TLorentzVector()

    lep_4vec.SetPtEtaPhiM(lep_pt[i] , lep_eta[i] , lep_phi[i] , lep_mass[i])
    alep_4vec.SetPtEtaPhiM(alep_pt[i] , alep_eta[i] , alep_phi[i] , alep_mass[i])

    ljet_4vec  = ROOT.TLorentzVector()
    sljet_4vec = ROOT.TLorentzVector()

    ljet_4vec.SetPtEtaPhiM(ljet_pt[i] , ljet_eta[i] , ljet_phi[i] , ljet_mass[i])
    sljet_4vec.SetPtEtaPhiM(sljet_pt[i] , sljet_eta[i] , sljet_phi[i] , sljet_mass[i])

    
    h_KinReco_fE_jet_step7.Fill(gen_b_4vec.E()/ljet_4vec.E())
    h_KinReco_fE_jet_step7.Fill(gen_ab_4vec.E()/ljet_4vec.E())
    h_KinReco_fE_jet_step7.Fill(gen_b_4vec.E()/sljet_4vec.E())
    h_KinReco_fE_jet_step7.Fill(gen_ab_4vec.E()/sljet_4vec.E())

    h_KinReco_fE_lep_step7.Fill(gen_lep_4vec.E()/lep_4vec.E())
    h_KinReco_fE_lep_step7.Fill(gen_alep_4vec.E()/alep_4vec.E())


    h_KinReco_d_angle_jet_step7.Fill(gen_b_4vec.Angle(sljet_4vec.Vect()))
    h_KinReco_d_angle_jet_step7.Fill(gen_b_4vec.Angle(ljet_4vec.Vect()))
    h_KinReco_d_angle_jet_step7.Fill(gen_ab_4vec.Angle(sljet_4vec.Vect()))
    h_KinReco_d_angle_jet_step7.Fill(gen_ab_4vec.Angle(ljet_4vec.Vect()))

    h_KinReco_d_angle_lep_step7.Fill(gen_lep_4vec.Angle(lep_4vec.Vect()))
    h_KinReco_d_angle_lep_step7.Fill(gen_alep_4vec.Angle(alep_4vec.Vect()))

    h_KinReco_mbl_true_step7.Fill((gen_alep_4vec + gen_b_4vec).M())
    h_KinReco_mbl_true_step7.Fill((gen_lep_4vec + gen_ab_4vec).M())
    


opfile.Write()
opfile.Close()
