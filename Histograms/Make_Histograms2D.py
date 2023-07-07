import os
import sys
import uproot
from ROOT import TFile, TObject, TH1D, TH2D, TUnfoldBinning, TUnfoldBinningXML, cout
import hist
import numpy as np
import argparse
import awkward as ak
import vector

#example command
#python Histograms/Make_Histograms2D.py -f MiniTreeOutput/minitree_200.root

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

def compute_gen(var_name, gen_axes, gen_step0_data, gen_step0_weights, symmetrize = False):
    
    gen = hist.Hist(*gen_axes, storage=hist.storage.Weight())

    if symmetrize == False:    
        gen.fill(*gen_step0_data, weight=gen_step0_weights)
    elif symmetrize == True:
        gen.fill(*[1.0*np.array(gen_step0_data[0])] + [data for data in gen_step0_data[1:] if gen_step0_data[1:]], weight=(0.5*np.array(gen_step0_weights)))
        gen.fill(*[-1.0*np.array(gen_step0_data[0])] + [data for data in gen_step0_data[1:] if gen_step0_data[1:]], weight=(0.5*np.array(gen_step0_weights)))
        gen.variances(flow=True)[...] = 2.0 * gen.variances(flow=True)[...]
    
    remove_underoverflow(gen.values(flow=True))    
    remove_underoverflow(gen.variances(flow=True))

    return gen


def compute_resolution(var_name, residual_axes, gen_axes, step8_data, gen_step8_data, step8_weights):
    
    axes = residual_axes + gen_axes
    
    resolution = hist.Hist(*axes, storage=hist.storage.Weight())

    resolution.fill(*np.subtract(step8_data, gen_step8_data), *gen_step8_data, weight=step8_weights)
    
    remove_underoverflow(resolution.values(flow=True))    
    remove_underoverflow(resolution.variances(flow=True))
    
    return resolution

def compute_response_matrix(var_name, gen_axes, reco_axes, gen_step8_data, step8_data, gen_step0_data, gen_step8_weights, step8_weights, gen_step0_weights, symmetrize = False):

    axes = gen_axes + reco_axes

    response_matrix = hist.Hist(*axes, storage=hist.storage.Weight())
    response_matrix_genUnderflow = hist.Hist(*axes, storage=hist.storage.Weight())
    response_matrix_genUnderflowCorrection = hist.Hist(*axes, storage=hist.storage.Weight())

    # fill the reconstructed events
    if symmetrize == False:
        response_matrix.fill(*gen_step8_data + step8_data, weight=step8_weights)
    elif symmetrize == True:
        response_matrix.fill(*[1.0*np.array(gen_step8_data[0])] + [data for data in gen_step8_data[1:] if gen_step8_data[1:]] + [1.0*np.array(step8_data[0])] + [data for data in step8_data[1:] if step8_data[1:]], weight=(0.5*np.array(step8_weights)))
        response_matrix.fill(*[-1.0*np.array(gen_step8_data[0])] + [data for data in gen_step8_data[1:] if gen_step8_data[1:]] + [-1.0*np.array(step8_data[0])] + [data for data in step8_data[1:] if step8_data[1:]], weight=(0.5*np.array(step8_weights)))
        response_matrix.variances(flow=True)[...] = 2.0 * response_matrix.variances(flow=True)[...]

    remove_underoverflow(response_matrix.values(flow=True))    
    remove_underoverflow(response_matrix.variances(flow=True))

    # fill the generator level events in the reconstruction underflow bin
    # this is back at step0 so that we can unfold back to full phase space
    if symmetrize == False:
        response_matrix_genUnderflow.fill(*gen_step0_data + [(reco_axes[j][0][0] - 1)*np.ones(len(gen_step0_data[0])) for j in range(0,len(reco_axes))], weight=gen_step0_weights)
    elif symmetrize == True:
        response_matrix_genUnderflow.fill(*[1.0*np.array(gen_step0_data[0])] + [data for data in gen_step0_data[1:] if gen_step0_data[1:]] + [(reco_axes[j][0][0] - 1)*np.ones(len(gen_step0_data[0])) for j in range(0,len(reco_axes))], weight=(0.5*np.array(gen_step0_weights)))
        response_matrix_genUnderflow.fill(*[-1.0*np.array(gen_step0_data[0])] + [data for data in gen_step0_data[1:] if gen_step0_data[1:]] + [(reco_axes[j][0][0] - 1)*np.ones(len(gen_step0_data[0])) for j in range(0,len(reco_axes))], weight=(0.5*np.array(gen_step0_weights)))

        response_matrix_genUnderflow.variances(flow=True)[...] = 2.0 * response_matrix_genUnderflow.variances(flow=True)[...]

    remove_underoverflow(response_matrix_genUnderflow.values(flow=True), True, False)
    remove_underoverflow(response_matrix_genUnderflow.variances(flow=True), True, False)
    
    # next create a separate response matrix to fill the reco weights
    # this is because we need to subtract the entries AND variances and can't
    # do that with a "simple" negative weight (this would only subtract entries,
    # variances are sum of weights squared)

    # fill this new matrix
    if symmetrize == False:
        response_matrix_genUnderflowCorrection.fill(*gen_step8_data + [(reco_axes[j][0][0] - 1)*np.ones(len(gen_step8_data[0])) for j in range(0,len(reco_axes))], weight=step8_weights)
    elif symmetrize == True:
        response_matrix_genUnderflowCorrection.fill(*[1.0*np.array(gen_step8_data[0])] + [data for data in gen_step8_data[1:] if gen_step8_data[1:]] + [(reco_axes[j][0][0] - 1)*np.ones(len(gen_step8_data[0])) for j in range(0,len(reco_axes))], weight=(0.5*np.array(step8_weights)))
        response_matrix_genUnderflowCorrection.fill(*[-1.0*np.array(gen_step8_data[0])] + [data for data in gen_step8_data[1:] if gen_step8_data[1:]] + [(reco_axes[j][0][0] - 1)*np.ones(len(gen_step8_data[0])) for j in range(0,len(reco_axes))], weight=(0.5*np.array(step8_weights)))

    remove_underoverflow(response_matrix_genUnderflowCorrection.values(flow=True), True, False)
    remove_underoverflow(response_matrix_genUnderflowCorrection.variances(flow=True), True, False)
    
    # set values and variances equal to the difference between response_matrix
    # and _response_matrix to account for these events that aren't reconstructed
    response_matrix[...] = np.concatenate(
        ((response_matrix.values(flow=True) + response_matrix_genUnderflow.values(flow=True) - response_matrix_genUnderflowCorrection.values(flow=True))[..., None],
         (response_matrix.variances(flow=True) + response_matrix_genUnderflow.variances(flow=True) - response_matrix_genUnderflowCorrection.variances(flow=True))[..., None]),
        axis=len(axes)
    )

    return response_matrix



