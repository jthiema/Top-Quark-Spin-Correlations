import subprocess

for count in range(670) :
    count += 1
    #print('sbatch Ntuple_' + str(count) + '.sh')
    subprocess.call('sbatch Ntuple_' + str(count) + '.sh', shell=True)

