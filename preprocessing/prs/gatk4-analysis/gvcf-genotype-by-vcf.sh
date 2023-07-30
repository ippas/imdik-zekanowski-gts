#!/usr/bin/env bash

#SBATCH -A plgsportwgs3-cpu
#SBATCH -p plgrid-long
#SBATCH -t 168:0:0
#SBATCH --mem=10GB
#SBATCH --cpus-per-task=1
#SBATCH -C localfs
#SBATCH --output=/net/pr2/projects/plgrid/plggneuromol/matzieb/slurm-log/%j.out
#SBATCH --error=/net/pr2/projects/plgrid/plggneuromol/matzieb/slurm-log/%j.err

module load java/11
export TOOLS_DIR="/net/pr2/projects/plgrid/plggneuromol/tools"


while test $# -gt 0; do
    case "$1" in
        --inputs)
            shift
            inputs=$1
            shift
            ;;
        *)
            echo "$1 is not a recognized flag!"                 
            break;
            ;;
    esac
done 

sg plggneuromol -c 'java \
        -Dconfig.file=preprocessing/prs/gatk4-analysis/cromwell.conf \
        -Djava.io.tmpdir=$SCRATCH_LOCAL\
        -jar $TOOLS_DIR/cromwell-85.jar run \
                preprocessing/prs/gatk4-analysis/gvcf-genotype-by-vcf.wdl \
                --inputs '"$inputs"' \
                --options preprocessing/prs/gatk4-analysis/options-gvcf-genotype-by-vcf.json'
