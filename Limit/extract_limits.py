import re
import uproot
import numpy as np

def main() :
    filelist     = open('filelist', 'r')
    lines        = filelist.readlines()

    twosig_minus = []
    onesig_minus = []
    median       = []
    onesig_plus  = []
    twosig_plus  = []

    for line in lines :
        ipfile   = line.strip('\n')
        masses   = re.findall("[0-9]+", ipfile)
        mstop    = int(masses[0])
        mchi0    = int(masses[1])

        if mstop - mchi0 == 175 or mstop - mchi0 == 174 :
            fileptr  = uproot.open(ipfile)['limit']
            limits   = fileptr['limit'].array()

            quantiles = [2.5, 16, 50, 84, 97.5]
            tm, om, med, op, tp = np.percentile(np.array(limits), quantiles)

            twosig_minus.append(tm)
            onesig_minus.append(om)
            median.append(med)
            onesig_plus.append(op)
            twosig_plus.append(tp)

            print('Processing file :: ' + str(ipfile))

        else : continue

    print('-2 sigma :: ' + str(twosig_minus))
    print('-1 sigma :: ' + str(onesig_minus))
    print('  Median :: ' + str(median))
    print('+1 sigma :: ' + str(onesig_plus))
    print('+2 sigma :: ' + str(twosig_plus))
    
if __name__ == '__main__' :
    main()