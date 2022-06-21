#!/bin/sh
#SBATCH  -A cms
#SBATCH --nodes=1
#SBATCH --time=1:59:00
#SBATCH --mem=10000
cd /home/miacobuc/FCCAn/Top-Quark-Spin-Corrleations
module load anaconda
source activate mycmsenv
source /cvmfc/fcc.cern.ch/sw/latest/setup.sh
python Histograms/concatandplot.py -i /depot/cms/top/miacobuc/MiniTreeOutput/ -o /depot/cms/top/miacobuc/hist.root 