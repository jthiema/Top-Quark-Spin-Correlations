import uproot
import numpy as np

print('Reading in the file ')
fileptr = uproot.open('Root_files/Top_reco_op_w_jets.root')['Step8']

print('Done, now reading in the weight array')
weight  = fileptr['weight'].array()

# Extract the weights

for i in range(0,110) :
    
    # Store weights along i-axis
    temp_array = [] 

    print('Processing variation :: ' + str(i) + ' of 110')
    # Indices 0-9 correspond to renorm and factorization variations
    if (i < 10) :
        
        dir_path  = 'Weights/ttbar/Renorm/'
        var_file   = 'Renorm_variation_' + str(i)
        
    # Indices 10-110 correspond to PDF variations
    else :
        dir_path  = 'Weights/ttbar/PDF/'
        var_file   = 'PDF_variation_'    + str(i)
         
    for j in range(len(weight)) :

        temp_array.append(weight[j][i])
            
    temp_array = np.array(temp_array)
    np.savetxt(dir_path + var_file + '.txt', temp_array)
    