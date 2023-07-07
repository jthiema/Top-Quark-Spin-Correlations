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
runfile.write("export X509_USER_PROXY=~/x509up_u`id -u`")
runfile.write("\n")
runfile.write("voms-proxy-init -voms cms -valid 192:00:00")
runfile.write("\n")

# loop through every other line
for j in range(0,len(lines),2) :
    if len(str(lines[j].strip())) == 0: continue
    if str(lines[j])[0] == "#": continue
    if str(lines[j]) == "\n": continue

    sh_file = "SlurmJobs/SlurmJob_" + str(i) + ".sh"
    
    with open(sh_file, "w") as cfg :
        cfg.write("#!/bin/sh")
        cfg.write("\n")
        cfg.write("#SBATCH  -A cms")
        cfg.write("\n")
        cfg.write("#SBATCH --ntasks=1")
        cfg.write("\n")
        #cfg.write("#SBATCH --cpus-per-task=" + str(args.cpu))
        cfg.write("#SBATCH --cpus-per-task=1")
        cfg.write("\n")
        #cfg.write("#SBATCH --mem-per-cpu=" + str(args.mem))
        cfg.write("#SBATCH --mem-per-cpu=8000")
        cfg.write("\n")
        cfg.write("#SBATCH --time=1:59:00")
        cfg.write("\n")
        cfg.write("export X509_USER_PROXY=~/x509up_u`id -u`")
        cfg.write("\n")
        cfg.write("cd " + BASE )
        cfg.write("\n")
        cfg.write("source " + BASE + "/init.sh")
        cfg.write("\n")

        if j+0 < len(lines):
            cfg.write(str(lines[j].strip("\n")))
            cfg.write("\n")
        if j+1 < len(lines):
            cfg.write(str(lines[j+1].strip("\n")))
            cfg.write("\n")


    runfile.write("sbatch SlurmJobs/SlurmJob_" + str(i) + ".sh")
    runfile.write("\n")

    i   += 1
