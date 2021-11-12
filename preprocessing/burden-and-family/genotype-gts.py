#!/usr/bin/env python3


import hail as hl
hl.init(tmp_dir='/net/scratch/people/plggosborcz', spark_conf={'spark.driver.memory': '10G', 'spark.executor.memory': '30G'}, default_reference='GRCh38') 

import os
files = os.listdir('/net/archive/groups/plggneuromol/imdik-zekanowski-gts/data/gvcf/')

gvcfs = []
for f in files:
    if (f.find("tbi")) == -1:
        gvcfs.append('/net/archive/groups/plggneuromol/imdik-zekanowski-gts/data/gvcf/'+f)
gvcfs.sort()


samples = []

for f in files:
    if (f.find("tbi")) == -1:
        samples.append((f.split('.'))[0])

samples.sort()


hl.experimental.run_combiner(gvcfs[0:10], out_file='/net/archive/groups/plggneuromol/imdik-zekanowski-gts/data/joint-gts-only/sparse0-9.mt',
                             tmp_path='/net/scratch/people/plggosborcz',
                             header = '/net/archive/groups/plggneuromol/imdik-zekanowski-gts/data/gvcf/header-460.txt',
                             sample_names = samples[0:10],
                             reference_genome='GRCh38', use_genome_default_intervals = True)

hl.experimental.run_combiner(gvcfs[10:30], out_file='/net/archive/groups/plggneuromol/imdik-zekanowski-gts/data/joint-gts-only/sparse11-29.mt',
                             tmp_path='/net/scratch/people/plggosborcz',
                             header = '/net/archive/groups/plggneuromol/imdik-zekanowski-gts/data/gvcf/header-460.txt',
                             sample_names = samples[10:30],
                             reference_genome='GRCh38', use_genome_default_intervals = True)

hl.experimental.run_combiner(gvcfs[30:100], out_file='/net/archive/groups/plggneuromol/imdik-zekanowski-gts/data/joint-gts-only/sparse30-99.mt',
                             tmp_path='/net/scratch/people/plggosborcz',
                             header = '/net/archive/groups/plggneuromol/imdik-zekanowski-gts/data/gvcf/header-460.txt',
                             sample_names = samples[30:100],
                             reference_genome='GRCh38', use_genome_default_intervals = True)

hl.experimental.run_combiner(gvcfs[100:], out_file='/net/archive/groups/plggneuromol/imdik-zekanowski-gts/data/joint-gts-only/sparse100-186.mt',
                             tmp_path='/net/scratch/people/plggosborcz',
                             header = '/net/archive/groups/plggneuromol/imdik-zekanowski-gts/data/gvcf/header-460.txt',
                             sample_names = samples[100:],
                             reference_genome='GRCh38', use_genome_default_intervals = True)


