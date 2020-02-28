# This script works with ntuples produced using the Delphes Ntuplizer found at :
# https://github.com/recotoolsbenchmarks/DelphesNtuplizer/blob/master/bin/Ntuplizer.py
# 		    Author : Amandeep Singh Bakshi

import math
import ROOT

from math import sqrt, pow, cos, sin, atan

# Delta R between the two leptons

def dR(lepton1,lepton2) :
       deltaEta = abs(lepton1.Eta() - lepton2.Eta())
       deltaPhi = abs(lepton1.Phi() - lepton2.Phi())
       dR = sqrt(deltaEta**2 + deltaPhi**2)
       return dR

#Get theta effective mixing for a given top polarization hypothesis
#The result also depends on the stop, top and chi0 mass hypotheses
#Also valid for an off-shell scenario

def GetThetaMixingangle(topPol, m_stop, m_top, m_chi0) :
      p_chi0 = sqrt( pow(m_top*m_top + m_chi0*m_chi0 - m_stop*m_stop,2)/4 - pow(m_top*m_chi0 , 2) ) / m_stop
      e_chi0 = sqrt( p_chi0*p_chi0 + m_chi0*m_chi0 )
      sqrPol = 0
      if (abs(topPol) < 1) : 
	 sqrPol   =   sqrt(1 - topPol*topPol)
      tanThetaEff = ( p_chi0*sqrPol - m_chi0*topPol) / (topPol*e_chi0 + p_chi0)
      return atan(tanThetaEff)


#Get the top polarization given an effective theta mixing hypothesis
#The result also depends on the stop, top and chi0 mass hypotheses
#Also valid for an off-shell scenario

def GetTopPolarization(thetaMixing, m_stop, m_top, m_chi0) :
      p_chi0 = sqrt( pow(m_top*m_top + m_chi0*m_chi0 - m_stop*m_stop,2)/4 - pow(m_top*m_chi0 , 2) ) / m_stop
      e_chi0 = sqrt( p_chi0*p_chi0 + m_chi0*m_chi0)
      pol    = p_chi0 * cos(2*thetaMixing) / (e_chi0 + m_chi0*sin(2*thetaMixing))
      return pol

# The following reweighting makes sense in all cases (OFF-SHELL CASE TOO)
# It assumes isotropy for the reference MC and any SUSY scenario as target
# (via a thetaMixingTarget input)

def GetWeight(thetaMixingTarget, top_arr, lep_arr, chi0_arr, m_top, m_chi0) :
 
    weight      = 1
    TOPMASS_REF = 175

    for i in range(2) :
    	cX        = cos(thetaMixingTarget)
    	sX        = sin(thetaMixingTarget)
    	coeffTop  = 2*sX*sX*(chi0_arr[i] * top_arr[i]) + 2*sX*cX *(m_chi0 * TOPMASS_REF)
    	coeffChi  = pow(cX*TOPMASS_REF, 2) - pow(sX*m_top, 2)
    	coeffNorm = (chi0_arr[i] * top_arr[i]) * (sX*sX + cX*cX*pow(TOPMASS_REF/m_top, 2)) + 2*sX*cX*( m_chi0*TOPMASS_REF )
    	weight   *= (coeffTop* (lep_arr[i] * top_arr[i]) + coeffChi*(lep_arr[i] * chi0_arr[i])) / (coeffNorm*(lep_arr[i] * top_arr[i]))

    return weight

