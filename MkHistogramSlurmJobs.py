#!/usr/bin/env python
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("commandlist")
args = parser.parse_args()

BASE = str(os.getenv("BASE"))

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

# loop through every other line
for j in range(0,len(lines),20) :
    if len(str(lines[j].strip())) == 0: continue
    if str(lines[j])[0] == "#": continue
    if str(lines[j]) == "\n": continue

    sh_file = "SlurmJobs/SlurmJob_" + str(i) + ".sh"
    
    with open(sh_file, "w") as cfg :
        cfg.write("#!/bin/sh")
        cfg.write("\n")
        cfg.write("#SBATCH  -A cms")
        cfg.write("\n")
        cfg.write("#SBATCH --nodes=1")
        cfg.write("\n")
        cfg.write("#SBATCH --time=0:19:00")
        cfg.write("\n")
        cfg.write("#SBATCH --mem=8000")
        cfg.write("\n")
        cfg.write("cd " + BASE )
        cfg.write("\n")
        cfg.write("module load anaconda/5.3.1-py37")
        cfg.write("\n")
        cfg.write("source activate venv")
        cfg.write("\n")
        cfg.write("source /cvmfs/fcc.cern.ch/sw/latest/setup.sh")
        cfg.write("\n")
        if j+0 < len(lines):
            cfg.write(str(lines[j].strip("\n")))
            cfg.write("\n")
        if j+1 < len(lines):
            cfg.write(str(lines[j+1].strip("\n")))
            cfg.write("\n") 
        if j+2 < len(lines):
            cfg.write(str(lines[j+2].strip("\n")))
            cfg.write("\n") 
        if j+3 < len(lines):
            cfg.write(str(lines[j+3].strip("\n")))
            cfg.write("\n") 
        if j+4 < len(lines):
            cfg.write(str(lines[j+4].strip("\n")))
            cfg.write("\n") 
        if j+5 < len(lines):
            cfg.write(str(lines[j+5].strip("\n")))
            cfg.write("\n") 
        if j+6 < len(lines):
            cfg.write(str(lines[j+6].strip("\n")))
            cfg.write("\n") 
        if j+7 < len(lines):
            cfg.write(str(lines[j+7].strip("\n")))
            cfg.write("\n") 
        if j+8 < len(lines):
            cfg.write(str(lines[j+8].strip("\n")))
            cfg.write("\n") 
        if j+9 < len(lines):
            cfg.write(str(lines[j+9].strip("\n")))
            cfg.write("\n") 
        if j+10 < len(lines):
            cfg.write(str(lines[j+10].strip("\n")))
            cfg.write("\n")
        if j+11 < len(lines):
            cfg.write(str(lines[j+11].strip("\n")))
            cfg.write("\n")
        if j+12 < len(lines):
            cfg.write(str(lines[j+12].strip("\n")))
            cfg.write("\n")
        if j+13 < len(lines):
            cfg.write(str(lines[j+13].strip("\n")))
            cfg.write("\n")
        if j+14 < len(lines):
            cfg.write(str(lines[j+14].strip("\n")))
            cfg.write("\n")
        if j+15 < len(lines):
            cfg.write(str(lines[j+15].strip("\n")))
            cfg.write("\n")
        if j+16 < len(lines):
            cfg.write(str(lines[j+16].strip("\n")))
            cfg.write("\n")
        if j+17 < len(lines):
            cfg.write(str(lines[j+17].strip("\n")))
            cfg.write("\n")
        if j+18 < len(lines):
            cfg.write(str(lines[j+18].strip("\n")))
            cfg.write("\n")
        if j+19 < len(lines):
            cfg.write(str(lines[j+19].strip("\n")))
            cfg.write("\n") 


    runfile.write("sbatch SlurmJobs/SlurmJob_" + str(i) + ".sh")
    runfile.write("\n")

    i   += 1
