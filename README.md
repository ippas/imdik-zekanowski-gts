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

In this part all analyses were conducted with Hail 0.2.79, while the preprocessing part was conducted with Hail 0.2.64.

### 1. Joint genotyping

This analysis started with joint calling of variants for the GTS cohort together with two control cohorts (in Hail).

### 2. Variant filtering

Quality filter were applied for the joint cohort:

- gnomad coverage 0.9 over 1 
- repeatmasker track (+/- 2 bp from the track) 

Following filters are applied per group:

- mean DP > 5 
- mean GQ > 50 
- hwe p-value per group > 0.05 
- max 3 samples with DP < 3 
- max 3 samples with GQ < 30 

### 3. Variants annotations:

The resulting MatrixTable was annotated with: HPO, genes, CADD, vep, gnomAD and phenotypes

### 4. Family filtering:

goal: to find pathogenic mutations with filtering in 17 families with at least 4 members

filtering option 1 - in all the genes (intragenic, CADD treshold - 20, maf  < 0.0001) 
filtering option 2 - in 953 selected genes (intragenic, CADD treshold - 20, maf  < 0.05)

variant segregation was analysed in two options:

option A: more than 0.66 of samples with GTS/tics with at least 1 alternate allele and less than 0.33 healthy samples with alternate alleles. 
option B: segregation schema that takes into account carriers without the disease

### 5. Burden tests for unrelated individuals:

goal: to find overrepresentation of damaging mutations in selected gene list

GTS - unrelated individuals with heavy tics (n = 37 - 2 samples excluded based on PCA, one sample - WGS_6827 excluded based on quality control)

elite sportsmen controls (n = 100; 2 samples excluded based on PCA) - main control

external 1kg controls (n = 98; selected to overlap with our samples on PCA)

burden test procedure:

burden score (CADD-weighted score) summed per each list and then groups are compared with t-tests. CADD is used as it incorporates predicted effect of damaging mutations, also those absent from gnomAD


