import math
import uproot
import numpy as np
import matplotlib.pyplot as plt

unc_file = ROOT.TFile("HL_YR_JEC.root","OPEN")
b_jes    = unc_file.Get('TOTAL_BJES_AntiKt4EMTopo_YR2018')

def JES_wt_calc(jet_pt):
    bin_num = math.floor(((jet_pt/3000)*201))               #Scale by largest Pt, times the number of bins
    JES_wt  = b_jes.GetBinContent(bin_num + 1)              #Start from 1 since that's how ROOT does it
    return JES_wt    

def JER_wt_calc(jet_eta):
    jer_unc = 0
    if   (jet_eta < 1) : jer_unc = 0.03
    elif (jet_eta > 1) : jer_unc = 0.05
    return jer_unc

print('Reading in the file ')
fileptr = uproot.open('Root_files/Top_reco_op_w_jets.root')['Step8']

print('Done, now reading in the jet arrays')
b_pt     = fileptr['b_pt'].array()
b_eta    = fileptr['b_eta'].array()
b_phi    = fileptr['b_phi'].array()
b_mass   = fileptr['b_mass'].array()

bbar_pt  = fileptr['bbar_pt'].array()
bbar_eta = fileptr['bbar_eta'].array()
bbar_phi = fileptr['bbar_phi'].array()
bbar_mass = fileptr['bbar_mass'].array()

# Extract the weights

JER_jet1_up   = []        
JER_jet1_nom  = []         
JER_jet1_down = []      

JER_jet2_up   = []        
JER_jet2_nom  = []         
JER_jet2_down = []        

for i in range(len(b_pt)):
    corr_factor_1 = JER_wt_calc(b_eta[i])    
    JER_jet1_up.append(  b_pt[i] * (1 + corr_factor_1))
    JER_jet1_nom.append( b_pt[i])
    JER_jet1_down.append(b_pt[i] * (1 - corr_factor_1))
    
    corr_factor_2 = JER_wt_calc(bbar_eta[i])    
    JER_jet2_up.append(  bbar_pt[i] * (1 + corr_factor_2))
    JER_jet2_nom.append( bbar_pt[i])
    JER_jet2_down.append(bbar_pt[i] * (1 - corr_factor_2))


JES_jet1_up   = []        
JES_jet1_nom  = []         
JES_jet1_down = []      

JES_jet2_up   = []        
JES_jet2_nom  = []         
JES_jet2_down = []        

for i in range(len(b_pt)):
    corr_factor_1 = JES_wt_calc(b_pt[i])    
    JES_jet1_up.append(  b_pt[i] * (1 + corr_factor_1))
    JES_jet1_nom.append( b_pt[i])
    JES_jet1_down.append(b_pt[i] * (1 - corr_factor_1))
    
    corr_factor_2 = JES_wt_calc(bbar_pt[i])    
    JES_jet2_up.append(  bbar_pt[i] * (1 + corr_factor_2))
    JES_jet2_nom.append( bbar_pt[i])
    JES_jet2_down.append(bbar_pt[i] * (1 - corr_factor_2))

JER_jet1_up   = np.array(JER_jet1_up)
JER_jet1_nom  = np.array(JER_jet1_nom)
JER_jet1_down = np.array(JER_jet1_down)

JER_jet2_up   = np.array(JER_jet2_up)
JER_jet2_nom  = np.array(JER_jet2_nom)
JER_jet2_down = np.array(JER_jet2_down)

JES_jet1_up   = np.array(JES_jet1_up)
JES_jet1_nom  = np.array(JES_jet1_nom)
JES_jet1_down = np.array(JES_jet1_down)

JES_jet2_up   = np.array(JES_jet2_up)
JES_jet2_nom  = np.array(JES_jet2_nom)
JES_jet2_down = np.array(JES_jet2_down)


fig,ax  = plt.subplots(figsize=(11,10))
binning = np.linspace(30, 300, 20)

# Generate UP and DOWN variations in histograms 
JER_ns_j11, bins, patches = ax.hist(np.clip(JER_jet1_nom, binning[0], binning[-1]), histtype='step', bins=binning, label = 'Nominal'      , linestyle='dashed', linewidth=2)
JER_ns_j12, bins, patches = ax.hist(np.clip(JER_jet1_up,  binning[0], binning[-1]), histtype='step', bins=binning, label = 'JER + 1 sigma', linestyle='dashed', linewidth=2)
JER_ns_j13, bins, patches = ax.hist(np.clip(JER_jet1_down,binning[0], binning[-1]), histtype='step', bins=binning, label = 'JER - 1 sigma', linestyle='dashed', linewidth=2)

JER_ns_j21, bins, patches = ax.hist(np.clip(JER_jet2_nom, binning[0], binning[-1]), histtype='step', bins=binning, label = 'Nominal'      , linestyle='dashed', linewidth=2)
JER_ns_j22, bins, patches = ax.hist(np.clip(JER_jet2_up,  binning[0], binning[-1]), histtype='step', bins=binning, label = 'JER + 1 sigma', linestyle='dashed', linewidth=2)
JER_ns_j23, bins, patches = ax.hist(np.clip(JER_jet2_down,binning[0], binning[-1]), histtype='step', bins=binning, label = 'JER - 1 sigma', linestyle='dashed', linewidth=2)

