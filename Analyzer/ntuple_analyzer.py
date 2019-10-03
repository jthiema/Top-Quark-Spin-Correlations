import math
import ROOT
from   ROOT    import kRed
from ratioplot import ratioplot



def dR(lepton1,lepton2) :
       deltaEta = abs(lepton1.Eta() - lepton2.Eta())
       deltaPhi = abs(lepton1.Phi() - lepton2.Phi())
       dR = math.sqrt(deltaEta**2 + deltaPhi**2)
       return dR

def main():

    file_name     = ROOT.TFile('output_ntuple.root')
    tree_name     = file_name.Get("Delphes_Ntuples/Delphes_Ntuples")
    treeReader    = ROOT.TTreeReader(tree_name)

    # Relevant TLorentzVectors
    # Needed for top reconstruction

    TL_muon       = ROOT.TLorentzVector()
    TL_elec       = ROOT.TLorentzVector()
    TL_jet        = ROOT.TLorentzVector()
    TL_gen_lep    = ROOT.TLorentzVector()
    TL_gen_jet    = ROOT.TLorentzVector()

    # Reconstructed information
   
    # Muons 
    b_muon_pt     = ROOT.TTreeReaderArray(float)(treeReader,'muon_pt')
    b_muon_eta    = ROOT.TTreeReaderArray(float)(treeReader,'muon_eta') 
    b_muon_phi    = ROOT.TTreeReaderArray(float)(treeReader,'muon_phi')
    b_muon_mass   = ROOT.TTreeReaderArray(float)(treeReader,'muon_mass')
    b_muon_charge = ROOT.TTreeReaderArray(int)(treeReader,'muon_charge')

    # Electrons 
    b_elec_pt     = ROOT.TTreeReaderArray(float)(treeReader,'elec_pt')
    b_elec_eta    = ROOT.TTreeReaderArray(float)(treeReader,'elec_eta')
    b_elec_phi    = ROOT.TTreeReaderArray(float)(treeReader,'elec_phi')
    b_elec_mass   = ROOT.TTreeReaderArray(float)(treeReader,'elec_mass')
    b_elec_charge = ROOT.TTreeReaderArray(int)(treeReader,'elec_charge')

    # Jets
    b_jet_pt      = ROOT.TTreeReaderArray(float)(treeReader,'jet_pt')
    b_jet_eta     = ROOT.TTreeReaderArray(float)(treeReader,'jet_eta')
    b_jet_phi     = ROOT.TTreeReaderArray(float)(treeReader,'jet_phi')
    b_jet_mass    = ROOT.TTreeReaderArray(float)(treeReader,'jet_mass')
    b_jet_btag    = ROOT.TTreeReaderArray(int)(treeReader,'jet_btag')

    # MET 
    b_met_pt      = ROOT.TTreeReaderArray(float)(treeReader,'met_pt')
 
    # Weights
    b_weight      = ROOT.TTreeReaderArray(float)(treeReader,'weight')


    # Generator level information

    # Gen Particles
    b_gen_part_pt     = ROOT.TTreeReaderArray(float)(treeReader,'genpart_pt')
    b_gen_part_eta    = ROOT.TTreeReaderArray(float)(treeReader,'genpart_eta')
    b_gen_part_phi    = ROOT.TTreeReaderArray(float)(treeReader,'genpart_phi')
    b_gen_part_mass   = ROOT.TTreeReaderArray(float)(treeReader,'genpart_mass')
    b_gen_part_charge = ROOT.TTreeReaderArray(float)(treeReader,'genpart_charge')
    b_gen_part_pid    = ROOT.TTreeReaderArray(int)(treeReader,'genpart_pid')

    # Gen Jets
    b_gen_jet_pt      = ROOT.TTreeReaderArray(float)(treeReader,'genjet_pt')
    b_gen_jet_eta     = ROOT.TTreeReaderArray(float)(treeReader,'genjet_eta')
    b_gen_jet_phi     = ROOT.TTreeReaderArray(float)(treeReader,'genjet_phi')
    b_gen_jet_mass    = ROOT.TTreeReaderArray(float)(treeReader,'genjet_mass')


    #Relevant Histograms

    # Renormalization Scale Variations
 
    hist_list  = []
    hist_names = []


    for i in range(0, 9):

        hist_name   = 'Delta_Phi_Renorm_variation_' + str(i)
        hist_names.append(hist_name)     # List of names

        hist_root   = ROOT.TH1F(hist_name, hist_name, 20, 0, 3.14159)
        hist_list.append(hist_root)      # List of ROOT TH1F Objects 

    # PDF Variations 

    for i in range(9, 110):

        hist_name   = 'Delta_Phi_PDF_variation_' + str(i)
        hist_names.append(hist_name)     # List of names

        hist_root   = ROOT.TH1F(hist_name, hist_name, 20, 0, 3.14159)
        hist_list.append(hist_root)      # List of ROOT TH1F Objects 


    loop_count    = 0

    while(treeReader.Next()):

        nb            = 0                # Number of B-Tags
    	jet_arr       = []               # Jet 4 vector Array
    	lepton_arr    = []		 # Lepton 4 vector Array
        lepton_charge = []               # Lepton Charge 
	w_sum         = 0                # Sum of weights per event

        loop_count   += 1

        if (loop_count % 1000 == 0):
        	print('Processing event %d' %(loop_count))

        ############### LEPTONS ###################

	# Loop over all leaves in parallel for Muons 
        for pt, eta, phi, m, charge in zip(b_muon_pt, b_muon_eta, b_muon_phi, b_muon_mass, b_muon_charge):

            #Apply the selection for leptons
	    if (pt > 30 and abs(eta) < 2.5) :            
               TL_muon.SetPtEtaPhiM(pt, eta, phi, m)        
     	       lepton_arr.append(TL_muon)
	       lepton_charge.append(charge)


        #Loop over leaves in parallel for Electrons
        for pt, eta, phi, m, charge in zip(b_elec_pt, b_elec_eta, b_elec_phi, b_elec_mass, b_elec_charge):

            #Apply the selection for leptons
            if (pt > 30 and abs(eta) < 2.5) :
               TL_elec.SetPtEtaPhiM(pt, eta, phi, m) 
               lepton_arr.append(TL_elec)
	       lepton_charge.append(charge)


        # 2 Leptons and Lepton dR cut
        if (len(lepton_arr) == 2):
           lepton1 = lepton_arr[0]
           lepton2 = lepton_arr[1]
           if (dR(lepton1,lepton2) < 0.2 ) : continue

        else : continue
        
    	#Opposite Sign cut
    	if (lepton_charge[0] * lepton_charge[1] != -1) : continue

        # Invariant mass cut
    	Mll = (lepton1 + lepton2).M()
    	if ( not ((Mll < 76 or Mll > 106) and Mll > 40)) : continue


        ############## JETS #####################
        
        # Loop over all leaves in parallel for Jets 
        for pt, eta, phi, m, btag in zip(b_jet_pt, b_jet_eta, b_jet_phi, b_jet_mass, b_jet_btag):

            #Apply the selection for jets + btagging criteria
            if (pt > 30 and abs(eta) < 2.5) :
               TL_jet.SetPtEtaPhiM(pt, eta, phi, m)
               jet_arr.append(TL_jet)
	       if (btag == 1) : nb += 1
    	
        if (len(jet_arr) > 1 and nb > 0):                       ## Sort by pt, maybe ?
            jet1 = jet_arr[0]
            jet2 = jet_arr[1]
        else : continue

        ############# MET #####################

        for met in b_met_pt :
            if ( met < 40 ) : continue

        ######## Delta Phi Filling ############

        delta_phi = abs(lepton1.DeltaPhi(lepton2)) 

        for i in range(0,110):
	    w_sum +=  b_weight[i]

     
        for h, i in zip(hist_list, range(0,110)):
	    h.Fill(delta_phi, (b_weight[i]/w_sum))

        ####### End Reconstructed Objects #####

    for h, hist_name in zip(hist_list, hist_names) :
    	C_file_loc    = 'Plots/' + hist_name + '.C'
    	h.Draw("ep")
    	h.SaveAs(C_file_loc)
    
    print('Done generating Delta Phi Variations, please check plots directory')  

