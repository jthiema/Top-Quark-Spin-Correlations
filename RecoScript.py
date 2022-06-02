#Reco Command: python Top_reco/Top_reco.py -i events_test.root -o events_test_reco.root

import os
f     = open('filelist.txt', 'r')
lines = f.readlines()

sh_file = 'Reco_commands.sh'


commandfile = open(sh_file, 'w')

if not os.path.exists("RecoOutput"): os.makedirs("RecoOutput")



for line in lines :
    
    line = line.strip('\n')
    inputfilestring = "minitree_" +line.replace("/mnt/hadoop/store/user/hyeonseo/mgp8_pp_tt012j_5f/events_","")
    outputfilestring = "Top_Reco_" +line.replace("/mnt/hadoop/store/user/hyeonseo/mgp8_pp_tt012j_5f/events_","")
    commandfile.write("python Top_reco/Top_reco.py -i MiniTreeOutput/"+ inputfilestring +" -o RecoOutput/"+ outputfilestring +"\n")
    
    
f.close()
commandfile.close()