JES_ns_j11, bins, patches = ax.hist(np.clip(JES_jet1_nom, binning[0], binning[-1]), histtype='step', bins=binning, label = 'Nominal'      , linestyle='dashed', linewidth=2)
JES_ns_j12, bins, patches = ax.hist(np.clip(JES_jet1_up,  binning[0], binning[-1]), histtype='step', bins=binning, label = 'JES + 1 sigma', linestyle='dashed', linewidth=2)
JES_ns_j13, bins, patches = ax.hist(np.clip(JES_jet1_down,binning[0], binning[-1]), histtype='step', bins=binning, label = 'JES - 1 sigma', linestyle='dashed', linewidth=2)

JES_ns_j21, bins, patches = ax.hist(np.clip(JES_jet2_nom, binning[0], binning[-1]), histtype='step', bins=binning, label = 'Nominal'      , linestyle='dashed', linewidth=2)
JES_ns_j22, bins, patches = ax.hist(np.clip(JES_jet2_up,  binning[0], binning[-1]), histtype='step', bins=binning, label = 'JES + 1 sigma', linestyle='dashed', linewidth=2)
JES_ns_j23, bins, patches = ax.hist(np.clip(JES_jet2_down,binning[0], binning[-1]), histtype='step', bins=binning, label = 'JES - 1 sigma', linestyle='dashed', linewidth=2)

# Ratios of UP and DOWN to Nominal
JER_r_jet1_up   = JER_ns_j12/JER_ns_j11
JER_r_jet1_down = JER_ns_j13/JER_ns_j11
JER_r_jet2_up   = JER_ns_j22/JER_ns_j21
JER_r_jet2_down = JER_ns_j23/JER_ns_j21

JES_r_jet1_up   = JES_ns_j12/JES_ns_j11
JES_r_jet1_down = JES_ns_j13/JES_ns_j11
JES_r_jet2_up   = JES_ns_j22/JES_ns_j21
JES_r_jet2_down = JES_ns_j23/JES_ns_j21

# Fill in the JER weights
JER_jet1_weight_up   = []
JER_jet1_weight_down = []

for i in range(len(b_pt)) :
    for j in range(len(bins) -1):
        if b_pt[i] > bins[j] and b_pt[i] < bins[j+1]:
            JER_jet1_weight_up.append(JER_r_jet1_up[j])
            JER_jet1_weight_down.append(JER_r_jet1_down[j])
            
        elif b_pt[i] > bins[-1]:
            JER_jet1_weight_up.append(1.)
            JER_jet1_weight_down.append(1.)
            break

JER_jet2_weight_up   = []
JER_jet2_weight_down = []

for i in range(len(bbar_pt)) :
    for j in range(len(bins) -1):
        if bbar_pt[i] > bins[j] and bbar_pt[i] < bins[j+1]:
            JER_jet2_weight_up.append(JER_r_jet2_up[j])
            JER_jet2_weight_down.append(JER_r_jet2_down[j])
            
        elif bbar_pt[i] > bins[-1]:
            JER_jet2_weight_up.append(1.)
            JER_jet2_weight_down.append(1.)
            break

# Convert to numpy arrays for storing
JER_jet1_weight_up  = np.array(JER_jet1_weight_up)
JER_jet1_weight_down= np.array(JER_jet1_weight_down)
JER_jet2_weight_up  = np.array(JER_jet2_weight_up)
JER_jet2_weight_down= np.array(JER_jet2_weight_down)

# Finally save the weights
np.savetxt('JER/JER_ljet_weight_up.txt'   , JER_jet1_weight_up)
np.savetxt('JER/JER_ljet_weight_down.txt' , JER_jet1_weight_down)
np.savetxt('JER/JER_sljet_weight_up.txt'  , JER_jet2_weight_up)
np.savetxt('JER/JER_sljet_weight_down.txt', JER_jet2_weight_down)

# Fill in the JES weights

JES_jet1_weight_up   = []
JES_jet1_weight_down = []

for i in range(len(b_pt)) :
    for j in range(len(bins) -1):
        if b_pt[i] > bins[j] and b_pt[i] < bins[j+1]:
            JES_jet1_weight_up.append(JES_r_jet1_up[j])
            JES_jet1_weight_down.append(JES_r_jet1_down[j])
            
        elif b_pt[i] > bins[-1]:
            JES_jet1_weight_up.append(1.)
            JES_jet1_weight_down.append(1.)
            break

JES_jet2_weight_up   = []
JES_jet2_weight_down = []

for i in range(len(bbar_pt)) :
    for j in range(len(bins) -1):
        if bbar_pt[i] > bins[j] and bbar_pt[i] < bins[j+1]:
            JES_jet2_weight_up.append(JES_r_jet2_up[j])
            JES_jet2_weight_down.append(JES_r_jet2_down[j])
            
        elif bbar_pt[i] > bins[-1]:
            JES_jet2_weight_up.append(1.)
            JES_jet2_weight_down.append(1.)
            break

# Convert to numpy arrays for storing
JES_jet1_weight_up  = np.array(JES_jet1_weight_up)
JES_jet1_weight_down= np.array(JES_jet1_weight_down)
JES_jet2_weight_up  = np.array(JES_jet2_weight_up)
JES_jet2_weight_down= np.array(JES_jet2_weight_down)

# Finally save the weights
np.savetxt('JES/JES_ljet_weight_up.txt'   , JES_jet1_weight_up)
np.savetxt('JES/JES_ljet_weight_down.txt' , JES_jet1_weight_down)
np.savetxt('JES/JES_sljet_weight_up.txt'  , JES_jet2_weight_up)
np.savetxt('JES/JES_sljet_weight_down.txt', JES_jet2_weight_down)