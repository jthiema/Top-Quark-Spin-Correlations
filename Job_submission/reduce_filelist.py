import re

def main():
    fileptr = open('filelist_desy', 'r')
    lines   = fileptr.readlines()

    outfile = open('outfile', 'w+')
    for line in lines :
        line = line.strip('\n')

	filename1 = re.findall('TTJets_DiLept_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_200PU_[0-9]+.root', line)
        filename2 = re.findall('TTJets_DiLept_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_[0-9]+_[0-9]+.root', line)
        filename3 = re.findall('TTJets_DiLept_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_[0-9]+_[0-9]+[a-z]+.root', line)

        if len(filename1) >  0 :
           outfile.write('%s\n' %filename1)

        elif len(filename2) >  0 :
           outfile.write('%s\n' %filename2)

        elif len(filename3) >  0 :
           outfile.write('%s\n' %filename3)
main()
