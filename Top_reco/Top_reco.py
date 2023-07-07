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
parser.add_argument('-v', '--verbose', action='count', default=0, help='Verbosity', required=False)

args       = parser.parse_args()
inputFile  = args.input
outputFile = args.input
verbose = args.verbose 

fileptr = uproot.open(inputFile)['Step7']

# Gen part info
#pt     = fileptr['genpart_pt'].array()
#eta    = fileptr['genpart_eta'].array()
#phi    = fileptr['genpart_phi'].array()
#pid    = fileptr['genpart_pid'].array()
#mass   = fileptr['genpart_mass'].array()
#status = fileptr['genpart_status'].array()

step7_gen_top_pt     = fileptr['gen_top_pt'].array()
step7_gen_top_eta    = fileptr['gen_top_eta'].array()
step7_gen_top_phi    = fileptr['gen_top_phi'].array()
step7_gen_top_mass    = fileptr['gen_top_mass'].array()

step7_gen_atop_pt     = fileptr['gen_atop_pt'].array()
step7_gen_atop_eta    = fileptr['gen_atop_eta'].array()
step7_gen_atop_phi    = fileptr['gen_atop_phi'].array()
step7_gen_atop_mass    = fileptr['gen_atop_mass'].array()

step7_gen_b_pt     = fileptr['gen_b_pt'].array()
step7_gen_b_eta    = fileptr['gen_b_eta'].array()
step7_gen_b_phi    = fileptr['gen_b_phi'].array()
step7_gen_b_mass    = fileptr['gen_b_mass'].array()

step7_gen_ab_pt     = fileptr['gen_ab_pt'].array()
step7_gen_ab_eta    = fileptr['gen_ab_eta'].array()
step7_gen_ab_phi    = fileptr['gen_ab_phi'].array()
step7_gen_ab_mass    = fileptr['gen_ab_mass'].array()

step7_gen_lep_pt     = fileptr['gen_lep_pt'].array()
step7_gen_lep_eta    = fileptr['gen_lep_eta'].array()
step7_gen_lep_phi    = fileptr['gen_lep_phi'].array()
step7_gen_lep_mass    = fileptr['gen_lep_mass'].array()
step7_gen_lep_pdgid = fileptr['gen_lep_pdgid'].array()

step7_gen_alep_pt     = fileptr['gen_alep_pt'].array()
step7_gen_alep_eta    = fileptr['gen_alep_eta'].array()
step7_gen_alep_phi    = fileptr['gen_alep_phi'].array()
step7_gen_alep_mass    = fileptr['gen_alep_mass'].array()
step7_gen_alep_pdgid = fileptr['gen_alep_pdgid'].array()

if (verbose > 0):

    step7_gen_lep_nearest_pt     = fileptr['gen_lep_nearest_pt'].array()
    step7_gen_lep_nearest_eta    = fileptr['gen_lep_nearest_eta'].array()
    step7_gen_lep_nearest_phi    = fileptr['gen_lep_nearest_phi'].array()
    step7_gen_lep_nearest_mass    = fileptr['gen_lep_nearest_mass'].array()
    step7_gen_lep_nearest_pdgid = fileptr['gen_lep_nearest_pdgid'].array()

    step7_gen_alep_nearest_pt     = fileptr['gen_alep_nearest_pt'].array()
    step7_gen_alep_nearest_eta    = fileptr['gen_alep_nearest_eta'].array()
    step7_gen_alep_nearest_phi    = fileptr['gen_alep_nearest_phi'].array()
    step7_gen_alep_nearest_mass    = fileptr['gen_alep_nearest_mass'].array()
    step7_gen_alep_nearest_pdgid = fileptr['gen_alep_nearest_pdgid'].array()

step7_gen_neu_pt     = fileptr['gen_neu_pt'].array()
step7_gen_neu_eta    = fileptr['gen_neu_eta'].array()
step7_gen_neu_phi    = fileptr['gen_neu_phi'].array()
step7_gen_neu_pdgid = fileptr['gen_neu_pdgid'].array()

step7_gen_aneu_pt     = fileptr['gen_aneu_pt'].array()
step7_gen_aneu_eta    = fileptr['gen_aneu_eta'].array()
step7_gen_aneu_phi    = fileptr['gen_aneu_phi'].array()
step7_gen_aneu_pdgid = fileptr['gen_aneu_pdgid'].array()

step7_gen_met_pt     = fileptr['gen_met_pt'].array()
step7_gen_met_phi    = fileptr['gen_met_phi'].array()

# Reco level info
step7_MET      = fileptr['MET'].array()
step7_MET_phi  = fileptr['MET_phi'].array()

step7_lep_pt     = fileptr['lep_pt'].array()
step7_lep_eta    = fileptr['lep_eta'].array()
step7_lep_phi    = fileptr['lep_phi'].array()
step7_lep_mass    = fileptr['lep_mass'].array()
step7_lep_pdgid = fileptr['lep_pdgid'].array()

step7_alep_pt     = fileptr['alep_pt'].array()
step7_alep_eta    = fileptr['alep_eta'].array()
step7_alep_phi    = fileptr['alep_phi'].array()
step7_alep_mass    = fileptr['alep_mass'].array()
step7_alep_pdgid = fileptr['alep_pdgid'].array()

