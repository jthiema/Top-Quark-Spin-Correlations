f     = open('filelist_root', 'r')
lines = f.readlines()


for line in lines :
    line = line.strip('\n')
    sh_file = 'Pkl_' + str(line) + '.sh'
    
    with open(sh_file, 'w') as cfg :
        cfg.write("#!/bin/sh")
        cfg.write("\n")
        cfg.write("#SBATCH  -A cms")
        cfg.write("\n")
        cfg.write("#SBATCH --nodes=1")
        cfg.write("\n")
        cfg.write("#SBATCH --time=00:10:00")
        cfg.write("\n")
        cfg.write("cd /depot/cms/top/bakshi3/SUSY_2018/Top_reco_op/")
        cfg.write("\n")
        cfg.write("module load anaconda/5.3.1-py37")
        cfg.write("\n")
        cfg.write("source activate venv")
        cfg.write("\n")
        cfg.write("python SUSY_dfs_parallel.py -i " + str(line) + " -o " + str(line).strip('.root') + ".pkl")
        cfg.write("\n")
