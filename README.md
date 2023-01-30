# Top-Quark-Spin-Correlations

My FW for the study of top quark spin correlations at the LHC, this is just a repository meant for the storage of scripts.
To list all files in the hadoop directory perform :
```
ls /mnt/hadoop/store/user/<username>/TTBar_Delphes > filelist_mnt
```
This updated filelist is the input to the make_jobs.py script.
This creates multiple scripts that can be submitted to the cms-a queue here at Purdue using the SLURM scheduler.
To submit :
```
python make_jobs.py
python submit_all.py
```
To monitor the jobs and the queues use :
```
squeue -u <username>
slist
```

## Ling's Recommended Method: How to Get Started w/ the Future Circular Coillder (https://en.wikipedia.org/wiki/Future_Circular_Collider)  
### Updated on 01/28/2023
- The FCC project is listed on another branch of the git repository

- First of all, everyone should have a Linux-like shell environment (Ubuntu17/18/19/20/22, CentOS7/8, ScientificLinux6/7, LinuxMint, WSL on Windows etc.) to work on.
- If you are on Windows10/11 machines, run powershell as administrator and type ... (you may need to restart the computer after installing WSL via "wsl --install" if you don't have it already) <br>
$ wsl --install -d ubuntu
- Once you are on Linux, make a prefered directory (let's say, starting from the home directory) on your local Linux machine using the following command lines: <br>
$ cd ~ <br>
$ mkdir CMS/FCC
- Then go to that directory: <br>
$ cd CMS/FCC
- Copy the .root file from the CMS Tier-2 server: <br>
$ scp 'purdue_username'@hammer.rcac.purdue.edu:/mnt/hadoop/store/user/hyeonseo/mgp8_pp_tt012j_5f/events_000012600.root ~/CMS/FCC
- This will ask for the boilerkey for the permission. 
- Now we need a data analysis software called ROOT to do the analysis. Simply, install the prerequisites first (https://root.cern/install/dependencies/). 
- Then install ROOT: <br>
$ cd ~/CMS <br>
$ wget https://root.cern/download/root_v6.26.10.Linux-centos8-x86_64-gcc8.5.tar.gz <br>
$ tar -xzvf root_v6.26.10.Linux-centos8-x86_64-gcc8.5.tar.gz <br>
$ source root/bin/thisroot.sh
- Then you have the access to ROOT6 altough ROOT7 is available as of 2023. You might need to build ROOT from source (https://root.cern/install/build_from_source/) to avoid conflicts with the libraries, linux dependencies and custom C++ classes. 
- Open ROOT by: <br>
$ root -l
- Close ROOT by (the root[] sign means that you are in ROOT, type the stuff following the sign): <br>
$ root[] .q
- Or open ROOT and load the file at the same time: <br>
$ root -l ~/CMS/FCC/events_000012600.root
- The TObject that we are insterested in is the TTress named events. You can ultilize the pointers by "->" commands. For instance, <br>
$ root[] .ls events->Print() <br>
$ root[] events->Scan("met.magnitude") <br>
$ root[] events->Draw("met.magnitude")
- To view all the P_x values (momentum in x-direction in lab frame): <br>
$ root[] events->Draw("electrons.core.p4.px") 
- To select the P_x values within -50<P_x<50: <br>
$ root[] events->Draw("electrons.core.p4.px", "electrons.core.p4.px<50 && electrons.core.p4.px>-50")
- Notice that the default TCanvas is called "c1" (More in https://root.cern.ch/doc/master/classTCanvas.html), so you can store the plot you drew by: <br>
$ root[] c1->SaveAs("~/CMS/FCC/'name_of_the_file'.png")
- The idea of opening ROOT on your local machine is to avoid xforwarding the graphical user interface (GUI) from the server to your desktop because the xforwarded TBrowser or the RBrowser behaves extremely slowly; it also allow you to install the tools you want to use despite you don't have the administrator permission to download stuffs to the T2 cluster. However, it is sometimes useful to graph the plots on the interactive interface. Now, here's a bigger toy to play with, and it requires a decent skill set to operate through the Purdue CMS Tier-2 cluster, that is this framework developed for FCC. It includes not only the particle physics event selection and also the physical reconstructions. To login to the T2 cluster, obtain the access to the clusters from Stefan (spiperov@purdue.edu). Once you are granted with the acess, then you can connect one of the cluster (Hammer, Brown, and more), for example (-Y or -X to enable the xforwarding software, you need to have them installed before opening a terminal): <br>
$ ssh -Y 'purdue_username'@hammer.rcac.purdue.edu
- Try to clone the FCC branch of this repo to the folder of your choice on the T2 cluster: <br>
$ git clone -b FCC https://github.com/jthiema/Top-Quark-Spin-Correlations.git
- It will ask you for your github username and the "password". But the "password" nowdays is not the password anymore. You need to login to the github website, then go to "Settings→Developer Settings" to generate classical personal tokens. Remember to select most of the options associated with the token and use the token as the password. 
- To start the project, call the initialization shell commands: <br>
```
$ source init.sh
```
- Do these to create the necessary folders (MiniTreeOutput & HistogramOutput):
```
$ python Make_Minitrees_Commands.py
$ python Make_Histograms_Commands.py
```
- Then select the commands you want to run from Minitrees_Commands.sh. For example, for events_000012600.root (1/9000 events): <br>
```
$ python Minitrees/Make_minitrees.py -i /mnt/hadoop/store/user/hyeonseo/mgp8_pp_tt012j_5f/events_000012600.root -o MiniTreeOutput/minitree_000012600.root 
$ python Top_reco/Top_reco.py -i MiniTreeOutput/minitree_000012600.root
$ python Histograms/Make_histograms.py -i MiniTreeOutput/minitree_000012600.root -o HistogramOutput/hstogram_000012600.root
```
- Modify /Plotting/MkPlots.cc:line 378 to <br>
```
TFile* f_hists = new TFile("../HistogramOutput/histogram_000012600.root","READ"); 
```
- And <br>
```
$ root -l -b MkPlots.cc++("")
```
- To view the results (the following command shows one of them, ex. the Missing Transverse Momentum associated with the unseen neutrinos), do: <br>
```
$ display Plotting/FinalPlots/h_met_pt.pdf
```
