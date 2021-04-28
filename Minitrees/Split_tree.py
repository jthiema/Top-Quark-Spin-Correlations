#!/usr/bin/python

# This script works with ntuples produced using the Delphes Ntuplizer found at :
# https://github.com/recotoolsbenchmarks/DelphesNtuplizer/blob/master/bin/Ntuplizer.py
#                   Author : Amandeep Singh Bakshi

import ROOT


def skim(chain, mp):
    for i in range(20): 
        if (abs(chain.genpart_pid[i]) == 1000006 and chain.genpart_mass[i] == mp):
            return True
    return False


def main():

    # Input files and trees
    inputFile = ROOT.TFile('SUSY_w_abs.root', 'OPEN')
    chain     = ROOT.TChain()
    chain.Add('SUSY_w_abs.root/Step8')

    mass_points = [175, 182.5, 190, 197.5, 205, 212.5, 220, 227.5, 235, 242.5]

    for mp in mass_points :
        if '.' in str(mp) :
            file_name = 'Mstop_' + (str(mp).replace('.', '_')) + '.root'
        else :
            file_name = 'Mstop_' + str(mp) + '.root'

        # Declare new tree and file
        new_file = ROOT.TFile(file_name, 'RECREATE')
        new_tree = chain.CloneTree(0)

        numberOfEntries = chain.GetEntries()

        # Useful counters
        n_skim = 0

        ################ Start event loop #######################

        for i_event in range(0, numberOfEntries):
            i_entry = chain.LoadTree(i_event)
            chain.GetEntry(i_event)

            if i_event % 1000 == 0:
                print('Processing event %i of %i' % (i_event, numberOfEntries))

            passed_skim = skim(chain, mp)
            if passed_skim:
                new_tree.Fill()
                n_skim += 1

        inputFile.Close()
        new_tree.AutoSave()
        new_file.Close()

        print('Processed events : %i, of which %i passed ' %
            (numberOfEntries, n_skim))

        print('Finished writing into file ::' + str(file_name))


if __name__ == '__main__' :
    main()