step7_jet_btag  = fileptr['jet_btag'].array()
step7_jet_pt    = fileptr['jet_pt'].array()
step7_jet_eta   = fileptr['jet_eta'].array()
step7_jet_phi   = fileptr['jet_phi'].array()
step7_jet_mass  = fileptr['jet_mass'].array()
step7_jet_size = fileptr['jet_size'].array()

step7_weight    = fileptr['weight'].array()


# Storing the reconstructed as arrays

step8_lep_pt   = []
step8_lep_eta  = []
step8_lep_phi  = []
step8_lep_mass = []
step8_lep_pdgid = []

step8_alep_pt   = []
step8_alep_eta  = []
step8_alep_phi  = []
step8_alep_mass = []
step8_alep_pdgid = []

step8_b_pt   = []
step8_b_eta  = []
step8_b_phi  = []
step8_b_mass = []

step8_ab_pt   = []
step8_ab_eta  = []
step8_ab_phi  = []
step8_ab_mass = []

step8_neu_pt  = []
step8_neu_eta = []
step8_neu_phi = []
step8_neu_pdgid = []

step8_aneu_pt  = []
step8_aneu_eta = []
step8_aneu_phi = []
step8_aneu_pdgid = []

step8_top_pt  = []
step8_top_eta = []
step8_top_phi = []
step8_top_mass = []
step8_top_rap = []

step8_atop_pt  = []
step8_atop_eta = []
step8_atop_phi = []
step8_atop_mass = []
step8_atop_rap = []

step8_tt_mass  = []
step8_tt_pt = []
step8_tt_eta = []
step8_tt_phi = []
step8_tt_rap = []

step8_met_pt = []
step8_met_phi = []


# Gen as arrays

step8_gen_tt_mass = []
step8_gen_tt_pt = []
step8_gen_tt_eta = []
step8_gen_tt_phi = []
step8_gen_tt_rap = []

step8_gen_top_pt  = []
step8_gen_top_eta = []
step8_gen_top_phi = []
step8_gen_top_mass = []
step8_gen_top_rap = []

step8_gen_atop_pt  = []
step8_gen_atop_eta = []
step8_gen_atop_phi = []
step8_gen_atop_mass = []
step8_gen_atop_rap = []

step8_gen_b_pt = []
step8_gen_b_eta= []
step8_gen_b_phi= []
step8_gen_b_mass= []

step8_gen_ab_pt = []
step8_gen_ab_eta= []
step8_gen_ab_phi= []
step8_gen_ab_mass= []

step8_gen_lep_pt = []
step8_gen_lep_eta= []
step8_gen_lep_phi= []
step8_gen_lep_mass= []
step8_gen_lep_pdgid = []

step8_gen_alep_pt = []
step8_gen_alep_eta= []
step8_gen_alep_phi= []
step8_gen_alep_mass= []
step8_gen_alep_pdgid = []

if (verbose > 0):
    
    step8_gen_lep_nearest_pt = []
    step8_gen_lep_nearest_eta= []
    step8_gen_lep_nearest_phi= []
    step8_gen_lep_nearest_mass= []
    step8_gen_lep_nearest_pdgid = []

    step8_gen_alep_nearest_pt = []
    step8_gen_alep_nearest_eta= []
    step8_gen_alep_nearest_phi= []
    step8_gen_alep_nearest_mass= []
    step8_gen_alep_nearest_pdgid = []

step8_gen_neu_pt = []
step8_gen_neu_eta= []
step8_gen_neu_phi= []
step8_gen_neu_pdgid = []

step8_gen_aneu_pt = []
step8_gen_aneu_eta= []
step8_gen_aneu_phi= []
step8_gen_aneu_pdgid = []

step8_gen_met_pt = []
step8_gen_met_phi = []

# Let's create a mask
selection = np.zeros(len(step7_jet_pt))

