import os
f     = open('filelist.txt', 'r')
lines = f.readlines()

sh_file = 'Histograms_Commands.sh'


commandfile = open(sh_file, 'w')

if not os.path.exists("HistogramOutput"): os.makedirs("HistogramOutput")



for line in lines :
    
    line = line.strip('\n')
    inputfilestring = "minitree_" +line.replace("/mnt/hadoop/store/user/hyeonseo/mgp8_pp_tt012j_5f/events_","")
    outputfilestring = "histogram_" +line.replace("/mnt/hadoop/store/user/hyeonseo/mgp8_pp_tt012j_5f/events_","")
    commandfile.write("python Histograms/Make_histograms.py -i MiniTreeOutput/"+inputfilestring+" -o HistogramOutput/"+ outputfilestring +"\n")
    
    
f.close()
commandfile.close()

