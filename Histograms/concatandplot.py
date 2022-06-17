import sys
import math
import ROOT
import uproot
import operator
import argparse
import numpy as np
from array import array
from datetime import datetime


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

fileptr = uproot.concatenate([inputFolder+'minitree_*.root:Step8'])
opfile = ROOT.TFile(outputFile, 'recreate')

htptgtpt = ROOT.TH2D('t_pt_v_gen_t_pt', 'pt vs gen pt', 1200,0,1200, 1200,0,1200 )
htetagteta = ROOT.TH2D('t_eta_v_gen_t_eta', 'eta vs gen eta', 1200,-2*np.pi,2*np.pi, 1200,-2*np.pi,2*np.pi)
htbarptgtbarpt = ROOT.TH2D('tbar_pt_v_gen_tbar_pt', 'pt vs gen pt', 1200,0,1200, 1200,0,1200 )
htbaretagtbareta = ROOT.TH2D('tbar_eta_v_gen_tbar_eta', 'eta vs gen eta', 1200,-2*np.pi,2*np.pi, 1200,-2*np.pi,2*np.pi)
httmgttm = ROOT.TH2D('ttbarmass_v_gen_ttbarmass', "mass vs gen mass", 1400, 0, 1400, 1400, 0, 1400)

for i in range(len(fileptr['top_pt'])):
    htptgtpt.Fill(fileptr['top_pt'][i], fileptr['gen_top_pt'][i])
    htetagteta.Fill(fileptr['top_eta'][i], fileptr['gen_top_eta'][i])
    htbarptgtbarpt.Fill(fileptr['atop_pt'][i], fileptr['gen_atop_pt'][i])
    htbaretagtbareta.Fill(fileptr['atop_eta'][i], fileptr['gen_atop_eta'][i])
    httmgttm.Fill(fileptr['tt_mass'][i], fileptr['gen_tt_mass'][i])

fileptr = uproot.concatenate([inputFolder+'minitree_*.root:Step7'])


h_KinReco_d_angle_jet_step7 = ROOT.TH1D("KinReco_d_angle_jet_step7", ";#alpha, rad;Entries", 200, 0, 0.5 ) 
h_KinReco_d_angle_lep_step7 = ROOT.TH1D("KinReco_d_angle_lep_step7", ";#alpha, rad;Entries", 200, 0, 0.2 )
h_KinReco_fE_jet_step7 = ROOT.TH1D("KinReco_fE_jet_step7", "Jet Energy Correction Factor;#frac{E^{true}_{jet}}{E^{reco}_{jet}};Entries", 100, 0, 4 )
h_KinReco_fE_lep_step7 = ROOT.TH1D("KinReco_fE_lep_step7", "Lepton Energy Correction Factor;#frac{E^{true}_{lep}}{E^{reco}_{lep}};Entries", 200, 0.5, 2.5 )  
h_KinReco_mbl_true_step7  = ROOT.TH1D("KinReco_mbl_true_step7","mbl_true", 100, 0, 180 )

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

    
    h_KinReco_fE_jet_step7.fill(gen_b_4vec.E()/ljet_4vec.E())
    h_KinReco_fE_jet_step7.fill(gen_ab_4vec.E()/ljet_4vec.E())
    h_KinReco_fE_jet_step7.fill(gen_b_4vec.E()/sljet_4vec.E())
    h_KinReco_fE_jet_step7.fill(gen_ab_4vec.E()/sljet_4vec.E())

    h_KinReco_fE_lep_step7.fill(gen_lep_4vec.E()/lep_4vec.E())
    h_KinReco_fE_lep_step7.fill(gen_alep_4vec.E()/alep_4vec.E())


    h_KinReco_d_angle_jet_step7.fill(gen_b_4vec.Angle(sljet_4vec.Vect()))
    h_KinReco_d_angle_jet_step7.fill(gen_b_4vec.Angle(ljet_4vec.Vect()))
    h_KinReco_d_angle_jet_step7.fill(gen_ab_4vec.Angle(sljet_4vec.Vect()))
    h_KinReco_d_angle_jet_step7.fill(gen_ab_4vec.Angle(ljet_4vec.Vect()))

    h_KinReco_d_angle_lep_step7.fill(gen_lep_4vec.Angle(lep_4vec.Vect()))
    h_KinReco_d_angle_lep_step7.fill(gen_alep_4vec.Angle(alep_4vec.Vect()))

    h_KinReco_mbl_true_step7.fill((gen_alep_4vec + gen_b_4vec).M())
    h_KinReco_mbl_true_step7.fill((gen_lep_4vec + gen_ab_4vec).M())
    

h_KinReco_fE_jet_step7.Write()  


opfile.Write()
opfile.Close()
