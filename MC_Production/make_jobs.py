import subprocess

# List of masses for which we have tarballs
stop_masses  = [300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 1200]

# Construct points along the line |(mstop - mchi0) - mtop| = 0, 10, 20 or 30 GeV
mtop         = 175 # in GeV, a useful approximation for now
allowed_diff = [-30, -20, -10, 0, 10, 20, 30]

for mstop in stop_masses :
    for ad in allowed_diff :
        mchi0   =  (mstop - mtop) - (ad) 

        # Directory name
        folder_name  = 'SUSY_mstop_' + str(mstop) + '_mchi0_' + str(mchi0)
        for i in range(1,101) :
            sh_file  = 'SUSY_mstop_' + str(mstop) + '_mchi0_' + str(mchi0) + '_slurm_' + str(i) + '.sh'  
            cfg_file = 'SUSY_mstop_' + str(mstop) + '_mchi0_' + str(mchi0) + '_cfg_'   + str(i) + '.py' 

            # Create a subfolder for the output files otherwise clashes in tarring and untarring
            subfolder_name = cfg_file.strip('.py')

            with open(sh_file, 'w') as cfg :
                cfg.write("#!/bin/sh")
                cfg.write("\n")
                cfg.write("#SBATCH  -A cms")
                cfg.write("\n")
                cfg.write("#SBATCH --nodes=1")
                cfg.write("\n")
                cfg.write("#SBATCH --time=02:00:00")
                cfg.write("\n")
                cfg.write("cd /depot/cms/top/bakshi3/MC_production/CMSSW_10_6_0/src/Production_jobs_40k/")
                cfg.write("\n")
                cfg.write("cd " + str(folder_name))
                cfg.write("\n")
                cfg.write("mkdir " + str(subfolder_name))
                cfg.write("\n")
                cfg.write("cp " + str(cfg_file) + ' ' + str(subfolder_name))
                cfg.write("\n")
                cfg.write("cd " + str(subfolder_name))
                cfg.write("\n")
                cfg.write("source /cvmfs/cms.cern.ch/cmsset_default.sh")
                cfg.write("\n")
                cfg.write("eval `scramv1 runtime -sh`")
                cfg.write("\n")
                cfg.write("cmsRun " + str(cfg_file))
                cfg.write("\n")