import sys
import math
import ROOT
import uproot
import operator
import argparse
import numpy as np
from array import array
from datetime import datetime
from Top_reco_helpers import try_smear

#Get theta effective mixing for a given top polarization hypothesis
#The result also depends on the stop, top and chi0 mass hypotheses
#Also valid for an off-shell scenario

def GetThetaMixingangle(topPol, m_stop, m_top, m_chi0) :
      p_chi0 = np.sqrt( pow(m_top*m_top + m_chi0*m_chi0 - m_stop*m_stop,2)/4 - pow(m_top*m_chi0,2) ) / m_stop
      e_chi0 = np.sqrt( p_chi0*p_chi0 + m_chi0*m_chi0 )
      sqrPol = 0
        
      if (abs(topPol) < 1) :
         sqrPol      =  np.sqrt(1 - topPol*topPol)

      tanThetaEff = ( p_chi0*sqrPol - m_chi0*topPol) / (topPol*e_chi0 + p_chi0)
      return np.arctan(tanThetaEff)

def GetWeight(thetaMixingTarget, top_arr, lep_arr, chi0_arr, m_top, m_chi0) :

    weight      = 1
    TOPMASS_REF = 175

    for i in range(2) :
        cX        = np.cos(thetaMixingTarget)
        sX        = np.sin(thetaMixingTarget)
        
        coeffTop  = 2*sX*sX*(chi0_arr[i] * top_arr[i]) + 2*sX*cX *(m_chi0 * TOPMASS_REF)
        coeffChi  = pow(cX*TOPMASS_REF, 2) - pow(sX*m_top, 2)
        
        coeffNorm = (chi0_arr[i] * top_arr[i]) * (sX*sX + cX*cX*pow(TOPMASS_REF/m_top, 2)) + 2*sX*cX*( m_chi0*TOPMASS_REF )
        weight   *= (coeffTop* (lep_arr[i] * top_arr[i]) + coeffChi*(lep_arr[i] * chi0_arr[i])) / (coeffNorm*(lep_arr[i] * top_arr[i]))

    return weight

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Input  Delphes Ntuple location')
parser.add_argument('-o', '--output', help='Output Delphes Minitree location')

args       = parser.parse_args()
inputFile  = args.input
outputFile = args.output

fileptr = uproot.open(inputFile)['Step8']

# Gen part info
pt     = fileptr['genpart_pt'].array()
eta    = fileptr['genpart_eta'].array()
phi    = fileptr['genpart_phi'].array()
pid    = fileptr['genpart_pid'].array()
mass   = fileptr['genpart_mass'].array()
status = fileptr['genpart_status'].array()

# Reco level info
MET      = fileptr['MET'].array()
MET_phi  = fileptr['MET_phi'].array()

e_pt     = fileptr['e_pt'].array()
e_eta    = fileptr['e_eta'].array()
e_phi    = fileptr['e_phi'].array()
e_charge = fileptr['e_charge'].array()

mu_pt     = fileptr['mu_pt'].array()
mu_eta    = fileptr['mu_eta'].array()
mu_phi    = fileptr['mu_phi'].array()
mu_charge = fileptr['mu_charge'].array()

jet_btag  = fileptr['jet_btag'].array()
jet_pt    = fileptr['jet_pt'].array()
jet_eta   = fileptr['jet_eta'].array()
jet_phi   = fileptr['jet_phi'].array()
jet_mass  = fileptr['jet_mass'].array()

weight    = fileptr['weight'].array()

# Storing the reconstructed as arrays

lep_pt   = []
lep_eta  = []
lep_phi  = []
lep_mass = []

alep_pt   = []
alep_eta  = []
alep_phi  = []
alep_mass = []

b_pt   = []
b_eta  = []
b_phi  = []
b_mass = []

bbar_pt   = []
bbar_eta  = []
bbar_phi  = []
bbar_mass = []

nu_pt  = []
nu_eta = []
nu_phi = []

anu_pt  = []
anu_eta = []
anu_phi = []

top_pt  = []
top_eta = []
top_phi = []
top_rap = []

atop_pt  = []
atop_eta = []
atop_phi = []
atop_rap = []

tt_mass  = []

# Gen as arrays

gen_tt_mass = []
gen_top_pt  = []
gen_top_eta = []
gen_top_phi = []
gen_top_rap = []

gen_atop_pt  = []
gen_atop_eta = []
gen_atop_phi = []
gen_atop_rap = []

# Let's create a mask
selection = np.zeros(len(jet_pt))