for i in range(len(step7_jet_pt)):
    
    if (i % 500 == 0):
        print('Processing event :: ' + str(i))
        now = datetime.now()   # Time keeping
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

    if (step7_lep_pt[i]>0 or step7_lep_pt[i]<0):

        lep  = ROOT.TLorentzVector()
        alep = ROOT.TLorentzVector()
    
        # lep charge -1 and alep charge +1
    
        lep.SetPtEtaPhiM(step7_lep_pt[i], step7_lep_eta[i], step7_lep_phi[i], step7_lep_mass[i])
        alep.SetPtEtaPhiM(step7_alep_pt[i], step7_alep_eta[i], step7_alep_phi[i], step7_alep_mass[i])
    
        met_x = step7_MET[i] * np.cos(step7_MET_phi[i])
        met_y = step7_MET[i] * np.sin(step7_MET_phi[i])
    
        # Only consider 2 btagged jets is found, high_w is used for single b-tag case
        n_btag = 0
        high_w = 0
        m_tt_final = 0
    
        # Loop over jet permutations and find those with 2-btags or highest sum of weights
    
        for j in range(len(step7_jet_pt[i])):     # First jet
            for k in range(len(step7_jet_pt[i])):  # Second jet
    
                if (j >= k):
                    continue
                if (step7_jet_pt[i][j] < 30 or step7_jet_pt[i][k] < 30):
                    continue
                if (abs(step7_jet_eta[i][j]) > 5.0 or abs(step7_jet_eta[i][k]) > 5.0):
                    continue
                if (step7_jet_btag[i][j] == 0 and step7_jet_btag[i][k] == 0):
                    continue
    
                jet1 = ROOT.TLorentzVector()
                jet2 = ROOT.TLorentzVector()
                jet1.SetPtEtaPhiM(step7_jet_pt[i][j], step7_jet_eta[i][j], step7_jet_phi[i][j], step7_jet_mass[i][j])
                jet2.SetPtEtaPhiM(step7_jet_pt[i][k], step7_jet_eta[i][k], step7_jet_phi[i][k], step7_jet_mass[i][k])
    
                if (lep.DeltaR(jet1) < 0.4 or lep.DeltaR(jet2) < 0.4 or alep.DeltaR(jet1) < 0.4 or alep.DeltaR(jet2) < 0.4):
                    continue
    
                # 2-Btag scenario
                if (step7_jet_btag[i][j] != 0 and step7_jet_btag[i][k] != 0):
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
                if ((step7_jet_btag[i][j] != 0 and step7_jet_btag[i][k] == 0) or (step7_jet_btag[i][j] == 0 and step7_jet_btag[i][k] != 0)):
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
    
    
        rcom = top_p4_final + atop_p4_final
    
        gen_top = ROOT.TLorentzVector()
        gen_top.SetPtEtaPhiM(step7_gen_top_pt[i], step7_gen_top_eta[i], step7_gen_top_phi[i], step7_gen_top_mass[i])
    
        gen_atop = ROOT.TLorentzVector()
        gen_atop.SetPtEtaPhiM(step7_gen_atop_pt[i], step7_gen_atop_eta[i], step7_gen_atop_phi[i], step7_gen_atop_mass[i])
    
        # COM 4-vec
        com = gen_top + gen_atop  # Adding the 4 vectors
    
        step8_tt_mass.append(m_tt_final)
        step8_tt_pt.append(rcom.Pt())
        step8_tt_eta.append(rcom.Eta())
        step8_tt_phi.append(rcom.Phi())
        step8_tt_rap.append(rcom.Rapidity())
    
        step8_top_pt.append(top_p4_final.Pt())
        step8_top_eta.append(top_p4_final.Eta())
        step8_top_phi.append(top_p4_final.Phi())
        step8_top_mass.append(top_p4_final.M())
        step8_top_rap.append(top_p4_final.Rapidity())
    
        step8_atop_pt.append(atop_p4_final.Pt())
        step8_atop_eta.append(atop_p4_final.Eta())
        step8_atop_phi.append(atop_p4_final.Phi())
        step8_atop_mass.append(atop_p4_final.M())
        step8_atop_rap.append(atop_p4_final.Rapidity())
    
        step8_neu_pt.append(nu_p4_final.Pt())
        step8_neu_eta.append(nu_p4_final.Eta())
        step8_neu_phi.append(nu_p4_final.Phi())
    
        step8_aneu_pt.append(nubar_p4_final.Pt())
        step8_aneu_eta.append(nubar_p4_final.Eta())
        step8_aneu_phi.append(nubar_p4_final.Phi())
    
        step8_lep_pt.append(lep.Pt())
        step8_lep_eta.append(lep.Eta())
        step8_lep_phi.append(lep.Phi())
        step8_lep_mass.append(lep.M())
        step8_lep_pdgid.append(step7_lep_pdgid[i])
    
        step8_alep_pt.append(alep.Pt())
        step8_alep_eta.append(alep.Eta())
        step8_alep_phi.append(alep.Phi())
        step8_alep_mass.append(alep.M())
        step8_alep_pdgid.append(step7_alep_pdgid[i])
    
        step8_b_pt.append(b_p4_final.Pt())
        step8_b_eta.append(b_p4_final.Eta())
        step8_b_phi.append(b_p4_final.Phi())
        step8_b_mass.append(b_p4_final.M())
    
        step8_ab_pt.append(bbar_p4_final.Pt())
        step8_ab_eta.append(bbar_p4_final.Eta())
        step8_ab_phi.append(bbar_p4_final.Phi())
        step8_ab_mass.append(bbar_p4_final.M())
    
        step8_met_pt.append(step7_MET[i])
        step8_met_phi.append(step7_MET_phi[i])
    
    
        step8_gen_tt_mass.append(com.M())
        step8_gen_tt_pt.append(com.Pt())
        step8_gen_tt_eta.append(com.Eta())
        step8_gen_tt_phi.append(com.Phi())
        step8_gen_tt_rap.append(com.Rapidity())
    
        step8_gen_top_pt.append(gen_top.Pt())
        step8_gen_top_eta.append(gen_top.Eta())
        step8_gen_top_phi.append(gen_top.Phi())
        step8_gen_top_mass.append(gen_top.M())
        step8_gen_top_rap.append(gen_top.Rapidity())
    
        step8_gen_atop_pt.append(gen_atop.Pt())
        step8_gen_atop_eta.append(gen_atop.Eta())
        step8_gen_atop_phi.append(gen_atop.Phi())
        step8_gen_atop_mass.append(gen_atop.M())
        step8_gen_atop_rap.append(gen_atop.Rapidity())
    
        step8_gen_b_pt.append(step7_gen_b_pt[i])
        step8_gen_b_eta.append(step7_gen_b_eta[i])
        step8_gen_b_phi.append(step7_gen_b_phi[i])
        step8_gen_b_mass.append(step7_gen_b_mass[i])
    
        step8_gen_ab_pt.append(step7_gen_ab_pt[i])
        step8_gen_ab_eta.append(step7_gen_ab_eta[i])
        step8_gen_ab_phi.append(step7_gen_ab_phi[i])
        step8_gen_ab_mass.append(step7_gen_ab_mass[i])
    
        step8_gen_lep_pt.append(step7_gen_lep_pt[i])
        step8_gen_lep_eta.append(step7_gen_lep_eta[i])
        step8_gen_lep_phi.append(step7_gen_lep_phi[i])
        step8_gen_lep_mass.append(step7_gen_lep_mass[i])
        step8_gen_lep_pdgid.append(step7_gen_lep_pdgid[i])
    
        step8_gen_alep_pt.append(step7_gen_alep_pt[i])
        step8_gen_alep_eta.append(step7_gen_alep_eta[i])
        step8_gen_alep_phi.append(step7_gen_alep_phi[i])
        step8_gen_alep_mass.append(step7_gen_alep_mass[i])
        step8_gen_alep_pdgid.append(step7_gen_alep_pdgid[i])

        if (verbose > 0):
    
            step8_gen_lep_nearest_pt.append(step7_gen_lep_nearest_pt[i])
            step8_gen_lep_nearest_eta.append(step7_gen_lep_nearest_eta[i])
            step8_gen_lep_nearest_phi.append(step7_gen_lep_nearest_phi[i])
            step8_gen_lep_nearest_mass.append(step7_gen_lep_nearest_mass[i])
            step8_gen_lep_nearest_pdgid.append(step7_gen_lep_nearest_pdgid[i])

            step8_gen_alep_nearest_pt.append(step7_gen_alep_nearest_pt[i])
            step8_gen_alep_nearest_eta.append(step7_gen_alep_nearest_eta[i])
            step8_gen_alep_nearest_phi.append(step7_gen_alep_nearest_phi[i])
            step8_gen_alep_nearest_mass.append(step7_gen_alep_nearest_mass[i])
            step8_gen_alep_nearest_pdgid.append(step7_gen_alep_nearest_pdgid[i])
    
        step8_gen_neu_pt.append(step7_gen_neu_pt[i])
        step8_gen_neu_eta.append(step7_gen_neu_eta[i])
        step8_gen_neu_phi.append(step7_gen_neu_phi[i])
        step8_gen_neu_pdgid.append(step7_gen_neu_pdgid[i])
    
        step8_gen_aneu_pt.append(step7_gen_aneu_pt[i])
        step8_gen_aneu_eta.append(step7_gen_aneu_eta[i])
        step8_gen_aneu_phi.append(step7_gen_aneu_phi[i])
        step8_gen_aneu_pdgid.append(step7_gen_aneu_pdgid[i])
    
        step8_gen_met_pt.append(step7_gen_met_pt[i])
        step8_gen_met_phi.append(step7_gen_met_phi[i])   
    
        # Create a mask for selection
        selection[i] = 1

