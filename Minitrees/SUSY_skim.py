#!/usr/bin/python

# This script works with ntuples produced using the Delphes Ntuplizer found at :
# https://github.com/recotoolsbenchmarks/DelphesNtuplizer/blob/master/bin/Ntuplizer.py
#                   Author : Amandeep Singh Bakshi

import ROOT
import uproot

# Delta Phi the right way
def deltaphi(e_phi, m_phi) :
  d_phi =  e_phi - m_phi
  if (d_phi >  np.pi) : d_phi -= 2*np.pi
  if (d_phi < -np.pi) : d_phi += 2*np.pi
  return d_phi

# dR between leptons
def dR(e_phi, e_eta, m_phi, m_eta) :
    d_eta = abs(e_eta - m_eta)
    d_phi = deltaphi(e_phi, m_phi)
    return np.sqrt(d_phi**2 + d_eta**2)

# Selection 
def skim(chain) :

    #Loop over the events 
    for i in range(len(jet_PUPPI_pt)) :         
    	# Temporary variables
    
    	e_idx     = []
    	mu_idx    = []

    	ef_idx    = []
    	muf_idx   = []
    
    	jet_idx   = []
    
    	btag_cnt  = 0
    
    	e_4vec    = ROOT.TLorentzVector()
    	mu_4vec   = ROOT.TLorentzVector()
    
    	########## Electrons ########## 
    
    	# Ensure pt > 20 GeV and eta < 2.4 and isolation
    	for j in range(len(electron_CHS_pt[i])) :
        	if (electron_CHS_pt[i][j]  < 20) : continue
          
        	if (electron_CHS_eta[i][j] > 2.4 or (electron_CHS_eta[i][j] > 1.4442 and electron_CHS_eta[i][j] < 1.5660)) : continue
          
        	if (electron_CHS_iso[i][j] < 0.0588) : continue
          
        	e_idx.append(j)

    	###########  Muons ############ 
    
    	# Ensure pt > 20 GeV and eta < 2.4 and isolation        
    	for j in range(len(muon_CHS_pt[i])) :            
        	if (muon_CHS_pt[i][j]  < 20 ) : continue
          
        	if (muon_CHS_eta[i][j] > 2.4) : continue
          
        	if (muon_CHS_iso[i][j] < 0.15): continue 
          
        	mu_idx.append(j)
    
    	# Ensure atleast one muon and one electron
    	if (len(e_idx) == 0 or len(mu_idx) == 0) : continue
    
    	# Check for opp sign charge pairings
    	for j in range(len(e_idx)) :
      	    for k in range(len(mu_idx)) :
       		if (electron_CHS_charge[i][j] * muon_CHS_charge[i][k] == -1):
          	    ef_idx.append(j)
          	    muf_idx.append(k)
    
    	# Ensure such a pairing exists     
    	if (len(ef_idx) == 0 or len(muf_idx) == 0): continue
    
    	# Assign leading indices to e and mu
    	e_index  = ef_idx[0]
    	mu_index = muf_idx[0]
    
    	# Defining the 4 vectors
    	e_4vec.SetPtEtaPhiM(electron_CHS_pt[i][e_index], electron_CHS_eta[i][e_index], electron_CHS_phi[i][e_index], 0.000511)
    	mu_4vec.SetPtEtaPhiM(muon_CHS_pt[i][mu_index]  , muon_CHS_eta[i][mu_index]   , muon_CHS_phi[i][mu_index]   , 0.105)
        
    	# Mll cut (Step 3 according to the FW)
    	if ((e_4vec + mu_4vec).M() < 20) : continue  
        
    	###########  Jets ###############

    	for j in range(len(jet_PUPPI_pt[i])) :
      
        # Ensure pt > 30 GeV and eta < 2.4 isolation 
        
        	if ((dR (electron_CHS_phi[i][e_index], electron_CHS_eta[i][e_index], jet_PUPPI_phi[i][j] , jet_PUPPI_eta[i][j] ) < 0.4)
        	or  (dR (muon_CHS_phi[i][mu_index]   , muon_CHS_eta[i][mu_index]   , jet_PUPPI_phi[i][j] , jet_PUPPI_eta[i][j] ) < 0.4)) : continue

        	if ( (jet_PUPPI_pt [i][j]  < 30))     : continue
          
        	if ((abs(jet_PUPPI_eta[i][j]) > 2.4)) : continue
        
        	if (jet_PUPPI_btag[i][j] != 0)        : btag_cnt += 1
            
        	jet_idx.append(j)
      
    	# 2 Jets (Step 5 according to the FW) 
    	if(len(jet_idx) < 2) : continue
      
    	# Atleast one b-tag 
    	if (btag_cnt == 0)   : continue    
    
    	ljet_idx  = jet_idx[0]
    	sljet_idx = jet_idx[1]

    	####### Fill the arrays ##########
    
    	# Leading and sub-leading lepton pts
    	if (electron_CHS_pt[i][e_index] > muon_CHS_pt[i][mu_index] and electron_CHS_pt[i][e_index] > 25) :
            l_pt.append(electron_CHS_pt[i][e_index])
            l_phi.append(electron_CHS_phi[i][e_index])
            l_eta.append(electron_CHS_eta[i][e_index])

            sl_pt.append(muon_CHS_pt[i][mu_index])
            sl_phi.append(muon_CHS_phi[i][mu_index])
            sl_eta.append(muon_CHS_eta[i][mu_index])

        elif (muon_CHS_pt[i][mu_index] > electron_CHS_pt[i][e_index] and muon_CHS_pt[i][mu_index] > 25) :
            sl_pt.append(electron_CHS_pt[i][e_index])
            sl_phi.append(electron_CHS_phi[i][e_index])
            sl_eta.append(electron_CHS_eta[i][e_index])

            l_pt.append(muon_CHS_pt[i][mu_index])
            l_phi.append(muon_CHS_phi[i][mu_index])
            l_eta.append(muon_CHS_eta[i][mu_index])
    
        else : continue
    
        # Leading and Subleading Pt
        ljet_pt.append(jet_PUPPI_pt[i][ljet_idx])
        ljet_phi.append(jet_PUPPI_phi[i][ljet_idx])
        ljet_eta.append(jet_PUPPI_eta[i][ljet_idx])
        ljet_mass.append(jet_PUPPI_eta[i][ljet_idx])

        sljet_pt.append(jet_PUPPI_pt[i][sljet_idx])
        sljet_phi.append(jet_PUPPI_phi[i][sljet_idx]) 
        sljet_eta.append(jet_PUPPI_eta[i][sljet_idx]) 
        sljet_mass.append(jet_PUPPI_eta[i][sljet_idx])        
    
        e_pt.append(electron_CHS_pt[i][e_index])
        mu_pt.append(muon_CHS_pt[i][mu_index])
    
        ET_miss.append(met_pt[i][0])
    

# Main, read ip tree and op final skimmed version    
def main() :

    # Input files and trees
    inputFile       = ROOT.TFile('SUSY_Ntuple_200.root', 'OPEN')
    chain           = ROOT.TChain()
    chain.Add('SUSY_Ntuple_200.root/Delphes_Ntuples')

    # Declare new tree and file
    new_file        =  ROOT.TFile('SUSY_Skimmed_200.root','RECREATE')
    new_tree        =  chain.CloneTree(0)

    numberOfEntries =  chain.GetEntries()

    # Useful counters
    n_skim          =  0

    ################ Start event loop #######################

    for i_event in range(0, numberOfEntries):
        i_entry = chain.LoadTree(i_event)
        chain.GetEntry(i_event)

        if i_event % 1000 == 0:
            print('Processing event %i of %i' % (i_event, numberOfEntries))

        passed_skim = skim(chain)
        if passed_skim :
                new_tree.Fill()
                n_skim += 1

    inputFile.Close()
    new_tree.AutoSave()
    new_file.Close()

    print('Processed events : %i, of which %i passed ' %(numberOfEntries, n_skim))
main()
