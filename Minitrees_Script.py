"""
i     = 0
f     = open('filelist.txt', 'r')
lines = f.readlines()


for line in lines :
    i   += 1
    line = line.strip('\n')
for every file in file list, make a command like this:
python Minitrees/Make_minitrees.py -i /mnt/hadoop/store/user/hyeonseo/mgp8_pp_tt012j_5f/events_000012600.root -o minitree_000012600.root
outside the loop: sh_file = 'Make_minitrees_commands.sh'
line.replace("/mnt/hadoop/store/user/hyeonseo/mgp8_pp_tt012j5f/events","")
outputfilestring = "minitree_" +line.replace("/mnt/hadoop/store/user/hyeonseo/mgp8_pp_tt012j5f/events","") + ".root"
commandfile = open(sh_file, 'w')
commandfile.write("python Minitrees/Make_minitrees.py -i "+line+" -o "+ outputfilestring +"\n")

"""

import os
f     = open('filelist.txt', 'r')
lines = f.readlines()

sh_file = 'Make_minitrees_commands.sh'


commandfile = open(sh_file, 'w')

if not os.path.exists("MiniTreeOutput"): os.makedirs("MiniTreeOutput")



for line in lines :
    
    line = line.strip('\n')
    outputfilestring = "minitree_" +line.replace("/mnt/hadoop/store/user/hyeonseo/mgp8_pp_tt012j_5f/events_","")
    commandfile.write("python Minitrees/Make_minitrees.py -i "+line+" -o MiniTreeOutput/"+ outputfilestring +"\n")
    
    
f.close()
commandfile.close()

