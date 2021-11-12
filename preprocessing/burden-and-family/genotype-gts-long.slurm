#!/bin/bash

## slurm configuration
#SBATCH --partition plgrid-long
#SBATCH -A plgdepresja
#SBATCH -N 1
#SBATCH --mem=40gb
#SBATCH --time 6-00:00:00
#SBATCH --ntasks-per-node=12
#SBATCH --job-name hail-script
#SBATCH --output %J.txt
 
module load plgrid/apps/spark/2.4.5 
module load plgrid/tools/python/3.6.5
 
start_spark_cluster

python3 genotype-gts.py