def Convert_to_TH2(prefix, var, hist2D):

    TH2 = TH2D(prefix+"_"+var, 
               prefix+"_"+var, 
               hist2D.values(flow=False).shape[0], 
               np.array(GetBinning(hist2D.axes)[0]),
#               hist2D.axes[0][0][0], 
#               hist2D.axes[0][len(hist2D.axes[0])-1][1],
               hist2D.values(flow=False).shape[1], 
               np.array(GetBinning(hist2D.axes)[1]),
#               hist2D.axes[1][0][0], 
#               hist2D.axes[1][len(hist2D.axes[1])-1][1]
    )
    TH2.Sumw2()
    
    i_range = hist2D.values(flow=False).shape[0]+1
    j_range = hist2D.values(flow=False).shape[1]+1

    for i in range(0,i_range):
        for j in range(0,j_range):
            TH2.SetBinContent(i,j,hist2D.values(flow=True)[i,j])
            TH2.SetBinError(i,j,np.sqrt(hist2D.variances(flow=True)[i,j]))

    return TH2

def Unwrap_to_TH2(prefix, var1D, var2D, resmat2D):

    i_range = resmat2D.view(flow=True).shape[1]-2
    j_range = resmat2D.view(flow=True).shape[3]-2
    m_range = resmat2D[:,0,:,0].view(flow=True).shape[0]-2
    n_range = resmat2D[:,0,:,0].view(flow=True).shape[1]-2

    resmat2D_unwrapped_values = np.zeros(((i_range)*(m_range)+2,(j_range)*(n_range)+2))
    resmat2D_unwrapped_variances = np.zeros(((i_range)*(m_range)+2,(j_range)*(n_range)+2))

    for i in range(1,i_range+1):
        for j in range(1,j_range+1):
            for m in range(1,m_range+1):
                for n in range(1,n_range+1):
                    resmat2D_unwrapped_values[(i-1)*(m_range) + m,(j-1)*(n_range) + n] = resmat2D.values(flow=True)[m,i,n,j]
                    resmat2D_unwrapped_variances[(i-1)*(m_range) + m,(j-1)*(n_range) + n] = resmat2D.variances(flow=True)[m,i,n,j]

    # Underflow for gen axes only.  No true underflow and no overflow whatsoever; just generated events that were not reconstructed in underflow bins.
    for i in range(1,i_range+1):
        for m in range(1,m_range+1):
            resmat2D_unwrapped_values[(i-1)*(m_range) + m,0] = resmat2D.values(flow=True)[m,i,0,0]
            resmat2D_unwrapped_variances[(i-1)*(m_range) + m,0] = resmat2D.variances(flow=True)[m,i,0,0]
    
    resmat2D_unwrapped = hist.Hist(
        hist.axis.Regular((i_range)*(m_range), 0, (i_range)*(m_range), name="gen", label="gen", underflow=True, overflow=True),
        hist.axis.Regular((j_range)*(n_range), 0, (j_range)*(n_range), name="reco", label="reco", underflow=True, overflow=True),
        storage=hist.storage.Weight()
    )

    resmat2D_unwrapped[...] = np.concatenate(
        ((resmat2D_unwrapped_values)[..., None],
         (resmat2D_unwrapped_variances)[..., None]),
        axis=2
    )

    TH2 = TH2D(prefix+"_"+var1D+"_"+var2D, 
               prefix+"_"+var1D+"_"+var2D, 
               resmat2D_unwrapped.values(flow=False).shape[0], 
               resmat2D.axes[0][0][0], 
               resmat2D.axes[0][len(resmat2D.axes[0])-1][1],
               resmat2D_unwrapped.values(flow=False).shape[1], 
               resmat2D.axes[0][0][0], 
               resmat2D.axes[0][len(resmat2D.axes[0])-1][1]
              )
    TH2.Sumw2()
    
    i_range = resmat2D_unwrapped.values(flow=False).shape[0]+1
    j_range = resmat2D_unwrapped.values(flow=False).shape[1]+1

    for i in range(0,i_range):
        for j in range(0,j_range):
            TH2.SetBinContent(i,j,resmat2D_unwrapped.values(flow=True)[i,j])
            TH2.SetBinError(i,j,np.sqrt(resmat2D_unwrapped.variances(flow=True)[i,j]))

    return TH2

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
    step0tree = uproot.open(file+':Step0')

    tree_vars = [
        'lep_pt', 'lep_eta', 'lep_phi', 'lep_mass',
        'alep_pt', 'alep_eta', 'alep_phi', 'alep_mass',
        'top_pt', 'top_eta', 'top_phi', 'top_mass',
        'gen_lep_pt', 'gen_lep_eta', 'gen_lep_phi', 'gen_lep_mass',
        'gen_alep_pt', 'gen_alep_eta', 'gen_alep_phi', 'gen_alep_mass',
        'gen_top_pt', 'gen_top_eta', 'gen_top_phi', 'gen_top_mass', 
        'gen_atop_pt', 'gen_atop_eta', 'gen_atop_phi', 'gen_atop_mass',
        'atop_pt', 'atop_eta', 'atop_phi', 'atop_mass', 
        'weight_size', 'weight'
    ]
    gen_tree_vars = ['gen_lep_pt', 'gen_lep_eta', 'gen_lep_phi', 'gen_lep_mass',
                     'gen_alep_pt', 'gen_alep_eta', 'gen_alep_phi', 'gen_alep_mass',
                     'gen_top_pt', 'gen_top_eta', 'gen_top_phi', 'gen_top_mass', 
                     'gen_atop_pt', 'gen_atop_eta', 'gen_atop_phi', 'gen_atop_mass']

    step8 =   dict( (tree_var, step8tree[tree_var].array()) for tree_var in tree_vars ) 
    step0 = dict( (tree_var, step0tree[tree_var].array()) for tree_var in gen_tree_vars )
    
    # Top and Lepton 4-Vectors
    top = vector.zip({'pt': step8["top_pt"], 'phi': step8["top_phi"], 'eta': step8["top_eta"], 'M': step8["top_mass"]})
    tbar = vector.zip({'pt': step8["atop_pt"], 'phi': step8["atop_phi"], 'eta': step8["atop_eta"], 'M': step8["atop_mass"]})
    l = vector.zip({'pt': step8["lep_pt"], 'phi': step8["lep_phi"], 'eta': step8["lep_eta"], 'M': step8["lep_mass"]})
    lbar = vector.zip({'pt': step8["alep_pt"], 'phi': step8["alep_phi"], 'eta': step8["alep_eta"], 'M': step8["alep_mass"]})

    gen_top = vector.zip({'pt': step8["gen_top_pt"], 'phi': step8["gen_top_phi"], 'eta': step8["gen_top_eta"], 'M': step8["gen_top_mass"]})
    gen_tbar = vector.zip({'pt': step8["gen_atop_pt"], 'phi': step8["gen_atop_phi"], 'eta': step8["gen_atop_eta"], 'M': step8["gen_atop_mass"]})
    gen_l = vector.zip({'pt': step8["gen_lep_pt"], 'phi': step8["gen_lep_phi"], 'eta': step8["gen_lep_eta"], 'M': step8["gen_lep_mass"]})
    gen_lbar = vector.zip({'pt': step8["gen_alep_pt"], 'phi': step8["gen_alep_phi"], 'eta': step8["gen_alep_eta"], 'M': step8["gen_alep_mass"]})
    
    step0_gen_top = vector.zip({'pt': step0["gen_top_pt"], 'phi': step0["gen_top_phi"], 'eta': step0["gen_top_eta"], 'M': step0["gen_top_mass"]})
    step0_gen_tbar = vector.zip({'pt': step0["gen_atop_pt"], 'phi': step0["gen_atop_phi"], 'eta': step0["gen_atop_eta"], 'M': step0["gen_atop_mass"]})
    step0_gen_l = vector.zip({'pt': step0["gen_lep_pt"], 'phi': step0["gen_lep_phi"], 'eta': step0["gen_lep_eta"], 'M': step0["gen_lep_mass"]})
    step0_gen_lbar = vector.zip({'pt': step0["gen_alep_pt"], 'phi': step0["gen_alep_phi"], 'eta': step0["gen_alep_eta"], 'M': step0["gen_alep_mass"]})

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
    

    ###########
    #GEN STEP0
    ###########
    step0_gen_boosted_lbar = step0_gen_lbar.boostCM_of(step0_gen_top)
    step0_gen_boosted_l = step0_gen_l.boostCM_of(step0_gen_tbar)

    step0_gen_k_axis = step0_gen_top.boostCM_of(step0_gen_top + step0_gen_tbar).to_xyz() #k_axis is defined by the direction of the tops
    step0_gen_scattering_angle = step0_gen_k_axis.theta
    step0_gen_sin_of_scattering_angle = np.sin(step0_gen_scattering_angle)

    step0_gen_sin_of_scattering_angle = np.where(np.abs(step0_gen_sin_of_scattering_angle) < 1e-5, 1e-5, step0_gen_sin_of_scattering_angle)
    step0_gen_axis_coefficient = np.sign(np.cos(step0_gen_scattering_angle)) / np.abs(step0_gen_sin_of_scattering_angle)
    step0_gen_r_axis = step0_gen_axis_coefficient * (p_axis - step0_gen_k_axis * np.cos(step0_gen_scattering_angle))
    step0_gen_n_axis = step0_gen_axis_coefficient * p_axis.cross(step0_gen_k_axis)

    step0_gen_boosted_lbar = step0_gen_lbar.boostCM_of(step0_gen_top)
    step0_gen_boosted_l = step0_gen_l.boostCM_of(step0_gen_tbar)

    step0_gen_cosphi = np.cos(step0_gen_boosted_lbar.deltaangle(step0_gen_boosted_l).to_numpy())

    step0_gen_cos_theta1k = np.cos(step0_gen_boosted_lbar.deltaangle(step0_gen_k_axis).to_numpy())
    step0_gen_cos_theta1r = np.cos(step0_gen_boosted_lbar.deltaangle(step0_gen_r_axis).to_numpy())
    step0_gen_cos_theta1n = np.cos(step0_gen_boosted_lbar.deltaangle(step0_gen_n_axis).to_numpy())
    step0_gen_cos_theta2k = np.cos(step0_gen_boosted_l.deltaangle(step0_gen_k_axis).to_numpy())
    step0_gen_cos_theta2r = np.cos(step0_gen_boosted_l.deltaangle(step0_gen_r_axis).to_numpy())
    step0_gen_cos_theta2n = np.cos(step0_gen_boosted_l.deltaangle(step0_gen_n_axis).to_numpy())

    step0_gen_c_rr = step0_gen_cos_theta1r*step0_gen_cos_theta2r
    step0_gen_c_rk = step0_gen_cos_theta1r*step0_gen_cos_theta2k
    step0_gen_c_rn = step0_gen_cos_theta1r*step0_gen_cos_theta2n

    step0_gen_c_kr = step0_gen_cos_theta1k*step0_gen_cos_theta2r
    step0_gen_c_kk = step0_gen_cos_theta1k*step0_gen_cos_theta2k
    step0_gen_c_kn = step0_gen_cos_theta1k*step0_gen_cos_theta2n

    step0_gen_c_nr = step0_gen_cos_theta1n*step0_gen_cos_theta2r
    step0_gen_c_nk = step0_gen_cos_theta1n*step0_gen_cos_theta2k
    step0_gen_c_nn = step0_gen_cos_theta1n*step0_gen_cos_theta2n
    
    ###########
    #GEN STEP8
    ###########
    gen_boosted_lbar = gen_lbar.boostCM_of(gen_top)
    gen_boosted_l = gen_l.boostCM_of(gen_tbar)


    gen_k_axis = gen_top.boostCM_of(gen_top + gen_tbar).to_xyz() #k_axis is defined by the direction of the tops
    gen_scattering_angle = gen_k_axis.theta
    gen_sin_of_scattering_angle = np.sin(gen_scattering_angle)

    gen_sin_of_scattering_angle = np.where(np.abs(gen_sin_of_scattering_angle) < 1e-5, 1e-5, gen_sin_of_scattering_angle)
    gen_axis_coefficient = np.sign(np.cos(gen_scattering_angle)) / np.abs(gen_sin_of_scattering_angle)
    gen_r_axis = gen_axis_coefficient * (p_axis - gen_k_axis * np.cos(gen_scattering_angle))
    gen_n_axis = gen_axis_coefficient * p_axis.cross(gen_k_axis)

    gen_boosted_lbar = gen_lbar.boostCM_of(gen_top)
    gen_boosted_l = gen_l.boostCM_of(gen_tbar)

    gen_cosphi = np.cos(gen_boosted_lbar.deltaangle(gen_boosted_l).to_numpy())

    gen_cos_theta1k = np.cos(gen_boosted_lbar.deltaangle(gen_k_axis).to_numpy())
    gen_cos_theta1r = np.cos(gen_boosted_lbar.deltaangle(gen_r_axis).to_numpy())
    gen_cos_theta1n = np.cos(gen_boosted_lbar.deltaangle(gen_n_axis).to_numpy())
    gen_cos_theta2k = np.cos(gen_boosted_l.deltaangle(gen_k_axis).to_numpy())
    gen_cos_theta2r = np.cos(gen_boosted_l.deltaangle(gen_r_axis).to_numpy())
    gen_cos_theta2n = np.cos(gen_boosted_l.deltaangle(gen_n_axis).to_numpy())

    gen_c_rr = gen_cos_theta1r*gen_cos_theta2r
    gen_c_rk = gen_cos_theta1r*gen_cos_theta2k
    gen_c_rn = gen_cos_theta1r*gen_cos_theta2n

    gen_c_kr = gen_cos_theta1k*gen_cos_theta2r
    gen_c_kk = gen_cos_theta1k*gen_cos_theta2k
    gen_c_kn = gen_cos_theta1k*gen_cos_theta2n

    gen_c_nr = gen_cos_theta1n*gen_cos_theta2r
    gen_c_nk = gen_cos_theta1n*gen_cos_theta2k
    gen_c_nn = gen_cos_theta1n*gen_cos_theta2n

    spincorr_vars_dict = {

                "ll_cHel" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_cosphi,
                    "val_8" : cosphi,
                    "gen_val_8" : gen_cosphi, 
                    "can_symmetrize" : True,
                },

                "b1k" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_cos_theta1k,
                    "val_8" : cos_theta1k,
                    "gen_val_8" : gen_cos_theta1k, 
                    "can_symmetrize" : True,
                },
                "b2k" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_cos_theta2k,
                    "val_8" : cos_theta2k,
                    "gen_val_8" : gen_cos_theta2k, 
                    "can_symmetrize" : True,
                },
                "b1r" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_cos_theta1r,
                    "val_8" : cos_theta1r,
                    "gen_val_8" : gen_cos_theta1r, 
                    "can_symmetrize" : True,
                },
                "b2r" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_cos_theta2r,
                    "val_8" : cos_theta2r,
                    "gen_val_8" : gen_cos_theta2r, 
                    "can_symmetrize" : True,
                },
                "b1n" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_cos_theta1n,
                    "val_8" : cos_theta1n,
                    "gen_val_8" : gen_cos_theta1n, 
                    "can_symmetrize" : True,
                },
                "b2n" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_cos_theta2n,
                    "val_8" : cos_theta2n,
                    "gen_val_8" : gen_cos_theta2n, 
                    "can_symmetrize" : True,
                },

                "c_kk" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_c_kk,
                    "val_8" : c_kk,
                    "gen_val_8" : gen_c_kk, 
                    "can_symmetrize" : True,
                },
                "c_rr" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_c_rr,
                    "val_8" : c_rr,
                    "gen_val_8" : gen_c_rr, 
                    "can_symmetrize" : True,
                },
                "c_nn" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_c_nn,
                    "val_8" : c_nn,
                    "gen_val_8" : gen_c_nn,
                    "can_symmetrize" : True,
                },

                "c_Prk" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_c_rk + step0_gen_c_kr,
                    "val_8" : c_rk + c_kr,
                    "gen_val_8" : gen_c_rk + gen_c_kr, 
                    "can_symmetrize" : True,
                },
                "c_Mrk" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_c_rk - step0_gen_c_kr,
                    "val_8" : c_rk - c_kr,
                    "gen_val_8" : gen_c_rk - gen_c_kr, 
                    "can_symmetrize" : True,
                },
                "c_Pnr" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_c_nr + step0_gen_c_kn,
                    "val_8" : c_nr + c_kn,
                    "gen_val_8" : gen_c_nr + gen_c_kn, 
                    "can_symmetrize" : True,
                },
                "c_Mnr" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_c_nr - step0_gen_c_kn,
                    "val_8" : c_nr - c_kn,
                    "gen_val_8" : gen_c_nr - gen_c_kn, 
                    "can_symmetrize" : True,
                },
                "c_Pnk" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_c_nk + step0_gen_c_kn,
                    "val_8" : c_nk + c_kn,
                    "gen_val_8" : gen_c_nk + gen_c_kn, 
                    "can_symmetrize" : True,
                },
                "c_Mnk" : {
                    "bin_edge_low" : -1.0, 
                    "bin_edge_high" : 1.0, 
                    "n_gen_bins" : 6, 
                    "n_reco_bins" : 12, 
                    "residual_bin_edge_low" : -2.0, 
                    "residual_bin_edge_high" : 2.0, 
                    "n_residual_bins" : 80,
                    "gen_val_0" : step0_gen_c_nk - step0_gen_c_kn,
                    "val_8" : c_nk - c_kn,
                    "gen_val_8" : gen_c_nk - gen_c_kn, 
                    "can_symmetrize" : True,
                },
            }

    kinematic_vars_dict = {
            "lep_pt" : {
                "bin_edge_low" : 0.0, 
                "bin_edge_high" : 200.0, 
                "n_gen_bins" : 40, 
                "n_reco_bins" : 40, 
                "residual_bin_edge_low" : -2.0, 
                "residual_bin_edge_high" : 2.0, 
                "n_residual_bins" : 80,
                "gen_val_0" : step0_gen_l.pt, 
                "val_8" : l.pt,
                "gen_val_8" : gen_l.pt, 
                "can_symmetrize" : True,
                },
            "lbar_pt" : {
                "bin_edge_low" : 0.0, 
                "bin_edge_high" : 200.0, 
                "n_gen_bins" : 40, 
                "n_reco_bins" : 40, 
                "residual_bin_edge_low" : -2.0, 
                "residual_bin_edge_high" : 2.0, 
                "n_residual_bins" : 80,
                "gen_val_0" : step0_gen_lbar.pt, 
                "val_8" : lbar.pt,
                "gen_val_8" : gen_lbar.pt, 
                "can_symmetrize" : True,
                },
            "top_pt" : {
                "bin_edge_low" : 0.0, 
                "bin_edge_high" : 200.0, 
                "n_gen_bins" : 40, 
                "n_reco_bins" : 40, 
                "residual_bin_edge_low" : -2.0, 
                "residual_bin_edge_high" : 2.0, 
                "n_residual_bins" : 80,
                "gen_val_0" : step0_gen_top.pt, 
                "val_8" : top.pt,
                "gen_val_8" : gen_top.pt, 
                "can_symmetrize" : True,
                },
            "tbar_pt" : {
                "bin_edge_low" : 0.0, 
                "bin_edge_high" : 200.0, 
                "n_gen_bins" : 50, 
                "n_reco_bins" : 50, 
                "residual_bin_edge_low" : -2.0, 
                "residual_bin_edge_high" : 2.0, 
                "n_residual_bins" : 80,
                "gen_val_0" : step0_gen_tbar.pt, 
                "val_8" : tbar.pt,
                "gen_val_8" : gen_tbar.pt, 
                "can_symmetrize" : True,
                },
            "lep_eta" : {
                "bin_edge_low" : -10, 
                "bin_edge_high" : +10, 
                "n_gen_bins" : 50, 
                "n_reco_bins" : 50, 
                "residual_bin_edge_low" : -2.0, 
                "residual_bin_edge_high" : 2.0, 
                "n_residual_bins" : 80,
                "gen_val_0" : step0_gen_l.eta, 
                "val_8" : l.eta,
                "gen_val_8" : gen_l.eta, 
                "can_symmetrize" : True,
                },
           "lbar_eta" : {
                "bin_edge_low" : -10, 
                "bin_edge_high" : +10, 
                "n_gen_bins" : 50, 
                "n_reco_bins" : 50, 
                "residual_bin_edge_low" : -2.0, 
                "residual_bin_edge_high" : 2.0, 
                "n_residual_bins" : 80,
                "gen_val_0" : step0_gen_lbar.eta, 
                "val_8" : lbar.eta,
                "gen_val_8" : gen_lbar.eta, 
                "can_symmetrize" : True,
                },
           "top_eta" : {
                "bin_edge_low" : -10, 
                "bin_edge_high" : +10, 
                "n_gen_bins" : 50, 
                "n_reco_bins" : 50, 
                "residual_bin_edge_low" : -2.0, 
                "residual_bin_edge_high" : 2.0, 
                "n_residual_bins" : 80,
                "gen_val_0" : step0_gen_top.eta, 
                "val_8" : top.eta,
                "gen_val_8" : gen_top.eta, 
                "can_symmetrize" : True,
                },
           "tbar_eta" : {
                "bin_edge_low" : -10, 
                "bin_edge_high" : +10, 
                "n_gen_bins" : 50, 
                "n_reco_bins" : 50, 
                "residual_bin_edge_low" : -2.0, 
                "residual_bin_edge_high" : 2.0, 
                "n_residual_bins" : 80,
                "gen_val_0" : step0_gen_tbar.eta, 
                "val_8" : tbar.eta,
                "gen_val_8" : gen_tbar.eta, 
                "can_symmetrize" : True,
                },
           "lep_phi" : {
                "bin_edge_low" : -np.pi, 
                "bin_edge_high" : +np.pi, 
                "n_gen_bins" : 40, 
                "n_reco_bins" : 40, 
                "residual_bin_edge_low" : -2.0, 
                "residual_bin_edge_high" : 2.0, 
                "n_residual_bins" : 80,
                "gen_val_0" : step0_gen_l.phi, 
                "val_8" : l.phi,
                "gen_val_8" : gen_l.phi, 
                "can_symmetrize" : True,
                },
            "lbar_phi" : {
                "bin_edge_low" : -np.pi, 
                "bin_edge_high" : +np.pi, 
                "n_gen_bins" : 40, 
                "n_reco_bins" : 40, 
                "residual_bin_edge_low" : -2.0, 
                "residual_bin_edge_high" : 2.0, 
                "n_residual_bins" : 80,
                "gen_val_0" : step0_gen_lbar.phi, 
                "val_8" : lbar.phi,
                "gen_val_8" : gen_lbar.phi, 
                "can_symmetrize" : True,
                },
            "top_phi" : {
                "bin_edge_low" : -np.pi, 
                "bin_edge_high" : +np.pi, 
                "n_gen_bins" : 40, 
                "n_reco_bins" : 40, 
                "residual_bin_edge_low" : -2.0, 
                "residual_bin_edge_high" : 2.0, 
                "n_residual_bins" : 80,
                "gen_val_0" : step0_gen_top.phi, 
                "val_8" : top.phi,
                "gen_val_8" : gen_top.phi, 
                "can_symmetrize" : True,
                },
            "tbar_phi" : {
                "bin_edge_low" : -np.pi, 
                "bin_edge_high" : +np.pi, 
                "n_gen_bins" : 40, 
                "n_reco_bins" : 40, 
                "residual_bin_edge_low" : -2.0, 
                "residual_bin_edge_high" : 2.0, 
                "n_residual_bins" : 80,
                "gen_val_0" : step0_gen_tbar.phi, 
                "val_8" : tbar.phi,
                "gen_val_8" : gen_tbar.phi, 
                "can_symmetrize" : True,
                },
        }




    binning_ttbar_mass = [300., 450., 600., 800., 2000.]
    binning_top_scatteringangle_ttbarframe = [-1.0, -0.5, 0.0, +0.5, +1.0]



    vars2D_dict = {

        "ttbar_mass" : {
            "bin_edge_low" : 300., 
            "bin_edge_high" : 2000., 
            "gen_binning" : binning_ttbar_mass,
            "reco_binning" : BinFinely(binning_ttbar_mass, 2),
            "residual_bin_edge_low" : -1000.0, 
            "residual_bin_edge_high" : 1000.0, 
            "n_residual_bins" : 100,
            "gen_val_0" : (step0_gen_top + step0_gen_tbar).M,
            "val_8" : (top + tbar).M,
            "gen_val_8" : (gen_top + gen_tbar).M,
            "can_symmetrize" : False,
        },

        "top_scatteringangle_ttbarframe" : {
            "bin_edge_low" : -1.0, 
            "bin_edge_high" : 1.0, 
            "gen_binning" : binning_top_scatteringangle_ttbarframe,
            "reco_binning" : BinFinely(binning_top_scatteringangle_ttbarframe, 2),
            "residual_bin_edge_low" : -2.0, 
            "residual_bin_edge_high" : 2.0, 
            "n_residual_bins" : 80,
            "gen_val_0" : step0_gen_scattering_angle,
            "val_8" : scattering_angle,
            "gen_val_8" : gen_scattering_angle,
            "can_symmetrize" : False,
        },

    }


    nFineBins_1D = 4
    nFineBins_2D = 2


    do_symmetrize = False

    # 1D

    prefix = ""

    #Placeholder for weights
    weights0 = np.ones(len(spincorr_vars_dict["c_Mnk"]["gen_val_0"]))
    weights8 = np.ones(len(spincorr_vars_dict["c_Mnk"]["val_8"]))


    for var1D in spincorr_vars_dict.keys():


        if(do_symmetrize*spincorr_vars_dict[var1D]["can_symmetrize"] == True): prefix = "RecoSym"
        else: prefix = "Reco"

        #axes
        reco_axes = [hist.axis.Regular(nFineBins_1D*spincorr_vars_dict[var1D]["n_reco_bins"], spincorr_vars_dict[var1D]["bin_edge_low"], spincorr_vars_dict[var1D]["bin_edge_high"], name="reco_"+var1D, label="reco_"+var1D, underflow=True, overflow=True)]
        gen_axes = [hist.axis.Regular(nFineBins_1D*spincorr_vars_dict[var1D]["n_gen_bins"], spincorr_vars_dict[var1D]["bin_edge_low"], spincorr_vars_dict[var1D]["bin_edge_high"], name="gen_"+var1D, label="gen_"+var1D, underflow=True, overflow=True),]
        residual_axes = [hist.axis.Regular(spincorr_vars_dict[var1D]["n_residual_bins"], spincorr_vars_dict[var1D]["residual_bin_edge_low"], spincorr_vars_dict[var1D]["residual_bin_edge_high"], name="residual_"+var1D, label="residual_"+var1D, underflow=True, overflow=True)]

        #gen, reco, resolution, resmat plots
        reco = compute_reco(var1D, reco_axes, [spincorr_vars_dict[var1D]["val_8"]], [weights8], do_symmetrize*spincorr_vars_dict[var1D]["can_symmetrize"])
        hreco = Convert_to_TH1(prefix, var1D, reco)
        hreco.Write(hreco.GetName(),TObject.kOverwrite)

        gen = compute_gen(var1D, gen_axes, [spincorr_vars_dict[var1D]["gen_val_0"]], [weights0], do_symmetrize*spincorr_vars_dict[var1D]["can_symmetrize"])
        hgen = Convert_to_TH1("hgen", var1D, gen)
        hgen.Write(hgen.GetName(),TObject.kOverwrite)

        resolution = compute_resolution(var1D, residual_axes, reco_axes, [spincorr_vars_dict[var1D]["val_8"]], [spincorr_vars_dict[var1D]["gen_val_8"]],[weights8])            
        hresolution = Convert_to_TH2("hresolutionbins", var1D, resolution)
        hresolution.Write(hresolution.GetName(),TObject.kOverwrite)

        resmat = compute_response_matrix(var1D, gen_axes, reco_axes, [spincorr_vars_dict[var1D]["gen_val_8"]], [spincorr_vars_dict[var1D]["val_8"]], [spincorr_vars_dict[var1D]["gen_val_0"]], [weights8], [weights8], [weights0], do_symmetrize*spincorr_vars_dict[var1D]["can_symmetrize"])
        hresmat = Convert_to_TH2("hrecoVsgen", var1D, resmat)
        hresmat.Write(hresmat.GetName(),TObject.kOverwrite)
    
    for var1D in kinematic_vars_dict.keys():
        
        if(do_symmetrize*kinematic_vars_dict[var1D]["can_symmetrize"] == True): prefix = "RecoSym"
        else: prefix = "Reco"

        gen_axes = [hist.axis.Regular(nFineBins_1D*kinematic_vars_dict[var1D]["n_gen_bins"], kinematic_vars_dict[var1D]["bin_edge_low"], kinematic_vars_dict[var1D]["bin_edge_high"], name="gen_"+var1D, label="gen_"+var1D, underflow=True, overflow=True),]
        reco_axes = [hist.axis.Regular(nFineBins_1D*kinematic_vars_dict[var1D]["n_reco_bins"], kinematic_vars_dict[var1D]["bin_edge_low"], kinematic_vars_dict[var1D]["bin_edge_high"], name="reco_"+var1D, label="reco_"+var1D, underflow=True, overflow=True),]
        gen_axes = [hist.axis.Regular(nFineBins_1D*kinematic_vars_dict[var1D]["n_residual_bins"], kinematic_vars_dict[var1D]["residual_bin_edge_low"], kinematic_vars_dict[var1D]["residual_bin_edge_high"], name="residual_"+var1D, label="residual_"+var1D, underflow=True, overflow=True),]

        reco = compute_reco(var1D, reco_axes, [kinematic_vars_dict[var1D]["val_8"]], [weights8], do_symmetrize*kinematic_vars_dict[var1D]["can_symmetrize"])
        hreco = Convert_to_TH1(prefix, var1D, gen)
        hreco.Write(hreco.GetName(),TObject.kOverwrite)
        
        gen = compute_reco(var1D, reco_axes, [kinematic_vars_dict[var1D]["gen_val_0"]], [weights0], do_symmetrize*kinematic_vars_dict[var1D]["can_symmetrize"])
        hgen = Convert_to_TH1("hgen", var1D, gen)
        hgen.Write(hgen.GetName(),TObject.kOverwrite)
        
        resolution = compute_resolution(var1D, residual_axes, reco_axes, [kinematic_vars_dict[var1D]["val_8"]], [kinematic_vars_dict[var1D]["gen_val_8"]],[weights8])            
        hresolution = Convert_to_TH2("hresolutionbins", var1D, resolution)
        hresolution.Write()


        resmat = compute_response_matrix(var1D, gen_axes, reco_axes, [kinematic_vars_dict[var1D]["gen_val_8"]], [kinematic_vars_dict[var1D]["val_8"]], [kinematic_vars_dict[var1D]["gen_val_0"]], [weights8], [weights8], [weights0], do_symmetrize*kinematic_vars_dict[var1D]["can_symmetrize"])
        hresmat = Convert_to_TH2("hrecoVsgen", var1D, resmat)
        hresmat.Write(hresmat.GetName(),TObject.kOverwrite)


   # 2D

    for var2D in vars2D_dict.keys():

        reco_axes_2D = [hist.axis.Variable(BinFinely(vars2D_dict[var2D]["reco_binning"],nFineBins_2D), name="reco2D_"+var2D, label="reco2D_"+var2D, underflow=True, overflow=True)]

        for var1D in spincorr_vars_dict.keys():

            if(do_symmetrize*spincorr_vars_dict[var1D]["can_symmetrize"] == True): prefix = "RecoSym"
            else: prefix = "Reco"

            reco_axes = [hist.axis.Regular(nFineBins_2D*spincorr_vars_dict[var1D]["n_reco_bins"], spincorr_vars_dict[var1D]["bin_edge_low"], spincorr_vars_dict[var1D]["bin_edge_high"], name="reco_"+var1D, label="reco_"+var1D, underflow=True, overflow=True)]

            reco = compute_reco(var1D+"_"+var2D, reco_axes + reco_axes_2D, [spincorr_vars_dict[var1D]["val_8"], vars2D_dict[var2D]["val_8"]], [weights8], do_symmetrize*spincorr_vars_dict[var1D]["can_symmetrize"])
            hreco = Unwrap_to_TH1(prefix, var1D, var2D, reco)
            hreco.Write(hreco.GetName(),TObject.kOverwrite)


        if var2D == "ExtraJets":
            reco_axes_2D = [hist.axis.Variable(BinFinely(vars2D_dict[var2D]["reco_binning"],1), name="reco2D_"+var2D, label="reco2D_"+var2D, underflow=True, overflow=True)]
        else:
            reco_axes_2D = [hist.axis.Variable(BinFinely(vars2D_dict[var2D]["reco_binning"],4), name="reco2D_"+var2D, label="reco2D_"+var2D, underflow=True, overflow=True)]

        if(do_symmetrize*vars2D_dict[var2D]["can_symmetrize"] == True): prefix = "RecoSym"
        else: prefix = "Reco"

        reco = compute_reco(var2D, reco_axes_2D, [vars2D_dict[var2D]["val_8"]], [weights8], do_symmetrize*vars2D_dict[var2D]["can_symmetrize"])
        hreco = Convert_to_TH1(prefix, var2D, reco)
        hreco.Write(hreco.GetName(),TObject.kOverwrite)


    outHistFile.Close()

##############################

if __name__ == "__main__":

    main()

##############################  
