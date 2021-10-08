#!/bin/bash

#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH -A plgsportwgs
#SBATCH -p plgrid
#SBATCH -t 48:0:0
#SBATCH --mem=14GB
#SBATCH --output=%j.out
#SBATCH --error=%j.err
#SBATCH --array=1-945
#SBATCH --output /net/archive/groups/plggneuromol/imdik-zekanowski-gts/preprocessing/job-log--%J.txt
#SBATCH --error /net/archive/groups/plggneuromol/imdik-zekanowski-gts/preprocessing/job-error--%J.err

set -ex

WD=/net/archive/groups/plggneuromol/
SIF_DIR=$PLG_GROUPS_SHARED/plggneuromol/singularity-images/

cd $WD

SELECTED_INTERVAL=`ls ./imdik-zekanowski-gts/data/external-data/intervals/ | head -$SLURM_ARRAY_TASK_ID | tail -1`
DIR_NAME=`echo $SELECTED_INTERVAL | tr "-" "\n" | head -1`

srun singularity exec --bind $WD,$SCRATCH $SIF_DIR/gatk-4.1.7.0-hg38_1.0.1.sif \
	gatk --java-options "-Xmx12g -Xms10g -Djava.io.tmpdir=$SCRATCH" GenotypeGVCFs \
		--reference /resources/Homo_sapiens_assembly38.fa \
		--annotate-with-num-discovered-alleles true \
		--variant gendb://./imdik-zekanowski-gts/data/joint-with-sportsmen/genomicsdb/$DIR_NAME \
		--output ./imdik-zekanowski-gts/data/joint-with-sportsmen/vcf-parts/$SLURM_ARRAY_TASK_ID-part.vcf.gz \
		--allow-old-rms-mapping-quality-annotation-data true




