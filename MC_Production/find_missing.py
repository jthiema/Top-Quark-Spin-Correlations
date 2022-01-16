import re 

with open ('small_root_files', 'r') as ip_file :
     lines = ip_file.readlines()

mstop_arr = []
mchi0_arr = []
cfg_arr   = []

cfg_cnt   = 0
for line in lines :
    line  = line.strip('\n')
    mstop = re.findall('mstop_[0-9]+',line)
    mstop = mstop[0].strip('mstop_')

    mchi0 = re.findall('mchi0_[0-9]+',line)
    mchi0 = mchi0[0].strip('mchi0_')

    cfgs  = re.findall('cfg_[0-9]+',line)
    cfgs  = cfgs[0].strip('cfg_')

    if mstop not in mstop_arr :
       cfg_arr.append(cfg_cnt)   # store the running count
       cfg_cnt = 0               # and then reset it
       mstop_arr.append(mstop)

    else : cfg_cnt += 1

    if mchi0 not in mchi0_arr : 
       mchi0_arr.append(mchi0)

    cfg_cnt += 1    
print(mstop_arr)
print(mchi0_arr)
print(cfg_arr)