def main():

    file_name     = ROOT.TFile('SUSY_no_spin.root')
    tree_name     = file_name.Get("Delphes_Ntuples")
    treeReader    = ROOT.TTreeReader(tree_name)

    # Gen Particles
    b_gen_part_pt     = ROOT.TTreeReaderArray(float)(treeReader,'genpart_pt')
    b_gen_part_eta    = ROOT.TTreeReaderArray(float)(treeReader,'genpart_eta')
    b_gen_part_phi    = ROOT.TTreeReaderArray(float)(treeReader,'genpart_phi')
    b_gen_part_mass   = ROOT.TTreeReaderArray(float)(treeReader,'genpart_mass')
    b_gen_part_m1     = ROOT.TTreeReaderArray(int)(treeReader,'genpart_m1')
    b_gen_part_pid    = ROOT.TTreeReaderArray(int)(treeReader,'genpart_pid')
    b_gen_part_stat   = ROOT.TTreeReaderArray(int)(treeReader,'genpart_status')

    # Histograms
    h_delta_phi_SUSY  = ROOT.TH1F('SUSY Delta Phi', 'SUSY Delta Phi', 20, 0, 3.14159)
    h_delta_phi_weigh = ROOT.TH1F('SUSY Delta Phi Weighted', 'SUSY Delta Phi Weighted', 20, 0, 3.14159)
    loop_count  = 0

    while(treeReader.Next()):

        loop_count    += 1

	if (loop_count % 1000 == 0) :
		print('Processing event :: %d' %(loop_count))	

	if (loop_count == 300000 ) : break

        # Declare relevant arrays
        lep_arr    = []
        top_arr    = []
        chi0_arr   = []

        ############### GEN LEPTONS ###################
       
        for pt, eta, mass, pid, phi, status in zip(b_gen_part_pt, b_gen_part_eta, b_gen_part_mass, b_gen_part_pid, b_gen_part_phi, b_gen_part_stat):

	    # Identify the stop 
	    if (abs(pid)  == 1000006 and status == 62):
	       print(pid, mass)
	       m_stop   = mass
 
	    # Identify the top quark
            elif (abs(pid) == 6) : 
	       m_top    = mass
	       TL_top   =  ROOT.TLorentzVector()
	       TL_top.SetPtEtaPhiM(pt, eta, phi, mass)   		
	       top_arr.append(TL_top)

	    # Identify the W decay fermions		
            elif ( (pid == -11  or pid == - 13) and pt > 30 and status == 23) :
	       TL_lep   = ROOT.TLorentzVector()
	       TL_lep.SetPtEtaPhiM(pt, eta, phi, mass)
	       lep_arr.append(TL_lep)

            elif ( (pid == 11  or pid == 13) and pt > 30 and status == 23) :
               TL_lep   = ROOT.TLorentzVector()
               TL_lep.SetPtEtaPhiM(pt, eta, phi, mass)
               lep_arr.append(TL_lep)

	    # Identify the chi0 neutralino
   	    elif (abs(pid)  == 1000022) :
	       m_chi0   = mass
	       TL_chi0  = ROOT.TLorentzVector()
	       TL_chi0.SetPtEtaPhiM(pt, eta, phi, mass)
	       chi0_arr.append(TL_chi0)

	if ( (len(chi0_arr) > 1) and (len(top_arr) > 1) and (len(lep_arr) > 1) ):
	    lepton1     = lep_arr[0]
	    lepton2     = lep_arr[1]
            delta_phi   = lepton1.DeltaPhi(lepton2)

            # Set Polarization to zero for now
	    thetaMixing = GetThetaMixingangle(0, m_stop , m_top, m_chi0)
	    weight      = GetWeight(thetaMixing, top_arr, lep_arr, chi0_arr, m_top, m_chi0)     
	
	    h_delta_phi_SUSY.Fill(delta_phi)
	    h_delta_phi_weigh.Fill(delta_phi, weight)

        else : continue

    c1 = ROOT.TCanvas("c1","c1",600,600)
    c1.cd()
    h_delta_phi_SUSY.Draw('histsame')
    h_delta_phi_weigh.SetLineColor(ROOT.kRed)
    h_delta_phi_weigh.Draw('histsame')
    raw_input('Press Enter to continue ::')
    '''
        gen_ferm_arr =  sorted(gen_ferm_arr, key=ROOT.TLorentzVector.Pt, reverse = True)         

        #Opposite Sign cut
        if (gen_lep_charge[0] * gen_lep_charge[1] != -1.0) : continue
	
	# 2 Leptons
	if (len(gen_lep_arr) >= 2) :
	   lepton1  = gen_lep_arr[0]
           lepton2  = gen_lep_arr[1]
           if (dR(lepton1, lepton2) < 0.2 ) : continue

	else : continue
        
        print('Made it ')

        ############## GEN JETS #######################

        #for pt, eta in zip(b_gen_jet_pt, b_gen_jet_eta):
            #if (pt > 30 and abs(eta) < 2.5) :
                #gen_jet_count += 1

        #if (gen_jet_count == 0) : continue	
	
        ######## Delta Phi Filling ############

        deltaphi = lepton1.DeltaPhi(lepton2)
        h_delta_phi_gen_vis.Fill(deltaphi)
	

    c1 = ROOT.TCanvas("c1","c1",600,600)
    c1.cd()
    h_delta_phi_gen_vis.Draw("ep")
    h_delta_phi_gen_vis.SaveAs("Delta_Phi_gen_vis.C")
    '''
main()
