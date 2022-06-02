#!/usr/bin/env python
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("commandlist")
args = parser.parse_args()

FCC_BASE = str(os.getenv("FCC_BASE"))

if not os.path.exists("MiniTreeOutput"): os.makedirs("MiniTreeOutput")
if not os.path.exists("RecoOutput"): os.makedirs("RecoOutput")

i = 0

if os.path.exists("SlurmJobs"):
    for job in os.listdir("SlurmJobs"):
        if i < int(job.strip('SlurmJob_').strip('.sh')): 
            i = int(job.strip('SlurmJob_').strip('.sh'))

else: os.makedirs("SlurmJobs")


commandlistfilepath = args.commandlist
commandlistfile     = open(commandlistfilepath, "r")
lines = commandlistfile.readlines()


runfile = open("RunSlurm_"+os.path.basename(commandlistfilepath).rsplit(".",1)[0]+".sh", "w")

runfile.write("#!/bin/sh")
runfile.write("\n")

for line in lines :
    if len(str(line.strip())) == 0: continue
    if str(line)[0] == "#": continue
    if str(line) == "\n": continue

    i   += 1
    line = line.strip("\n")
    sh_file = "SlurmJobs/SlurmJob_" + str(i) + ".sh"
    
    with open(sh_file, "w") as cfg :
        cfg.write("#!/bin/sh")
        cfg.write("\n")
        cfg.write("#SBATCH  -A cms")
        cfg.write("\n")
        cfg.write("#SBATCH --nodes=1")
        cfg.write("\n")
        cfg.write("#SBATCH --time=3:00:00")
        cfg.write("\n")
        cfg.write("#SBATCH --mem=8000")
        cfg.write("\n")
        cfg.write("cd " + FCC_BASE )
        cfg.write("\n")
        cfg.write("module load anaconda/5.3.1-py37")
        cfg.write("\n")
        cfg.write("source activate venv")
        cfg.write("\n")
        cfg.write("source /cvmfs/fcc.cern.ch/sw/latest/setup.sh")
        cfg.write("\n")
        cfg.write(str(line))


    runfile.write("sbatch SlurmJobs/SlurmJob_" + str(i) + ".sh")
    runfile.write("\n")
