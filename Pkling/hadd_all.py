import re
import os
import subprocess

def main() :
    BASE_DIR  = os.getcwd() 
    with open ('filelist_dirs', 'r') as fileptr :
        lines = fileptr.readlines()
    
    for line in lines :
        line = line.strip('\n')
        os.chdir(line)

        mstop   = re.findall('Mstop_[0-9]+', line)[0]
        mchi0   = re.findall('mchi0_[0-9]+', line)[0]
        op_file = str(mstop) + '_' + str(mchi0) + '.root'

        print(f'hadd {op_file} *.root ')
        subprocess.call(f'hadd {op_file} *.root ', shell=True)
        os.chdir(BASE_DIR)

if __name__ == '__main__' :
    main()