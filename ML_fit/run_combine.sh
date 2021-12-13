#!/bin/sh 
text2workspace.py c_hel_combine_card -m 172.5 -o c_hel_combine.root
# combine -M AsymptoticLimits c_hel_combine.root  -m 172.5
combineTool.py -M Impacts -d c_hel_combine.root -m 172.5 --rMin -1 --rMax 2 --robustFit 1 --doInitialFit --toys 1000
mv higgsCombine_initialFit_Test.MultiDimFit.mH172.5.123456.root  higgsCombine_initialFit_Test.MultiDimFit.mH172.5.root

combineTool.py -M Impacts -d c_hel_combine.root -m 172.5 --rMin -1 --rMax 2 --robustFit 1 --doFits       --toys 1000
python rename.py

combineTool.py -M Impacts -d c_hel_combine.root -m 172.5 --rMin -1 --rMax 2 --robustFit 1 --output c_hel_impacts.json
plotImpacts.py -i c_hel_impacts.json -o c_hel.pdf

