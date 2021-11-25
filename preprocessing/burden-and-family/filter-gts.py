#!/usr/bin/env python3

import hail as hl
print('hail imported')
hl.init(tmp_dir='/net/scratch/people/plggosborcz', spark_conf={'spark.driver.memory': '10G', 'spark.executor.memory': '10G'}, default_reference='GRCh38')
print('hail initialized')

rpmk = hl.read_table('/net/archive/groups/plggneuromol/imdik-zekanowski-gts/data/external-data/repeatmasker-extended-keyed.ht')
cov = hl.read_table('/net/archive/groups/plggneuromol/imdik-zekanowski-gts/data/external-data/gnomad/gnomad-cov-keyed.ht')

mt = hl.read_matrix_table('/net/archive/groups/plggneuromol/imdik-zekanowski-gts/data/joint-gts-only/fams-unfiltered.mt')
mt = mt.filter_rows(hl.is_defined(rpmk[mt.locus]), keep = False)

mt.checkpoint('/net/scratch/people/plggosborcz/temp-mts/gts-rpmk.mt')

mt = mt.filter_rows(hl.is_defined(cov[mt.locus]), keep = True)
mt.checkpoint('/net/scratch/people/plggosborcz/temp-mts/gts-cov.mt')

mt = mt.annotate_rows(dp_qc = hl.agg.stats(mt.DP),
                     gq_qc = hl.agg.stats(mt.GQ),
                     hwe = hl.agg.hardy_weinberg_test(mt.GT))

mt = mt.annotate_rows(n_below_dp_3 = hl.agg.count_where(mt.DP < 3),
                      n_below_gq_30 = hl.agg.count_where(mt.GQ <30))

mt.checkpoint('/net/scratch/people/plggosborcz/temp-mts/gts-qc.mt')

mt = mt.filter_rows((mt.dp_qc.mean > 5) &
                    (mt.gq_qc.mean > 50) &
                    (mt.hwe.p_value > 0.05) &
                    (mt.n_below_dp_3 < 3) &
                    (mt.n_below_gq_30 < 30))

mt.checkpoint('/net/archive/groups/plggneuromol/imdik-zekanowski-gts/data/joint-gts-only/gts-fams-filtered.mt')