step8_weight_sel = step7_weight[selection == 1]
print(len(step8_top_pt))

# Empty arrays that get mapped to histograms in a root file
# Selected leptons and jets

lep_pt_arr = array('f', [0.])
lep_eta_arr = array('f', [0.])
lep_phi_arr = array('f', [0.])
lep_mass_arr = array('f', [0.])
lep_pdgid_arr = array('f', [0.])

alep_pt_arr   = array('f', [0.])
alep_eta_arr  = array('f', [0.])
alep_phi_arr  = array('f', [0.])
alep_mass_arr = array('f', [0.])
alep_pdgid_arr  = array('f', [0.])

lep_pt_arr = array('f', [0.])
lep_eta_arr = array('f', [0.])
lep_phi_arr = array('f', [0.])
lep_mass_arr = array('f', [0.])
lep_pdgid_arr = array('f', [0.])

alep_pt_arr   = array('f', [0.])
alep_eta_arr  = array('f', [0.])
alep_phi_arr  = array('f', [0.])
alep_mass_arr = array('f', [0.])
alep_pdgid_arr  = array('f', [0.])

b_pt_arr = array('f', [0.])
b_eta_arr = array('f', [0.])
b_phi_arr = array('f', [0.])
b_mass_arr = array('f', [0.])

ab_pt_arr   = array('f', [0.])
ab_eta_arr  = array('f', [0.])
ab_phi_arr  = array('f', [0.])
ab_mass_arr = array('f', [0.])

# Reconstructed tops and nus
neu_pt_arr  = array('f', [0.])
neu_eta_arr = array('f', [0.])
neu_phi_arr = array('f', [0.])

aneu_pt_arr  = array('f', [0.])
aneu_eta_arr = array('f', [0.])
aneu_phi_arr = array('f', [0.])

top_pt_arr = array('f', [0.])
top_eta_arr = array('f', [0.])
top_phi_arr = array('f', [0.])
top_mass_arr = array('f', [0.])
top_rap_arr = array('f', [0.])

atop_pt_arr = array('f', [0.])
atop_eta_arr = array('f', [0.])
atop_phi_arr = array('f', [0.])
atop_mass_arr = array('f', [0.])
atop_rap_arr = array('f', [0.])

