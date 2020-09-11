# WGS analysis of GTS data:

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

Genomic vcf's were obtained from Intelliseq for all samples. Joint genotyping was performed with gatk 4.1.8. See [this file](joint_genotyping.md) for details on how the analysis was run.

### 2. Filtering steps (filtering for coverage with gnomAD and filtering out low-complexity regions, split of multiallelic variants)

All analyses were performed with Hail 0.2.30.

[This script](jupyter-hail.slurm) was used to run jupyter notebooks with hail on prometheus.

Repeats were removed using UCSC available rmsk track, alleles were split using hail hl.split_multi_hts() function (star alleles removed) and PCA was conducted (one outlier detected - sample 464 and removed from the analysis, main PCs were families). Variants were annotated with coverage from gnomad v3 and filtered for coverage_over_1 > 0.9 (90% of samples with DP of at least 1) and with AF of non-finnish european population and other fields. Genes were also annotated with their respective HPO terms. [full code avaiable here](vcf_filter_anno.ipynb)

### 3. Family - based analysis:

A table od variants based on MAF < 0.0001 and a model of dominant heritability with incomplete penetrance applied to large (4 or more indivudals families). [Code is available here](family_table_export.ipynb)

### 4. Variariant overrepresentation analysis

For variant analysis, all variants were annotated with their CADD scores. GnomAD allele frequencies (non-finnish european) were used to simulate controls (in this notebook)[link]. The cohort and simulated controls were later joined into one matrix table. 







------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------- analyses below this line regard first batch of samples and will be repeated for all samples ----------------------------------




#### 2. SKAT test
The output of step 6 was used to for a SKAT test and then a try to use the top genes to predict phenotypes on other samples. The analysis notebook is available [here](http://149.156.177.112/projects/imdik-zekanowski-gts/large_vcf_analysis/data_from_prometheus/SKAT_heavy_vs_gnomad_test_on_families.html).


* SKAT analysis of all genes - with and without related individuals ([code available here](SKAT_all_genes_classifier_based_on_brain_enriched(1).ipynb))
* classifier based on brain-enriched genes ([code available here](SKAT_all_genes_classifier_based_on_brain_enriched(1).ipynb))


### data and hail enviornment set up

1. Hail enviornment was created in a [docker container](Dockerfile)

2. To start the container: `docker run -it --rm -p 8889:8889 -p 4040:4040 -v $PWD:/hail hail-jupyter`

3. To connect from local:`ssh -N -f -L localhost:8889:localhost:8889 ifpan` then `localhost:8889` in browser



### PART 3: structural variants analysis
vcf od merged structural variants was obtained from Intelliseq and transfered to plgrid prometheus cluster

************** add link to analysis! ***********************



