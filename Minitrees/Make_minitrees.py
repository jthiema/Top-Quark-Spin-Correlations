import ROOT
import uproot
import argparse
import numpy as np
from   array import array
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
    parser.add_argument ('-i', '--input' , help='Input  Delphes Ntuple location'  )
    parser.add_argument ('-o', '--output', help='Output Delphes Minitree location')

    args = parser.parse_args()
    inputFile  = args.input
    outputFile = args.output

    fileptr    = uproot.open(inputFile)['Delphes_Ntuples']

    # Gen level data
    gen_part_eta    = fileptr['genpart_eta'].array()
    gen_part_phi    = fileptr['genpart_phi'].array()
    gen_part_pt     = fileptr['genpart_pt'].array()
    gen_part_mass   = fileptr['genpart_mass'].array()
    gen_part_pid    = fileptr['genpart_pid'].array()
    gen_part_status = fileptr['genpart_status'].array()
    gen_part_charge = fileptr['genpart_charge'].array()

    # JET MET
    jet_pt   = fileptr['jet_pt'].array()
    jet_eta  = fileptr['jet_eta'].array()
    jet_phi  = fileptr['jet_phi'].array()
    jet_mass = fileptr['jet_mass'].array()
    jet_btag = fileptr['jet_btag'].array()

    met_pt   = fileptr['met_pt'].array()
    weight   = fileptr['weight'].array()

    # Electrons
    elec_pt   = fileptr['elec_pt'].array()
    elec_eta  = fileptr['elec_eta'].array()
    elec_phi  = fileptr['elec_phi'].array()
    elec_mass = fileptr['elec_mass'].array()
    elec_charge = fileptr['elec_charge'].array()
    elec_reliso = fileptr['elec_reliso'].array()

    # Muons
    muon_pt   = fileptr['muon_pt'].array()
    muon_eta  = fileptr['muon_eta'].array()
    muon_phi  = fileptr['muon_phi'].array()
    muon_mass = fileptr['muon_mass'].array()
    muon_charge = fileptr['muon_charge'].array()
    muon_reliso = fileptr['muon_reliso'].array()

    # Empty arrays
    # Similar to histograms in ROOT

    l_pt  = []
    l_eta = []
    l_phi = []

    sl_pt  = []
    sl_eta = []
    sl_phi = []

    ljet_pt  = []
    ljet_eta = []
    ljet_phi = []
    ljet_mass = []

    sljet_pt  = []
    sljet_eta = []
    sljet_phi = []
    sljet_mass = []

    ST = []
    HT = []
    ET_miss = []

    # Let's create a mask
    selection = np.zeros(len(jet_pt))

    # Loop over the events
    for i in range(len(jet_pt)):
       
        if (i % 1000 == 0) :   
        	print('Processing event ' + str(i) + ' of ' + str(len(jet_pt)) )

        # Temporary variables

        e_idx   = []
        mu_idx  = []

        ef_idx  = []
        muf_idx = []

        jet_idx = []

        btag_cnt = 0

        e_4vec  = ROOT.TLorentzVector()
        mu_4vec = ROOT.TLorentzVector()

        ########## Electrons ##########

        # Ensure pt > 20 GeV and eta < 2.4 and isolation
        for j in range(len(elec_pt[i])):
            if (elec_pt[i][j] < 20):
                continue

            if (elec_eta[i][j] > 2.4 or (elec_eta[i][j] > 1.4442 and elec_eta[i][j] < 1.5660)):
                continue

            if (elec_reliso[i][j] < 0.0588):
                continue

            e_idx.append(j)

        ###########  Muons ############

        # Ensure pt > 20 GeV and eta < 2.4 and isolation
        for j in range(len(muon_pt[i])):
            if (muon_pt[i][j] < 20):
                continue

            if (muon_eta[i][j] > 2.4):
                continue

            if (muon_reliso[i][j] < 0.15):
                continue

            mu_idx.append(j)

        # Ensure atleast one muon and one electron
        if (len(e_idx) == 0 or len(mu_idx) == 0):
            continue

        # Check for opp sign charge pairings
        for j in range(len(e_idx)):
            for k in range(len(mu_idx)):
                if (elec_charge[i][j] * muon_charge[i][k] == -1):
                    ef_idx.append(j)
                    muf_idx.append(k)

        # Ensure such a pairing exists
        if (len(ef_idx) == 0 or len(muf_idx) == 0):
            continue

        # Assign leading indices to e and mu
        e_index = ef_idx[0]
        mu_index = muf_idx[0]

        # Defining the 4 vectors
        e_4vec.SetPtEtaPhiM(
            elec_pt[i][e_index], elec_eta[i][e_index], elec_phi[i][e_index], 0.000511)
        mu_4vec.SetPtEtaPhiM(
            muon_pt[i][mu_index], muon_eta[i][mu_index], muon_phi[i][mu_index], 0.105)

        # Mll cut (Step 3 according to the FW)
        if ((e_4vec + mu_4vec).M() < 20):
            continue

        ###########  Jets ###############

        for j in range(len(jet_pt[i])):

            # Ensure pt > 30 GeV and eta < 2.4 isolation

            if ((dR(elec_phi[i][e_index], elec_eta[i][e_index], jet_phi[i][j], jet_eta[i][j]) < 0.4)
                    or (dR(muon_phi[i][mu_index], muon_eta[i][mu_index], jet_phi[i][j], jet_eta[i][j]) < 0.4)):
                continue

            if ((jet_pt[i][j] < 30)):
                continue

            if ((abs(jet_eta[i][j]) > 2.4)):
                continue

            if (jet_btag[i][j] != 0):
                btag_cnt += 1

            jet_idx.append(j)

        # 2 Jets (Step 5 according to the FW)
        if(len(jet_idx) < 2):
            continue

        # Atleast one b-tag
        if (btag_cnt == 0):
            continue

        ljet_idx = jet_idx[0]
        sljet_idx = jet_idx[1]

        ####### Fill the arrays ##########

        # Leading and sub-leading lepton pts
        if (elec_pt[i][e_index] > muon_pt[i][mu_index] and elec_pt[i][e_index] > 25):
            l_pt.append(elec_pt[i][e_index])
            l_phi.append(elec_phi[i][e_index])
            l_eta.append(elec_eta[i][e_index])

            sl_pt.append(muon_pt[i][mu_index])
            sl_phi.append(muon_phi[i][mu_index])
            sl_eta.append(muon_eta[i][mu_index])

        elif (muon_pt[i][mu_index] > elec_pt[i][e_index] and muon_pt[i][mu_index] > 25):
            sl_pt.append(elec_pt[i][e_index])
            sl_phi.append(elec_phi[i][e_index])
            sl_eta.append(elec_eta[i][e_index])

            l_pt.append(muon_pt[i][mu_index])
            l_phi.append(muon_phi[i][mu_index])
            l_eta.append(muon_eta[i][mu_index])

        else:
            continue

        # Leading and Subleading Pt
        ljet_pt.append(jet_pt[i][ljet_idx])
        ljet_phi.append(jet_phi[i][ljet_idx])
        ljet_eta.append(jet_eta[i][ljet_idx])
        ljet_mass.append(jet_eta[i][ljet_idx])

        sljet_pt.append(jet_pt[i][sljet_idx])
        sljet_phi.append(jet_phi[i][sljet_idx])
        sljet_eta.append(jet_eta[i][sljet_idx])
        sljet_mass.append(jet_eta[i][sljet_idx])

        ET_miss.append(met_pt[i][0])

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

        # Append to lists
        HT.append(Ht)
        ST.append(St)

        # Create a mask for selection
        selection[i] = 1

    # Other varaibles that we need
    llbar_deta = abs(np.array(l_eta) - np.array(sl_eta))
    llbar_dphi = abs(abs(abs(np.array(l_phi) - np.array(sl_phi)) - np.pi) - np.pi)

    bbbar_deta = abs(np.array(ljet_eta) - np.array(sljet_eta))
    bbbar_dphi = abs(abs(abs(np.array(ljet_phi) - np.array(sljet_phi)) - np.pi) - np.pi)

    weight_sel = weight[selection == 1]
    gen_pt_sel = gen_part_pt[selection == 1]
    gen_pid_sel = gen_part_pid[selection == 1]
    gen_eta_sel = gen_part_eta[selection == 1]
    gen_phi_sel = gen_part_phi[selection == 1]
    gen_mass_sel = gen_part_mass[selection == 1]
    gen_status_sel = gen_part_status[selection == 1]

    # make new root file with new tree
    opfile = ROOT.TFile(outputFile, 'recreate')
    tree   = ROOT.TTree("Step8", "Step8")
    hist   = ROOT.TH1F('Nevents', 'Nevents', 1, 0.5, 1.5)

    maxn = 9999
    HT_arr = array('f', [0.])
    ST_arr = array('f', [0.])
    MET_arr = array('f', [0.])

    l_pt_arr = array('f', [0.])
    l_eta_arr = array('f', [0.])
    l_phi_arr = array('f', [0.])

    sl_pt_arr = array('f', [0.])
    sl_eta_arr = array('f', [0.])
    sl_phi_arr = array('f', [0.])

    ljet_pt_arr = array('f', [0.])
    ljet_eta_arr = array('f', [0.])
    ljet_phi_arr = array('f', [0.])

    sljet_pt_arr = array('f', [0.])
    sljet_eta_arr = array('f', [0.])
    sljet_phi_arr = array('f', [0.])

    llbar_deta_arr = array('f', [0.])
    llbar_dphi_arr = array('f', [0.])
    bbbar_deta_arr = array('f', [0.])
    bbbar_dphi_arr = array('f', [0.])

    weight_size_arr = array('i', [0])
    weight_arr = array('f', maxn*[0.])

    genpart_size_arr = array('i', [0])
    genpart_pid_arr = array('i', maxn*[0])
    genpart_status_arr = array('i', maxn*[0])

    genpart_pt_arr = array('f', maxn*[0.])
    genpart_eta_arr = array('f', maxn*[0.])
    genpart_phi_arr = array('f', maxn*[0.])
    genpart_mass_arr = array('f', maxn*[0.])

    # create the branches and assign the fill-variables to them as doubles (D)
    tree.Branch("HT", HT_arr, 'HT/D')
    tree.Branch("ST", ST_arr, 'ST/D')
    tree.Branch("MET", MET_arr, 'MET/D')

    tree.Branch("l_pt_arr", l_pt_arr, 'l_pt_arr/F')
    tree.Branch("l_eta_arr", l_eta_arr, 'l_eta_arr/F')
    tree.Branch("l_phi_arr", l_phi_arr, 'l_phi_arr/F')

    tree.Branch("sl_pt_arr", sl_pt_arr, 'sl_pt_arr/F')
    tree.Branch("sl_eta_arr", sl_eta_arr, 'sl_eta_arr/F')
    tree.Branch("sl_phi_arr", sl_phi_arr, 'sl_phi_arr/F')

    tree.Branch("ljet_pt_arr", ljet_pt_arr, 'ljet_pt_arr/F')
    tree.Branch("ljet_eta_arr", ljet_eta_arr, 'ljet_eta_arr/F')
    tree.Branch("ljet_phi_arr", ljet_phi_arr, 'ljet_phi_arr/F')

    tree.Branch("sljet_pt_arr", sljet_pt_arr, 'sljet_pt_arr/F')
    tree.Branch("sljet_eta_arr", sljet_eta_arr, 'sljet_eta_arr/F')
    tree.Branch("sljet_phi_arr", sljet_phi_arr, 'sljet_phi_arr/F')

    tree.Branch("llbar_deta_arr", llbar_deta_arr, 'llbar_deta_arr/F')
    tree.Branch("llbar_dphi_arr", llbar_dphi_arr, 'llbar_dphi_arr/F')
    tree.Branch("bbbar_deta_arr", bbbar_deta_arr, 'bbbar_deta_arr/F')
    tree.Branch("bbbar_dphi_arr", bbbar_dphi_arr, 'bbbar_dphi_arr/F')

    tree.Branch("genpart_size"  , genpart_size_arr  , "genpart_size/I")
    tree.Branch("genpart_pid"   , genpart_pid_arr   , "genpart_pid[genpart_size]/I")
    tree.Branch("genpart_status", genpart_status_arr,"genpart_status[genpart_size]/I")

    tree.Branch("weight_size", weight_size_arr, "weight_size/I")
    tree.Branch("weight"     , weight_arr     , "weight[weight_size]/F")

    tree.Branch("genpart_pt"  , genpart_pt_arr  , "genpart_pt[genpart_size]/F")
    tree.Branch("genpart_eta" , genpart_eta_arr , "genpart_eta[genpart_size]/F")
    tree.Branch("genpart_phi" , genpart_phi_arr , "genpart_phi[genpart_size]/F")
    tree.Branch("genpart_mass", genpart_mass_arr, "genpart_mass[genpart_size]/F")

    for i in range(len(HT)):
        HT_arr[0] = HT[i]
        ST_arr[0] = ST[i]
        MET_arr[0] = ET_miss[i]

        l_pt_arr[0] = l_pt[i]
        l_eta_arr[0] = l_eta[i]
        l_phi_arr[0] = l_phi[i]

        sl_pt_arr[0] = sl_pt[i]
        sl_eta_arr[0] = sl_eta[i]
        sl_phi_arr[0] = sl_phi[i]

        ljet_pt_arr[0] = ljet_pt[i]
        ljet_eta_arr[0] = ljet_eta[i]
        ljet_phi_arr[0] = ljet_phi[i]

        sljet_pt_arr[0] = sljet_pt[i]
        sljet_eta_arr[0] = sljet_eta[i]
        sljet_phi_arr[0] = sljet_phi[i]

        llbar_deta_arr[0] = llbar_deta[i]
        llbar_dphi_arr[0] = llbar_dphi[i]
        bbbar_deta_arr[0] = bbbar_deta[i]
        bbbar_dphi_arr[0] = bbbar_dphi[i]

        weight_size_arr[0]  = len(weight_sel[i])
        genpart_size_arr[0] = len(gen_pt_sel[i])

        for j in range(genpart_size_arr[0]):
            genpart_pt_arr[j] = gen_pt_sel[i][j]
            genpart_pid_arr[j] = gen_pid_sel[i][j]
            genpart_eta_arr[j] = gen_eta_sel[i][j]
            genpart_phi_arr[j] = gen_phi_sel[i][j]
            genpart_mass_arr[j] = gen_mass_sel[i][j]
            genpart_status_arr[j] = gen_status_sel[i][j]

        for k in range(weight_size_arr[0]):
            weight_arr[k] = weight_sel[i][k]

        tree.Fill()

    for i in range(len(selection)):
    	hist.Fill(i)

    # Write the tree into the output file and close the file
    opfile.Write()
    opfile.Close()


main()
