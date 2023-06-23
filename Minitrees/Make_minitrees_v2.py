import ROOT
import uproot
import argparse
import numpy as np
from   array import array
import awkward as ak
import matplotlib.pyplot as plt

def deltaphi(e_phi, m_phi):
    d_phi = e_phi - m_phi
    if (d_phi > np.pi):
        d_phi -= 2*np.pi
    if (d_phi < -np.pi):
        d_phi += 2*np.pi
    return d_phi

def dR(e_phi, e_eta, m_phi, m_eta):
    d_eta = abs(e_eta - m_eta)
    d_phi = deltaphi(e_phi, m_phi)
    return np.sqrt(d_phi**2 + d_eta**2)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input  Delphes Ntuple location')
    parser.add_argument('-o', '--output', help='Output Delphes Minitree location')

    args = parser.parse_args()
    inputFile = args.input
    outputFile = args.output

    fileptr = uproot.open(inputFile)['Delphes_Ntuples']
    
    # Jet MET
    jet_pt   = fileptr['jet_pt'].array()
    jet_eta  = fileptr['jet_eta'].array()
    jet_phi  = fileptr['jet_phi'].array()
    jet_mass = fileptr['jet_mass'].array()
    jet_btag = fileptr['jet_btag'].array()
    
    NEvents = len(jet_pt)
    #NEvents = 100

    met_pt    = fileptr['met_pt'].array()
    met_phi   = fileptr['met_phi'].array()
    weight    = fileptr['weight'].array()
    scalar_ht = fileptr['scalar_ht'].array()

    # Electrons
    elec_pt     = fileptr['elec_pt'].array()
    elec_eta    = fileptr['elec_eta'].array()
    elec_phi    = fileptr['elec_phi'].array()
    elec_mass   = fileptr['elec_mass'].array()
    elec_charge = fileptr['elec_charge'].array()
    elec_reliso = fileptr['elec_reliso'].array()

    # Muons
    muon_pt     = fileptr['muon_pt'].array()
    muon_eta    = fileptr['muon_eta'].array()
    muon_phi    = fileptr['muon_phi'].array()
    muon_mass   = fileptr['muon_mass'].array()
    muon_charge = fileptr['muon_charge'].array()
    muon_reliso = fileptr['muon_reliso'].array()

    # Gen level jets
    genjet_pt   = fileptr['genjet_pt'].array()
    genjet_eta  = fileptr['genjet_eta'].array()
    genjet_phi  = fileptr['genjet_phi'].array()
    genjet_mass = fileptr['genjet_mass'].array()
    #genjet_btag = fileptr['genjet_btag'].array()

    # Gen level data
    genpart_pt     = fileptr['genpart_pt'].array()
    genpart_eta    = fileptr['genpart_eta'].array()
    genpart_phi    = fileptr['genpart_phi'].array()
    genpart_mass   = fileptr['genpart_mass'].array()
    genpart_pid    = fileptr['genpart_pid'].array()
    genpart_status = fileptr['genpart_status'].array()
    genpart_charge = fileptr['genpart_charge'].array()

    # These empty arrays are the branch arrays for the output file
 
    # RECO

    selection_step = np.zeros(NEvents)
    
    lep_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    lep_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    lep_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    lep_mass    = np.array(np.full((1,NEvents), np.nan)).flatten()
    lep_pdgid = np.array(np.full((1,NEvents), np.nan)).flatten()

    alep_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    alep_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    alep_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    alep_mass    = np.array(np.full((1,NEvents), np.nan)).flatten()
    alep_pdgid = np.array(np.full((1,NEvents), np.nan)).flatten()

    lep_nearest_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    lep_nearest_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    lep_nearest_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    lep_nearest_mass    = np.array(np.full((1,NEvents), np.nan)).flatten()
    lep_nearest_pdgid = np.array(np.full((1,NEvents), np.nan)).flatten()

    alep_nearest_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    alep_nearest_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    alep_nearest_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    alep_nearest_mass    = np.array(np.full((1,NEvents), np.nan)).flatten()
    alep_nearest_pdgid = np.array(np.full((1,NEvents), np.nan)).flatten()

    # By leading and subleading Pt
    l_pt   = np.array(np.full((1,NEvents), np.nan)).flatten()
    l_eta  = np.array(np.full((1,NEvents), np.nan)).flatten()
    l_phi  = np.array(np.full((1,NEvents), np.nan)).flatten()
    l_mass = np.array(np.full((1,NEvents), np.nan)).flatten()

    sl_pt   = np.array(np.full((1,NEvents), np.nan)).flatten()
    sl_eta  = np.array(np.full((1,NEvents), np.nan)).flatten()
    sl_phi  = np.array(np.full((1,NEvents), np.nan)).flatten()
    sl_mass = np.array(np.full((1,NEvents), np.nan)).flatten()

    # By Lepton flavor
    e_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    e_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    e_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    e_charge = np.array(np.full((1,NEvents), np.nan)).flatten()

    mu_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    mu_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    mu_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    mu_charge = np.array(np.full((1,NEvents), np.nan)).flatten()

    ljet_pt   = np.array(np.full((1,NEvents), np.nan)).flatten()
    ljet_eta  = np.array(np.full((1,NEvents), np.nan)).flatten()
    ljet_phi  = np.array(np.full((1,NEvents), np.nan)).flatten()
    ljet_mass = np.array(np.full((1,NEvents), np.nan)).flatten()

    sljet_pt   = np.array(np.full((1,NEvents), np.nan)).flatten()
    sljet_eta  = np.array(np.full((1,NEvents), np.nan)).flatten()
    sljet_phi  = np.array(np.full((1,NEvents), np.nan)).flatten()
    sljet_mass = np.array(np.full((1,NEvents), np.nan)).flatten()

    bjet_nearest_pt   = np.array(np.full((1,NEvents), np.nan)).flatten()
    bjet_nearest_eta  = np.array(np.full((1,NEvents), np.nan)).flatten()
    bjet_nearest_phi  = np.array(np.full((1,NEvents), np.nan)).flatten()
    bjet_nearest_mass = np.array(np.full((1,NEvents), np.nan)).flatten()

    abjet_nearest_pt   = np.array(np.full((1,NEvents), np.nan)).flatten()
    abjet_nearest_eta  = np.array(np.full((1,NEvents), np.nan)).flatten()
    abjet_nearest_phi  = np.array(np.full((1,NEvents), np.nan)).flatten()
    abjet_nearest_mass = np.array(np.full((1,NEvents), np.nan)).flatten()

    ST = np.array(np.full((1,NEvents), np.nan)).flatten()
    HT = np.array(np.full((1,NEvents), np.nan)).flatten()
    HT_check = np.array(np.full((1,NEvents), np.nan)).flatten()
    ET_miss  = np.array(np.full((1,NEvents), np.nan)).flatten()
    MET_phi  = np.array(np.full((1,NEvents), np.nan)).flatten()

    # GEN

    gen_top_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_top_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_top_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_top_mass    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_top_status = np.array(np.full((1,NEvents), np.nan)).flatten()

    gen_atop_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_atop_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_atop_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_atop_mass    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_atop_status = np.array(np.full((1,NEvents), np.nan)).flatten()

    gen_b_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_b_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_b_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_b_mass    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_b_status = np.array(np.full((1,NEvents), np.nan)).flatten()

    gen_ab_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_ab_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_ab_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_ab_mass    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_ab_status = np.array(np.full((1,NEvents), np.nan)).flatten()

    gen_lep_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_lep_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_lep_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_lep_mass    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_lep_pdgid = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_lep_status = np.array(np.full((1,NEvents), np.nan)).flatten()

    gen_alep_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_alep_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_alep_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_alep_mass    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_alep_pdgid = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_alep_status = np.array(np.full((1,NEvents), np.nan)).flatten()

    gen_lep_nearest_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_lep_nearest_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_lep_nearest_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_lep_nearest_mass    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_lep_nearest_pdgid = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_lep_nearest_status = np.array(np.full((1,NEvents), np.nan)).flatten()

    gen_alep_nearest_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_alep_nearest_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_alep_nearest_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_alep_nearest_mass    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_alep_nearest_pdgid = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_alep_nearest_status = np.array(np.full((1,NEvents), np.nan)).flatten()

    gen_neu_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_neu_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_neu_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_neu_pdgid = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_neu_status = np.array(np.full((1,NEvents), np.nan)).flatten()

    gen_aneu_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_aneu_eta    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_aneu_phi    = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_aneu_pdgid = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_aneu_status = np.array(np.full((1,NEvents), np.nan)).flatten()

    gen_met_pt     = np.array(np.full((1,NEvents), np.nan)).flatten()
    gen_met_phi     = np.array(np.full((1,NEvents), np.nan)).flatten()
    
    # for MET reconstruction
    
    # Let's create a mask
    selection = np.zeros(NEvents) 

    # Loop over the events
    for i in range(NEvents):

        if (i % 1000 == 0):
            print('Processing event ' + str(i) + ' of ' + str(NEvents))

        # Temporary variables

        e_idx  = []
        mu_idx = []

        ef_idx  = []
        muf_idx = []

        jet_idx = []

        btag_cnt = 0

        e_4vec  = ROOT.TLorentzVector()
        mu_4vec = ROOT.TLorentzVector()

        gen_lep_4vec  = ROOT.TLorentzVector()
        gen_alep_4vec = ROOT.TLorentzVector()

        gen_neu_4vec  = ROOT.TLorentzVector()
        gen_aneu_4vec = ROOT.TLorentzVector()

        ###########  GEN  ###########

        selection_step[i] = 0
        
        gen_top_index = -1
        gen_atop_index = -1
        gen_b_index = -1
        gen_ab_index = -1
        gen_lep_index = -1
        gen_alep_index = -1

        for j in range(len(genpart_pid[i]) - 1) :

            # Look for the first gen lepton, neutrino pairs on the list 

            if( ( (genpart_pid[i][j] == 11 and genpart_pid[i][j+1] == -12) or (genpart_pid[i][j] == 13 and genpart_pid[i][j+1] == -14) or (genpart_pid[i][j] == 15 and genpart_pid[i][j+1] == -16) ) and gen_lep_index == -1 ):

                gen_lep_4vec.SetPtEtaPhiM(genpart_pt[i][j] , genpart_eta[i][j] , genpart_phi[i][j] , genpart_mass[i][j])
                gen_aneu_4vec.SetPtEtaPhiM(genpart_pt[i][j+1] , genpart_eta[i][j+1] , genpart_phi[i][j+1] , 0)

                if( (gen_lep_4vec + gen_aneu_4vec).M() < 70.4 or (gen_lep_4vec + gen_aneu_4vec).M() > 90.4  ): continue

                gen_lep_index = j # a flag to check for lepton 

            if( ( (genpart_pid[i][j] == -11 and genpart_pid[i][j+1] == 12) or (genpart_pid[i][j] == -13 and genpart_pid[i][j+1] == 14) or (genpart_pid[i][j] == -15 and genpart_pid[i][j+1] == 16) ) and gen_alep_index == -1 ):

                gen_alep_4vec.SetPtEtaPhiM(genpart_pt[i][j] , genpart_eta[i][j] , genpart_phi[i][j] , genpart_mass[i][j])
                gen_neu_4vec.SetPtEtaPhiM(genpart_pt[i][j+1] , genpart_eta[i][j+1] , genpart_phi[i][j+1] , 0)

                if ( (gen_alep_4vec + gen_neu_4vec).M() < 70.4 or (gen_alep_4vec + gen_neu_4vec).M() > 90.4  ): continue

                gen_alep_index = j # a flag for anti-leptons 

            # gen top quarks with status 62

            if ( genpart_pid[i][j] == 6 and genpart_status[i][j] == 62):

                gen_top_index = j

            if ( genpart_pid[i][j] == -6 and genpart_status[i][j] == 62):

                gen_atop_index = j
                
            # gen b quarks with status 23

            if ( genpart_pid[i][j] == 5 and genpart_status[i][j] == 23):

                gen_b_index = j

            if ( genpart_pid[i][j] == -5 and genpart_status[i][j] == 23):

                gen_ab_index = j


        if ( gen_lep_index == -1 or gen_alep_index == -1):
            
            continue # ensures that there's at least one dilepton pair 

        ####### Fill the GEN arrays ##########

        gen_lep_pt[i]=genpart_pt[i][gen_lep_index]
        gen_lep_eta[i]=genpart_eta[i][gen_lep_index]
        gen_lep_phi[i]=genpart_phi[i][gen_lep_index]
        gen_lep_mass[i]=genpart_mass[i][gen_lep_index]
        gen_lep_pdgid[i]=genpart_pid[i][gen_lep_index]
        gen_lep_status[i]=genpart_status[i][gen_lep_index]
        
        gen_aneu_pt[i]=genpart_pt[i][gen_lep_index+1]
        gen_aneu_eta[i]=genpart_eta[i][gen_lep_index+1]
        gen_aneu_phi[i]=genpart_phi[i][gen_lep_index+1]
        gen_aneu_pdgid[i]=genpart_pid[i][gen_lep_index+1]
        gen_aneu_status[i]=genpart_status[i][gen_lep_index+1]

        gen_alep_pt[i]=genpart_pt[i][gen_alep_index]
        gen_alep_eta[i]=genpart_eta[i][gen_alep_index]
        gen_alep_phi[i]=genpart_phi[i][gen_alep_index]
        gen_alep_mass[i]=genpart_mass[i][gen_alep_index]
        gen_alep_pdgid[i]=genpart_pid[i][gen_alep_index]
        gen_alep_status[i]=genpart_status[i][gen_alep_index]
        
        gen_neu_pt[i]=genpart_pt[i][gen_alep_index+1]
        gen_neu_eta[i]=genpart_eta[i][gen_alep_index+1]
        gen_neu_phi[i]=genpart_phi[i][gen_alep_index+1]
        gen_neu_pdgid[i]=genpart_pid[i][gen_alep_index+1]
        gen_neu_status[i]=genpart_status[i][gen_alep_index+1]

        gen_top_pt[i]=genpart_pt[i][gen_top_index]
        gen_top_eta[i]=genpart_eta[i][gen_top_index]
        gen_top_phi[i]=genpart_phi[i][gen_top_index]
        gen_top_mass[i]=genpart_mass[i][gen_top_index]
        gen_top_status[i]=genpart_status[i][gen_top_index]
                
        gen_atop_pt[i]=genpart_pt[i][gen_atop_index]
        gen_atop_eta[i]=genpart_eta[i][gen_atop_index]
        gen_atop_phi[i]=genpart_phi[i][gen_atop_index]
        gen_atop_mass[i]=genpart_mass[i][gen_atop_index]
        gen_atop_status[i]=genpart_status[i][gen_atop_index]

        gen_b_pt[i]=genpart_pt[i][gen_b_index]
        gen_b_eta[i]=genpart_eta[i][gen_b_index]
        gen_b_phi[i]=genpart_phi[i][gen_b_index]
        gen_b_mass[i]=genpart_mass[i][gen_b_index]
        gen_b_status[i]=genpart_status[i][gen_b_index]
                
        gen_ab_pt[i]=genpart_pt[i][gen_ab_index]
        gen_ab_eta[i]=genpart_eta[i][gen_ab_index]
        gen_ab_phi[i]=genpart_phi[i][gen_ab_index]
        gen_ab_mass[i]=genpart_mass[i][gen_ab_index]
        gen_ab_status[i]=genpart_status[i][gen_ab_index]

        # Calculate gen met from gen neutrino and anti-neutrino

        gen_met_pt[i]=(gen_neu_4vec + gen_aneu_4vec).Pt()
        gen_met_phi[i]=(gen_neu_4vec + gen_aneu_4vec).Phi()   
    
    ###########  RECO  ###########
        
        ########## Electrons ##########

        # Ensure pt > 20 GeV and eta < 5.0 and isolation
        for j in range(len(elec_pt[i])):
            if (elec_pt[i][j] < 20):
                continue

            if ( abs(elec_eta[i][j]) > 5.0 ):
                continue

            #if (elec_reliso[i][j] > 0.0588):
            #    continue

            e_idx.append(j)

        ###########  Muons ############

        # Ensure pt > 20 GeV and eta < 5.0 and isolation
        for j in range(len(muon_pt[i])):
            if (muon_pt[i][j] < 20):
                continue

            if (abs(muon_eta[i][j]) > 5.0):       # Should be 4?
                continue

            #if (muon_reliso[i][j] > 0.15):
            #    continue

            mu_idx.append(j)

        # Ensure exactly one muon and one electron
        if (len(e_idx) != 1 or len(mu_idx) != 1):
           
            continue 

        # Check for opp sign charge pairings
        for j in range(len(e_idx)):
            for k in range(len(mu_idx)):
                # e_idx and mu_idx have the list of valid electron and muon indices
                tmp_e_idx  = e_idx[j]
                tmp_mu_idx = mu_idx[k]

                if (elec_charge[i][tmp_e_idx] * muon_charge[i][tmp_mu_idx] == -1):
                    ef_idx.append(tmp_e_idx)
                    muf_idx.append(tmp_mu_idx)

        # Ensure such a pairing exists
        if (len(ef_idx) == 0 or len(muf_idx) == 0):         
            continue

        # Assign leading indices to e and mu
        e_index = ef_idx[0]
        mu_index = muf_idx[0]

        # Defining the 4 vectors
        e_4vec.SetPtEtaPhiM(elec_pt[i][e_index]  , elec_eta[i][e_index] , elec_phi[i][e_index] , elec_mass[i][e_index])
        mu_4vec.SetPtEtaPhiM(muon_pt[i][mu_index], muon_eta[i][mu_index], muon_phi[i][mu_index],  muon_mass[i][mu_index])

        # Mll cut (Step 3 according to the FW)
        if ((e_4vec + mu_4vec).M() < 20):            
            continue

        ###########  Jets ###############

        for j in range(len(jet_pt[i])):

            # Ensure pt > 30 GeV and eta < 5.0 isolation

            if ((dR(elec_phi[i][e_index],  elec_eta[i][e_index], jet_phi[i][j], jet_eta[i][j]) < 0.4)
            or (dR(muon_phi[i][mu_index], muon_eta[i][mu_index], jet_phi[i][j], jet_eta[i][j]) < 0.4)):
                continue

            if ((jet_pt[i][j] < 40)): ##Increase from 30 to 40
                continue

            if ((abs(jet_eta[i][j]) > 5.0)):
                continue

            if (jet_btag[i][j] != 0):
                btag_cnt += 1

            jet_idx.append(j)

        # 2 Jets (Step 5 according to the FW)
        if(len(jet_idx) < 2):
            continue

        # Atleast one b-tag (Step 6 according to the FW)
        if (btag_cnt == 0):
            continue  
            
        ljet_idx = jet_idx[0]
        sljet_idx = jet_idx[1]

        # Search for gen leptons that are closer to the reco lepton than the method used above

        gen_lep_nearest_index = gen_lep_index
        gen_alep_nearest_index = gen_alep_index

        # Initialize the dR with the gen lepton above, if it exits, else np.nan

        if ((elec_charge[i][e_index] < 0 and muon_charge[i][mu_index] > 0) and gen_lep_index > -1):

            gen_lep_dR = dR(elec_phi[i][e_index],  elec_eta[i][e_index], genpart_phi[i][gen_lep_index], genpart_eta[i][gen_lep_index])

        elif ((elec_charge[i][e_index] > 0 and muon_charge[i][mu_index] < 0) and gen_lep_index > -1):

            gen_lep_dR = dR(muon_phi[i][mu_index], muon_eta[i][mu_index], genpart_phi[i][gen_lep_index], genpart_eta[i][gen_lep_index])

        else: gen_lep_dR = np.nan

        if ((elec_charge[i][e_index] < 0 and muon_charge[i][mu_index] > 0) and gen_alep_index > -1):

            agen_lep_dR = dR(muon_phi[i][mu_index], muon_eta[i][mu_index], genpart_phi[i][gen_alep_index], genpart_eta[i][gen_alep_index])

        elif ((elec_charge[i][e_index] > 0 and muon_charge[i][mu_index] < 0) and gen_alep_index > -1):

            agen_lep_dR = dR(elec_phi[i][e_index],  elec_eta[i][e_index], genpart_phi[i][gen_alep_index], genpart_eta[i][gen_alep_index])

        else: agen_lep_dR = np.nan
        
        # begin search for a closer gen lepton

        for j in range(len(genpart_pid[i])):

            if (elec_charge[i][e_index] < 0 and muon_charge[i][mu_index] > 0):

                if (genpart_pid[i][j] == 11):

                    if (dR(elec_phi[i][e_index],  elec_eta[i][e_index], genpart_phi[i][j], genpart_eta[i][j]) < gen_lep_dR):

                        gen_lep_dR = dR(elec_phi[i][e_index],  elec_eta[i][e_index], genpart_phi[i][j], genpart_eta[i][j])
                        gen_lep_nearest_index = j

                elif (genpart_pid[i][j] == -13):

                    if (dR(muon_phi[i][mu_index], muon_eta[i][mu_index], genpart_phi[i][j], genpart_eta[i][j]) < agen_lep_dR):

                        agen_lep_dR = dR(muon_phi[i][mu_index], muon_eta[i][mu_index], genpart_phi[i][j], genpart_eta[i][j])
                        gen_alep_nearest_index = j

            elif (elec_charge[i][e_index] > 0 and muon_charge[i][mu_index] < 0):

                if (genpart_pid[i][j] == -11):

                    if (dR(elec_phi[i][e_index],  elec_eta[i][e_index], genpart_phi[i][j], genpart_eta[i][j]) < gen_lep_dR):

                        agen_lep_dR = dR(elec_phi[i][e_index],  elec_eta[i][e_index], genpart_phi[i][j], genpart_eta[i][j])
                        gen_alep_nearest_index = j

                elif (genpart_pid[i][j] == 13):

                    if (dR(muon_phi[i][mu_index], muon_eta[i][mu_index], genpart_phi[i][j], genpart_eta[i][j]) < agen_lep_dR):

                        gen_lep_dR = dR(muon_phi[i][mu_index], muon_eta[i][mu_index], genpart_phi[i][j], genpart_eta[i][j])
                        gen_lep_nearest_index = j

        # append arrays with nearest lepton, if found, else fill with np.nan

        gen_lep_nearest_pt[i] = genpart_pt[i][gen_lep_nearest_index]
        gen_lep_nearest_eta[i] = genpart_eta[i][gen_lep_nearest_index]
        gen_lep_nearest_phi[i] = genpart_phi[i][gen_lep_nearest_index]
        gen_lep_nearest_mass[i] = genpart_mass[i][gen_lep_nearest_index]
        gen_lep_nearest_pdgid[i] = genpart_pid[i][gen_lep_nearest_index]
        gen_lep_nearest_status[i] = genpart_status[i][gen_lep_nearest_index]

        gen_alep_nearest_pt[i] = genpart_pt[i][gen_alep_nearest_index]
        gen_alep_nearest_eta[i] = genpart_eta[i][gen_alep_nearest_index]
        gen_alep_nearest_phi[i] = genpart_phi[i][gen_alep_nearest_index]
        gen_alep_nearest_mass[i] = genpart_mass[i][gen_alep_nearest_index]
        gen_alep_nearest_pdgid[i] = genpart_pid[i][gen_alep_nearest_index]
        gen_alep_nearest_status[i] = genpart_status[i][gen_alep_nearest_index]

        ####### Fill the RECO arrays ##########

        # Find the nearest reco jets to the gen b quarks

        bjet_nearest_index = -1
        abjet_nearest_index = -1

        bjet_dR = 9999
        abjet_dR = 9999

        for idx in jet_idx:

            if (dR(genpart_phi[i][gen_b_index], genpart_eta[i][gen_b_index], jet_phi[i][idx], jet_eta[i][idx]) < bjet_dR):

                 bjet_dR = dR(genpart_phi[i][gen_b_index], genpart_eta[i][gen_b_index], jet_phi[i][idx], jet_eta[i][idx])
                 bjet_nearest_index = idx

            if (dR(genpart_phi[i][gen_ab_index], genpart_eta[i][gen_ab_index], jet_phi[i][idx], jet_eta[i][idx]) < abjet_dR):

                 abjet_dR = dR(genpart_phi[i][gen_ab_index], genpart_eta[i][gen_ab_index], jet_phi[i][idx], jet_eta[i][idx])
                 abjet_nearest_index = idx

        bjet_nearest_pt[i] = jet_pt[i][bjet_nearest_index]
        bjet_nearest_phi[i] = jet_phi[i][bjet_nearest_index]
        bjet_nearest_eta[i] = jet_eta[i][bjet_nearest_index]
        bjet_nearest_mass[i] = jet_mass[i][bjet_nearest_index]
        
        abjet_nearest_pt[i] = jet_pt[i][abjet_nearest_index]
        abjet_nearest_phi[i] = jet_phi[i][abjet_nearest_index]
        abjet_nearest_eta[i] = jet_eta[i][abjet_nearest_index]
        abjet_nearest_mass[i] = jet_mass[i][abjet_nearest_index]

             
        # Find the nearest reco leptons to the gen leptons

        lep_nearest_index = -1
        alep_nearest_index = -1

        lep_nearest_pdgid_tmp = 0
        alep_nearest_pdgid_tmp = 0

        lep_dR = 9999
        alep_dR = 9999

        for idx in e_idx:

            if (genpart_pid[i][gen_lep_index] * elec_charge[i][idx] < 0 and dR(genpart_phi[i][gen_lep_index], genpart_eta[i][gen_lep_index], elec_phi[i][idx], elec_eta[i][idx]) < lep_dR):

                 lep_dR = dR(genpart_phi[i][gen_lep_index], genpart_eta[i][gen_lep_index], elec_phi[i][idx], elec_eta[i][idx])
                 lep_nearest_index = idx
                 lep_nearest_pdgid_tmp = -11*elec_charge[i][idx]

            if (genpart_pid[i][gen_alep_index] * elec_charge[i][idx] < 0 and dR(genpart_phi[i][gen_alep_index], genpart_eta[i][gen_alep_index], elec_phi[i][idx], elec_eta[i][idx]) < alep_dR):

                 alep_dR = dR(genpart_phi[i][gen_alep_index], genpart_eta[i][gen_alep_index], elec_phi[i][idx], elec_eta[i][idx])
                 alep_nearest_index = idx
                 alep_nearest_pdgid_tmp = -11*elec_charge[i][idx]

        for idx in mu_idx:

            if (genpart_pid[i][gen_lep_index] * muon_charge[i][idx] < 0 and dR(genpart_phi[i][gen_lep_index], genpart_eta[i][gen_lep_index], muon_phi[i][idx], muon_eta[i][idx]) < lep_dR):

                 lep_dR = dR(genpart_phi[i][gen_lep_index], genpart_eta[i][gen_lep_index], muon_phi[i][idx], muon_eta[i][idx])
                 lep_nearest_index = idx
                 lep_nearest_pdgid_tmp = -13*muon_charge[i][idx]

            if (genpart_pid[i][gen_alep_index] * muon_charge[i][idx] < 0 and dR(genpart_phi[i][gen_alep_index], genpart_eta[i][gen_alep_index], muon_phi[i][idx], muon_eta[i][idx]) < alep_dR):

                 alep_dR = dR(genpart_phi[i][gen_alep_index], genpart_eta[i][gen_alep_index], muon_phi[i][idx], muon_eta[i][idx])
                 alep_nearest_index = idx
                 alep_nearest_pdgid_tmp = -13*muon_charge[i][idx]
             
        if ( lep_nearest_pdgid_tmp == 11 ):

            lep_nearest_pt[i] = elec_pt[i][lep_nearest_index]
            lep_nearest_phi[i] = elec_phi[i][lep_nearest_index]
            lep_nearest_eta[i] = elec_eta[i][lep_nearest_index]
            lep_nearest_mass[i] = elec_mass[i][lep_nearest_index]
            lep_nearest_pdgid[i] = 11

        elif ( lep_nearest_pdgid_tmp == 13 ):

            lep_nearest_pt[i] = muon_pt[i][lep_nearest_index]
            lep_nearest_phi[i] = muon_phi[i][lep_nearest_index]
            lep_nearest_eta[i] = muon_eta[i][lep_nearest_index]
            lep_nearest_mass[i] = muon_mass[i][lep_nearest_index]
            lep_nearest_pdgid[i] = 13

        if ( alep_nearest_pdgid_tmp == -11 ):

            alep_nearest_pt[i] = elec_pt[i][alep_nearest_index]
            alep_nearest_phi[i] = elec_phi[i][alep_nearest_index]
            alep_nearest_eta[i] = elec_eta[i][alep_nearest_index]
            alep_nearest_mass[i] = elec_mass[i][alep_nearest_index]
            alep_nearest_pdgid[i] = -11

        elif ( alep_nearest_pdgid_tmp == -13 ):

            alep_nearest_pt[i] = muon_pt[i][alep_nearest_index]
            alep_nearest_phi[i] = muon_phi[i][alep_nearest_index]
            alep_nearest_eta[i] = muon_eta[i][alep_nearest_index]
            alep_nearest_mass[i] = muon_mass[i][alep_nearest_index]
            alep_nearest_pdgid[i] = -13


        # Leading and sub-leading lepton pts
        if (elec_pt[i][e_index] > muon_pt[i][mu_index] and elec_pt[i][e_index] > 25):
            l_pt[i] = elec_pt[i][e_index]
            l_phi[i] = elec_phi[i][e_index]
            l_eta[i] = elec_eta[i][e_index]
            l_mass[i] = elec_mass[i][e_index]

            sl_pt[i] = muon_pt[i][mu_index]
            sl_phi[i] = muon_phi[i][mu_index]
            sl_eta[i] = muon_eta[i][mu_index]
            sl_mass[i] = muon_mass[i][mu_index]

        elif (muon_pt[i][mu_index] > elec_pt[i][e_index] and muon_pt[i][mu_index] > 25):
            sl_pt[i] = elec_pt[i][e_index]
            sl_phi[i] = elec_phi[i][e_index]
            sl_eta[i] = elec_eta[i][e_index]
            sl_mass[i] = elec_mass[i][e_index]

            l_pt[i] = muon_pt[i][mu_index]
            l_phi[i] = muon_phi[i][mu_index]
            l_eta[i] = muon_eta[i][mu_index]
            l_mass[i] = muon_mass[i][mu_index]       

        # By flavor
        e_pt[i] = elec_pt[i][e_index]
        e_eta[i] = elec_eta[i][e_index]
        e_phi[i] = elec_phi[i][e_index]
        e_charge[i] = elec_charge[i][e_index]
        
        mu_pt[i] = muon_pt[i][mu_index]
        mu_eta[i] = muon_eta[i][mu_index]
        mu_phi[i] = muon_phi[i][mu_index]
        mu_charge[i] = muon_charge[i][mu_index]

        if (elec_charge[i][e_index] < 0 and muon_charge[i][mu_index] > 0):

            lep_pt[i] = elec_pt[i][e_index]
            lep_eta[i] = elec_eta[i][e_index]
            lep_phi[i] = elec_phi[i][e_index]
            lep_mass[i] = elec_mass[i][e_index]
            lep_pdgid[i] = 11
            
            alep_pt[i] = muon_pt[i][mu_index]
            alep_eta[i] = muon_eta[i][mu_index]
            alep_phi[i] = muon_phi[i][mu_index]
            alep_mass[i] = muon_mass[i][mu_index]
            alep_pdgid[i] = -13

        elif (elec_charge[i][e_index] > 0 and muon_charge[i][mu_index] < 0):

            alep_pt[i] = elec_pt[i][e_index]
            alep_eta[i] = elec_eta[i][e_index]
            alep_phi[i] = elec_phi[i][e_index]
            alep_mass[i] = elec_mass[i][e_index]
            alep_pdgid[i] = -11
            
            lep_pt[i] = muon_pt[i][mu_index]
            lep_eta[i] = muon_eta[i][mu_index]
            lep_phi[i] = muon_phi[i][mu_index]
            lep_mass[i] = muon_mass[i][mu_index]
            lep_pdgid[i] = 13
            
        #print("Check lep_pt at iteration:", i, lep_pt[i])
        
        # Leading and Subleading Pt
        ljet_pt[i] = jet_pt[i][ljet_idx]
        ljet_phi[i] = jet_phi[i][ljet_idx]
        ljet_eta[i] = jet_eta[i][ljet_idx]
        ljet_mass[i] = jet_mass[i][ljet_idx]
        
        sljet_pt[i] = jet_pt[i][sljet_idx]
        sljet_phi[i] = jet_phi[i][sljet_idx]
        sljet_eta[i] = jet_eta[i][sljet_idx]
        sljet_mass[i] = jet_mass[i][sljet_idx]
        
        ET_miss[i] = met_pt[i][0]
        MET_phi[i] = met_phi[i][0]

        # HT and ST
        # temporary variables
        Ht = 0
        St = 0

        for j in range(len(jet_pt[i])):
            Ht += jet_pt[i][j]
            St += jet_pt[i][j]

        for j in range(len(elec_pt[i])):
            St += elec_pt[i][j]

        for j in range(len(muon_pt[i])):
            St += muon_pt[i][j]

        St += met_pt[i][0]

        # Append to lists
        HT[i] = Ht
        ST[i] = St
        HT_check[i] = scalar_ht[i][0]

        # Create a mask for selection
        selection[i] = 1   
        selection_step[i] = 7
        
    # Other variables that we need
    llbar_deta = abs(np.array(l_eta) - np.array(sl_eta))
    llbar_dphi = abs(abs(abs(np.array(l_phi) - np.array(sl_phi)) - np.pi) - np.pi)

    bbbar_deta = abs(np.array(ljet_eta) - np.array(sljet_eta))
    bbbar_dphi = abs(abs(abs(np.array(ljet_phi) - np.array(sljet_phi)) - np.pi) - np.pi)

    # Store all info for additional jets and gen particles

    weight_sel = weight[selection == 1]

    jet_pt_sel   = jet_pt[selection == 1]
    jet_eta_sel  = jet_eta[selection == 1]
    jet_phi_sel  = jet_phi[selection == 1]
    jet_mass_sel = jet_mass[selection == 1]
    jet_btag_sel = jet_btag[selection == 1]    

    #print(len(HT)) 
    print(lep_pt) 
    #print('len lep_pt', len(lep_pt))
    #print('elec_pt', elec_pt)
    print('jet_pt_sel', jet_pt_sel)
    #print('len jet_pt_sel', len(jet_pt_sel))
    
    gen_pt_sel     = genpart_pt[selection == 1]
    gen_pid_sel    = genpart_pid[selection == 1]
    gen_eta_sel    = genpart_eta[selection == 1]
    gen_phi_sel    = genpart_phi[selection == 1]
    gen_mass_sel   = genpart_mass[selection == 1]
    gen_status_sel = genpart_status[selection == 1]
    #gen_charge_sel = genpart_charge[selection == 1]

    #genjet_pt_sel   = genjet_pt[selection == 1]
    #genjet_eta_sel  = genjet_eta[selection == 1]
    #genjet_phi_sel  = genjet_phi[selection == 1]
    #genjet_mass_sel = genjet_mass[selection == 1]
    #genjet_btag_sel = genjet_btag[selection == 1]
   
    # Request arrays for branches
    maxn    = 9999

    selection_step_arr = array('f', [0.])
    
    HT_arr  = array('f', [0.])
    ST_arr  = array('f', [0.])
    MET_arr = array('f', [0.])
    MET_phi_arr  = array('f', [0.])
    HT_check_arr = array('f', [0.])

    l_pt_arr   = array('f', [0.])
    l_eta_arr  = array('f', [0.])
    l_phi_arr  = array('f', [0.])
    l_mass_arr = array('f', [0.])

    sl_pt_arr   = array('f', [0.])
    sl_eta_arr  = array('f', [0.])
    sl_phi_arr  = array('f', [0.])
    sl_mass_arr = array('f', [0.])

    # By flavor
    e_pt_arr      = array('f', [0.])
    e_eta_arr     = array('f', [0.])
    e_phi_arr     = array('f', [0.])
    e_charge_arr  = array('f', [0.])

    mu_pt_arr     = array('f', [0.])
    mu_eta_arr    = array('f', [0.])
    mu_phi_arr    = array('f', [0.])
    mu_charge_arr = array('f', [0.])

    lep_pt_arr      = array('f', [0.])
    lep_eta_arr     = array('f', [0.])
    lep_phi_arr     = array('f', [0.])
    lep_mass_arr     = array('f', [0.])
    lep_pdgid_arr  = array('f', [0.])

    alep_pt_arr     = array('f', [0.])
    alep_eta_arr    = array('f', [0.])
    alep_phi_arr    = array('f', [0.])
    alep_mass_arr    = array('f', [0.])
    alep_pdgid_arr = array('f', [0.])

    lep_nearest_pt_arr      = array('f', [0.])
    lep_nearest_eta_arr     = array('f', [0.])
    lep_nearest_phi_arr     = array('f', [0.])
    lep_nearest_mass_arr     = array('f', [0.])
    lep_nearest_pdgid_arr  = array('f', [0.])

    alep_nearest_pt_arr     = array('f', [0.])
    alep_nearest_eta_arr    = array('f', [0.])
    alep_nearest_phi_arr    = array('f', [0.])
    alep_nearest_mass_arr    = array('f', [0.])
    alep_nearest_pdgid_arr = array('f', [0.])

    ljet_pt_arr   = array('f', [0.])
    ljet_eta_arr  = array('f', [0.])
    ljet_phi_arr  = array('f', [0.])
    ljet_mass_arr = array('f', [0.])

    sljet_pt_arr   = array('f', [0.])
    sljet_eta_arr  = array('f', [0.])
    sljet_phi_arr  = array('f', [0.])
    sljet_mass_arr = array('f', [0.])

    bjet_nearest_pt_arr   = array('f', [0.])
    bjet_nearest_eta_arr  = array('f', [0.])
    bjet_nearest_phi_arr  = array('f', [0.])
    bjet_nearest_mass_arr = array('f', [0.])

    abjet_nearest_pt_arr   = array('f', [0.])
    abjet_nearest_eta_arr  = array('f', [0.])
    abjet_nearest_phi_arr  = array('f', [0.])
    abjet_nearest_mass_arr = array('f', [0.])

    llbar_deta_arr = array('f', [0.])
    llbar_dphi_arr = array('f', [0.])
    bbbar_deta_arr = array('f', [0.])
    bbbar_dphi_arr = array('f', [0.])

    weight_size_arr = array('i', [0])
    weight_arr      = array('f', maxn*[0.])

    jet_size_arr = array('i', [0])

    jet_pt_arr   = array('f', maxn*[0.])
    jet_eta_arr  = array('f', maxn*[0.])
    jet_phi_arr  = array('f', maxn*[0.])
    jet_mass_arr = array('f', maxn*[0.])
    jet_btag_arr = array('i', maxn*[0])
    
    #step0_file = 'preminitree_test.root'
    opfile = ROOT.TFile(outputFile, 'recreate')
    Step0tree = ROOT.TTree("Step0", "Step0")
    #Step0_dilepton = ROOT.TTree("Step0_dilepton", "Step0_dilepton")
    
    genpart_size_arr_0 = array('i', [0])
    genpart_pt_arr_0 = array('f', maxn*[0.])

    genpart_eta_arr_0  = array('f', maxn*[0.])
    genpart_phi_arr_0  = array('f', maxn*[0.])
    genpart_pid_arr_0  = array('i', maxn*[0])
    genpart_mass_arr_0 = array('f', maxn*[0.])
    genpart_status_arr_0 = array('i', maxn*[0])
    #genpart_charge_arr_0 = array('f', maxn*[0])
    
    gen_top_pt_arr_0      = array('f', [0.])
    gen_top_eta_arr_0     = array('f', [0.])
    gen_top_phi_arr_0     = array('f', [0.])
    gen_top_mass_arr_0     = array('f', [0.])
    gen_top_status_arr_0  = array('f', [0.])

    gen_atop_pt_arr_0     = array('f', [0.])
    gen_atop_eta_arr_0    = array('f', [0.])
    gen_atop_phi_arr_0    = array('f', [0.])
    gen_atop_mass_arr_0    = array('f', [0.])
    gen_atop_status_arr_0  = array('f', [0.])

    gen_b_pt_arr_0      = array('f', [0.])
    gen_b_eta_arr_0     = array('f', [0.])
    gen_b_phi_arr_0     = array('f', [0.])
    gen_b_mass_arr_0     = array('f', [0.])
    gen_b_status_arr_0  = array('f', [0.])

    gen_ab_pt_arr_0     = array('f', [0.])
    gen_ab_eta_arr_0    = array('f', [0.])
    gen_ab_phi_arr_0    = array('f', [0.])
    gen_ab_mass_arr_0    = array('f', [0.])
    gen_ab_status_arr_0  = array('f', [0.])

    gen_lep_pt_arr_0      = array('f', [0.])
    gen_lep_eta_arr_0     = array('f', [0.])
    gen_lep_phi_arr_0     = array('f', [0.])
    gen_lep_mass_arr_0     = array('f', [0.])
    gen_lep_pdgid_arr_0  = array('f', [0.])
    gen_lep_status_arr_0  = array('f', [0.])

    gen_alep_pt_arr_0     = array('f', [0.])
    gen_alep_eta_arr_0    = array('f', [0.])
    gen_alep_phi_arr_0    = array('f', [0.])
    gen_alep_mass_arr_0    = array('f', [0.])
    gen_alep_pdgid_arr_0 = array('f', [0.])
    gen_alep_status_arr_0  = array('f', [0.])

    gen_lep_nearest_pt_arr_0      = array('f', [0.])
    gen_lep_nearest_eta_arr_0     = array('f', [0.])
    gen_lep_nearest_phi_arr_0     = array('f', [0.])
    gen_lep_nearest_mass_arr_0     = array('f', [0.])
    gen_lep_nearest_pdgid_arr_0  = array('f', [0.])
    gen_lep_nearest_status_arr_0  = array('f', [0.])

    gen_alep_nearest_pt_arr_0     = array('f', [0.])
    gen_alep_nearest_eta_arr_0    = array('f', [0.])
    gen_alep_nearest_phi_arr_0    = array('f', [0.])
    gen_alep_nearest_mass_arr_0    = array('f', [0.])
    gen_alep_nearest_pdgid_arr_0 = array('f', [0.])
    gen_alep_nearest_status_arr_0  = array('f', [0.])

    gen_neu_pt_arr_0      = array('f', [0.])
    gen_neu_eta_arr_0     = array('f', [0.])
    gen_neu_phi_arr_0     = array('f', [0.])
    gen_neu_mass_arr_0     = array('f', [0.])
    gen_neu_pdgid_arr_0  = array('f', [0.])
    gen_neu_status_arr_0  = array('f', [0.])

    gen_aneu_pt_arr_0     = array('f', [0.])
    gen_aneu_eta_arr_0    = array('f', [0.])
    gen_aneu_phi_arr_0    = array('f', [0.])
    gen_aneu_mass_arr_0    = array('f', [0.])
    gen_aneu_pdgid_arr_0 = array('f', [0.])
    gen_aneu_status_arr_0  = array('f', [0.])

    gen_met_pt_arr_0     = array('f', [0.])
    gen_met_phi_arr_0    = array('f', [0.])
    
    # Gen jets
    #Step0tree.Branch("genjet_size_0", genjet_size_arr_0, "genjet_size_0/I")
    #Step0tree.Branch("genjet_btag_0", genjet_btag_arr_0, "genjet_btag_0[genjet_size_0]/I")

    #Step0tree.Branch("genjet_pt_0"  , genjet_pt_arr_0  , "genjet_pt_0[genjet_size_0]/F")
    #Step0tree.Branch("genjet_eta_0" , genjet_eta_arr_0 , "genjet_eta_0[genjet_size_0]/F")
    #Step0tree.Branch("genjet_phi_0" , genjet_phi_arr_0 , "genjet_phi_0[genjet_size_0]/F")
    #Step0tree.Branch("genjet_mass_0", genjet_mass_arr_0, "genjet_mass_0[genjet_size_0]/F")

    # Selection Mark
    Step0tree.Branch("selection_step", selection_step_arr, "selection_step/I")
    
    # Gen particles
    Step0tree.Branch("genpart_size_0", genpart_size_arr_0, "genpart_size_0/I")
    Step0tree.Branch("genpart_pid_0", genpart_pid_arr_0, "genpart_pid_0[genpart_size_0]/I")
    Step0tree.Branch("genpart_status_0", genpart_status_arr_0,"genpart_status_0[genpart_size_0]/I")

    Step0tree.Branch("genpart_pt_0", genpart_pt_arr_0, "genpart_pt_0[genpart_size_0]/F")
    Step0tree.Branch("genpart_eta_0", genpart_eta_arr_0, "genpart_eta_0[genpart_size_0]/F")
    Step0tree.Branch("genpart_phi_0", genpart_phi_arr_0, "genpart_phi_0[genpart_size_0]/F")
    Step0tree.Branch("genpart_mass_0", genpart_mass_arr_0,"genpart_mass_0[genpart_size_0]/F")
    #Step7tree.Branch("genpart_charge", genpart_charge_arr,"genpart_charge[genpart_size]/F")

    #Gen particle branches
    # By flavor
    Step0tree.Branch("gen_top_pt_0"    , gen_top_pt_arr_0    , 'gen_top_pt_0/F')
    Step0tree.Branch("gen_top_eta_0"   , gen_top_eta_arr_0   , 'gen_top_eta_0/F')
    Step0tree.Branch("gen_top_phi_0"   , gen_top_phi_arr_0   , 'gen_top_phi_0/F')
    Step0tree.Branch("gen_top_mass_0"   , gen_top_mass_arr_0   , 'gen_top_mass_0/F')
    Step0tree.Branch("gen_top_status_0", gen_top_status_arr_0, 'gen_top_status_0/F')

    Step0tree.Branch("gen_atop_pt_0"    , gen_atop_pt_arr_0    , 'gen_atop_pt_0/F')
    Step0tree.Branch("gen_atop_eta_0"   , gen_atop_eta_arr_0   , 'gen_atop_eta_0/F')
    Step0tree.Branch("gen_atop_phi_0"   , gen_atop_phi_arr_0   , 'gen_atop_phi_0/F')
    Step0tree.Branch("gen_atop_mass_0"   , gen_atop_mass_arr_0   , 'gen_atop_mass_0/F')
    Step0tree.Branch("gen_atop_status_0", gen_atop_status_arr_0, 'gen_atop_status_0/F')
    
    Step0tree.Branch("gen_b_pt_0"    , gen_b_pt_arr_0    , 'gen_b_pt_0/F')
    Step0tree.Branch("gen_b_eta_0"   , gen_b_eta_arr_0   , 'gen_b_eta_0/F')
    Step0tree.Branch("gen_b_phi_0"   , gen_b_phi_arr_0   , 'gen_b_phi_0/F')
    Step0tree.Branch("gen_b_mass_0"   , gen_b_mass_arr_0   , 'gen_b_mass_0/F')
    Step0tree.Branch("gen_b_status_0", gen_b_status_arr_0, 'gen_b_status_0/F')

    Step0tree.Branch("gen_ab_pt_0"    , gen_ab_pt_arr_0    , 'gen_ab_pt_0/F')
    Step0tree.Branch("gen_ab_eta_0"   , gen_ab_eta_arr_0   , 'gen_ab_eta_0/F')
    Step0tree.Branch("gen_ab_phi_0"   , gen_ab_phi_arr_0   , 'gen_ab_phi_0/F')
    Step0tree.Branch("gen_ab_mass_0"   , gen_ab_mass_arr_0   , 'gen_ab_mass_0/F')
    Step0tree.Branch("gen_ab_status_0", gen_ab_status_arr_0, 'gen_ab_status_0/F')

    Step0tree.Branch("gen_lep_nearest_pt_0"    , gen_lep_nearest_pt_arr_0    , 'gen_lep_nearest_pt_0/F')
    Step0tree.Branch("gen_lep_nearest_eta_0"   , gen_lep_nearest_eta_arr_0   , 'gen_lep_nearest_eta_0/F')
    Step0tree.Branch("gen_lep_nearest_phi_0"   , gen_lep_nearest_phi_arr_0   , 'gen_lep_nearest_phi_0/F')
    Step0tree.Branch("gen_lep_nearest_mass_0"   , gen_lep_nearest_mass_arr_0   , 'gen_lep_nearest_mass_0/F')
    Step0tree.Branch("gen_lep_nearest_pdgid_0", gen_lep_nearest_pdgid_arr_0, 'gen_lep_nearest_pdgid_0/F')
    Step0tree.Branch("gen_lep_nearest_status_0", gen_lep_nearest_status_arr_0, 'gen_lep_nearest_status_0/F')

    Step0tree.Branch("gen_alep_nearest_pt_0"    , gen_alep_nearest_pt_arr_0    , 'gen_alep_nearest_pt_0/F')
    Step0tree.Branch("gen_alep_nearest_eta_0"   , gen_alep_nearest_eta_arr_0   , 'gen_alep_nearest_eta_0/F')
    Step0tree.Branch("gen_alep_nearest_phi_0"   , gen_alep_nearest_phi_arr_0   , 'gen_alep_nearest_phi_0/F')
    Step0tree.Branch("gen_alep_nearest_mass_0"   , gen_alep_nearest_mass_arr_0   , 'gen_alep_nearest_mass_0/F')
    Step0tree.Branch("gen_alep_nearest_pdgid_0", gen_alep_nearest_pdgid_arr_0, 'gen_alep_nearest_pdgid_0/F')
    Step0tree.Branch("gen_alep_nearest_status_0", gen_alep_nearest_status_arr_0, 'gen_alep_nearest_status_0/F')

    Step0tree.Branch("gen_lep_pt_0"    , gen_lep_pt_arr_0    , 'gen_lep_pt_0/F')
    Step0tree.Branch("gen_lep_eta_0"   , gen_lep_eta_arr_0   , 'gen_lep_eta_0/F')
    Step0tree.Branch("gen_lep_phi_0"   , gen_lep_phi_arr_0   , 'gen_lep_phi_0/F')
    Step0tree.Branch("gen_lep_mass_0"   , gen_lep_mass_arr_0   , 'gen_lep_mass_0/F')
    Step0tree.Branch("gen_lep_pdgid_0", gen_lep_pdgid_arr_0, 'gen_lep_pdgid_0/F')
    Step0tree.Branch("gen_lep_status_0", gen_lep_status_arr_0, 'gen_lep_status_0/F')

    Step0tree.Branch("gen_alep_pt_0"    , gen_alep_pt_arr_0    , 'gen_alep_pt_0/F')
    Step0tree.Branch("gen_alep_eta_0"   , gen_alep_eta_arr_0   , 'gen_alep_eta_0/F')
    Step0tree.Branch("gen_alep_phi_0"   , gen_alep_phi_arr_0   , 'gen_alep_phi_0/F')
    Step0tree.Branch("gen_alep_mass_0"   , gen_alep_mass_arr_0   , 'gen_alep_mass_0/F')
    Step0tree.Branch("gen_alep_pdgid_0", gen_alep_pdgid_arr_0, 'gen_alep_pdgid_0/F')
    Step0tree.Branch("gen_alep_status_0", gen_alep_status_arr_0, 'gen_alep_status_0/F')

    Step0tree.Branch("gen_neu_pt_0"    , gen_neu_pt_arr_0    , 'gen_neu_pt_0/F')
    Step0tree.Branch("gen_neu_eta_0"   , gen_neu_eta_arr_0   , 'gen_neu_eta_0/F')
    Step0tree.Branch("gen_neu_phi_0"   , gen_neu_phi_arr_0   , 'gen_neu_phi_0/F')
    Step0tree.Branch("gen_neu_pdgid_0", gen_neu_pdgid_arr_0, 'gen_neu_pdgid_0/F')
    Step0tree.Branch("gen_neu_status_0", gen_neu_status_arr_0, 'gen_neu_status_0/F')

    Step0tree.Branch("gen_aneu_pt_0"    , gen_aneu_pt_arr_0    , 'gen_aneu_pt_0/F')
    Step0tree.Branch("gen_aneu_eta_0"   , gen_aneu_eta_arr_0   , 'gen_aneu_eta_0/F')
    Step0tree.Branch("gen_aneu_phi_0"   , gen_aneu_phi_arr_0   , 'gen_aneu_phi_0/F')
    Step0tree.Branch("gen_aneu_pdgid_0", gen_aneu_pdgid_arr_0, 'gen_aneu_pdgid_0/F')
    Step0tree.Branch("gen_aneu_status_0", gen_aneu_status_arr_0, 'gen_aneu_status_0/F')

    Step0tree.Branch("gen_met_pt_0"    , gen_met_pt_arr_0    , 'gen_met_pt_0/F')
    Step0tree.Branch("gen_met_phi_0"   , gen_met_phi_arr_0   , 'gen_met_phi_0/F')
    
    # Store all gen information into the Step0 tree
    #Step0tree.Branch("gen_lep_pt_0", gen_lep_pt_arr_0, 'gen_lep_pt_0/F')

    for i in range(len(gen_lep_pt)):
        selection_step_arr[0] = selection_step[i]
        
        gen_lep_pt_arr_0[0]     = gen_lep_pt[i]
        gen_lep_eta_arr_0[0]     = gen_lep_eta[i]
        gen_lep_phi_arr_0[0]     = gen_lep_phi[i]
        gen_lep_mass_arr_0[0]     = gen_lep_mass[i]
        gen_lep_pdgid_arr_0[0]     = gen_lep_pdgid[i]
        gen_lep_status_arr_0[0]     = gen_lep_status[i]

        gen_alep_pt_arr_0[0]     = gen_alep_pt[i]
        gen_alep_eta_arr_0[0]     = gen_alep_eta[i]
        gen_alep_phi_arr_0[0]     = gen_alep_phi[i]
        gen_alep_mass_arr_0[0]     = gen_alep_mass[i]
        gen_alep_pdgid_arr_0[0]     = gen_alep_pdgid[i]
        gen_alep_status_arr_0[0]     = gen_alep_status[i]
        
        gen_neu_pt_arr_0[0]     = gen_neu_pt[i]
        gen_neu_eta_arr_0[0]     = gen_neu_eta[i]
        gen_neu_phi_arr_0[0]     = gen_neu_phi[i]
        gen_neu_pdgid_arr_0[0]     = gen_neu_pdgid[i]
        gen_neu_status_arr_0[0]     = gen_neu_status[i]
        
        gen_aneu_pt_arr_0[0]     = gen_aneu_pt[i]
        gen_aneu_eta_arr_0[0]     = gen_aneu_eta[i]
        gen_aneu_phi_arr_0[0]     = gen_aneu_phi[i]
        gen_aneu_pdgid_arr_0[0]     = gen_aneu_pdgid[i]
        gen_aneu_status_arr_0[0]     = gen_aneu_status[i]
        Step0tree.Fill()

    opfile.Write()
    opfile.Close()    
    
    # Make new root file with new tree
    opfile = ROOT.TFile(outputFile, 'update')
    #Step0tree = ROOT.TTree("Step0", "Step0") 
    Step7tree = ROOT.TTree("Step7", "Step7")
    hist   = ROOT.TH1F('Nevents', 'Nevents', 1, 0.5, 1.5)    
    
    # s7 GEN

    genpart_size_arr = array('i', [0])

    genpart_pt_arr   = array('f', maxn*[0.])
    genpart_eta_arr  = array('f', maxn*[0.])
    genpart_phi_arr  = array('f', maxn*[0.])
    genpart_pid_arr  = array('i', maxn*[0])
    genpart_mass_arr = array('f', maxn*[0.])
    genpart_status_arr = array('i', maxn*[0])
    #genpart_charge_arr = array('f', maxn*[0])

    #genjet_size_arr = array('i', [0])

    #genjet_pt_arr   = array('f', maxn*[0.])
    #genjet_eta_arr  = array('f', maxn*[0.])
    #genjet_phi_arr  = array('f', maxn*[0.])
    #genjet_mass_arr = array('f', maxn*[0.])
    #genjet_btag_arr = array('i', maxn*[0])

    gen_top_pt_arr      = array('f', [0.])
    gen_top_eta_arr     = array('f', [0.])
    gen_top_phi_arr     = array('f', [0.])
    gen_top_mass_arr     = array('f', [0.])
    gen_top_status_arr  = array('f', [0.])

    gen_atop_pt_arr     = array('f', [0.])
    gen_atop_eta_arr    = array('f', [0.])
    gen_atop_phi_arr    = array('f', [0.])
    gen_atop_mass_arr    = array('f', [0.])
    gen_atop_status_arr  = array('f', [0.])

    gen_b_pt_arr      = array('f', [0.])
    gen_b_eta_arr     = array('f', [0.])
    gen_b_phi_arr     = array('f', [0.])
    gen_b_mass_arr     = array('f', [0.])
    gen_b_status_arr  = array('f', [0.])

    gen_ab_pt_arr     = array('f', [0.])
    gen_ab_eta_arr    = array('f', [0.])
    gen_ab_phi_arr    = array('f', [0.])
    gen_ab_mass_arr    = array('f', [0.])
    gen_ab_status_arr  = array('f', [0.])

    gen_lep_pt_arr      = array('f', [0.])
    gen_lep_eta_arr     = array('f', [0.])
    gen_lep_phi_arr     = array('f', [0.])
    gen_lep_mass_arr     = array('f', [0.])
    gen_lep_pdgid_arr  = array('f', [0.])
    gen_lep_status_arr  = array('f', [0.])

    gen_alep_pt_arr     = array('f', [0.])
    gen_alep_eta_arr    = array('f', [0.])
    gen_alep_phi_arr    = array('f', [0.])
    gen_alep_mass_arr    = array('f', [0.])
    gen_alep_pdgid_arr = array('f', [0.])
    gen_alep_status_arr  = array('f', [0.])

    gen_lep_nearest_pt_arr      = array('f', [0.])
    gen_lep_nearest_eta_arr     = array('f', [0.])
    gen_lep_nearest_phi_arr     = array('f', [0.])
    gen_lep_nearest_mass_arr     = array('f', [0.])
    gen_lep_nearest_pdgid_arr  = array('f', [0.])
    gen_lep_nearest_status_arr  = array('f', [0.])

    gen_alep_nearest_pt_arr     = array('f', [0.])
    gen_alep_nearest_eta_arr    = array('f', [0.])
    gen_alep_nearest_phi_arr    = array('f', [0.])
    gen_alep_nearest_mass_arr    = array('f', [0.])
    gen_alep_nearest_pdgid_arr = array('f', [0.])
    gen_alep_nearest_status_arr  = array('f', [0.])

    gen_neu_pt_arr      = array('f', [0.])
    gen_neu_eta_arr     = array('f', [0.])
    gen_neu_phi_arr     = array('f', [0.])
    gen_neu_mass_arr     = array('f', [0.])
    gen_neu_pdgid_arr  = array('f', [0.])
    gen_neu_status_arr  = array('f', [0.])

    gen_aneu_pt_arr     = array('f', [0.])
    gen_aneu_eta_arr    = array('f', [0.])
    gen_aneu_phi_arr    = array('f', [0.])
    gen_aneu_mass_arr    = array('f', [0.])
    gen_aneu_pdgid_arr = array('f', [0.])
    gen_aneu_status_arr  = array('f', [0.])

    gen_met_pt_arr     = array('f', [0.])
    gen_met_phi_arr    = array('f', [0.])

    # Create the branches and assign the fill-variables to them as floats (F)
    
    Step7tree.Branch("selection_step", selection_step_arr, "selection_step/F")

    Step7tree.Branch("HT", HT_arr, 'HT/F')
    Step7tree.Branch("ST", ST_arr, 'ST/F')
    Step7tree.Branch("MET", MET_arr, 'MET/F')
    Step7tree.Branch("HT_check", HT_check_arr, 'HT_check/F')
    Step7tree.Branch("MET_phi" , MET_phi_arr , 'MET_phi/F')

    # Leading and sub-leading leptons
    Step7tree.Branch("l_pt", l_pt_arr, 'l_pt/F')
    Step7tree.Branch("l_eta", l_eta_arr, 'l_eta/F')
    Step7tree.Branch("l_phi", l_phi_arr, 'l_phi/F')
    Step7tree.Branch("l_mass", l_mass_arr, 'l_mass/F')

    Step7tree.Branch("sl_pt", sl_pt_arr, 'sl_pt/F')
    Step7tree.Branch("sl_eta", sl_eta_arr, 'sl_eta/F')
    Step7tree.Branch("sl_phi", sl_phi_arr, 'sl_phi/F')
    Step7tree.Branch("sl_mass", sl_mass_arr, 'sl_mass/F')

    # By flavor
    Step7tree.Branch("e_pt"    , e_pt_arr    , 'e_pt/F')
    Step7tree.Branch("e_eta"   , e_eta_arr   , 'e_eta/F')
    Step7tree.Branch("e_phi"   , e_phi_arr   , 'e_phi/F')
    Step7tree.Branch("e_charge", e_charge_arr, 'e_charge/F')

    Step7tree.Branch("mu_pt"    , mu_pt_arr    , 'mu_pt/F')
    Step7tree.Branch("mu_eta"   , mu_eta_arr   , 'mu_eta/F')
    Step7tree.Branch("mu_phi"   , mu_phi_arr   , 'mu_phi/F')
    Step7tree.Branch("mu_charge", mu_charge_arr, 'mu_charge/F')
 
    Step7tree.Branch("lep_pt"    , lep_pt_arr    , 'lep_pt/F')
    Step7tree.Branch("lep_eta"   , lep_eta_arr   , 'lep_eta/F')
    Step7tree.Branch("lep_phi"   , lep_phi_arr   , 'lep_phi/F')
    Step7tree.Branch("lep_mass"   , lep_mass_arr   , 'lep_mass/F')
    Step7tree.Branch("lep_pdgid", lep_pdgid_arr, 'lep_pdgid/F')

    Step7tree.Branch("alep_pt"    , alep_pt_arr    , 'alep_pt/F')
    Step7tree.Branch("alep_eta"   , alep_eta_arr   , 'alep_eta/F')
    Step7tree.Branch("alep_phi"   , alep_phi_arr   , 'alep_phi/F')
    Step7tree.Branch("alep_mass"   , alep_mass_arr   , 'alep_mass/F')
    Step7tree.Branch("alep_pdgid", alep_pdgid_arr, 'alep_pdgid/F')
 
    Step7tree.Branch("lep_nearest_pt"    , lep_nearest_pt_arr    , 'lep_nearest_pt/F')
    Step7tree.Branch("lep_nearest_eta"   , lep_nearest_eta_arr   , 'lep_nearest_eta/F')
    Step7tree.Branch("lep_nearest_phi"   , lep_nearest_phi_arr   , 'lep_nearest_phi/F')
    Step7tree.Branch("lep_nearest_mass"   , lep_nearest_mass_arr   , 'lep_nearest_mass/F')
    Step7tree.Branch("lep_nearest_pdgid", lep_nearest_pdgid_arr, 'lep_nearest_pdgid/F')

    Step7tree.Branch("alep_nearest_pt"    , alep_nearest_pt_arr    , 'alep_nearest_pt/F')
    Step7tree.Branch("alep_nearest_eta"   , alep_nearest_eta_arr   , 'alep_nearest_eta/F')
    Step7tree.Branch("alep_nearest_phi"   , alep_nearest_phi_arr   , 'alep_nearest_phi/F')
    Step7tree.Branch("alep_nearest_mass"   , alep_nearest_mass_arr   , 'alep_nearest_mass/F')
    Step7tree.Branch("alep_nearest_pdgid", alep_nearest_pdgid_arr, 'alep_nearest_pdgid/F')
 
    # Leading and sub-leading jets
    Step7tree.Branch("ljet_pt", ljet_pt_arr, 'ljet_pt/F')
    Step7tree.Branch("ljet_eta", ljet_eta_arr, 'ljet_eta/F')
    Step7tree.Branch("ljet_phi", ljet_phi_arr, 'ljet_phi/F')
    Step7tree.Branch("ljet_mass", ljet_mass_arr, 'ljet_mass/F')

    Step7tree.Branch("sljet_pt", sljet_pt_arr, 'sljet_pt/F')
    Step7tree.Branch("sljet_eta", sljet_eta_arr, 'sljet_eta/F')
    Step7tree.Branch("sljet_phi", sljet_phi_arr, 'sljet_phi/F')
    Step7tree.Branch("sljet_mass", sljet_mass_arr, 'sljet_mass/F')

    #
    Step7tree.Branch("bjet_nearest_pt", bjet_nearest_pt_arr, 'bjet_nearest_pt/F')
    Step7tree.Branch("bjet_nearest_eta", bjet_nearest_eta_arr, 'bjet_nearest_eta/F')
    Step7tree.Branch("bjet_nearest_phi", bjet_nearest_phi_arr, 'bjet_nearest_phi/F')
    Step7tree.Branch("bjet_nearest_mass", bjet_nearest_mass_arr, 'bjet_nearest_mass/F')

    Step7tree.Branch("abjet_nearest_pt", abjet_nearest_pt_arr, 'abjet_nearest_pt/F')
    Step7tree.Branch("abjet_nearest_eta", abjet_nearest_eta_arr, 'abjet_nearest_eta/F')
    Step7tree.Branch("abjet_nearest_phi", abjet_nearest_phi_arr, 'abjet_nearest_phi/F')
    Step7tree.Branch("abjet_nearest_mass", abjet_nearest_mass_arr, 'abjet_nearest_mass/F')

    # Lepton angular stuff
    Step7tree.Branch("llbar_deta", llbar_deta_arr, 'llbar_deta/F')
    Step7tree.Branch("llbar_dphi", llbar_dphi_arr, 'llbar_dphi/F')
    Step7tree.Branch("bbbar_deta", bbbar_deta_arr, 'bbbar_deta/F')
    Step7tree.Branch("bbbar_dphi", bbbar_dphi_arr, 'bbbar_dphi/F')

    # Weights
    Step7tree.Branch("weight_size", weight_size_arr, "weight_size/I")
    Step7tree.Branch("weight", weight_arr, "weight[weight_size]/F")

    # Reco PUPPI jets
    Step7tree.Branch("jet_size", jet_size_arr, "jet_size/I")
    Step7tree.Branch("jet_btag", jet_btag_arr, "jet_btag[jet_size]/I")

    Step7tree.Branch("jet_pt", jet_pt_arr, "jet_pt[jet_size]/F")
    Step7tree.Branch("jet_eta", jet_eta_arr, "jet_eta[jet_size]/F")
    Step7tree.Branch("jet_phi", jet_phi_arr, "jet_phi[jet_size]/F")
    Step7tree.Branch("jet_mass", jet_mass_arr, "jet_mass[jet_size]/F")

    # Gen jets
    #Step7tree.Branch("genjet_size", genjet_size_arr, "genjet_size/I")
    #Step7tree.Branch("genjet_btag", genjet_btag_arr, "genjet_btag[genjet_size]/I")

    #Step7tree.Branch("genjet_pt"  , genjet_pt_arr  , "genjet_pt[genjet_size]/F")
    #Step7tree.Branch("genjet_eta" , genjet_eta_arr , "genjet_eta[genjet_size]/F")
    #Step7tree.Branch("genjet_phi" , genjet_phi_arr , "genjet_phi[genjet_size]/F")
    #Step7tree.Branch("genjet_mass", genjet_mass_arr, "genjet_mass[genjet_size]/F")

    # Gen particles
    Step7tree.Branch("genpart_size", genpart_size_arr, "genpart_size/I")
    Step7tree.Branch("genpart_pid", genpart_pid_arr, "genpart_pid[genpart_size]/I")
    Step7tree.Branch("genpart_status", genpart_status_arr,"genpart_status[genpart_size]/I")

    Step7tree.Branch("genpart_pt", genpart_pt_arr, "genpart_pt[genpart_size]/F")
    Step7tree.Branch("genpart_eta", genpart_eta_arr, "genpart_eta[genpart_size]/F")
    Step7tree.Branch("genpart_phi", genpart_phi_arr, "genpart_phi[genpart_size]/F")
    Step7tree.Branch("genpart_mass", genpart_mass_arr,"genpart_mass[genpart_size]/F")
    #Step7tree.Branch("genpart_charge", genpart_charge_arr,"genpart_charge[genpart_size]/F")

    #Gen particle branches
    # By flavor
    Step7tree.Branch("gen_top_pt"    , gen_top_pt_arr    , 'gen_top_pt/F')
    Step7tree.Branch("gen_top_eta"   , gen_top_eta_arr   , 'gen_top_eta/F')
    Step7tree.Branch("gen_top_phi"   , gen_top_phi_arr   , 'gen_top_phi/F')
    Step7tree.Branch("gen_top_mass"   , gen_top_mass_arr   , 'gen_top_mass/F')
    Step7tree.Branch("gen_top_status", gen_top_status_arr, 'gen_top_status/F')

    Step7tree.Branch("gen_atop_pt"    , gen_atop_pt_arr    , 'gen_atop_pt/F')
    Step7tree.Branch("gen_atop_eta"   , gen_atop_eta_arr   , 'gen_atop_eta/F')
    Step7tree.Branch("gen_atop_phi"   , gen_atop_phi_arr   , 'gen_atop_phi/F')
    Step7tree.Branch("gen_atop_mass"   , gen_atop_mass_arr   , 'gen_atop_mass/F')
    Step7tree.Branch("gen_atop_status", gen_atop_status_arr, 'gen_atop_status/F')

    Step7tree.Branch("gen_b_pt"    , gen_b_pt_arr    , 'gen_b_pt/F')
    Step7tree.Branch("gen_b_eta"   , gen_b_eta_arr   , 'gen_b_eta/F')
    Step7tree.Branch("gen_b_phi"   , gen_b_phi_arr   , 'gen_b_phi/F')
    Step7tree.Branch("gen_b_mass"   , gen_b_mass_arr   , 'gen_b_mass/F')
    Step7tree.Branch("gen_b_status", gen_b_status_arr, 'gen_b_status/F')

    Step7tree.Branch("gen_ab_pt"    , gen_ab_pt_arr    , 'gen_ab_pt/F')
    Step7tree.Branch("gen_ab_eta"   , gen_ab_eta_arr   , 'gen_ab_eta/F')
    Step7tree.Branch("gen_ab_phi"   , gen_ab_phi_arr   , 'gen_ab_phi/F')
    Step7tree.Branch("gen_ab_mass"   , gen_ab_mass_arr   , 'gen_ab_mass/F')
    Step7tree.Branch("gen_ab_status", gen_ab_status_arr, 'gen_ab_status/F')

    Step7tree.Branch("gen_lep_nearest_pt"    , gen_lep_nearest_pt_arr    , 'gen_lep_nearest_pt/F')
    Step7tree.Branch("gen_lep_nearest_eta"   , gen_lep_nearest_eta_arr   , 'gen_lep_nearest_eta/F')
    Step7tree.Branch("gen_lep_nearest_phi"   , gen_lep_nearest_phi_arr   , 'gen_lep_nearest_phi/F')
    Step7tree.Branch("gen_lep_nearest_mass"   , gen_lep_nearest_mass_arr   , 'gen_lep_nearest_mass/F')
    Step7tree.Branch("gen_lep_nearest_pdgid", gen_lep_nearest_pdgid_arr, 'gen_lep_nearest_pdgid/F')
    Step7tree.Branch("gen_lep_nearest_status", gen_lep_nearest_status_arr, 'gen_lep_nearest_status/F')

    Step7tree.Branch("gen_alep_nearest_pt"    , gen_alep_nearest_pt_arr    , 'gen_alep_nearest_pt/F')
    Step7tree.Branch("gen_alep_nearest_eta"   , gen_alep_nearest_eta_arr   , 'gen_alep_nearest_eta/F')
    Step7tree.Branch("gen_alep_nearest_phi"   , gen_alep_nearest_phi_arr   , 'gen_alep_nearest_phi/F')
    Step7tree.Branch("gen_alep_nearest_mass"   , gen_alep_nearest_mass_arr   , 'gen_alep_nearest_mass/F')
    Step7tree.Branch("gen_alep_nearest_pdgid", gen_alep_nearest_pdgid_arr, 'gen_alep_nearest_pdgid/F')
    Step7tree.Branch("gen_alep_nearest_status", gen_alep_nearest_status_arr, 'gen_alep_nearest_status/F')

    Step7tree.Branch("gen_lep_pt"    , gen_lep_pt_arr    , 'gen_lep_pt/F')
    Step7tree.Branch("gen_lep_eta"   , gen_lep_eta_arr   , 'gen_lep_eta/F')
    Step7tree.Branch("gen_lep_phi"   , gen_lep_phi_arr   , 'gen_lep_phi/F')
    Step7tree.Branch("gen_lep_mass"   , gen_lep_mass_arr   , 'gen_lep_mass/F')
    Step7tree.Branch("gen_lep_pdgid", gen_lep_pdgid_arr, 'gen_lep_pdgid/F')
    Step7tree.Branch("gen_lep_status", gen_lep_status_arr, 'gen_lep_status/F')

    Step7tree.Branch("gen_alep_pt"    , gen_alep_pt_arr    , 'gen_alep_pt/F')
    Step7tree.Branch("gen_alep_eta"   , gen_alep_eta_arr   , 'gen_alep_eta/F')
    Step7tree.Branch("gen_alep_phi"   , gen_alep_phi_arr   , 'gen_alep_phi/F')
    Step7tree.Branch("gen_alep_mass"   , gen_alep_mass_arr   , 'gen_alep_mass/F')
    Step7tree.Branch("gen_alep_pdgid", gen_alep_pdgid_arr, 'gen_alep_pdgid/F')
    Step7tree.Branch("gen_alep_status", gen_alep_status_arr, 'gen_alep_status/F')

    Step7tree.Branch("gen_neu_pt"    , gen_neu_pt_arr    , 'gen_neu_pt/F')
    Step7tree.Branch("gen_neu_eta"   , gen_neu_eta_arr   , 'gen_neu_eta/F')
    Step7tree.Branch("gen_neu_phi"   , gen_neu_phi_arr   , 'gen_neu_phi/F')
    Step7tree.Branch("gen_neu_pdgid", gen_neu_pdgid_arr, 'gen_neu_pdgid/F')
    Step7tree.Branch("gen_neu_status", gen_neu_status_arr, 'gen_neu_status/F')

    Step7tree.Branch("gen_aneu_pt"    , gen_aneu_pt_arr    , 'gen_aneu_pt/F')
    Step7tree.Branch("gen_aneu_eta"   , gen_aneu_eta_arr   , 'gen_aneu_eta/F')
    Step7tree.Branch("gen_aneu_phi"   , gen_aneu_phi_arr   , 'gen_aneu_phi/F')
    Step7tree.Branch("gen_aneu_pdgid", gen_aneu_pdgid_arr, 'gen_aneu_pdgid/F')
    Step7tree.Branch("gen_aneu_status", gen_aneu_status_arr, 'gen_aneu_status/F')

    Step7tree.Branch("gen_met_pt"    , gen_met_pt_arr    , 'gen_met_pt/F')
    Step7tree.Branch("gen_met_phi"   , gen_met_phi_arr   , 'gen_met_phi/F')

    #print(len(HT), ' is the length of ', *HT, 'and the sum of valid numbers is ', ak.count_nonzero(HT))

    k_jet = 0
    for i in range(NEvents):    
        selection_step_arr[0] = selection_step[i] 

        if (selection_step[i]==7):
                
            print('step7tree jet loop i k=', i, k_jet)
            
            jet_size_arr[0]     = len(jet_pt_sel[k_jet])
            weight_size_arr[0]  = len(weight_sel[k_jet])
            genpart_size_arr[0] = len(gen_pt_sel[k_jet])
            #genjet_size_arr[0]  = len(genjet_pt_sel[i])            
                            
            for j in range(jet_size_arr[0]):
                jet_pt_arr[j]   = jet_pt_sel[k_jet][j]
                jet_eta_arr[j]  = jet_eta_sel[k_jet][j]
                jet_phi_arr[j]  = jet_phi_sel[k_jet][j]
                jet_mass_arr[j] = jet_mass_sel[k_jet][j]
                jet_btag_arr[j] = int(jet_btag_sel[k_jet][j])
            
            #for j in range(genjet_size_arr[0]):
                #genjet_pt_arr[j]   = genjet_pt_sel[i][j]
                #genjet_eta_arr[j]  = genjet_eta_sel[i][j]
                #genjet_phi_arr[j]  = genjet_phi_sel[i][j]
                #genjet_mass_arr[j] = genjet_mass_sel[i][j]
                #genjet_btag_arr[j] = genjet_btag_sel[i][j]
            
            for j in range(genpart_size_arr[0]):
                genpart_pt_arr[j]   = gen_pt_sel[k_jet][j]
                genpart_pid_arr[j]  = gen_pid_sel[k_jet][j]
                genpart_eta_arr[j]  = gen_eta_sel[k_jet][j]
                genpart_phi_arr[j]  = gen_phi_sel[k_jet][j]
                genpart_mass_arr[j] = gen_mass_sel[k_jet][j]
                genpart_status_arr[j] = gen_status_sel[k_jet][j]
                #genpart_charge_arr[j] = gen_charge_sel[i][j]            
            
            for k in range(weight_size_arr[0]):
                weight_arr[k] = weight_sel[k_jet][k]
                
            #Step7tree.Fill()     
            
            print('step7tree outer loop i = ', i)  
    
            HT_arr[0]  = HT[i]
            ST_arr[0]  = ST[i]
            MET_arr[0] = ET_miss[i]
    
            HT_check_arr[0] = HT_check[i]
            MET_phi_arr[0]  = MET_phi[i]
    
            l_pt_arr[0]   = l_pt[i]
            l_eta_arr[0]  = l_eta[i]
            l_phi_arr[0]  = l_phi[i]
            l_mass_arr[0] = l_mass[i]
    
            sl_pt_arr[0]   = sl_pt[i]
            sl_eta_arr[0]  = sl_eta[i]
            sl_phi_arr[0]  = sl_phi[i]
            sl_mass_arr[0] = sl_mass[i]
    
            e_pt_arr[0]     = e_pt[i]
            e_eta_arr[0]    = e_eta[i]
            e_phi_arr[0]    = e_phi[i]
            e_charge_arr[0] = e_charge[i]
    
            mu_pt_arr[0]     = mu_pt[i]
            mu_eta_arr[0]    = mu_eta[i]
            mu_phi_arr[0]    = mu_phi[i]
            mu_charge_arr[0] = mu_charge[i]
    
            lep_pt_arr[0]     = lep_pt[i]
            lep_eta_arr[0]    = lep_eta[i]
            lep_phi_arr[0]    = lep_phi[i]
            lep_mass_arr[0]    = lep_mass[i]
            lep_pdgid_arr[0] = lep_pdgid[i]
    
            alep_pt_arr[0]     = alep_pt[i]
            alep_eta_arr[0]    = alep_eta[i]
            alep_phi_arr[0]    = alep_phi[i]
            alep_mass_arr[0]    = alep_mass[i]
            alep_pdgid_arr[0] = alep_pdgid[i]
            
            lep_nearest_pt_arr[0]     = lep_nearest_pt[i]
            lep_nearest_eta_arr[0]    = lep_nearest_eta[i]
            lep_nearest_phi_arr[0]    = lep_nearest_phi[i]
            lep_nearest_mass_arr[0]    = lep_nearest_mass[i]
            lep_nearest_pdgid_arr[0] = lep_nearest_pdgid[i]
    
            alep_nearest_pt_arr[0]     = alep_nearest_pt[i]
            alep_nearest_eta_arr[0]    = alep_nearest_eta[i]
            alep_nearest_phi_arr[0]    = alep_nearest_phi[i]
            alep_nearest_mass_arr[0]    = alep_nearest_mass[i]
            alep_nearest_pdgid_arr[0] = alep_nearest_pdgid[i]
    
            ljet_pt_arr[0]   = ljet_pt[i]
            ljet_eta_arr[0]  = ljet_eta[i]
            ljet_phi_arr[0]  = ljet_phi[i]
            ljet_mass_arr[0] = ljet_mass[i]
    
            sljet_pt_arr[0]   = sljet_pt[i]
            sljet_eta_arr[0]  = sljet_eta[i]
            sljet_phi_arr[0]  = sljet_phi[i]
            sljet_mass_arr[0] = sljet_mass[i] 
            
            bjet_nearest_pt_arr[0]   = bjet_nearest_pt[i]
            bjet_nearest_eta_arr[0]  = bjet_nearest_eta[i]
            bjet_nearest_phi_arr[0]  = bjet_nearest_phi[i]
            bjet_nearest_mass_arr[0] = bjet_nearest_mass[i]
    
            abjet_nearest_pt_arr[0]   = abjet_nearest_pt[i]
            abjet_nearest_eta_arr[0]  = abjet_nearest_eta[i]
            abjet_nearest_phi_arr[0]  = abjet_nearest_phi[i]
            abjet_nearest_mass_arr[0] = abjet_nearest_mass[i]
    
            llbar_deta_arr[0] = llbar_deta[i]
            llbar_dphi_arr[0] = llbar_dphi[i]
            bbbar_deta_arr[0] = bbbar_deta[i]
            bbbar_dphi_arr[0] = bbbar_dphi[i]
        
            #print(i, ', len(jet_pt_sel)=', len(jet_pt_sel[i]), ', jet_pt_sel=', jet_pt_sel[i])
    
            # Gen
    
            gen_top_pt_arr[0]     = gen_top_pt[i]
            gen_top_eta_arr[0]    = gen_top_eta[i]
            gen_top_phi_arr[0]    = gen_top_phi[i]
            gen_top_mass_arr[0]    = gen_top_mass[i]
            gen_top_status_arr[0] = gen_top_status[i]
    
            gen_atop_pt_arr[0]     = gen_atop_pt[i]
            gen_atop_eta_arr[0]    = gen_atop_eta[i]
            gen_atop_phi_arr[0]    = gen_atop_phi[i]
            gen_atop_mass_arr[0]    = gen_atop_mass[i]
            gen_atop_status_arr[0] = gen_atop_status[i] 
            
            gen_b_pt_arr[0]     = gen_b_pt[i]
            gen_b_eta_arr[0]    = gen_b_eta[i]
            gen_b_phi_arr[0]    = gen_b_phi[i]
            gen_b_mass_arr[0]    = gen_b_mass[i]
            gen_b_status_arr[0] = gen_b_status[i]
    
            gen_ab_pt_arr[0]     = gen_ab_pt[i]
            gen_ab_eta_arr[0]    = gen_ab_eta[i]
            gen_ab_phi_arr[0]    = gen_ab_phi[i]
            gen_ab_mass_arr[0]    = gen_ab_mass[i]
            gen_ab_status_arr[0] = gen_ab_status[i]
    
            gen_lep_pt_arr[0]     = gen_lep_pt[i]
            gen_lep_eta_arr[0]    = gen_lep_eta[i]
            gen_lep_phi_arr[0]    = gen_lep_phi[i]
            gen_lep_mass_arr[0]    = gen_lep_mass[i]
            gen_lep_pdgid_arr[0] = gen_lep_pdgid[i]
            gen_lep_status_arr[0] = gen_lep_status[i]
    
            gen_alep_pt_arr[0]     = gen_alep_pt[i]
            gen_alep_eta_arr[0]    = gen_alep_eta[i]
            gen_alep_phi_arr[0]    = gen_alep_phi[i]
            gen_alep_mass_arr[0]    = gen_alep_mass[i]
            gen_alep_pdgid_arr[0] = gen_alep_pdgid[i]
            gen_alep_status_arr[0] = gen_alep_status[i]
    
            gen_lep_nearest_pt_arr[0]     = gen_lep_nearest_pt[i]
            gen_lep_nearest_eta_arr[0]    = gen_lep_nearest_eta[i]
            gen_lep_nearest_phi_arr[0]    = gen_lep_nearest_phi[i]
            gen_lep_nearest_mass_arr[0]    = gen_lep_nearest_mass[i]
            gen_lep_nearest_pdgid_arr[0] = gen_lep_nearest_pdgid[i]
            gen_lep_nearest_status_arr[0] = gen_lep_nearest_status[i]
    
            gen_alep_nearest_pt_arr[0]     = gen_alep_nearest_pt[i]
            gen_alep_nearest_eta_arr[0]    = gen_alep_nearest_eta[i]
            gen_alep_nearest_phi_arr[0]    = gen_alep_nearest_phi[i]
            gen_alep_nearest_mass_arr[0]    = gen_alep_nearest_mass[i]
            gen_alep_nearest_pdgid_arr[0] = gen_alep_nearest_pdgid[i]
            gen_alep_nearest_status_arr[0] = gen_alep_nearest_status[i]
    
            gen_neu_pt_arr[0]     = gen_neu_pt[i]
            gen_neu_eta_arr[0]    = gen_neu_eta[i]
            gen_neu_phi_arr[0]    = gen_neu_phi[i]
            gen_neu_pdgid_arr[0] = gen_neu_pdgid[i]
            gen_neu_status_arr[0] = gen_neu_status[i]
    
            gen_aneu_pt_arr[0]     = gen_aneu_pt[i]
            gen_aneu_eta_arr[0]    = gen_aneu_eta[i]
            gen_aneu_phi_arr[0]    = gen_aneu_phi[i]
            gen_aneu_pdgid_arr[0] = gen_aneu_pdgid[i]
            gen_aneu_status_arr[0] = gen_aneu_status[i]
    
            gen_met_pt_arr[0]     = gen_met_pt[i]
            gen_met_phi_arr[0]    = gen_met_phi[i]     
    
            Step7tree.Fill()             
     
            k_jet += 1
        
    for i in range(len(selection)):
        hist.Fill(i)
    
    print('Number of events that pass selection :: ' + str(len(ljet_pt)))
    # print('gen_lep_pt_arr :: ' + str(len(gen_lep_pt_arr))) 
    #print('gen_lep_pt_arr :: ' + str(len(gen_lep_pt_arr))) 
    print('gen_lep_pt :: ' + str(len(gen_lep_pt))) 
    #print('gen_lep_nearest_pt_arr :: ' + str(len(gen_lep_nearest_pt_arr))) 
    print('gen_lep_nearest_pt :: ' + str(len(gen_lep_nearest_pt))) 
    
    # Write the tree into the output file and close the file
    opfile.Write()
    opfile.Close()

main()