import os
import subprocess

def main() :
    BASE_DIR  = os.getcwd() 
    with open ('filelist_dirs', 'r') as fileptr :
        lines = fileptr.readlines()
    
    for line in lines :
        line  = line.strip('\n')
        line  = line.strip('./')

        # Define input and output file and path names
        ip_file = str(line) + '.root'
        ip_path = os.path.join(BASE_DIR, line, ip_file)
        op_file = str(line) + '.pkl'
        op_path = os.path.join(BASE_DIR, op_file)

        # Use subprocess to make the pkl files for ML inputs
        print(f'python make_pkls.py -i {ip_path} -o {op_path} ')
        subprocess.call(f'python make_pkls.py -i {ip_path} -o {op_path} ', shell=True)

if __name__ == '__main__' :
    main()