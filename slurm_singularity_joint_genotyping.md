## How to run intelliseq joint genotyping on SLURM HPC cluster (example for Prometheus cyfronet)

### 1. Create an input file. To get the input template run womtool with the following code in an interactive SLURM task:

```
srun -N 2 --ntasks-per-node=24 -t 01:0:0 -p plgrid-testing --pty /bin/bash -l
wget $WORKFLOW-URL
module load plgrid/tools/cromwell/50
$WOMTOOL_RUN inputs $WORKFLOW-PATH
```

short script to echo the input (beware of the extra commas)
```
echo {\"gvcf_joint_genotyping_workflow.gvcf_gz\": [
ls *gz | xargs -i bash -c 'echo \" {} \"',
echo ], \"gvcf_joint_genotyping_workflow.gvcf_gz_tbi\": [
ls *tbi | xargs -i bash -c 'echo \" {} \"',
echo ], \"gvcf_joint_genotyping_workflow.kit\": \"genome\"}
```

### 2. Create a cromwell config file with the following text:

*note: it is crucial to export cache directories for singularity on HPC clusters, as singularity will automatically use user's home directory for cache, which often has limited space.*

```
include required(classpath("application"))

backend {
    default: singularity
    providers: {
        singularity {
            # The backend custom configuration.
            actor-factory = "cromwell.backend.impl.sfs.config.ConfigBackendLifecycleActorFactory"

            config {
                run-in-background = true
                runtime-attributes = """
                  String? docker
                """
                submit-docker = """
                # Build the Docker image into a singularity image, using the head node
    		DOCKER_NAME=$(sed -e 's/[^A-Za-z0-9._-]/_/g' <<< ${docker})
    		IMAGE=${cwd}/$DOCKER_NAME.sif
  	        if [ ! -f $IMAGE ]; then
        		singularity pull $IMAGE docker://${docker}
    		fi
		  export SINGULARITY_LOCALCACHEDIR=$SCRATCH_LOCAL
		  export SINGULARITY_CACHEDIR=$SCRATCH
		  export SINGULARITY_TEMPDIR=$SCRATCH
		  singularity exec --bind ${cwd}:${docker_cwd} $IMAGE ${job_shell} ${script}
                """
            }
	}
    }
}
```

### 3. Create an sbatch script to run cromwell 
```
#!/bin/bash

## slurm configuration
#SBATCH --partition plgrid
#SBATCH -N 5
#SBATCH -C localfs #this allows singularity to use $SCRATCH_LOCAL
#SBATCH --ntasks-per-node=24
#SBATCH --time 12:00:00
#SBATCH --begin=now
#SBATCH --job-name cromwell-server
#SBATCH --output job-log--%J.txt


module load plgrid/tools/cromwell/50 
module load plgrid/tools/singularity 

unset XDG_RUNTIME_DIR
 
java -Xmx1000M -Dconfig.file=$PATH-TO-CONFIG -jar $WORKFLOW-PATH -i input.json #you can also specify the output directory
```

### 4. Run the sbatch script:
```
newgrp $GROUP # substitute with your group name, this avoids the "disc quota exceeded error"
sbatch cromwell-sbatch.slurm
```
*note: first run of each container will require singularity to build a container from scratch and this takes a surprising amount of time*


## The workflow above is suitable for a limited amount od samples. For more samples we are going to run GenomicsDB:
This is run manually with gatk on cyfronet. First files need to be processed with bcftools to collapse lines with multiple genotypes.

```
#!/bin/bash

## slurm configuration
#SBATCH --partition plgrid-testing
#SBATCH -N 2
#SBATCH --ntasks-per-node=24
#SBATCH --time 01:00:00
#SBATCH --begin=now
#SBATCH --job-name bcftools-norm
#SBATCH --output job-log--%J.txt


module load plgrid/tools/bcftools



ls *.gz | xargs -t -d "\n" -I "{}" -P 0 srun -n 2 -N 1 --mem=5gb bcftools norm -m +any -O z -o ./bcftools_output/{} {}
```


```
#!/bin/bash

## slurm configuration
#SBATCH --partition plgrid
#SBATCH -N 10
#SBATCH --ntasks-per-node=24
#SBATCH --time 48:00:00
#SBATCH --begin=now
#SBATCH --job-name gatk-genomicsdb
#SBATCH --output job-log--%J.txt


module load plgrid/tools/gatk/4.1.3.0


FILE_LIST=`ls *gz | xargs -i bash -c 'echo -V {}'`

gatk --java-options "-Xmx512g -Xmx4g" GenomicsDBImport $FILE_LIST -L ./genomics-db/part1-interval-list.interval_list -L ./genomics-db/part2-interval-list.interval_list --genomicsdb-workspace-path ./genomics-db/test_on_2_samples --tmp-dir=$SCRATCH

```

*note : interval list from here: http://anakin.intelliseq.pl/public/intelliseqngs/workflows/resources/intervals/broad-institute-wgs-calling-regions/hg38.even.handcurated.20k.broad-institute-hg38.interval_list*


### The same was run on io server in docker containers:

1. To run bcftools norm:
```
:/home/ifpan/projects/imdik-zekanowski-gts/data/gvcf_with_new_samples$ ls *gz | xargs -P 0 -n 1 -i"{}" docker run --rm -v $PWD:/data biocontainers/bcftools:1.3.1 bcftools norm -m +any -O z -o /data/bcftools_output/{} /data/{} 
```
