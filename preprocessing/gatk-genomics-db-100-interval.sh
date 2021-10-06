#!/bin/bash

## slurm configuration
#SBATCH --partition plgrid-testing
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --mem 120gb
#SBATCH --time 01:00:00
#SBATCH --begin=now
#SBATCH --job-name gatk-genomicsdb
#SBATCH --output /net/archive/groups/plggneuromol/imdik-zekanowski-gts/preprocessing/job-log--%J.txt
#SBATCH --error /net/archive/groups/plggneuromol/imdik-zekanowski-gts/preprocessing/job-error--%J.err

set -ex

WD=/net/archive/groups/plggneuromol/
SIF_DIR=$PLG_GROUPS_SHARED/plggneuromol/singularity-images/

cd $WD

FILE_LIST_GTS=`ls $WD/imdik-zekanowski-gts/data/gvcf/*gz | xargs -i bash -c 'echo -V {}'`
FILE_LIST_SPORTSMEN=`ls $WD/imdik-zekanowski-sportwgs/data/gvcf/*gz | xargs -i bash -c 'echo -V {}'`

INDEX=1
SELECTED_INTERVAL=`ls $WD/imdik-zekanowski-gts/data/external-data/intervals/ | head -$INDEX`

DIR_NAME=`echo $SELECTED_INTERVAL | tr "-" "\n" | head -1`
mkdir $WD/imdik-zekanowski-gts/preprocessing/genomicsdb/$DIR_NAME

srun singularity exec --bind $WD,$SCRATCH $SIF_DIR/gatk-4.1.7.0-hg38_1.0.1.sif \
	sh -c "gatk --java-options '-Xmx14g -Djava.io.tmpdir=$SCRATCH' GenomicsDBImport $FILE_LIST_GTS $FILE_LIST_SPORTSMEN \
			 -L $SELECTED_INTERVAL \
			 --genomicsdb-workspace-path $WD/genomics-db/$DIR_NAME \
			 --tmp-dir=$SCRATCH \
			 --batch-size 10 \
			 --consolidate true"

