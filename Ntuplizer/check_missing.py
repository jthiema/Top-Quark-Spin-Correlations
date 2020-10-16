import re


def find_missing(lst): 
    return [x for x in range(lst[0], lst[-1]+1)  
                               if x not in lst] 
def main() :
    fileptr  = open('filelist')
    lines    = fileptr.readlines()
    pat_list = []

    for line in lines :
    	line      = line.strip('\n')
    	pattern   = re.findall('SUSY_Ntuple_[0-9]+', line)[0]
    	pattern   = int(pattern.strip('SUSY_Ntuple_'))
    	pat_list.append(pattern)
    	pat_list.sort()

    missing = find_missing(pat_list)

    with open('missing', 'w') as f:
	for item in missing:
            f.write("%d\n" % item)

main()