for i in range(len(jet_pt)):

    if (i % 500 == 0):
        print('Processing event :: ' + str(i))
        now = datetime.now()   # Time keeping
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

    lep  = ROOT.TLorentzVector()
    alep = ROOT.TLorentzVector()

    # lep charge -1 and alep charge +1
    if  (e_charge[i] == -1. and mu_charge[i] == 1.):
        lep.SetPtEtaPhiM(e_pt[i], e_eta[i], e_phi[i], 0.0)
        alep.SetPtEtaPhiM(mu_pt[i], mu_eta[i], mu_phi[i], 0.105)

    elif (e_charge[i] == 1. and mu_charge[i] == -1.):
        lep.SetPtEtaPhiM(mu_pt[i], mu_eta[i], mu_phi[i], 0.105)
        alep.SetPtEtaPhiM(e_pt[i], e_eta[i], e_phi[i], 0.0)

    met_x = MET[i] * np.cos(MET_phi[i])
    met_y = MET[i] * np.sin(MET_phi[i])

    # Only consider 2 btagged jets is found, high_w is used for single b-tag case
    n_btag = 0
    high_w = 0
    m_tt_final = 0

    # Loop over jet permutations and find those with 2-btags or highest sum of weights

    for j in range(len(jet_pt[i])):     # First jet
        for k in range(len(jet_pt[i])):  # Second jet

            if (j >= k):
                continue
            if (jet_pt[i][j] < 30 or jet_pt[i][k] < 30):
                continue
            if (abs(jet_eta[i][j]) > 2.4 or abs(jet_eta[i][k]) > 2.4):
                continue
            if (jet_btag[i][j] == 0 and jet_btag[i][k] == 0):
                continue

            jet1 = ROOT.TLorentzVector()
            jet2 = ROOT.TLorentzVector()
            jet1.SetPtEtaPhiM(jet_pt[i][j], jet_eta[i][j], jet_phi[i][j], jet_mass[i][j])
            jet2.SetPtEtaPhiM(jet_pt[i][k], jet_eta[i][k], jet_phi[i][k], jet_mass[i][k])

            if (lep.DeltaR(jet1) < 0.4 or lep.DeltaR(jet2) < 0.4 or alep.DeltaR(jet1) < 0.4 or alep.DeltaR(jet2) < 0.4):
                continue

            # 2-Btag scenario
            if (jet_btag[i][j] != 0 and jet_btag[i][k] != 0):

                m_tt_1, top_p4_1, atop_p4_1, nu_p4_1, nubar_p4_1, sw_1 = try_smear(jet1, jet2, alep, lep, met_x, met_y, i)
                m_tt_2, top_p4_2, atop_p4_2, nu_p4_2, nubar_p4_2, sw_2 = try_smear(jet2, jet1, alep, lep, met_x, met_y, i)

                if (m_tt_1 == -999 and m_tt_2 == -999):
                    continue

                n_btag = 2

                if (m_tt_2 == -999):
                    m_tt_final     = m_tt_1
                    top_p4_final   = top_p4_1
                    atop_p4_final  = atop_p4_1
                    nu_p4_final    = nu_p4_1
                    nubar_p4_final = nubar_p4_1
                    b_p4_final     = jet1
                    bbar_p4_final  = jet2  

                if (m_tt_1 == -999):
                    m_tt_final     = m_tt_2
                    top_p4_final   = top_p4_2
                    atop_p4_final  = atop_p4_2
                    nu_p4_final    = nu_p4_2
                    nubar_p4_final = nubar_p4_2
                    b_p4_final     = jet2
                    bbar_p4_final  = jet1  

                if((m_tt_1 != -999 and m_tt_2 != -999) and sw_2 <= sw_1):
                    m_tt_final     = m_tt_1
                    top_p4_final   = top_p4_1
                    atop_p4_final  = atop_p4_1
                    nu_p4_final    = nu_p4_1
                    nubar_p4_final = nubar_p4_1
                    b_p4_final     = jet1
                    bbar_p4_final  = jet2  

                if((m_tt_1 != -999 and m_tt_2 != -999) and sw_1 <= sw_2):
                    m_tt_final     = m_tt_2
                    top_p4_final   = top_p4_2
                    atop_p4_final  = atop_p4_2
                    nu_p4_final    = nu_p4_2
                    nubar_p4_final = nubar_p4_2
                    b_p4_final     = jet2
                    bbar_p4_final  = jet1  

            if (n_btag == 2):
                continue

            # 1-Btag scenario
            if ((jet_btag[i][j] != 0 and jet_btag[i][k] == 0) or (jet_btag[i][j] == 0 and jet_btag[i][k] != 0)):
                m_tt_1, top_p4_1, atop_p4_1, nu_p4_1, nubar_p4_1, sw_1 = try_smear(jet1, jet2, alep, lep, met_x, met_y, i)
                m_tt_2, top_p4_2, atop_p4_2, nu_p4_2, nubar_p4_2, sw_2 = try_smear(jet2, jet1, alep, lep, met_x, met_y, i)

                if (m_tt_1 == -999 and m_tt_2 == -999):
                    continue

                if (m_tt_2 == -999 and high_w <= sw_1):
                    m_tt_final     = m_tt_1
                    top_p4_final   = top_p4_1
                    atop_p4_final  = atop_p4_1
                    nu_p4_final    = nu_p4_1
                    nubar_p4_final = nubar_p4_1
                    high_w         = sw_1
                    b_p4_final     = jet1
                    bbar_p4_final  = jet2  

                if (m_tt_1 == -999 and high_w <= sw_2):
                    m_tt_final     = m_tt_2
                    top_p4_final   = top_p4_2
                    atop_p4_final  = atop_p4_2
                    nu_p4_final    = nu_p4_2
                    nubar_p4_final = nubar_p4_2
                    high_w         = sw_2
                    b_p4_final     = jet2
                    bbar_p4_final  = jet1

                if((m_tt_1 != -999 and m_tt_2 != -999) and sw_2 <= sw_1 and high_w <= sw_1):
                    m_tt_final     = m_tt_1
                    top_p4_final   = top_p4_1
                    atop_p4_final  = atop_p4_1
                    nu_p4_final    = nu_p4_1
                    nubar_p4_final = nubar_p4_1
                    high_w         = sw_1
                    b_p4_final     = jet1
                    bbar_p4_final  = jet2  

                if((m_tt_1 != -999 and m_tt_2 != -999) and sw_1 <= sw_2 and high_w <= sw_2):
                    m_tt_final     = m_tt_2
                    top_p4_final   = top_p4_2
                    atop_p4_final  = atop_p4_2
                    nu_p4_final    = nu_p4_2
                    nubar_p4_final = nubar_p4_2
                    high_w         = sw_2
                    b_p4_final     = jet2
                    bbar_p4_final  = jet1 

                else:
                    continue

    if m_tt_final == 0:
        continue

    for j in range(len(pt[i])):
        # Gen level tops for Ecom
        if (pid[i][j] == 6) and (status[i][j] == 62):
            gen_top = ROOT.TLorentzVector()
            gen_top.SetPtEtaPhiM(pt[i][j], eta[i][j], phi[i][j], mass[i][j])

        if (pid[i][j] == -6) and (status[i][j] == 62):
            gen_atop = ROOT.TLorentzVector()
            gen_atop.SetPtEtaPhiM(pt[i][j], eta[i][j], phi[i][j], mass[i][j])

        else:
            continue

    # COM 4-vec
    com = gen_top + gen_atop  # Adding the 4 vectors

    tt_mass.append(m_tt_final)
    top_pt.append(top_p4_final.Pt())
    top_eta.append(top_p4_final.Eta())
    top_phi.append(top_p4_final.Phi())
    top_rap.append(top_p4_final.Rapidity())

    atop_pt.append(atop_p4_final.Pt())
    atop_eta.append(atop_p4_final.Eta())
    atop_phi.append(atop_p4_final.Phi())
    atop_rap.append(atop_p4_final.Rapidity())

    nu_pt.append(nu_p4_final.Pt())
    nu_eta.append(nu_p4_final.Eta())
    nu_phi.append(nu_p4_final.Phi())

    anu_pt.append(nubar_p4_final.Pt())
    anu_eta.append(nubar_p4_final.Eta())
    anu_phi.append(nubar_p4_final.Phi())

    lep_pt.append(lep.Pt())
    lep_eta.append(lep.Eta())
    lep_phi.append(lep.Phi())
    lep_mass.append(lep.M())

    alep_pt.append(alep.Pt())
    alep_eta.append(alep.Eta())
    alep_phi.append(alep.Phi())
    alep_mass.append(alep.M())

    b_pt.append(b_p4_final.Pt())
    b_eta.append(b_p4_final.Eta())
    b_phi.append(b_p4_final.Phi())
    b_mass.append(b_p4_final.M())

    bbar_pt.append(bbar_p4_final.Pt())
    bbar_eta.append(bbar_p4_final.Eta())
    bbar_phi.append(bbar_p4_final.Phi())
    bbar_mass.append(bbar_p4_final.M())

    gen_tt_mass.append(com.M())
    gen_top_pt.append(gen_top.Pt())
    gen_top_eta.append(gen_top.Eta())
    gen_top_phi.append(gen_top.Phi())
    gen_top_rap.append(gen_top.Rapidity())

    gen_atop_pt.append(gen_atop.Pt())
    gen_atop_eta.append(gen_atop.Eta())
    gen_atop_phi.append(gen_atop.Phi())
    gen_atop_rap.append(gen_atop.Rapidity())

    # Create a mask for selection
    selection[i] = 1

