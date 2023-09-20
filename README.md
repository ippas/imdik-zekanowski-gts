# WGS analysis of GTS data:

### *This data is analysed within two projects. The first project is called oligogenic-model and the second is called burden-and-family.* 

# Oligogenic model

*archive code - these folders contain the first iteration of the paper results*

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

goal: to find overrepresentation of damaging mutations in selected gene lists

GTS - unrelated individuals with heavy tics (n = 37 - 2 samples excluded based on PCA, - 1 sample - excluded based on quality control)
elite sportsmen controls (n = 100 - 2 samples excluded based on PCA) - main control
external 1000genomes project controls (n = 98; selected to overlap with our samples on PCA)

burden test procedure: burden score (CADD-weighted score) summed per each list and then groups are compared with t-tests.


