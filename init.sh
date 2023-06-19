#!/bin/sh
module load anaconda/2020.11-py38
source activate mycmsenv
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
conda activate /depot/cms/conda_envs/jthiema/Coffea-Jason
export HLLHC_BASE=$PWD
