#!/usr/bin/python

# This script works with ntuples produced using the Delphes Ntuplizer found at :
# https://github.com/recotoolsbenchmarks/DelphesNtuplizer/blob/master/bin/Ntuplizer.py
#                   Author : Amandeep Singh Bakshi

import ROOT


def skim(chain, mc):
    for i in range(len(chain.genpart_mass)):  # Playing around
        if (chain.genpart_pid[i] == 1000022 and chain.genpart_mass[i] == mc):
            return True
    return False


mstop_mass_points = [175, 182.5, 190, 197.5,
                     205, 212.5, 220, 227.5, 235, 242.5]
mchi0_mass_points = [0, 7.5, 15, 22.5, 30, 37.5, 45, 52.5, 60]

for ms in mstop_mass_points:
    for mc in mchi0_mass_points:
        if (ms - mc == 167.5) or (ms - mc == 175) or (ms - mc == 182.5):

            if '.' in str(ms):
                ip_file_name = 'Mstop_' + (str(ms).replace('.', '_')) + '.root'
            else:
                ip_file_name = 'Mstop_' + str(ms) + '.root'

            # Input files and trees
            inputFile = ROOT.TFile(ip_file_name, 'OPEN')
            chain = ROOT.TChain()
            chain.Add(ip_file_name + '/Step8')

            numberOfEntries = chain.GetEntries()

            # Declare new tree and file
            if '.' in str(ms) and '.' in str(mc):
                op_file_name = 'Mstop_' + \
                    (str(ms).replace('.', '_')) + '_mchi_' + \
                    (str(mc).replace('.', '_')) + '.root'

            elif '.' in str(ms) and '.' not in str(mc):
                op_file_name = 'Mstop_' + \
                    (str(ms).replace('.', '_')) + '_mchi_' + str(mc) + '.root'

            elif '.' not in str(ms) and '.' in str(mc):
                op_file_name = 'Mstop_' + \
                    str(ms) + '_mchi_' + (str(mc).replace('.', '_')) + '.root'

            else:
                op_file_name = 'Mstop_' + \
                    str(ms) + '_mchi_' + str(mc) + '.root'

            new_file = ROOT.TFile(op_file_name, 'RECREATE')
            new_tree = chain.CloneTree(0)

            # Useful counters
            n_skim = 0

            ################ Start event loop #######################

            for i_event in range(0, numberOfEntries):
                i_entry = chain.LoadTree(i_event)
                chain.GetEntry(i_event)

                if i_event % 1000 == 0:
                    print('Processing event %i of %i' %
                          (i_event, numberOfEntries))

                passed_skim = skim(chain, mc)

                if passed_skim:
                    new_tree.Fill()
                    n_skim += 1

            inputFile.Close()
            new_tree.AutoSave()
            new_file.Close()

            print('Processed events : %i, of which %i passed ' %
                  (numberOfEntries, n_skim))

        else:
            continue

    print('Finished processing file ::' + str(op_file_name))

print('Done all, check output directory')
