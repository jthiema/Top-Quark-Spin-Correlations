import os
import sys
import uproot
from ROOT import TFile, TObject, TH1D, TH2D, TUnfoldBinning, TUnfoldBinningXML, cout
import hist
import numpy as np
import argparse
import awkward as ak
import vector

def remove_underoverflow(histogram, doGen = True , doReco = True):

    if len(histogram.shape) == 1:
        
        x_range = len(histogram[:]) - 1

        histogram[1] = histogram[0] + histogram[1]
        histogram[0] = histogram[0] - histogram[0]
    
        histogram[x_range - 1] = histogram[x_range] + histogram[x_range - 1]
        histogram[x_range] = histogram[x_range] - histogram[x_range]
    
    elif len(histogram.shape) == 2:
        
        x_range = len(histogram[:,0]) - 1 
        y_range = len(histogram[0,:]) - 1
        
        if doGen:
            histogram[1,:] = histogram[0,:] + histogram[1,:]
            histogram[0,:] = histogram[0,:] - histogram[0,:]
        
        if doReco:
            histogram[:,1] = histogram[:,0] + histogram[:,1]
            histogram[:,0] = histogram[:,0] - histogram[:,0]
    
        if doGen:
            histogram[x_range - 1,:] = histogram[x_range,:] + histogram[x_range - 1,:]
            histogram[x_range,:] = histogram[x_range,:] - histogram[x_range,:]

        if doReco:
            histogram[:,y_range - 1] = histogram[:,y_range] + histogram[:,y_range - 1]
            histogram[:,y_range] = histogram[:,y_range] - histogram[:,y_range]
        
        
    elif len(histogram.shape) == 3:
        
        x_range = len(histogram[:,0,0]) - 1
        y_range = len(histogram[0,:,0]) - 1
        z_range = len(histogram[0,0,:]) - 1

        histogram[1,:,:] = histogram[0,:,:] + histogram[1,:,:]
        histogram[0,:,:] = histogram[0,:,:] - histogram[0,:,:]
        histogram[:,1,:] = histogram[:,0,:] + histogram[:,1,:]
        histogram[:,0,:] = histogram[:,0,:] - histogram[:,0,:]
        histogram[:,:,1] = histogram[:,:,0] + histogram[:,:,1]
        histogram[:,:,0] = histogram[:,:,0] - histogram[:,:,0]
    
        histogram[x_range - 1,:,:] = histogram[x_range,:,:] + histogram[x_range - 1,:,:]
        histogram[x_range,:,:] = histogram[x_range,:,:] - histogram[x_range,:,:]
        histogram[:,y_range - 1,:] = histogram[:,y_range,:] + histogram[:,y_range - 1,:]
        histogram[:,y_range,:] = histogram[:,y_range,:] - histogram[:,y_range,:]
        histogram[:,:,z_range - 1] = histogram[:,:,z_range] + histogram[:,:,z_range - 1]
        histogram[:,:,z_range] = histogram[:,:,z_range] - histogram[:,:,z_range]
        
    elif len(histogram.shape) == 4:

        w_range = len(histogram[:,0,0,0]) - 1
        x_range = len(histogram[0,:,0,0]) - 1
        y_range = len(histogram[0,0,:,0]) - 1
        z_range = len(histogram[0,0,0,:]) - 1

        if doGen:
            histogram[1,:,:,:] = histogram[0,:,:,:] + histogram[1,:,:,:]
            histogram[0,:,:,:] = histogram[0,:,:,:] - histogram[0,:,:,:]
            histogram[:,1,:,:] = histogram[:,0,:,:] + histogram[:,1,:,:]
            histogram[:,0,:,:] = histogram[:,0,:,:] - histogram[:,0,:,:]
        
        if doReco:
            histogram[:,:,1,:] = histogram[:,:,0,:] + histogram[:,:,1,:]
            histogram[:,:,0,:] = histogram[:,:,0,:] - histogram[:,:,0,:]
            histogram[:,:,:,1] = histogram[:,:,:,0] + histogram[:,:,:,1]
            histogram[:,:,:,0] = histogram[:,:,:,0] - histogram[:,:,:,0]

        if doGen:
            histogram[w_range - 1,:,:,:] = histogram[w_range,:,:,:] + histogram[w_range - 1,:,:,:]
            histogram[w_range,:,:,:] = histogram[w_range,:,:,:] - histogram[w_range,:,:,:]
            histogram[:,x_range - 1,:,:] = histogram[:,x_range,:,:] + histogram[:,x_range - 1,:,:]
            histogram[:,x_range,:,:] = histogram[:,x_range,:,:] - histogram[:,x_range,:,:]

        if doReco:
            histogram[:,:,y_range - 1,:] = histogram[:,:,y_range,:] + histogram[:,:,y_range - 1,:]
            histogram[:,:,y_range,:] = histogram[:,:,y_range,:] - histogram[:,:,y_range,:]
            histogram[:,:,:,z_range - 1] = histogram[:,:,:,z_range] + histogram[:,:,:,z_range - 1]
            histogram[:,:,:,z_range] = histogram[:,:,:,z_range] - histogram[:,:,:,z_range]
    
    return histogram


