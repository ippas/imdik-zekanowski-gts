# WGS analysis of GTS data:

## *This data is split into two projects. The first project is called oligogenic-model and the second is called burden-and-family.* 

# Oligogenic model

*note: In June 2020 35 new samples were obtained to be added to the analyses. We repeated genotyping (from gvcf stage) to incorporate them. Below is the full information for the whole analysis of all 186 samples*

Data were copied to the Prometheus cluster (see the [documentation](https://kdm.cyfronet.pl/portal/Prometheus:Podstawy)) with a batch script:

```
#!/bin/bash
## slurm configuration
#SBATCH --partition plgrid
#SBATCH -N 1
#SBATCH -C localfs
#SBATCH --ntasks-per-node=1
#SBATCH --time 48:00:00
#SBATCH --begin=now
#SBATCH --job-name copy
#SBATCH --output job-log--%J.txt

wget --user=$USER --password=$PASSWORD -r -nH --cut-dirs=2 --no-parent --reject="index.html*" -c $URL
```

### 1. Joint genotyping

Genomic vcf's were obtained from Intelliseq for all samples. Joint genotyping was performed with gatk 4.1.8.

### 2. Filtering steps (filtering for coverage with gnomAD and filtering out low-complexity regions, split of multiallelic variants)

All analyses were performed with Hail 0.2.30.

Repeats were removed using UCSC available rmsk track, alleles were split using hail hl.split_multi_hts() function (star alleles removed) and PCA was conducted (one outlier detected - sample 464 and removed from the analysis, main PCs were families). Variants were annotated with coverage from gnomad v3 and filtered for coverage_over_1 > 0.9 (90% of samples with DP of at least 1) and with AF of non-finnish european population and other fields. Genes were also annotated with their respective HPO terms. [full code avaiable here](vcf-filter-anno.ipynb)

### 3. Family - based analysis:

A table od variants based on MAF < 0.0001 and a model of dominant heritability with incomplete penetrance applied to large (4 or more indivudals families).

### 4. Variariant overrepresentation analysis

For variant analysis, all variants were annotated with their CADD scores. GnomAD allele frequencies (non-finnish european) were used to simulate controls. The cohort and simulated controls were later joined into one matrix table.

#### SKAT test and oligogenic model

Th prepared matrix-table was then analysed to creat an oligogenic (5 genes) model of GTS.