m_ttbar_arr   = array('f', [0.])
ttbar_pt_arr   = array('f', [0.])
ttbar_eta_arr   = array('f', [0.])
ttbar_phi_arr   = array('f', [0.])
ttbar_rap_arr   = array('f', [0.])

met_pt_arr = array('f', [0.])
met_phi_arr= array('f', [0.])

# Weights 
maxn    = 9999
weight_size_arr = array('i', [0])
weight_arr      = array('f', maxn*[0.])

# Gen entries
gen_m_ttbar_arr = array('f', [0.])
gen_ttbar_pt_arr   = array('f', [0.])
gen_ttbar_eta_arr   = array('f', [0.])
gen_ttbar_phi_arr   = array('f', [0.])
gen_ttbar_rap_arr   = array('f', [0.])

gen_top_pt_arr = array('f', [0.])
gen_top_eta_arr = array('f', [0.])
gen_top_phi_arr = array('f', [0.])
gen_top_mass_arr = array('f', [0.])
gen_top_rap_arr = array('f', [0.])

gen_atop_pt_arr = array('f', [0.])
gen_atop_eta_arr = array('f', [0.])
gen_atop_phi_arr = array('f', [0.])
gen_atop_mass_arr = array('f', [0.])
gen_atop_rap_arr = array('f', [0.])

gen_b_pt_arr  = array('f', [0.])
gen_b_eta_arr = array('f', [0.])
gen_b_phi_arr = array('f', [0.])
gen_b_mass_arr = array('f', [0.])

gen_ab_pt_arr = array('f', [0.])
gen_ab_eta_arr= array('f', [0.])
gen_ab_phi_arr= array('f', [0.])
gen_ab_mass_arr= array('f', [0.])

gen_lep_pt_arr  = array('f', [0.])
gen_lep_eta_arr = array('f', [0.])
gen_lep_phi_arr = array('f', [0.])
gen_lep_mass_arr = array('f', [0.])
gen_lep_pdgid_arr  = array('f', [0.])

gen_alep_pt_arr = array('f', [0.])
gen_alep_eta_arr= array('f', [0.])
gen_alep_phi_arr= array('f', [0.])
gen_alep_mass_arr= array('f', [0.])
gen_alep_pdgid_arr = array('f', [0.])

if (verbose > 0):

    gen_lep_nearest_pt_arr  = array('f', [0.])
    gen_lep_nearest_eta_arr = array('f', [0.])
    gen_lep_nearest_phi_arr = array('f', [0.])
    gen_lep_nearest_mass_arr = array('f', [0.])
    gen_lep_nearest_pdgid_arr  = array('f', [0.])

    gen_alep_nearest_pt_arr = array('f', [0.])
    gen_alep_nearest_eta_arr= array('f', [0.])
    gen_alep_nearest_phi_arr= array('f', [0.])
    gen_alep_nearest_mass_arr= array('f', [0.])
    gen_alep_nearest_pdgid_arr = array('f', [0.])

gen_neu_pt_arr  = array('f', [0.])
gen_neu_eta_arr = array('f', [0.])
gen_neu_phi_arr = array('f', [0.])
gen_neu_pdgid_arr  = array('f', [0.])

gen_aneu_pt_arr = array('f', [0.])
gen_aneu_eta_arr= array('f', [0.])
gen_aneu_phi_arr= array('f', [0.])
gen_aneu_pdgid_arr = array('f', [0.])

gen_met_pt_arr = array('f', [0.])
gen_met_phi_arr= array('f', [0.])


opfile = ROOT.TFile(outputFile, 'update')
tree   = ROOT.TTree("Step8", "Step8")

# Leptons and jets

tree.Branch("lep_pt", lep_pt_arr, 'lep_pt/F')
tree.Branch("lep_eta", lep_eta_arr, 'lep_eta/F')
tree.Branch("lep_phi", lep_phi_arr, 'lep_phi/F')
tree.Branch("lep_mass", lep_mass_arr, 'lep_mass/F')
tree.Branch("lep_pdgid", lep_pdgid_arr, 'lep_pdgid/F')

tree.Branch("alep_pt", alep_pt_arr, 'alep_pt/F')
tree.Branch("alep_eta", alep_eta_arr, 'alep_eta/F')
tree.Branch("alep_phi", alep_phi_arr, 'alep_phi/F')
tree.Branch("alep_mass", alep_mass_arr, 'alep_mass/F')
tree.Branch("alep_pdgid", alep_pdgid_arr, 'alep_pdgid/F')

tree.Branch("b_pt", b_pt_arr, 'b_pt/F')
tree.Branch("b_eta", b_eta_arr, 'b_eta/F')
tree.Branch("b_phi", b_phi_arr, 'b_phi/F')
tree.Branch("b_mass", b_mass_arr, 'b_mass/F')

tree.Branch("ab_pt", ab_pt_arr, 'ab_pt/F')
tree.Branch("ab_eta", ab_eta_arr, 'ab_eta/F')
tree.Branch("ab_phi", ab_phi_arr, 'ab_phi/F')
tree.Branch("ab_mass", ab_mass_arr, 'ab_mass/F')

# Tops and nus

