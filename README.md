### Data analysis:

Samples were analysed with hail (0.2.27) in jupyter notebooks. Due to bein large outliers in PCA analysis two samples: 'WGS_139', 'WGS_D6816' were excluded. What is more samples: 'S_7288' and 'S_7289' and also: 'S_7240' and 'S_7241' had their samples_id's swapped in relation with their barcodes. During the analysis this was corrected.

#### 1. vcf filtering and annotation: 

step 1. repeats were removed using [UCSC](http://genome.ucsc.edu/cgi-bin/hgTables?hgsid=783011485_TrGD3OcGBeo5teIeaB31VgYFHLkz&clade=mammal&org=Human&db=hg38&hgta_group=rep&hgta_track=knownGene&hgta_table=0&hgta_regionType=genome&position=chr1%3A11%2C102%2C837-11%2C267%2C747&hgta_outputType=primaryTable&hgta_outFileName=) available rmsk track

step 2. alleles were split using hail hl.split_multi_hts() function (star alleles removed)

step 3. variants were annotated with gnomad coverage and filtered ...


add info: Filtering rare_variants conditions for step 1: gene lists. If a gene list was >150 long, AF in nfe from gnomAD was filtered at 0.0001, for shorter lists: 0.001. Variants that occured in any of the controls were excluded


### data and setting up the hail enviornment

1. Hail enviornment was created in a [docker container](Dockerfile)

2. To start the container: `docker run -it --rm -p 8889:8889 -v $PWD:/hail hail-jupyter` 

3. To connect from local:`ssh -N -f -L localhost:8889:localhost:8889 ifpan` then `localhost:8889` in browser
 
