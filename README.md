## Data analysis:

Samples were analysed with hail (0.2.27 (small vcf) and 0.2.29 (large vcf) in jupyter notebooks. 

samples: 'S_7288' and 'S_7289' and also: 'S_7240' and 'S_7241' had their samples_id's swapped in relation with their barcodes. During the analysis this was corrected.

### PART1: small vcf analysis:
For initial analysis,an annotated file was obtained from ISeq. Variants were filtered and only variants in coding regions and with SnpEff (http://snpeff.sourceforge.net/SnpEff_manual.html#intro) putative impact ‘MODERATE’ or ‘HIGH’ were retained (approx 40 000 variants). Due to being large outliers in PCA analysis two samples: 'WGS_139', 'WGS_D6816' were excluded. 

Analysis was conducted in three parts:
1. [Main analysis file](small_vcf_analysis.ipynb) that produced pandas dataframes
2. [Notebook to export appropriate csv and excel files](csv-work.ipynb)
3. [Variant overrepresentation vs gnomAD](variant_overrepresentation_small_vcf.ipynb). This analysis was not really polished and finished as I wanted to have proper gnomAD controls and conduct the overrepresentation per genes not per variants. 

## small vcf results:
description of initial results is available [here](https://docs.google.com/document/d/1wTMr_adtZWmKsrAAQDkk6aXU-3-p6bbi84qVoKFFIro/edit?usp=sharing) and resulting tables are available[here](http://149.156.177.112/projects/imdik-zekanowski-gts/small_vcf_analysis/out_files/)


### PART2 : large vcf analysis:

#### 1. vcf filtering and annotation was performed in  steps

[step 1](step1_filter_repeatmasker.ipynb): repeats were removed using UCSC available rmsk track (bed was first splitted using split command `split -d -l 200000 repeatmasker-all rpmsk`)

[step 2](step2_split_select.ipynb): alleles were split using hail hl.split_multi_hts() function (star alleles removed) and PCA was conducted (no outliers detected, main PCs were families)

[step 3](step3_gnomad_anno.ipynb): variants were annotated with coverage from gnomad v3 and filtered for coverage_over_1 > 0.9 (90% of samples with DP of at least 1) and with AF of non-finnish european population and other fields:
`vep.intergenic_consequences,vep.most_severe_consequence, vep.motif_feature_consequences, vep.regulatory_feature_consequencesm, vep.transcript_consequences, vep.variant_class, gnmd.rsid`

[step 4](step4_cadd.ipynb): variants were annotated with CADD

[step 5](step5_gwas_annotate.ipynb): variants were annotated with p values from GTS gwas study

separate step: Drawing of 151 simulated gnomad controls and annotation of the dataset

[step 6](step_6_nearest_genes_phenotypes_gnomad_merge_pca.ipynb): two tables: simulated controls from gnomad and samples were joined and annotated with phenotypes (only samples are annotated) and with nearest genes (20kb from transcript, all variants annotated)


### data and hail enviornment set up

1. Hail enviornment was created in a [docker container](Dockerfile)

2. To start the container: `docker run -it --rm -p 8889:8889 -p 4040:4040 -v $PWD:/hail hail-jupyter` 

3. To connect from local:`ssh -N -f -L localhost:8889:localhost:8889 ifpan` then `localhost:8889` in browser
 
