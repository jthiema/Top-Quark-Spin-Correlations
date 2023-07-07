import os
f     = open('filelist.txt', 'r')
lines = f.readlines()

sh_file = 'Minitrees_Commands.sh'


commandfile = open(sh_file, 'w')

if not os.path.exists("MiniTreeOutput"): os.makedirs("MiniTreeOutput")



for line in lines :
    
    line = line.strip('\n')
    outputfilestring = "minitree_" +line.replace("root://eos.cms.rcac.purdue.edu//store/user/abakshi/TTBar_Ntuples/TT_Dilept_","")
    commandfile.write("python Minitrees/Make_minitrees.py -i "+line+" -o MiniTreeOutput/"+ outputfilestring +"\n")
    commandfile.write("python Top_reco/Top_reco.py -i MiniTreeOutput/"+ outputfilestring+"\n")
    
    
f.close()
commandfile.close()
