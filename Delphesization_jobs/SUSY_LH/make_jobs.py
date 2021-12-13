i     = 0 
f     = open('filelist', 'r')
lines = f.readlines()


for line in lines :
    i   += 1
    line = line.strip('\n')
    sh_file = 'Delphesize_SUSY_LH_' + str(i) + '.sh'
    
    with open(sh_file, 'w') as cfg :
        cfg.write("#!/bin/sh")
        cfg.write("\n")
        cfg.write("#SBATCH  -A cms-a")
        cfg.write("\n")
        cfg.write("#SBATCH --nodes=1")
        cfg.write("\n")
        cfg.write("#SBATCH --time=24:00:00")
        cfg.write("\n")
        cfg.write("cd /depot/cms/users/bakshi3/CMSSW_9_1_0_pre3/delphes/")
        cfg.write("\n")
        cfg.write("source /cvmfs/cms.cern.ch/cmsset_default.sh")
        cfg.write("\n")
        cfg.write("export SCRAM_ARCH=slc6_amd64_gcc530")
        cfg.write("\n")
        cfg.write("eval `scramv1 runtime -sh`")
        cfg.write("\n")
        cfg.write("./DelphesCMSFWLite cards/CMS_PhaseII/CMS_PhaseII_200PU_v03.tcl /depot/cms/top/bakshi3/SUSY/SC_samples/SUSY_LH/Delphes/SUSY_LH_" + str(i) + ".root  " + " /depot/cms/top/bakshi3/SUSY/SC_samples/SUSY_LH/MINIAODSIM/PU2017_12Apr2018_GridpackScan_94X_mc2017_realistic_v14-v1/240000/" + str(line))
        cfg.write("\n")