weight_sel = weight[selection == 1]

# Empty arrays that get mapped to histograms in a root file
# Selected leptons and jets
l_pt_arr = array('f', [0.])
l_eta_arr = array('f', [0.])
l_phi_arr = array('f', [0.])
l_mass_arr = array('f', [0.])

lbar_pt_arr   = array('f', [0.])
lbar_eta_arr  = array('f', [0.])
lbar_phi_arr  = array('f', [0.])
lbar_mass_arr = array('f', [0.])

b_pt_arr = array('f', [0.])
b_eta_arr = array('f', [0.])
b_phi_arr = array('f', [0.])
b_mass_arr = array('f', [0.])

bbar_pt_arr   = array('f', [0.])
bbar_eta_arr  = array('f', [0.])
bbar_phi_arr  = array('f', [0.])
bbar_mass_arr = array('f', [0.])

# Reconstructed tops and nus
nu_pt_arr  = array('f', [0.])
nu_eta_arr = array('f', [0.])
nu_phi_arr = array('f', [0.])

nubar_pt_arr  = array('f', [0.])
nubar_eta_arr = array('f', [0.])
nubar_phi_arr = array('f', [0.])

t_pt_arr = array('f', [0.])
t_eta_arr = array('f', [0.])
t_phi_arr = array('f', [0.])
t_rap_arr = array('f', [0.])

