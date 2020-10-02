#!/usr/bin/python

# This script works with ntuples produced using the Delphes Ntuplizer found at :
# https://github.com/recotoolsbenchmarks/DelphesNtuplizer/blob/master/bin/Ntuplizer.py
#                   Author : Amandeep Singh Bakshi

import ROOT

def skim(chain):
    for i in range(20):  #Playing around
        if (abs(chain.genpart_pid[i]) == 1000006 and chain.genpart_mass[i] == 220) :
           return True
    return False

def main() :

    # Input files and trees
    inputFile       = ROOT.TFile('SUSY_no_spin.root', 'OPEN')
    chain 	    = ROOT.TChain()
    chain.Add('SUSY_no_spin.root/Delphes_Ntuples')

    # Declare new tree and file
    new_file        =  ROOT.TFile('Mstop_220.root','RECREATE')
    new_tree        =  chain.CloneTree(0)

    numberOfEntries =  chain.GetEntries()

    # Useful counters 
    n_skim 	    =  0 

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