tree.Branch("neu_pt", neu_pt_arr, 'neu_pt/F')
tree.Branch("neu_eta", neu_eta_arr, 'neu_eta/F')
tree.Branch("neu_phi", neu_phi_arr, 'neu_phi/F')

tree.Branch("aneu_pt", aneu_pt_arr, 'aneu_pt/F')
tree.Branch("aneu_eta", aneu_eta_arr, 'aneu_eta/F')
tree.Branch("aneu_phi", aneu_phi_arr, 'aneu_phi/F')

tree.Branch("top_pt", top_pt_arr, 'top_pt/F')
tree.Branch("top_eta", top_eta_arr, 'top_eta/F')
tree.Branch("top_phi", top_phi_arr, 'top_phi/F')
tree.Branch("top_mass", top_mass_arr, 'top_mass/F')
tree.Branch("top_rap", top_rap_arr, 'top_rap/F')

tree.Branch("atop_pt", atop_pt_arr, 'atop_pt/F')
tree.Branch("atop_eta", atop_eta_arr, 'atop_eta/F')
tree.Branch("atop_phi", atop_phi_arr, 'atop_phi/F')
tree.Branch("atop_mass", atop_mass_arr, 'atop_mass/F')
tree.Branch("atop_rap", atop_rap_arr, 'atop_rap/F')

tree.Branch("tt_mass", m_ttbar_arr, 'tt_mass/F')
tree.Branch("tt_pt", ttbar_pt_arr, 'tt_pt/F')
tree.Branch("tt_eta", ttbar_eta_arr, 'tt_eta/F')
tree.Branch("tt_phi", ttbar_phi_arr, 'tt_phi/F')
tree.Branch("tt_rap", ttbar_rap_arr, 'tt_rap/F')

tree.Branch("met_pt"    , met_pt_arr    , 'met_pt/F')
tree.Branch("met_phi"   , met_phi_arr   , 'met_phi/F')

# Weights
#tree.Branch("sc_weight", sc_weight_arr, "sc_weight/F")
tree.Branch("weight_size", weight_size_arr, "weight_size/I")
tree.Branch("weight", weight_arr, "weight[weight_size]/F")

# Gen branches
tree.Branch("gen_tt_mass", gen_m_ttbar_arr, 'gen_tt_mass/F')
tree.Branch("gen_tt_pt", gen_ttbar_pt_arr, 'gen_tt_pt/F')
tree.Branch("gen_tt_eta", gen_ttbar_eta_arr, 'gen_tt_eta/F')
tree.Branch("gen_tt_phi", gen_ttbar_phi_arr, 'gen_tt_phi/F')
tree.Branch("gen_tt_rap", gen_ttbar_rap_arr, 'gen_tt_rap/F')

tree.Branch("gen_top_pt",  gen_top_pt_arr, 'gen_top_pt/F')
tree.Branch("gen_top_eta", gen_top_eta_arr, 'gen_top_eta/F')
tree.Branch("gen_top_phi", gen_top_phi_arr, 'gen_top_phi/F')
tree.Branch("gen_top_mass"   , gen_top_mass_arr   , 'gen_top_mass/F')
tree.Branch("gen_top_rap", gen_top_rap_arr, 'gen_top_rap/F')

tree.Branch("gen_atop_pt", gen_atop_pt_arr, 'gen_atop_pt/F')
tree.Branch("gen_atop_eta", gen_atop_eta_arr, 'gen_atop_eta/F')
tree.Branch("gen_atop_phi", gen_atop_phi_arr, 'gen_atop_phi/F')
tree.Branch("gen_atop_mass"   , gen_atop_mass_arr   , 'gen_atop_mass/F')
tree.Branch("gen_atop_rap", gen_atop_rap_arr, 'gen_atop_rap/F')

tree.Branch("gen_b_pt"    , gen_b_pt_arr    , 'gen_b_pt/F')
tree.Branch("gen_b_eta"   , gen_b_eta_arr   , 'gen_b_eta/F')
tree.Branch("gen_b_phi"   , gen_b_phi_arr   , 'gen_b_phi/F')
tree.Branch("gen_b_mass"   , gen_b_mass_arr   , 'gen_b_mass/F')

tree.Branch("gen_ab_pt"    , gen_ab_pt_arr    , 'gen_ab_pt/F')
tree.Branch("gen_ab_eta"   , gen_ab_eta_arr   , 'gen_ab_eta/F')
tree.Branch("gen_ab_phi"   , gen_ab_phi_arr   , 'gen_ab_phi/F')
tree.Branch("gen_ab_mass"   , gen_ab_mass_arr   , 'gen_ab_mass/F')

tree.Branch("gen_lep_pt"    , gen_lep_pt_arr    , 'gen_lep_pt/F')
tree.Branch("gen_lep_eta"   , gen_lep_eta_arr   , 'gen_lep_eta/F')
tree.Branch("gen_lep_phi"   , gen_lep_phi_arr   , 'gen_lep_phi/F')
tree.Branch("gen_lep_mass"   , gen_lep_mass_arr   , 'gen_lep_mass/F')
tree.Branch("gen_lep_pdgid", gen_lep_pdgid_arr, 'gen_lep_pdgid/F')