def compute_reco(var_name, reco_axes, step8_data, step8_weights, symmetrize = False):

    reco = hist.Hist(*reco_axes, storage=hist.storage.Weight())

    if symmetrize == False:
        reco.fill(*step8_data, weight=step8_weights)
    elif symmetrize == True:
        reco.fill(*[1.0*np.array(step8_data[0])] + [data for data in step8_data[1:] if step8_data[1:]], weight=(0.5*np.array(step8_weights)))
        reco.fill(*[-1.0*np.array(step8_data[0])] + [data for data in step8_data[1:] if step8_data[1:]], weight=(0.5*np.array(step8_weights)))
        reco.variances(flow=True)[...] = 2.0 * reco.variances(flow=True)[...]

    remove_underoverflow(reco.values(flow=True))
    remove_underoverflow(reco.variances(flow=True))

    return reco


def Convert_to_TH1(prefix, var, hist1D):


    TH1 = TH1D(prefix+"_"+var, 
               prefix+"_"+var, 
               hist1D.values(flow=False).shape[0], 
               np.array(GetBinning(hist1D.axes)[0]),
               #hist1D.axes[0][0][0], 
               #hist1D.axes[0][len(hist1D.axes[0])-1][1]
    )
    TH1.Sumw2()

    for i in range(0, hist1D.values(flow=False).shape[0] + 1):
        TH1.SetBinContent(i,hist1D.values(flow=True)[i])
        TH1.SetBinError(i,np.sqrt(hist1D.variances(flow=True)[i]))                     

    return TH1


def Unwrap_to_TH1(prefix, var1D, var2D, hist2D):
    
    TH1 = TH1D(prefix+"_"+var1D+"_vs_"+var2D, 
                prefix+"_"+var1D+"_vs_"+var2D, 
                (hist2D.values(flow=False).shape[0])*(hist2D.values(flow=False).shape[1]), 
                hist2D.axes[0][0][0], 
                hist2D.axes[0][len(hist2D.axes[0])-1][1]
                )
    
    TH1.Sumw2()

    i_range = hist2D.values(flow=False).shape[0]+1
    j_range = hist2D.values(flow=False).shape[1]+1
                        
    for i in range(1,i_range):
        for j in range(1,j_range):
            TH1.SetBinContent((j-1)*(i_range-1)+i, hist2D.values(flow=True)[i,j])
            TH1.SetBinError((j-1)*(i_range-1)+i, np.sqrt(hist2D.variances(flow=True)[i,j]))
    
    return TH1


def BinFinely(Original_Binning, nFineBins):
    Fine_Binning = sum([[Original_Binning[j]+(Original_Binning[j+1]-Original_Binning[j])*(i/nFineBins) for i in range (0,nFineBins)] for j in range(0,len(Original_Binning)-1)] + [[Original_Binning[len(Original_Binning)-1]]],[])
    return Fine_Binning


def GetBinning(axeslist):
    return [[axeslist[i][j][0] for j in range(0,len(axeslist[i]))] + [axeslist[i][len(axeslist[i])-1][1]] for i in range(0,len(axeslist))]


# To run, example:
# python scripts/makeTUnfoldHisto.py -y 2016ULpostVFP -s Nominal -c emu

def main():

    parser = argparse.ArgumentParser(description=__doc__)
#    parser.add_argument('-c', '--channel', dest='channel',
#                            action='store', default='',
#                            help='Channel (example: ee, emu, mumu')
#    parser.add_argument('-s', '--systematic', dest='systematic',
#                            action='store', default='Nominal',
#                            help='Systematic (example: Nominal, JER_UP, etc.')
    parser.add_argument('-f', '--file', dest='file',
                            action='store', default='',
                            help='File (example:ttbarsignalplustau_fromDilepton')

    opts, opts_unknown = parser.parse_known_args()
