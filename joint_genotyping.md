### Joint genotyping code

* gatk version : 4.1.8.0
* bcftoolsversion : 1.3.1

1. To run bcftools norm (this is to genomicsDB to accept the g.vcf files):
```
ls *gz | xargs -P 0 -n 1 -i"{}" docker run --rm -v $PWD:/data biocontainers/bcftools:1.3.1 bcftools norm -m +any -O z -o /data/bcftools_output/{} /data/{} 
```

2. To index each file:
```
ls *gz | xargs -P 0 -n 1 -i"{}" docker run --rm -v $PWD:/data broadinstitute/gatk gatk IndexFeatureFile -I /data/{}
```

3. To prepare 20 separate intervals w Intelliseq's task:

```
wget https://gitlab.com/intelliseq/workflows/raw/interval-group@1.1.2/src/main/wdl/tasks/interval-group/interval-group.wdl
wget http://anakin.intelliseq.pl/public/intelliseqngs/workflows/resources/intervals/broad-institute-wgs-calling-regions/hg38.even.handcurated.20k.broad-institute-hg38.interval_list

#run womtool to get the input.json pattern

java -jar /opt/tools/cromwell/cromwell-44.jar run interval-group.wdl -i input.json
```

input.json:
```
{
  "interval_group_workflow.interval_group.max_no_pieces_to_scatter_an_interval_file": "20",
  "interval_group_workflow.interval_group.interval_file": "hg38.even.handcurated.20k.broad-institute-hg38.interval_list"
}
```

4. To create the genomicsDB:
```
FILE_LIST=`ls *gz | xargs -i bash -c 'echo -V /data/{}'`

docker run --rm -v $PWD:/data broadinstitute/gatk gatk --java-options "-Xmx12g -Xmx5g" GenomicsDBImport $FILE_LIST -L /data/intervals/part001-hg38.even.handcurated.20k.broad-institute-hg38.interval_list --genomicsdb-workspace-path /data/genomics-db-001 --batch-size 25 --consolidate true
```

5. To perform joint genotyping:
```
docker run --rm -v $PWD:/data broadinstitute/gatk gatk --java-options "-Xmx12g" GenotypeGVCFs -R /data/Homo_sapiens_assembly38.fa.gz -V gendb:///data/genomics-db-001 -O /data/part001.vcf.gz --annotate-with-num-discovered-alleles true --allow-old-rms-mapping-quality-annotation-data true
```
*Steps 4 and 5 were performed for each of the 20 intervals* 

Then all files were processed with Hail in a Jupyter notebook and then joined.
