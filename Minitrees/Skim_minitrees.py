
import sys
import math
import ROOT
import uproot
import operator
import argparse
import numpy as np
from array import array
from datetime import datetime

def deltaphi(e_phi, m_phi) :
    d_phi =  e_phi - m_phi
    if (d_phi >  np.pi) : d_phi -= 2*np.pi
    if (d_phi < -np.pi) : d_phi += 2*np.pi
    return d_phi

def dR(e_phi, e_eta, m_phi, m_eta) :
    d_eta = abs(e_eta - m_eta)
    d_phi = deltaphi(e_phi, m_phi)
    return np.sqrt(d_phi**2 + d_eta**2)

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Input  Delphes Ntuple location')
parser.add_argument('-o', '--output', help='Output Delphes Minitree location')

args       = parser.parse_args()
inputFile  = args.input
outputFile = args.output

tt_ptr = uproot.open(inputFile)['Step8']

# Gen part info
genpt     = tt_ptr['genpart_pt'].array()
geneta    = tt_ptr['genpart_eta'].array()
genphi    = tt_ptr['genpart_phi'].array()
genpid    = tt_ptr['genpart_pid'].array()
genmass   = tt_ptr['genpart_mass'].array()
genstatus = tt_ptr['genpart_status'].array()

# Storing the reconstructed as arrays
gen_l_pt   = []
gen_l_phi  = []
gen_l_eta  = []
gen_l_mass = []

gen_al_pt   = []
gen_al_phi  = []
gen_al_eta  = []
gen_al_mass = []

gen_top_pt  = []
gen_top_eta = []
gen_top_phi = []
gen_top_mass= []

gen_atop_pt  = []
gen_atop_eta = []
gen_atop_phi = []
gen_atop_mass= []

#Loop over the events 
for i in range(len(genpt)) :
  
    l_count  = 0
    al_count = 0
    l_index  = 0
    al_index = 0

    b_count    = 0 
    bbar_count = 0  
    
    # Find the ltons and store their indices
    for j in range(len(genpid[i]) - 1) :

        '''
        if ((genpid[i][j] ==  5)  and (genstatus[i][j] ==  52) and (b_count == 0) ) :
            b_index  = j
            b_count += 1
            
        elif((genpid[i][j] == -5) and (genstatus[i][j] ==  52) and (bbar_count == 0)) :       
            bbar_index  = j
            bbar_count += 1
        '''
        
        if  ( ((genpid[i][j] == 11)  or (genpid[i][j] ==  13) or (genpid[i][j] ==  15)) and ((genpid[i][j+1] == -12) or (genpid[i][j+1] == -14) or (genpid[i][j+1] == -16)) and (l_count == 0)) :
            l_index  = j
            l_count += 1
            
        elif( ((genpid[i][j] == -11) or (genpid[i][j] == -13) or (genpid[i][j] == -15)) and ((genpid[i][j+1] ==  12) or (genpid[i][j+1] ==  14) or (genpid[i][j+1] == 16))  and (al_count == 0)) :       
            al_index  = j
            al_count += 1
            
        else : continue
            
    # Dilton        
    if ( (l_count == 0 or al_count == 0) and (l_index == 0 or al_index  == 0) ): continue  

    '''
    # Jet cuts
    if (genpt[i][b_index]  <  30 or genpt[i][bbar_index]  <  30) : continue
    if (geneta[i][b_index] > 2.4 or geneta[i][bbar_index] > 2.4) : continue        
    
    if ((dR (genphi[i][l_index] , geneta[i][l_index] , genphi[i][b_index]   , geneta[i][b_index]    ) < 0.4)
    or  (dR (genphi[i][al_index], geneta[i][al_index], genphi[i][b_index]   , geneta[i][b_index]    ) < 0.4)
    or  (dR (genphi[i][l_index] , geneta[i][l_index] , genphi[i][bbar_index], geneta[i][bbar_index] ) < 0.4)
    or  (dR (genphi[i][al_index], geneta[i][al_index], genphi[i][bbar_index], geneta[i][bbar_index] ) < 0.4) ) : continue 
    '''

    #DR cut
    if(dR(genphi[i][l_index], geneta[i][l_index], genphi[i][al_index], geneta[i][al_index]) < 0.4):
        continue


    #ltons
    gen_l_pt.append(genpt[i][l_index])
    gen_l_phi.append(genphi[i][l_index])
    gen_l_eta.append(geneta[i][l_index])
    gen_l_mass.append(genmass[i][l_index])  
    
    #Anti-lton
    gen_al_pt.append(genpt[i][al_index])
    gen_al_phi.append(genphi[i][al_index])
    gen_al_eta.append(geneta[i][al_index])  
    gen_al_mass.append(genmass[i][al_index])  
    
    # Tops
    gen_top_pt.append(genpt[i][2])
    gen_top_eta.append(geneta[i][2])
    gen_top_phi.append(genphi[i][2])
    gen_top_mass.append(genmass[i][2])

    # Anti-tops
    gen_atop_pt.append(genpt[i][3])
    gen_atop_eta.append(geneta[i][3])
    gen_atop_phi.append(genphi[i][3])
    gen_atop_mass.append(genmass[i][3])


