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
$ scp <purdue username>@hammer.rcac.purdue.edu:/mnt/hadoop/store/user/hyeonseo/mgp8_pp_tt012j_5f/events_000012600.root ~/CMS/FCC
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
$ root[] c1->SaveAs("~/CMS/FCC/<the name of the file>.png")

