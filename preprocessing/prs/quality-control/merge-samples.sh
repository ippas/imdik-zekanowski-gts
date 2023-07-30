#!/usr/bin/env bash

#SBATCH -A plgsportwgs3-cpu
#SBATCH -p plgrid
#SBATCH -t 72:0:0
#SBATCH --mem=20GB
#SBATCH --cpus-per-task=1
#SBATCH -C localfs
#SBATCH --output=/net/pr2/projects/plgrid/plggneuromol/matzieb/slurm-log/%j.out
#SBATCH --error=/net/pr2/projects/plgrid/plggneuromol/matzieb/slurm-log/%j.err

module load bcftools/1.14-gcc-11.2.0
module load java/11


# merging genotyped vcf file 
bcftools merge $(ls ../imdik-zekanowski-sportwgs/data/genotyped-vcf-gz/*gz | grep -v B502 | grep -v B506; ls data/genotyped-vcf-gz/*gz | grep -v B502 | grep -v B506) | bgzip -c > data/prs/tourett-sportsmen-merged.vcf.gz


# create tabix file for merged genotypes
tabix -p vcf data/prs/tourett-sportsmen-merged.vcf.gz