tree.Branch("gen_alep_pt"    , gen_alep_pt_arr    , 'gen_alep_pt/F')
tree.Branch("gen_alep_eta"   , gen_alep_eta_arr   , 'gen_alep_eta/F')
tree.Branch("gen_alep_phi"   , gen_alep_phi_arr   , 'gen_alep_phi/F')
tree.Branch("gen_alep_mass"   , gen_alep_mass_arr   , 'gen_alep_mass/F')
tree.Branch("gen_alep_pdgid", gen_alep_pdgid_arr, 'gen_alep_pdgid/F')

if (verbose > 0):
    
    tree.Branch("gen_lep_nearest_pt"    , gen_lep_nearest_pt_arr    , 'gen_lep_nearest_pt/F')
    tree.Branch("gen_lep_nearest_eta"   , gen_lep_nearest_eta_arr   , 'gen_lep_nearest_eta/F')
    tree.Branch("gen_lep_nearest_phi"   , gen_lep_nearest_phi_arr   , 'gen_lep_nearest_phi/F')
    tree.Branch("gen_lep_nearest_mass"   , gen_lep_nearest_mass_arr   , 'gen_lep_nearest_mass/F')
    tree.Branch("gen_lep_nearest_pdgid", gen_lep_nearest_pdgid_arr, 'gen_lep_nearest_pdgid/F')

    tree.Branch("gen_alep_nearest_pt"    , gen_alep_nearest_pt_arr    , 'gen_alep_nearest_pt/F')
    tree.Branch("gen_alep_nearest_eta"   , gen_alep_nearest_eta_arr   , 'gen_alep_nearest_eta/F')
    tree.Branch("gen_alep_nearest_phi"   , gen_alep_nearest_phi_arr   , 'gen_alep_nearest_phi/F')
    tree.Branch("gen_alep_nearest_mass"   , gen_alep_nearest_mass_arr   , 'gen_alep_nearest_mass/F')
    tree.Branch("gen_alep_nearest_pdgid", gen_alep_nearest_pdgid_arr, 'gen_alep_nearest_pdgid/F')

tree.Branch("gen_neu_pt"    , gen_neu_pt_arr    , 'gen_neu_pt/F')
tree.Branch("gen_neu_eta"   , gen_neu_eta_arr   , 'gen_neu_eta/F')
tree.Branch("gen_neu_phi"   , gen_neu_phi_arr   , 'gen_neu_phi/F')
tree.Branch("gen_neu_pdgid", gen_neu_pdgid_arr, 'gen_neu_pdgid/F')

tree.Branch("gen_aneu_pt"    , gen_aneu_pt_arr    , 'gen_aneu_pt/F')
tree.Branch("gen_aneu_eta"   , gen_aneu_eta_arr   , 'gen_aneu_eta/F')
tree.Branch("gen_aneu_phi"   , gen_aneu_phi_arr   , 'gen_aneu_phi/F')
tree.Branch("gen_aneu_pdgid", gen_aneu_pdgid_arr, 'gen_aneu_pdgid/F')

tree.Branch("gen_met_pt"    , gen_met_pt_arr    , 'gen_met_pt/F')
tree.Branch("gen_met_phi"   , gen_met_phi_arr   , 'gen_met_phi/F')


