import subprocess

fileptr = open('missing','r')
lines   = fileptr.readlines()

for line in lines:
    line = line.strip('\n')
    subprocess.call('sbatch Ntuple_' + str(line) + '.sh', shell=True)

