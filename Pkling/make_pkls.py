import uproot 
import argparse
import pandas as pd

def main() :

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input' , help='Input SUSY root file')
    parser.add_argument('-o', '--output', help='Output SUSY pkl file')

    args       = parser.parse_args()
    inputFile  = args.input
    outputFile = args.output

    ptr      = uproot.open(inputFile)['Step8']  

    l_pt     = ptr['l_pt'].array()
    l_phi    = ptr['l_phi'].array()
    l_eta    = ptr['l_eta'].array()
    l_mass   = ptr['l_mass'].array()

    lbar_pt   = ptr['sl_pt'].array()
    lbar_phi  = ptr['sl_phi'].array()
    lbar_eta  = ptr['sl_eta'].array()
    lbar_mass = ptr['sl_mass'].array()

    e_pt     = ptr['e_pt'].array()
    e_phi    = ptr['e_phi'].array()
    e_eta    = ptr['e_eta'].array()
    e_charge = ptr['e_charge'].array()

    mu_pt     = ptr['mu_pt'].array()
    mu_phi    = ptr['mu_phi'].array()
    mu_eta    = ptr['mu_eta'].array()
    mu_charge = ptr['mu_charge'].array()

    ljet_pt     = ptr['ljet_pt'].array()
    ljet_phi    = ptr['ljet_phi'].array()
    ljet_eta    = ptr['ljet_eta'].array()
    ljet_mass   = ptr['ljet_mass'].array()

    sljet_pt     = ptr['sljet_pt'].array()
    sljet_phi    = ptr['sljet_phi'].array()
    sljet_eta    = ptr['sljet_eta'].array()
    sljet_mass   = ptr['sljet_mass'].array()

    llbar_deta    = ptr['llbar_deta'].array()
    llbar_dphi    = ptr['llbar_dphi'].array()
    bbbar_deta    = ptr['bbbar_deta'].array()
    bbbar_dphi    = ptr['bbbar_dphi'].array()

    MET     = ptr['MET'].array()
    MET_phi = ptr['MET_phi'].array()

    arr        = [e_pt, e_eta, e_phi, e_charge, mu_pt  , mu_eta  , mu_phi  , mu_charge, 
                  l_pt, l_eta, l_phi, l_mass  , lbar_pt, lbar_eta, lbar_phi, lbar_mass,
                  ljet_pt , ljet_eta , ljet_phi , ljet_mass , 
                  sljet_pt, sljet_eta, sljet_phi, sljet_mass, 
                  llbar_dphi, llbar_deta, bbbar_dphi, bbbar_deta, MET, MET_phi]

    df         = pd.DataFrame(data = arr).T

    df.columns = ['e_pt', 'e_eta', 'e_phi', 'e_charge', 'mu_pt'  , 'mu_eta'  , 'mu_phi'  , 'mu_charge', 
                  'l_pt', 'l_eta', 'l_phi', 'l_mass'  , 'lbar_pt', 'lbar_eta', 'lbar_phi', 'lbar_mass',
                  'ljet_pt' , 'ljet_eta' , 'ljet_phi' , 'ljet_mass' , 
                  'sljet_pt', 'sljet_eta', 'sljet_phi', 'sljet_mass', 
                  'llbar_dphi', 'llbar_deta', 'bbbar_dphi', 'bbbar_deta', 'MET', 'MET_phi']


    df.to_pickle(outputFile)
    print('Done processing file')

main()