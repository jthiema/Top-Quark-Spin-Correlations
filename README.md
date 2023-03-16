# Top-Quark-Spin-Correlations
## Forking the Repository
- It's important to duplicate this repository to your own github repository so that the modifications only apply to your repository. 
- Click "Fork" button on the github webpage on top right. 
- Unselect "Forking the master branch only".
- Copy the url in the green "<> Code" button. Then do 
```
$ git clone <url>
$ git remote add origin git@github.com:<Your Github Username>/Top-Quark-Spin-Correlations.git
$ git remote add ling git@github.com:holytpk/Top-Quark-Spin-Correlations.git
$ git remote -v 
```

## Ling's Recommended Method: How to Get Started w/ the HL-LHC (https://en.wikipedia.org/wiki/Future_Circular_Collider)  
### Updated on 02/28/2023

- To start the project, call the initialization shell commands: <br>
```
$ source init.sh
```
- For HL-LHC, we need to convert the delphes files into ntuples.
```
$ mkdir Ntuples
$ python Ntuplizer/Delphes_Ntuplizer_custom.py -i /mnt/hadoop/store/user/abakshi/TTBar_Delphes/TTJets_DiLept_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_200PU_1.root -o Ntuples/ntuple_TTJets_DiLept_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_200PU_1.root

```
- Do these to create the necessary folders (MiniTreeOutput & HistogramOutput):
```
$ python Make_Minitrees_Commands.py
$ python Make_Histograms_Commands.py
```
- Then select the commands you want to run from Minitrees_Commands.sh. Ex: <br>
```
$ python Minitrees/Make_minitrees.py -i Ntuples/ntuple_TTJets_DiLept_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_200PU_1.root -o MiniTreeOutput/minitree_TTJets_DiLept_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_200PU_1.root
$ python Top_reco/Top_reco.py -i MiniTreeOutput/minitree_TTJets_DiLept_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_200PU_1.root
$ python Histograms/Make_histograms.py -i MiniTreeOutput/minitree_TTJets_DiLept_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_200PU_1.root -o HistogramOutput/histogram_TTJets_DiLept_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_200PU_1.root
```
- Modify /Plotting/MkPlots.cc:line 378 to <br>
```
TFile* f_hists = new TFile("../HistogramOutput/histogram_TTJets_DiLept_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_200PU_1.root","READ"); 
```
- And <br>
```
$ root -l -b MkPlots.cc++("")
$ cd Plotting
$ root -l -b eff_lep_pt_cut.cc
```
- To view the results (the following command shows one of them, ex. the Missing Transverse Momentum associated with the unseen neutrinos), do: <br>
```
$ display Plotting/FinalPlots/h_met_pt.pdf
```

### For Those Who Had Trouble Building ROOT Locally
Open Jupyterhub on Hammer (does not require VPN): notebook.hammer.rcac.purdue.edu. <br>
Open the script and modify it as you want, you can perform all the interactive steps by switching to a proper kernel, ex. Coffea. <br>
If you want to view directories above your home directory, ask Jason for help, XD. <br>
You can also open a terminal to execute commands by clicking the "new" dropdown list which is right next to the "upload" button. <br>