tbar_pt_arr = array('f', [0.])
tbar_eta_arr = array('f', [0.])
tbar_phi_arr = array('f', [0.])
tbar_rap_arr = array('f', [0.])

m_ttbar_arr   = array('f', [0.])

# Weights 
maxn    = 9999
weight_size_arr = array('i', [0])
weight_arr      = array('f', maxn*[0.])

# Gen entries
gen_t_pt_arr = array('f', [0.])
gen_t_eta_arr = array('f', [0.])
gen_t_phi_arr = array('f', [0.])
gen_t_rap_arr = array('f', [0.])

gen_tbar_pt_arr = array('f', [0.])
gen_tbar_eta_arr = array('f', [0.])
gen_tbar_phi_arr = array('f', [0.])
gen_tbar_rap_arr = array('f', [0.])

gen_m_ttbar_arr = array('f', [0.])

opfile = ROOT.TFile(outputFile, 'recreate')
tree   = ROOT.TTree("Step8", "Step8")

# Leptons and jets
tree.Branch("l_pt", l_pt_arr, 'l_pt/F')
tree.Branch("l_eta", l_eta_arr, 'l_eta/F')
tree.Branch("l_phi", l_phi_arr, 'l_phi/F')
tree.Branch("l_mass", l_mass_arr, 'l_mass/F')

tree.Branch("lbar_pt", lbar_pt_arr, 'lbar_pt/F')
tree.Branch("lbar_eta", lbar_eta_arr, 'lbar_eta/F')
tree.Branch("lbar_phi", lbar_phi_arr, 'lbar_phi/F')
tree.Branch("lbar_mass", lbar_mass_arr, 'lbar_mass/F')

tree.Branch("b_pt", b_pt_arr, 'b_pt/F')
tree.Branch("b_eta", b_eta_arr, 'b_eta/F')
tree.Branch("b_phi", b_phi_arr, 'b_phi/F')
tree.Branch("b_mass", b_mass_arr, 'b_mass/F')

tree.Branch("bbar_pt", bbar_pt_arr, 'bbar_pt/F')
tree.Branch("bbar_eta", bbar_eta_arr, 'bbar_eta/F')
tree.Branch("bbar_phi", bbar_phi_arr, 'bbar_phi/F')
tree.Branch("bbar_mass", bbar_mass_arr, 'bbar_mass/F')

# Tops and nus

tree.Branch("nu_pt", nu_pt_arr, 'nu_pt/F')
tree.Branch("nu_eta", nu_eta_arr, 'nu_eta/F')
tree.Branch("nu_phi", nu_phi_arr, 'nu_phi/F')

tree.Branch("nubar_pt", nubar_pt_arr, 'nubar_pt/F')
tree.Branch("nubar_eta", nubar_eta_arr, 'nubar_eta/F')
tree.Branch("nubar_phi", nubar_phi_arr, 'nubar_phi/F')

