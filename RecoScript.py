#Reco Command: python Top_reco/Top_reco.py -i events_test.root

import os
f     = open('filelist.txt', 'r')
lines = f.readlines()

sh_file = 'Reco_commands.sh'


commandfile = open(sh_file, 'w')


for line in lines :
    
    line = line.strip('\n')
    inputfilestring = "minitree_" +line.replace("/mnt/hadoop/store/user/hyeonseo/mgp8_pp_tt012j_5f/events_","")
    commandfile.write("python Top_reco/Top_reco.py -i MiniTreeOutput/"+ inputfilestring +"\n")
    
    
f.close()
commandfile.close()
