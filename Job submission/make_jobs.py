i     = 0
f     = open('filelist_mnt', 'r')
lines = f.readlines()


for line in lines :
    i   += 1
    line = line.strip('\n')
    sh_file = 'Ntuple_' + str(i) + '.sh'
    
    with open(sh_file, 'w') as cfg :
        cfg.write("#!/bin/sh")
        cfg.write("\n")
        cfg.write("#SBATCH  -A cms-a")
        cfg.write("\n")
        cfg.write("#SBATCH --nodes=1")
        cfg.write("\n")
        cfg.write("#SBATCH --time=06:00:00")
        cfg.write("\n")
        cfg.write("cd /depot/cms/users/bakshi3/CMSSW_9_1_0_pre3/delphes/")
        cfg.write("\n")
        cfg.write("source /cvmfs/cms.cern.ch/cmsset_default.sh")
        cfg.write("\n")
        cfg.write("export SCRAM_ARCH=slc6_amd64_gcc530")
        cfg.write("\n")
        cfg.write("eval `scramv1 runtime -sh`")
        cfg.write("\n")
        cfg.write("python Delphes_Ntuplizer_custom.py -i /mnt/hadoop/store/user/abakshi/TTBar_Delphes/" + str(line) + " -o /depot/cms/top/bakshi3/TTBar/TTBar_Ntuples/TT_Dilept_" + str(i) + ".root")
        cfg.write("\n")