# Empty arrays that get mapped to histograms in a root file

gen_top_pt_arr  = array('f', [0.])
gen_top_eta_arr = array('f', [0.])
gen_top_phi_arr = array('f', [0.])
gen_top_mass_arr = array('f', [0.])

gen_atop_pt_arr  = array('f', [0.])
gen_atop_eta_arr = array('f', [0.])
gen_atop_phi_arr = array('f', [0.])
gen_atop_mass_arr = array('f', [0.])

gen_l_pt_arr   = array('f', [0.])
gen_l_eta_arr  = array('f', [0.])
gen_l_phi_arr  = array('f', [0.])
gen_l_mass_arr = array('f', [0.])

gen_al_pt_arr   = array('f', [0.])
gen_al_eta_arr  = array('f', [0.])
gen_al_phi_arr  = array('f', [0.])
gen_al_mass_arr = array('f', [0.])

opfile = ROOT.TFile(outputFile, 'recreate')
tree   = ROOT.TTree("Step8", "Step8")


# Tops and nus
tree.Branch("gen_top_pt" , gen_top_pt_arr , 'gen_top_pt/F')
tree.Branch("gen_top_eta", gen_top_eta_arr, 'gen_top_eta/F')
tree.Branch("gen_top_phi", gen_top_phi_arr, 'gen_top_phi/F')
tree.Branch("gen_top_mass", gen_top_mass_arr, 'gen_top_mass/F')

tree.Branch("gen_atop_pt" , gen_atop_pt_arr , 'gen_atop_pt/F')
tree.Branch("gen_atop_eta", gen_atop_eta_arr, 'gen_atop_eta/F')
tree.Branch("gen_atop_phi", gen_atop_phi_arr, 'gen_atop_phi/F')
tree.Branch("gen_atop_mass", gen_atop_mass_arr, 'gen_atop_mass/F')

tree.Branch("gen_l_pt" , gen_l_pt_arr , 'gen_l_pt/F')
tree.Branch("gen_l_eta", gen_l_eta_arr, 'gen_l_eta/F')
tree.Branch("gen_l_phi", gen_l_phi_arr, 'gen_l_phi/F')
tree.Branch("gen_l_mass", gen_l_mass_arr, 'gen_l_mass/F')

tree.Branch("gen_al_pt" , gen_al_pt_arr , 'gen_al_pt/F')
tree.Branch("gen_al_eta", gen_al_eta_arr, 'gen_al_eta/F')
tree.Branch("gen_al_phi", gen_al_phi_arr, 'gen_al_phi/F')
tree.Branch("gen_al_mass", gen_al_mass_arr, 'gen_al_mass/F')

for i in range(len(gen_top_pt)):

    gen_top_pt_arr[0]  = gen_top_pt[i]
    gen_top_eta_arr[0] = gen_top_eta[i]
    gen_top_phi_arr[0] = gen_top_phi[i]
    gen_top_mass_arr[0] = gen_top_mass[i]

    gen_atop_pt_arr[0]  = gen_atop_pt[i]
    gen_atop_eta_arr[0] = gen_atop_eta[i]
    gen_atop_phi_arr[0] = gen_atop_phi[i]
    gen_atop_mass_arr[0] = gen_atop_mass[i]

    gen_l_pt_arr[0]   = gen_l_pt[i]
    gen_l_eta_arr[0]  = gen_l_eta[i]
    gen_l_phi_arr[0]  = gen_l_phi[i]
    gen_l_mass_arr[0] = gen_l_mass[i]

    gen_al_pt_arr[0]   = gen_al_pt[i]
    gen_al_eta_arr[0]  = gen_al_eta[i]
    gen_al_phi_arr[0]  = gen_al_phi[i]
    gen_al_mass_arr[0] = gen_al_mass[i]

    tree.Fill()

# Write the tree into the output file and close the file
opfile.Write()
opfile.Close()