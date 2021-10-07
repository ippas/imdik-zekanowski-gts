#!/bin/bash

#SBATCH -A plgsportwgs
#SBATCH -p plgrid
#SBATCH -t 1-0:0:0
#SBATCH --cpus-per-task=1
#SBATCH --mem=14GB
#SBATCH --output=%j.out
#SBATCH --error=%j.err

set -ex

WD=$PLG_GROUPS_SHARED/plggneuromol/jhajto/imdik-fichna-onesample/a7582/
SIF_DIR=$PLG_GROUPS_SHARED/plggneuromol/singularity-images/

cd $WD

curl "http://anakin.intelliseq.pl/public/intelliseqngs/workflows/resources/intervals/broad-institute-wgs-calling-regions/hg38.even.handcurated.20k.broad-institute-hg38.interval_list" > all.interval_list

srun singularity exec --bind $WD,$SCRATCH $SIF_DIR/gatk-4.1.7.0-hg38_1.0.1.sif \
	gatk --java-options "-Xms4g -Xmx12g -Djava.io.tmpdir=$SCRATCH" HaplotypeCaller \
		-R /resources/reference-genomes/broad-institute-hg38/Homo_sapiens_assembly38.fa \
		-I a7582_markdup-recalibrated.bam \
		-L all.interval_list \
		-O a7582.g.vcf.gz \
		-ERC GVCF \
		--bam-output a7582_realigned-haplotypecaller.bam \
		-contamination 0

srun singularity exec --bind $WD,$SCRATCH $SIF_DIR/gatk-4.1.7.0-hg38_1.0.1.sif \
	gatk --java-options "-Xmx5g -Xms5g -Djava.io.tmpdir=$SCRATCH" GenotypeGVCFs \
		--intervals all.interval_list \
		--reference /resources/Homo_sapiens_assembly38.fa \
		--annotate-with-num-discovered-alleles true \
		--variant a7582.g.vcf.gz \
		--output a7582.vcf.gz
