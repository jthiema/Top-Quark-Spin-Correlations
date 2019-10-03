#!/bin/python
import re  
import ROOT
import numpy  as np

def main() :
    
    full_arr = []
    PDF_hist = ROOT.TH1F('PDF_unc_percentage' , 'PDF_unc_percentage', 20, 0, 3.14159)
    Ren_hist = ROOT.TH1F('Ren_unc_percentage' , 'Ren_unc_percentage', 20, 0, 3.14159)

    # First use regex to read in the bin by bin numbers 
 
    # Over all files

    for i in range(0,110) :	
	if (i < 9) :
            filename  = 'Delta_Phi_Renorm_variation_' + str(i) +'.C'
            fileptr   = open(filename)

	else :
            filename  = 'Delta_Phi_PDF_variation_' + str(i) +'.C' 
	    fileptr   = open(filename)

        arr = []      # array for all bin content

        print('In file ::' + str(filename))

        # Over all lines

        for line in fileptr.readlines() :
		pattern = re.findall(r"SetBinContent\(\d+,\d+.\d+\)", line)

		# Over all matched patterns

		for string  in pattern :
			pat = re.sub(r"SetBinContent\(\d+,", " ", string)
                        pat = re.sub("\)", " ", pat)
		        arr.append(float(pat))

        full_arr.append(arr)
	print(full_arr[0])
    # Now implement the PDF uncertainties 

    # PDF Formula from https://arxiv.org/pdf/1510.03865.pdf page 49

    # Over all bins
    for i in range(20):
	arr_by_bin   = []

	# Over all histograms 
	for j in range(110) :
		arr_by_bin.append(full_arr[j][i])       # Slower so fix

        mean = np.array(arr_by_bin).mean()    		# The mean cross-section per bin <sigma>
 	std  = np.array(arr_by_bin).std()     		# Mean standard deviation per bin <delta_sigma>

	if (j < 9 ):
	   Ren_hist.SetBinContent(i,std/mean * 100)
	else :        
	   PDF_hist.SetBinContent(i,std/mean * 100)

        print('For bin ' + str(i))
	print('Percentage error ::' + str(std/mean * 100)) 

    Ren_hist.Draw('ep')
    Ren_hist.SaveAs('Ren_unc.C')

    PDF_hist.Draw('ep')
    PDF_hist.SaveAs('PDF_unc.C')
main() 

