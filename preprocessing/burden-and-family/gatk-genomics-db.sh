#!/bin/bash

## slurm configuration
#SBATCH --partition plgrid
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem 20gb
#SBATCH --time 3-00:00:00
#SBATCH --begin=now
#SBATCH --job-name gatk-genomicsdb
#SBATCH --array=1-945%20
#SBATCH --output /net/archive/groups/plggneuromol/imdik-zekanowski-gts/preprocessing/burden-and-family/job-log--%A-%a.txt
#SBATCH --error /net/archive/groups/plggneuromol/imdik-zekanowski-gts/preprocessing/burden-and-family/job-error--%A-%a.err

set -ex

WD=/net/archive/groups/plggneuromol/
SIF_DIR=$PLG_GROUPS_SHARED/plggneuromol/singularity-images/

cd $WD

FILE_LIST_GTS=`ls ./imdik-zekanowski-gts/data/gvcf/*gz | xargs -i bash -c 'echo -V {} '`
FILE_LIST_SPORTSMEN=`ls ./imdik-zekanowski-sportwgs/data/gvcf/*gz | xargs -i bash -c 'echo -V {} '`

FILE_LIST_GTS=$(echo $FILE_LIST_GTS | tr '\n' ' ')
FILE_LIST_SPORTSMEN=$(echo $FILE_LIST_SPORTSMEN | tr '\n' ' ')

SELECTED_INTERVAL=`ls ./imdik-zekanowski-gts/data/external-data/intervals/ | head -$SLURM_ARRAY_TASK_ID | tail -1`

DIR_NAME=`echo $SELECTED_INTERVAL | tr "-" "\n" | head -1`

srun singularity exec --bind $WD,$SCRATCH $SIF_DIR/gatk-4.1.7.0-hg38_1.0.1.sif \
	sh -c "gatk --java-options \"-Xmx15g -Xms14g\" GenomicsDBImport \
			  $FILE_LIST_GTS \
			  $FILE_LIST_SPORTSMEN \
			 -L ./imdik-zekanowski-gts/data/external-data/intervals/$SELECTED_INTERVAL \
			 --genomicsdb-workspace-path=./imdik-zekanowski-gts/data/joint-with-sportsmen/genomicsdb/$DIR_NAME \
			 --tmp-dir=$SCRATCH \
			 --batch-size 15 \
			 --genomicsdb-vcf-buffer-size 163840 \
 			 --consolidate true"

