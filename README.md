# WGS analysis of GTS data:

### *This data is analysed within two projects. The first project is called oligogenic-model and the second is called burden-and-family.* 

# Oligogenic model

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

Repeats were removed using UCSC available rmsk track, alleles were split using hail hl.split_multi_hts() function (star alleles removed) and PCA was conducted (one outlier detected - sample 464 and removed from the analysis, main PCs were families). Variants were annotated with coverage from gnomad v3 and filtered for coverage_over_1 > 0.9 (90% of samples with DP of at least 1) and with AF of non-finnish european population and other fields. Genes were also annotated with their respective HPO terms.

### 3. Variariant overrepresentation analysis

For variant analysis, all variants were annotated with their CADD scores. GnomAD allele frequencies (non-finnish european) were used to simulate controls. The cohort and simulated controls were later joined into one matrix table.

### 4. SKAT test and oligogenic model

Th prepared matrix-table was then analysed to create an oligogenic (5 genes) model of GTS.

# Burden and family

In this part all analyses were conducted with Hail