#    systematic = opts.systematic
#    channel = opts.channel
    file = opts.file


    print("Processing: " + file)


    HLLHC_BASE = os.environ['HLLHC_BASE'] + "/"

    if not os.path.exists(HLLHC_BASE + "HistogramOutput"): os.makedirs(HLLHC_BASE + "HistogramOutput")

    outHistFile = TFile.Open ( HLLHC_BASE + file.replace("MiniTreeOutput/minitree","HistogramOutput/histogram") , "RECREATE" )
    outHistFile.cd()

    step8tree = uproot.open(file+':Step8')

    tree_vars = [
        'lep_pt', 'lep_eta', 'lep_phi', 'lep_mass',
        'alep_pt', 'alep_eta', 'alep_phi', 'alep_mass',
        'top_pt', 'top_eta', 'top_phi', 'top_mass', 
        'atop_pt', 'atop_eta', 'atop_phi', 'atop_mass', 
        'weight_size', 'weight'
    ]


    step8 =   dict( (tree_var, step8tree[tree_var].array()) for tree_var in tree_vars ) 

    # Top and Lepton 4-Vectors
    top = vector.zip({'pt': step8["top_pt"], 'phi': step8["top_phi"], 'eta': step8["top_eta"], 'M': step8["top_mass"]})
    tbar = vector.zip({'pt': step8["atop_pt"], 'phi': step8["atop_phi"], 'eta': step8["atop_eta"], 'M': step8["atop_mass"]})
    l = vector.zip({'pt': step8["lep_pt"], 'phi': step8["lep_phi"], 'eta': step8["lep_eta"], 'M': step8["lep_mass"]})
    lbar = vector.zip({'pt': step8["alep_pt"], 'phi': step8["alep_phi"], 'eta': step8["alep_eta"], 'M': step8["alep_mass"]})

    # Calculation of Top Polarizations and Spin Correlations

    boosted_lbar = lbar.boostCM_of(top)
    boosted_l = l.boostCM_of(tbar)

    # define axes
    p_axis = vector.obj(x = 0, y = 0, z = 1) #p_axis is the proton axis, defined to be 1 in z direction
    k_axis = top.boostCM_of(top + tbar).to_xyz() #k_axis is defined by the direction of the tops
    scattering_angle = k_axis.theta
    sin_of_scattering_angle = np.sin(scattering_angle)
    #where used to find conditions when sign flip
    sin_of_scattering_angle = np.where(np.abs(sin_of_scattering_angle) < 1e-5, 1e-5, sin_of_scattering_angle)
    axis_coefficient = np.sign(np.cos(scattering_angle)) / np.abs(sin_of_scattering_angle)
    r_axis = axis_coefficient * (p_axis - k_axis * np.cos(scattering_angle))
    n_axis = axis_coefficient * p_axis.cross(k_axis)
    
    boosted_lbar = lbar.boostCM_of(top)
    boosted_l = l.boostCM_of(tbar)

    #llbar_cHel
    cosphi = np.cos(boosted_lbar.deltaangle(boosted_l).to_numpy())

    # convert series to numpy array with to_numpy
    cos_theta1k = np.cos(boosted_lbar.deltaangle(k_axis).to_numpy())
    cos_theta1r = np.cos(boosted_lbar.deltaangle(r_axis).to_numpy())
    cos_theta1n = np.cos(boosted_lbar.deltaangle(n_axis).to_numpy())
    cos_theta2k = np.cos(boosted_l.deltaangle(k_axis).to_numpy())
    cos_theta2r = np.cos(boosted_l.deltaangle(r_axis).to_numpy())
    cos_theta2n = np.cos(boosted_l.deltaangle(n_axis).to_numpy())

    c_rr = cos_theta1r*cos_theta2r
    c_rk = cos_theta1r*cos_theta2k
    c_rn = cos_theta1r*cos_theta2n
    
    c_kr = cos_theta1k*cos_theta2r
    c_kk = cos_theta1k*cos_theta2k
    c_kn = cos_theta1k*cos_theta2n

    c_nr = cos_theta1n*cos_theta2r
    c_nk = cos_theta1n*cos_theta2k
    c_nn = cos_theta1n*cos_theta2n
    

    vars1D_dict = {

        "lep_pt" : {
            "bin_edge_low" : 0.0, 
            "bin_edge_high" : 200.0, 
            "n_reco_bins" : 40, 
            "val_8" : step8["lep_pt"],
            "can_symmetrize" : True,
        },

        "LLBarcHel" : {
            "bin_edge_low" : -1.0, 
            "bin_edge_high" : 1.0, 
            "n_reco_bins" : 12, 
            "val_8" : cosphi,
            "can_symmetrize" : True,
        },

    }


    binning_ttbar_mass = [250., 450., 600., 800., 2000.]
    binning_top_scatteringangle_ttbarframe = [-1.0, -0.5, 0.0, +0.5, +1.0]
    binning_top_pt = [0., 80., 150., 250., 550.]
    binning_n_extraJets_iso08 = [-0.5, 0.5, 1.5, 2.5, 3.5]


    vars2D_dict = {

        "TTBarMass" : {
            "bin_edge_low" : 300., 
            "bin_edge_high" : 2000., 
            "reco_binning" : BinFinely(binning_ttbar_mass, 1),
            "val_8" : (top + tbar).M,
            "can_symmetrize" : False,
        },

    }

    nFineBins_1D = 2
    nFineBins_2D = 1

    do_symmetrize = False

    # 1D

    prefix = ""

    for var1D in vars1D_dict.keys():


        if(do_symmetrize*vars1D_dict[var1D]["can_symmetrize"] == True): prefix = "RecoSym"
        else: prefix = "Reco"

        reco_axes = [hist.axis.Regular(nFineBins_1D*vars1D_dict[var1D]["n_reco_bins"], vars1D_dict[var1D]["bin_edge_low"], vars1D_dict[var1D]["bin_edge_high"], name="reco_"+var1D, label="reco_"+var1D, underflow=True, overflow=True)]

        reco = compute_reco(var1D, reco_axes, [vars1D_dict[var1D]["val_8"]], [np.ones(len(vars1D_dict[var1D]["val_8"]))], do_symmetrize*vars1D_dict[var1D]["can_symmetrize"])
        hreco = Convert_to_TH1(prefix, var1D, reco)
        hreco.Write(hreco.GetName(),TObject.kOverwrite)

    # 2D

    for var2D in vars2D_dict.keys():

        reco_axes_2D = [hist.axis.Variable(BinFinely(vars2D_dict[var2D]["reco_binning"],nFineBins_2D), name="reco2D_"+var2D, label="reco2D_"+var2D, underflow=True, overflow=True)]

        for var1D in vars1D_dict.keys():

            if(do_symmetrize*vars1D_dict[var1D]["can_symmetrize"] == True): prefix = "RecoSym"
            else: prefix = "Reco"

            reco_axes = [hist.axis.Regular(nFineBins_2D*vars1D_dict[var1D]["n_reco_bins"], vars1D_dict[var1D]["bin_edge_low"], vars1D_dict[var1D]["bin_edge_high"], name="reco_"+var1D, label="reco_"+var1D, underflow=True, overflow=True)]

            reco = compute_reco(var1D+"_"+var2D, reco_axes + reco_axes_2D, [vars1D_dict[var1D]["val_8"], vars2D_dict[var2D]["val_8"]], [np.ones(len(vars1D_dict[var1D]["val_8"]))], do_symmetrize*vars1D_dict[var1D]["can_symmetrize"])
            hreco = Unwrap_to_TH1(prefix, var1D, var2D, reco)
            hreco.Write(hreco.GetName(),TObject.kOverwrite)


        if var2D == "ExtraJets":
            reco_axes_2D = [hist.axis.Variable(BinFinely(vars2D_dict[var2D]["reco_binning"],1), name="reco2D_"+var2D, label="reco2D_"+var2D, underflow=True, overflow=True)]
        else:
            reco_axes_2D = [hist.axis.Variable(BinFinely(vars2D_dict[var2D]["reco_binning"],4), name="reco2D_"+var2D, label="reco2D_"+var2D, underflow=True, overflow=True)]

        if(do_symmetrize*vars2D_dict[var2D]["can_symmetrize"] == True): prefix = "RecoSym"
        else: prefix = "Reco"

        reco = compute_reco(var2D, reco_axes_2D, [vars2D_dict[var2D]["val_8"]], [np.ones(len(vars1D_dict[var1D]["val_8"]))], do_symmetrize*vars2D_dict[var2D]["can_symmetrize"])
        hreco = Convert_to_TH1(prefix, var2D, reco)
        hreco.Write(hreco.GetName(),TObject.kOverwrite)


    outHistFile.Close()

##############################

if __name__ == "__main__":

    main()

##############################  