tree.Branch("t_pt", t_pt_arr, 't_pt/F')
tree.Branch("t_eta", t_eta_arr, 't_eta/F')
tree.Branch("t_phi", t_phi_arr, 't_phi/F')
tree.Branch("t_rapidity", t_rap_arr, 't_rapidity/F')

tree.Branch("tbar_pt", tbar_pt_arr, 'tbar_pt/F')
tree.Branch("tbar_eta", tbar_eta_arr, 'tbar_eta/F')
tree.Branch("tbar_phi", tbar_phi_arr, 'tbar_phi/F')
tree.Branch("tbar_rapidity", tbar_rap_arr, 'tbar_rapidity/F')

tree.Branch("tt_mass", m_ttbar_arr, 'tt_mass/F')

# Weights
#tree.Branch("sc_weight", sc_weight_arr, "sc_weight/F")
tree.Branch("weight_size", weight_size_arr, "weight_size/I")
tree.Branch("weight", weight_arr, "weight[weight_size]/F")

# Gen branches
tree.Branch("gen_t_pt",  gen_t_pt_arr, 'gen_t_pt/F')
tree.Branch("gen_t_eta", gen_t_eta_arr, 'gen_t_eta/F')
tree.Branch("gen_t_phi", gen_t_phi_arr, 'gen_t_phi/F')
tree.Branch("gen_t_rapidity", gen_t_rap_arr, 'gen_t_rapidity/F')

tree.Branch("gen_tbar_pt", gen_tbar_pt_arr, 'gen_tbar_pt/F')
tree.Branch("gen_tbar_eta", gen_tbar_eta_arr, 'gen_tbar_eta/F')
tree.Branch("gen_tbar_phi", gen_tbar_phi_arr, 'gen_tbar_phi/F')
tree.Branch("gen_tbar_rapidity", gen_tbar_rap_arr, 'gen_tbar_rapidity/F')

tree.Branch("gen_tt_mass", gen_m_ttbar_arr, 'gen_tt_mass/F')


for i in range(len(top_pt)):

    l_pt_arr[0]   = lep_pt[i]
    l_eta_arr[0]  = lep_eta[i]
    l_phi_arr[0]  = lep_phi[i]
    l_mass_arr[0] = lep_mass[i]

    lbar_pt_arr[0]   = alep_pt[i]
    lbar_eta_arr[0]  = alep_eta[i]
    lbar_phi_arr[0]  = alep_phi[i]
    lbar_mass_arr[0] = alep_mass[i]

    b_pt_arr[0]   = b_pt[i]
    b_eta_arr[0]  = b_eta[i]
    b_phi_arr[0]  = b_phi[i]
    b_mass_arr[0] = b_mass[i]

    bbar_pt_arr[0]   = bbar_pt[i]
    bbar_eta_arr[0]  = bbar_eta[i]
    bbar_phi_arr[0]  = bbar_phi[i]
    bbar_mass_arr[0] = bbar_mass[i]

    nu_pt_arr[0]  = nu_pt[i]
    nu_eta_arr[0] = nu_eta[i]
    nu_phi_arr[0] = nu_phi[i]

    nubar_pt_arr[0]  = anu_pt[i]
    nubar_eta_arr[0] = anu_eta[i]
    nubar_phi_arr[0] = anu_phi[i]

    t_pt_arr[0]  = top_pt[i]
    t_eta_arr[0] = top_eta[i]
    t_phi_arr[0] = top_phi[i]
    t_rap_arr[0] = top_rap[i]

    tbar_pt_arr[0]  = atop_pt[i]
    tbar_eta_arr[0] = atop_eta[i]
    tbar_phi_arr[0] = atop_phi[i]
    tbar_rap_arr[0] = atop_rap[i]

    m_ttbar_arr[0]   = tt_mass[i]
    
    gen_t_pt_arr[0] = gen_top_pt[i]
    gen_t_eta_arr[0] = gen_top_eta[i]
    gen_t_phi_arr[0] = gen_top_phi[i]
    gen_t_rap_arr[0] = gen_top_rap[i]

    gen_tbar_pt_arr[0] = gen_atop_pt[i]
    gen_tbar_eta_arr[0] = gen_atop_eta[i]
    gen_tbar_phi_arr[0] = gen_atop_phi[i]
    gen_tbar_rap_arr[0] = gen_atop_rap[i]

    gen_m_ttbar_arr[0] = gen_tt_mass[i]
    
    weight_size_arr[0]  = len(weight_sel[i])

    for k in range(weight_size_arr[0]):
        weight_arr[k] = weight_sel[i][k]

    tree.Fill()

# Write the tree into the output file and close the file
opfile.Write()
opfile.Close()
