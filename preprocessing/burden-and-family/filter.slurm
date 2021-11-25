#!/bin/bash

## slurm configuration
#SBATCH --partition plgrid-now
#SBATCH -N 1
#SBATCH --mem=20gb
#SBATCH --time 12:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --job-name hail-script
#SBATCH --output %J.txt
 
module load plgrid/apps/spark/2.4.5 
module load plgrid/tools/python/3.6.5
 
start_spark_cluster

python3 filter-gts.py
