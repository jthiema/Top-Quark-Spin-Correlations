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

fileptr = uproot.concatenate([inputFolder+'topreco_*.root:Step8'])
opfile = ROOT.TFile(outputFile, 'recreate')

htptgtpt = ROOT.TH2D('t_pt_v_gen_t_pt', 'pt vs gen pt', 1200,0,1200, 1200,0,1200 )
htetagteta = ROOT.TH2D('t_eta_v_gen_t_eta', 'eta vs gen eta', 1200,-2*np.pi,2*np.pi, 1200,-2*np.pi,2*np.pi)
htbarptgtbarpt = ROOT.TH2D('tbar_pt_v_gen_tbar_pt', 'pt vs gen pt', 1200,0,1200, 1200,0,1200 )
htbaretagtbareta = ROOT.TH2D('tbar_eta_v_gen_tbar_eta', 'eta vs gen eta', 1200,-2*np.pi,2*np.pi, 1200,-2*np.pi,2*np.pi)
httmgttm = ROOT.TH2D('ttbarmass_v_gen_ttbarmass', "mass vs gen mass", 1400, 0, 1400, 1400, 0, 1400)

for i in range(len(fileptr['t_pt'])):
    htptgtpt.Fill(fileptr['t_pt'][i], fileptr['gen_t_pt'][i])
    htetagteta.Fill(fileptr['t_eta'][i], fileptr['gen_t_eta'][i])
    htbarptgtbarpt.Fill(fileptr['tbar_pt'][i], fileptr['gen_tbar_pt'][i])
    htbaretagtbareta.Fill(fileptr['tbar_eta'][i], fileptr['gen_tbar_eta'][i])
    httmgttm.Fill(fileptr['tt_mass'][i], fileptr['gen_tt_mass'][i])

opfile.Write()
opfile.Close()