'''

    c = ROOT.TCanvas("c","c",600,600)
    c.cd()
    h_delta_phi_reco_vis.Draw("ep")
    h_delta_phi_reco_vis.SaveAs("Delta_Phi_reco_vis.C")
    c.SaveAs("Delta_Phi_reco_vis.pdf")


    print('Done processing Reco Objects now moving to Gen Objects ')


    loop_count  = 0 


    ###### Generator level now ###########

    while(treeReader.Next()):

        gen_lep_count  = 0
        gen_jet_count  = 0
        gen_lep_charge = []

        loop_count   += 1

        if (loop_count % 1000 == 0):
                print('Processing event %d' %(loop_count))

        if (loop_count == 10000) : break

        ############### GEN LEPTONS ###################
       
        for pt, eta, charge, pid in zip(b_gen_part_pt, b_gen_part_eta, b_gen_part_charge, b_gen_part_pid):

            if ((abs(pid) == 11 or abs(pid) == 13) and pt > 30 and abs(eta) < 2.5) :
               gen_lep_count += 1 
               gen_lep_charge.append(charge)
               	
        # 2 Leptons and Lepton dR cut
        if (gen_lep_count != 2): continue

        #Opposite Sign cut
        if (gen_lep_charge[0] * gen_lep_charge[1] != -1.0) : continue

        ############## GEN JETS #######################

        for pt, eta in zip(b_gen_jet_pt, b_gen_jet_eta):
            if (pt > 30 and abs(eta) < 2.5) :
		gen_jet_count += 1

        if (gen_jet_count == 0) : continue

        ######## Delta Phi Filling ############

        deltaphi = lepton1.DeltaPhi(lepton2)
        h_delta_phi_gen_vis.Fill(deltaphi)


    c1 = ROOT.TCanvas("c1","c1",600,600)
    c1.cd()
    h_delta_phi_gen_vis.Draw("ep")
    h_delta_phi_gen_vis.SaveAs("Delta_Phi_gen_vis.C")
    c1.SaveAs("Delta_Phi_gen_vis.pdf")


    c2 = ROOT.TCanvas("c","c",600,600)
    c2.cd()
    h_delta_phi_reco_vis.Draw("ep")
    h_delta_phi_reco_vis.SetLineColor(kRed)
    h_delta_phi_gen_vis.Draw("same")
    ratioplot(h_delta_phi_reco_vis, h_delta_phi_gen_vis)
    raw_input("Press Enter to continue...")

'''
if __name__ == '__main__':
   main()
