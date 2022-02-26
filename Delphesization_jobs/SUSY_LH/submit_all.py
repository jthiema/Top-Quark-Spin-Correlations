import subprocess

for count in range(44) :
    count += 1
    subprocess.call('sbatch Delphesize_SUSY_LH_' + str(count) + '.sh', shell=True)

