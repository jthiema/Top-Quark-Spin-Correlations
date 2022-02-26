import re
import os
import subprocess

fileptr = open('filelist_minitree', 'r')
lines   = fileptr.readlines()

for line in lines :
    line    = line.strip('\n')
    pattern = re.findall('[0-9]+', line)
    mstop   = pattern[0]
    mchi0   = pattern[1]

    folder_name = 'Mstop_' + str(mstop) + '_mchi0_' + str(mchi0)
    if not os.path.exists(folder_name) :
        os.mkdir(folder_name)

    print(f'mv {line} {folder_name}')
    subprocess.call(f'mv {line} {folder_name}', shell=True)