for i in range(len(step8_top_pt)):

    lep_pt_arr[0]   = step8_lep_pt[i]
    lep_eta_arr[0]  = step8_lep_eta[i]
    lep_phi_arr[0]  = step8_lep_phi[i]
    lep_mass_arr[0] = step8_lep_mass[i]
    lep_pdgid_arr[0]  = step8_lep_pdgid[i]

    alep_pt_arr[0]   = step8_alep_pt[i]
    alep_eta_arr[0]  = step8_alep_eta[i]
    alep_phi_arr[0]  = step8_alep_phi[i]
    alep_mass_arr[0] = step8_alep_mass[i]
    alep_pdgid_arr[0]  = step8_alep_pdgid[i]

    b_pt_arr[0]   = step8_b_pt[i]
    b_eta_arr[0]  = step8_b_eta[i]
    b_phi_arr[0]  = step8_b_phi[i]
    b_mass_arr[0] = step8_b_mass[i]

    ab_pt_arr[0]   = step8_ab_pt[i]
    ab_eta_arr[0]  = step8_ab_eta[i]
    ab_phi_arr[0]  = step8_ab_phi[i]
    ab_mass_arr[0] = step8_ab_mass[i]

    neu_pt_arr[0]  = step8_neu_pt[i]
    neu_eta_arr[0] = step8_neu_eta[i]
    neu_phi_arr[0] = step8_neu_phi[i]

    aneu_pt_arr[0]  = step8_aneu_pt[i]
    aneu_eta_arr[0] = step8_aneu_eta[i]
    aneu_phi_arr[0] = step8_aneu_phi[i]

    top_pt_arr[0]  = step8_top_pt[i]
    top_eta_arr[0] = step8_top_eta[i]
    top_phi_arr[0] = step8_top_phi[i]
    top_mass_arr[0] = step8_top_mass[i]
    top_rap_arr[0] = step8_top_rap[i]

    atop_pt_arr[0]  = step8_atop_pt[i]
    atop_eta_arr[0] = step8_atop_eta[i]
    atop_phi_arr[0] = step8_atop_phi[i]
    atop_mass_arr[0] = step8_atop_mass[i]
    atop_rap_arr[0] = step8_atop_rap[i]

    m_ttbar_arr[0]   = step8_tt_mass[i]
    ttbar_pt_arr[0] = step8_tt_pt[i]
    ttbar_eta_arr[0] = step8_tt_eta[i]
    ttbar_phi_arr[0] = step8_tt_phi[i]
    ttbar_rap_arr[0] = step8_tt_rap[i]

    met_pt_arr[0] = step8_met_pt[i]
    met_phi_arr[0] =step8_met_phi[i]    

    gen_m_ttbar_arr[0] = step8_gen_tt_mass[i]
    gen_ttbar_pt_arr[0] = step8_gen_tt_pt[i]
    gen_ttbar_eta_arr[0] = step8_gen_tt_eta[i]
    gen_ttbar_phi_arr[0] = step8_gen_tt_phi[i]
    gen_ttbar_rap_arr[0] = step8_gen_tt_rap[i]

    gen_top_pt_arr[0] = step8_gen_top_pt[i]
    gen_top_eta_arr[0] = step8_gen_top_eta[i]
    gen_top_phi_arr[0] = step8_gen_top_phi[i]
    gen_top_mass_arr[0]    = step8_gen_top_mass[i]
    gen_top_rap_arr[0] = step8_gen_top_rap[i]

    gen_atop_pt_arr[0] = step8_gen_atop_pt[i]
    gen_atop_eta_arr[0] = step8_gen_atop_eta[i]
    gen_atop_phi_arr[0] = step8_gen_atop_phi[i]
    gen_atop_mass_arr[0]    = step8_gen_atop_mass[i]
    gen_atop_rap_arr[0] = step8_gen_atop_rap[i]

    gen_b_pt_arr[0]     = step8_gen_b_pt[i]
    gen_b_eta_arr[0]    = step8_gen_b_eta[i]
    gen_b_phi_arr[0]    = step8_gen_b_phi[i]
    gen_b_mass_arr[0]    = step8_gen_b_mass[i]

    gen_ab_pt_arr[0]     = step8_gen_ab_pt[i]
    gen_ab_eta_arr[0]    = step8_gen_ab_eta[i]
    gen_ab_phi_arr[0]    = step8_gen_ab_phi[i]
    gen_ab_mass_arr[0]    = step8_gen_ab_mass[i]

    gen_lep_pt_arr[0]     = step8_gen_lep_pt[i]
    gen_lep_eta_arr[0]    = step8_gen_lep_eta[i]
    gen_lep_phi_arr[0]    = step8_gen_lep_phi[i]
    gen_lep_mass_arr[0]    = step8_gen_lep_mass[i]
    gen_lep_pdgid_arr[0] = step8_gen_lep_pdgid[i]

    gen_alep_pt_arr[0]     = step8_gen_alep_pt[i]
    gen_alep_eta_arr[0]    = step8_gen_alep_eta[i]
    gen_alep_phi_arr[0]    = step8_gen_alep_phi[i]
    gen_alep_mass_arr[0]    = step8_gen_alep_mass[i]
    gen_alep_pdgid_arr[0] = step8_gen_alep_pdgid[i]

    if (verbose > 0):
        
        gen_lep_nearest_pt_arr[0]     = step8_gen_lep_nearest_pt[i]
        gen_lep_nearest_eta_arr[0]    = step8_gen_lep_nearest_eta[i]
        gen_lep_nearest_phi_arr[0]    = step8_gen_lep_nearest_phi[i]
        gen_lep_nearest_mass_arr[0]    = step8_gen_lep_nearest_mass[i]
        gen_lep_nearest_pdgid_arr[0] = step8_gen_lep_nearest_pdgid[i]

        gen_alep_nearest_pt_arr[0]     = step8_gen_alep_nearest_pt[i]
        gen_alep_nearest_eta_arr[0]    = step8_gen_alep_nearest_eta[i]
        gen_alep_nearest_phi_arr[0]    = step8_gen_alep_nearest_phi[i]
        gen_alep_nearest_mass_arr[0]    = step8_gen_alep_nearest_mass[i]
        gen_alep_nearest_pdgid_arr[0] = step8_gen_alep_nearest_pdgid[i]

    gen_neu_pt_arr[0]     = step8_gen_neu_pt[i]
    gen_neu_eta_arr[0]    = step8_gen_neu_eta[i]
    gen_neu_phi_arr[0]    = step8_gen_neu_phi[i]
    gen_neu_pdgid_arr[0] = step8_gen_neu_pdgid[i]

    gen_aneu_pt_arr[0]     = step8_gen_aneu_pt[i]
    gen_aneu_eta_arr[0]    = step8_gen_aneu_eta[i]
    gen_aneu_phi_arr[0]    = step8_gen_aneu_phi[i]
    gen_aneu_pdgid_arr[0] = step8_gen_aneu_pdgid[i]

    gen_met_pt_arr[0]     = step8_gen_met_pt[i]
    gen_met_phi_arr[0]    = step8_gen_met_phi[i]

    weight_size_arr[0]  = len(step8_weight_sel[i])

    for k in range(weight_size_arr[0]):
        weight_arr[k] = step8_weight_sel[i][k]

    tree.Fill()

# Write the tree into the output file and close the file
opfile.Write()
opfile.Close()
