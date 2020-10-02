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
