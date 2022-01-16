import os
import subprocess

fileptr = open('filelist', 'r')
lines   = fileptr.readlines()

# We need 1 million events per mass point
# Thus 100 cfg files to be run with 100 different seeds per mass point
# 12 mass points * 7 along the line * 100 cfgs = 8400 cmsRun jobs

for line in lines :
    frag_name   = line.strip('\n')
    folder_name = frag_name.replace('_fragment.py', '')

    # 8400 is too many files, move them to folders with 100 jobs each
    if not os.path.exists(folder_name) :
        os.mkdir(folder_name)

    for i in range(1, 101) :
        cfg_name  = frag_name.replace('fragment', 'cfg_' + str(i))
        file_name = frag_name.replace('fragment.py', str(i) + '.root')

        print('Executing command ::')
        print('')
        print('cmsDriver.py Configuration/GenProduction/python/' + str(frag_name)       + 
            ' --fileout file:' + str(file_name) + ' -s LHE,GEN --eventcontent RAWSIM '  +
            ' --datatier GEN --conditions auto:mc --python_filename=' + str(cfg_name)   + 
            ' --beamspot Realistic25ns13TeVEarly2017Collision -n 40000 --no_exec --mc ' +
            ' --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(' + str(i) + ')"  ')

        subprocess.call('cmsDriver.py Configuration/GenProduction/python/' + str(frag_name)       + 
            ' --fileout file:' + str(file_name) + ' -s LHE,GEN --eventcontent RAWSIM '  +
            ' --datatier GEN --conditions auto:mc --python_filename=' + str(cfg_name)   + 
            ' --beamspot Realistic25ns13TeVEarly2017Collision -n 40000 --no_exec --mc ' +
            ' --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(' + str(i) + ')"  ', 
            shell=True)

        print('Done with cfg file :: '    + str(cfg_name))
        print('Now copying to folder :: ' + str(folder_name))
        print('mv ' + str(cfg_name) + ' ' + str(folder_name))
        subprocess.call('mv ' + str(cfg_name) + ' ' + str(folder_name), shell=True)

fileptr.close()