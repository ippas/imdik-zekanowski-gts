import os
localfs_path = os.environ.get('SCRATCH_LOCAL') + '/'

import hail as hl
import numpy as np
from bokeh.io import show, output_notebook

def read_in_pheno_anno_pw(mt_path, suffix):
    
    mt = hl.read_matrix_table(
        mt_path
    )
    
    #annotate with genes
    
    gtf = hl.import_table(
    '/net/pr2/projects/plgrid/plggneuromol/resources/genecode_43/gencode.v43.basic.annotation.gtf',
    delimiter = "\t",
    no_header = True,
    comment = "#"
    )

    # filter the gtf to only contain protein-coding genes with any GO term
    gtf = gtf.filter((gtf.f2 == 'gene') & (gtf.f8.contains('protein_coding')))

    gtf = gtf.select(
        gene_position = hl.locus_interval(
            gtf.f0,
            hl.int(gtf.f3),
            hl.int(gtf.f4),
            reference_genome='GRCh38'
        ),
        gene_symbol = gtf.f8.split("\"")[5]
    )  

    go_genes = hl.import_table(
        '/net/pr2/projects/plgrid/plggneuromol/resources/human-genes-with-GO-and-symbols'
    )

    go_genes = go_genes.key_by(go_genes['UniProtKB Gene Name symbol'])

    gtf = gtf.key_by(gtf['gene_symbol'])
    gtf = gtf.filter(
        hl.is_defined(
            go_genes[gtf.gene_symbol]
        )
    )

    # overall we are keeping 18303 genes. At this poin the within gene intervals are extended by 20kb each side
    start = hl.if_else(
        gtf.gene_position.start.position <= 20000, 1, gtf.gene_position.start.position - 20000
    )

    contig_len = hl.contig_length(gtf.gene_position.start.contig, reference_genome='GRCh38') 

    stop = hl.if_else(
        (contig_len - gtf.gene_position.end.position) <= 20000,
        contig_len,
        gtf.gene_position.end.position + 20000
    )

    gtf = gtf.annotate(
        interval_20kb =
        hl.locus_interval(
            gtf.gene_position.start.contig,
            start,
            stop,
            reference_genome='GRCh38'
        )
    )

    gtf = gtf.key_by(gtf.interval_20kb)
    
    mt = mt.filter_rows(mt.cadd.score_phred > 0)
    
    mt = mt.annotate_rows(
        nearest_genes_20kb = hl.array(
            hl.set(
                gtf.index(mt.locus, all_matches=True)['gene_symbol']))
    )
    
    mt = mt.filter_rows(hl.agg.any(mt.GT.is_non_ref()))
    mt = mt.explode_rows(mt.nearest_genes_20kb)
    
    mt = mt.checkpoint(localfs_path+suffix+'.mt')
    
    return(mt)

def read_in_pheno_anno_sport(mt_path, suffix): # this only keeps : GTS, sportsmen and healthy from families
    
    mt = hl.read_matrix_table(
        mt_path
    )
    
    #annotate with genes
    
    gtf = hl.import_table(
    '/net/pr2/projects/plgrid/plggneuromol/resources/genecode_43/gencode.v43.basic.annotation.gtf',
    delimiter = "\t",
    no_header = True,
    comment = "#"
    )

    # filter the gtf to only contain protein-coding genes with any GO term
    gtf = gtf.filter((gtf.f2 == 'gene') & (gtf.f8.contains('protein_coding')))

    gtf = gtf.select(
        gene_position = hl.locus_interval(
            gtf.f0,
            hl.int(gtf.f3),
            hl.int(gtf.f4),
            reference_genome='GRCh38'
        ),
        gene_symbol = gtf.f8.split("\"")[5]
    )  

    go_genes = hl.import_table(
        '/net/pr2/projects/plgrid/plggneuromol/resources/human-genes-with-GO-and-symbols'
    )

    go_genes = go_genes.key_by(go_genes['UniProtKB Gene Name symbol'])

    gtf = gtf.key_by(gtf['gene_symbol'])
    gtf = gtf.filter(
        hl.is_defined(
            go_genes[gtf.gene_symbol]
        )
    )

    # overall we are keeping 18303 genes. At this poin the within gene intervals are extended by 20kb each side
    start = hl.if_else(
        gtf.gene_position.start.position <= 20000, 1, gtf.gene_position.start.position - 20000
    )

    contig_len = hl.contig_length(gtf.gene_position.start.contig, reference_genome='GRCh38') 

    stop = hl.if_else(
        (contig_len - gtf.gene_position.end.position) <= 20000,
        contig_len,
        gtf.gene_position.end.position + 20000
    )

    gtf = gtf.annotate(
        interval_20kb =
        hl.locus_interval(
            gtf.gene_position.start.contig,
            start,
            stop,
            reference_genome='GRCh38'
        )
    )

    gtf = gtf.key_by(gtf.interval_20kb)
    
    
    mt = mt.filter_rows(mt.cadd.score_phred > 0)
    
    mt = mt.annotate_rows(
        nearest_genes_20kb = hl.array(
            hl.set(
                gtf.index(mt.locus, all_matches=True)['gene_symbol']))
    )
    
    mt = mt.filter_rows(hl.agg.any(mt.GT.is_non_ref()))
    mt = mt.explode_rows(mt.nearest_genes_20kb)
    
    pheno = hl.import_table(
    '/net/pr2/projects/plgrid/plggneuromol/imdik-zekanowski-gts/data/pheno/GTS-coded-corrected-june-2021.csv',
    impute=True,
    delimiter=',',
    quote="\""
    )

    pheno = pheno.key_by(pheno.ID)
    
    mt = mt.annotate_cols(phenotypes = pheno[mt.s])
    
    mt = mt.filter_cols(
        (mt.phenotypes.family != '.') | (mt.group == 'local_controls')
    ) # families and sportsmen
        
    mt = mt.filter_cols(
        (mt.phenotypes.phenotype != 'tics') | (mt.group == 'local_controls')
    ) #remove people with tics
    
    mt = mt.checkpoint(localfs_path+suffix+'.mt')
    
    return(mt)

def read_in_pheno_anno_all(mt_path, suffix):
    
    mt = hl.read_matrix_table(
        mt_path
    )
    
    #annotate with genes
    
    gtf = hl.import_table(
    '/net/pr2/projects/plgrid/plggneuromol/resources/genecode_43/gencode.v43.basic.annotation.gtf',
    delimiter = "\t",
    no_header = True,
    comment = "#"
    )

    # filter the gtf to only contain protein-coding genes with any GO term
    gtf = gtf.filter((gtf.f2 == 'gene') & (gtf.f8.contains('protein_coding')))

    gtf = gtf.select(
        gene_position = hl.locus_interval(
            gtf.f0,
            hl.int(gtf.f3),
            hl.int(gtf.f4),
            reference_genome='GRCh38'
        ),
        gene_symbol = gtf.f8.split("\"")[5]
    )  

    go_genes = hl.import_table(
        '/net/pr2/projects/plgrid/plggneuromol/resources/human-genes-with-GO-and-symbols'
    )

    go_genes = go_genes.key_by(go_genes['UniProtKB Gene Name symbol'])

    gtf = gtf.key_by(gtf['gene_symbol'])
    gtf = gtf.filter(
        hl.is_defined(
            go_genes[gtf.gene_symbol]
        )
    )

    # overall we are keeping 18303 genes. At this poin the within gene intervals are extended by 20kb each side
    start = hl.if_else(
        gtf.gene_position.start.position <= 20000, 1, gtf.gene_position.start.position - 20000
    )

    contig_len = hl.contig_length(gtf.gene_position.start.contig, reference_genome='GRCh38') 

    stop = hl.if_else(
        (contig_len - gtf.gene_position.end.position) <= 20000,
        contig_len,
        gtf.gene_position.end.position + 20000
    )

    gtf = gtf.annotate(
        interval_20kb =
        hl.locus_interval(
            gtf.gene_position.start.contig,
            start,
            stop,
            reference_genome='GRCh38'
        )
    )

    gtf = gtf.key_by(gtf.interval_20kb)
    
    
    mt = mt.filter_rows(mt.cadd.score_phred > 0)
    
    mt = mt.annotate_rows(
        nearest_genes_20kb = hl.array(
            hl.set(
                gtf.index(mt.locus, all_matches=True)['gene_symbol']))
    )
    
    mt = mt.filter_rows(hl.agg.any(mt.GT.is_non_ref()))
    mt = mt.explode_rows(mt.nearest_genes_20kb)
    
    pheno = hl.import_table(
    '/net/pr2/projects/plgrid/plggneuromol/imdik-zekanowski-gts/data/pheno/GTS-coded-corrected-june-2021.csv',
    impute=True,
    delimiter=',',
    quote="\""
    )

    pheno = pheno.key_by(pheno.ID)
    
    mt = mt.annotate_cols(phenotypes = pheno[mt.s])
    
    mt = mt.checkpoint(localfs_path+suffix+'.mt')
    
    return(mt)


def aggregate_per_burden(mt, path):
    
    mt = mt.naive_coalesce(500)
    mt = mt.checkpoint(localfs_path+path+'.mt')
    
    cadds = [0,5,10,16]
    results = mt.group_rows_by(mt.nearest_genes_20kb).aggregate(
        **{
            f'n_non_ref_above_cadd_{c}': hl.agg.filter(
                mt.cadd.score_phred > c, hl.agg.sum(mt.GT.n_alt_alleles())
            )
    for c in cadds
        },
        **{
            f'n_non_ref_above_cadd_weited_{c}': hl.agg.filter(
                mt.cadd.score_phred > c, hl.agg.sum(mt.GT.n_alt_alleles()*mt.cadd.score_phred)
            )
    for c in cadds
        }
    )
    
    results = results.checkpoint(localfs_path+path+'per_burden_agg.mt')
    
    return(results)

def stand_burden(results, path):
    
    cadds = [0,5,10,16]
    
    results = results.annotate_rows(
         **{
             **{
                 f'per_gene_stats_above_cadd_{c}': hl.agg.stats(
                     results[f'n_non_ref_above_cadd_{c}']
                 )
                 for c in cadds
             },
            **{
                 f'per_gene_stats_weited_above_cadd_{c}': hl.agg.stats(
                     results[f'n_non_ref_above_cadd_weited_{c}']
                 )
                 for c in cadds
            }
        }
    )
    
    results = results.annotate_entries(
         **{
             **{
                 f'per_gene_stand_above_cadd_{c}': 
                     (
                         (
                             results[f'n_non_ref_above_cadd_{c}'] - results[f'per_gene_stats_above_cadd_{c}'].mean
                         )
                     )
                 for c in cadds
             },
            **{
                 f'per_gene_stand_weited_above_cadd_{c}': 
                     (
                         (
                             results[f'n_non_ref_above_cadd_weited_{c}'] - results[f'per_gene_stats_weited_above_cadd_{c}'].mean
                         )
                     )
                 for c in cadds
             },
             **{
                 f'per_gene_stdev_above_cadd_{c}': 
                     (
                         (
                             results[f'n_non_ref_above_cadd_{c}'] - results[f'per_gene_stats_above_cadd_{c}'].mean
                         )/results[f'per_gene_stats_above_cadd_{c}'].stdev
                     )
                 for c in cadds
             },
            **{
                 f'per_gene_stdev_weited_above_cadd_{c}': 
                     (
                         (
                             results[f'n_non_ref_above_cadd_weited_{c}'] - results[f'per_gene_stats_weited_above_cadd_{c}'].mean
                         )/results[f'per_gene_stats_weited_above_cadd_{c}'].stdev
                     )
                 for c in cadds
             }
        }
    )
    

    results = results.checkpoint(localfs_path+path+'stand_per_gene.mt')
    
    return(results)

def stand_with_ref(results, reference, path):
    
    reference = reference.rows()
    reference = reference.checkpoint(localfs_path+path+'ref_rows.mt')
    
    cadds = [0,5,10,16]

    print('x')
    
    results = results.annotate_rows(
        **{
            f'per_gene_stats_above_cadd_mean_pl{c}': reference[results.row_key][f'per_gene_stats_above_cadd_{c}'].mean
            for c in cadds
        }
    )
          
    
    results = results.checkpoint(localfs_path+path+'res_anno_temp1.mt')
    
    results = results.annotate_rows(
        **{
            f'per_gene_stats_above_cadd_stdev_pl{c}': reference[results.row_key][f'per_gene_stats_above_cadd_{c}'].stdev
            for c in cadds
        }
    )
    
    results = results.checkpoint(localfs_path+path+'res_anno_temp2.mt')
    
    results = results.annotate_rows(
        **{
            f'per_gene_stats_above_cadd_weit_mean_pl{c}': reference[results.row_key][f'per_gene_stats_weited_above_cadd_{c}'].mean
            for c in cadds
        }
    )
    
    results = results.checkpoint(localfs_path+path+'res_anno_temp3.mt')
    
    results = results.annotate_rows(
        **{
            f'per_gene_stats_above_cadd_weit_stdev_pl{c}': reference[results.row_key][f'per_gene_stats_weited_above_cadd_{c}'].stdev
        for c in cadds
        }
    )
    
    results = results.checkpoint(localfs_path+path+'res_anno.mt')

    results = results.annotate_entries(
        **{
            **{
                f'per_gene_stand_above_cadd_{c}':
                (
                    results[f'n_non_ref_above_cadd_{c}'] - results[f'per_gene_stats_above_cadd_mean_pl{c}']
                )
                for c in cadds
            },
            **{
                f'per_gene_stand_weited_above_cadd_{c}':
                (
                    results[f'n_non_ref_above_cadd_weited_{c}'] - results[f'per_gene_stats_above_cadd_weit_mean_pl{c}']
                )
                for c in cadds
            },
            **{
                f'per_gene_stdev_above_cadd_{c}':
                (
                    results[f'n_non_ref_above_cadd_{c}'] - results[f'per_gene_stats_above_cadd_mean_pl{c}']
                )/results[f'per_gene_stats_above_cadd_stdev_pl{c}']
                for c in cadds
            },
            **{
                f'per_gene_stdev_weited_above_cadd_{c}':
                (
                    results[f'n_non_ref_above_cadd_weited_{c}'] - results[f'per_gene_stats_above_cadd_weit_mean_pl{c}']
                )/results[f'per_gene_stats_above_cadd_weit_stdev_pl{c}']
                for c in cadds
            }
        }
    )

    results = results.checkpoint(localfs_path+path+'stand_per_gene_with_ref.mt')

    return(results)

def prep_eur_for_skat(mts, path):
    
    gtf = hl.import_table(
        '/net/pr2/projects/plgrid/plggneuromol/resources/genecode_43/gencode.v43.basic.annotation.gtf',
        delimiter = "\t",
        no_header = True,
        comment = "#"
    )

    # filter the gtf to only contain protein-coding genes with any GO term
    gtf = gtf.filter((gtf.f2 == 'gene') & (gtf.f8.contains('protein_coding')))

    gtf = gtf.select(
        gene_position = hl.locus_interval(
            gtf.f0,
            hl.int(gtf.f3),
            hl.int(gtf.f4),
            reference_genome='GRCh38'
        ),
        gene_symbol = gtf.f8.split("\"")[5]
    )  

    go_genes = hl.import_table(
        '/net/pr2/projects/plgrid/plggneuromol/resources/human-genes-with-GO-and-symbols'
    )

    go_genes = go_genes.key_by(go_genes['UniProtKB Gene Name symbol'])

    gtf = gtf.key_by(gtf['gene_symbol'])
    gtf = gtf.filter(
        hl.is_defined(
            go_genes[gtf.gene_symbol]
        )
    )

    # overall we are keeping 18303 genes. At this poin the within gene intervals are extended by 20kb each side
    start = hl.if_else(
        gtf.gene_position.start.position <= 20000, 1, gtf.gene_position.start.position - 20000
    )

    contig_len = hl.contig_length(gtf.gene_position.start.contig, reference_genome='GRCh38') 

    stop = hl.if_else(
        (contig_len - gtf.gene_position.end.position) <= 20000,
        contig_len,
        gtf.gene_position.end.position + 20000
    )

    gtf = gtf.annotate(
        interval_20kb =
        hl.locus_interval(
            gtf.gene_position.start.contig,
            start,
            stop,
            reference_genome='GRCh38'
        )
    )

    gtf = gtf.key_by(gtf.interval_20kb)

    for idx, mt in enumerate(mts):    

        mt = mt.annotate_rows(
                nearest_genes_20kb = hl.array(
                    hl.set(
                        gtf.index(mt.locus, all_matches=True)['gene_symbol'])
                )
        )

        mt = mt.filter_rows(hl.agg.any(mt.GT.is_non_ref()))
        mt = mt.explode_rows(mt.nearest_genes_20kb)

        # annotate with sex
        eur_phenos = hl.import_table(
            '/net/pr2/projects/plgrid/plggneuromol/matzieb/projects/imdik-zekanowski-sportwgs/data/prs-data/1kg-sportsmen-pheno.tsv'
        )
        eur_phenos = eur_phenos.key_by(eur_phenos['sample'])

        mt = mt.filter_rows(mt.cadd.score_phred > 0)

        mt = mt.checkpoint(localfs_path+'_'+str(idx)+'_tempx.mt')

        mt = mt.annotate_cols(
            sex = hl.if_else(
                mt.group == 'GTS',
                mt.phenotypes.sex,                                  
                hl.if_else(
                    eur_phenos[mt.col_key].gender == "male",
                    'M',
                    'F'
                )
            )
        )

        mt = mt.checkpoint(localfs_path+'_'+str(idx)+path+'annot.mt')

        mts[idx] = mt
    
    return(mts)

def model_assignment(results, genes):
    
    results = results.annotate_cols(
        skat_pheno = hl.if_else(
            results.group == 'GTS',
            hl.if_else(
                results.phenotypes.phenotype == 'GTS',
                'YES',
                'NO'),
            'NO'
        )
    )
    
    cadds = [0,5,10,16]
    
    results = results.filter_rows(
        hl.literal(genes).contains(results.nearest_genes_20kb)
    )

    results = results.annotate_cols(
        gts = hl.int(results.skat_pheno == 'YES')
    )
    
    group = np.array(results.gts.collect())
    
    results = results.annotate_cols(
        sport = hl.int(results.group == 'local_controls')
    )
    sport = np.array(results.sport.collect())
    
    
    assignments = results.annotate_cols(
        **{
            f'n_non_ref_above_cadd_sum_{c}': hl.agg.sum(results[f'per_gene_stdev_above_cadd_{c}'])
            for c in cadds
        },
        **{
            f'n_non_ref_weited_above_cadd_sum_{c}': hl.agg.sum(results[f'per_gene_stdev_weited_above_cadd_{c}'])
            for c in cadds
        }
    )
    
    model_sum = []
    model_weits = []
    
    for c in cadds:      
        model_sum.append(
            np.array(assignments[f'n_non_ref_above_cadd_sum_{c}'].collect())
        )
        model_weits.append(
            np.array(assignments[f'n_non_ref_weited_above_cadd_sum_{c}'].collect())
        )
        
    return(group, sport, model_sum, model_weits)

def prep_pl_for_skat(mts):
    
    for idx, mt in enumerate(mts):
       
        if os.path.exists(localfs_path+'_pl_'+str(idx)+'ann.mt'):
            
            mts[idx] = hl.read_matrix_table(localfs_path+'_pl_'+str(idx)+'ann.mt')
            
        else:
            
            if os.path.exists(localfs_path+'_'+str(idx)+'_tmp.mt'):
                
                mt = hl.read_matrix_table(localfs_path+'_'+str(idx)+'_tmp.mt')
                
            else:   
    
                gtf = hl.import_table(
                    '/net/pr2/projects/plgrid/plggneuromol/resources/genecode_43/gencode.v43.basic.annotation.gtf',
                    delimiter = "\t",
                    no_header = True,
                    comment = "#"
                )

                # filter the gtf to only contain protein-coding genes with any GO term
                gtf = gtf.filter((gtf.f2 == 'gene') & (gtf.f8.contains('protein_coding')))

                gtf = gtf.select(
                    gene_position = hl.locus_interval(
                        gtf.f0,
                        hl.int(gtf.f3),
                        hl.int(gtf.f4),
                        reference_genome='GRCh38'
                    ),
                    gene_symbol = gtf.f8.split("\"")[5]
                )  

                go_genes = hl.import_table(
                    '/net/pr2/projects/plgrid/plggneuromol/resources/human-genes-with-GO-and-symbols'
                )

                go_genes = go_genes.key_by(go_genes['UniProtKB Gene Name symbol'])

                gtf = gtf.key_by(gtf['gene_symbol'])
                gtf = gtf.filter(
                    hl.is_defined(
                        go_genes[gtf.gene_symbol]
                    )
                )

                # overall we are keeping 18303 genes. At this poin the within gene intervals are extended by 20kb each side
                start = hl.if_else(
                    gtf.gene_position.start.position <= 20000, 1, gtf.gene_position.start.position - 20000
                )

                contig_len = hl.contig_length(gtf.gene_position.start.contig, reference_genome='GRCh38') 

                stop = hl.if_else(
                    (contig_len - gtf.gene_position.end.position) <= 20000,
                    contig_len,
                    gtf.gene_position.end.position + 20000
                )

                gtf = gtf.annotate(
                    interval_20kb =
                    hl.locus_interval(
                        gtf.gene_position.start.contig,
                        start,
                        stop,
                        reference_genome='GRCh38'
                    )
                )

                gtf = gtf.key_by(gtf.interval_20kb)

                mt = mt.annotate_rows(
                        nearest_genes_20kb = hl.array(
                            hl.set(
                                gtf.index(mt.locus, all_matches=True)['gene_symbol'])
                        )
                )

                mt = mt.filter_rows(hl.agg.any(mt.GT.is_non_ref()))
                mt = mt.explode_rows(mt.nearest_genes_20kb)

                mt = mt.filter_rows(mt.cadd.score_phred > 0)
                mt = mt.naive_coalesce(100)

                mt = mt.checkpoint(localfs_path+'_'+str(idx)+'_tmp.mt')

            
            mt = mt.annotate_cols(
                sex = hl.if_else(
                    mt.group == 'GTS',
                    mt.phenotypes.sex,                                  
                    mt.sex
                )
            )

            mt = mt.checkpoint(localfs_path+'_pl_'+str(idx)+'ann.mt')

            mts[idx] = mt
    
    return(mts)

def run_skat_log(mtx, pcs, field, suffix):
    
    scores = [mtx[field][x] for x in list(range(pcs))]
    is_male = hl.float(mtx.sex == 'M')
    
    skat_table = hl.skat(key_expr=mtx.nearest_genes_20kb,
                         weight_expr=mtx.cadd.score_phred,
                         y=(mtx.group == 'GTS'),
                         x=mtx.GT.n_alt_alleles(),
                         covariates=[1, is_male] + scores,
                         max_size = 2500,
                         logistic = True)
    
    skat_table = skat_table.checkpoint(localfs_path+'skat_table_'+str(pcs)+'_'+field+suffix+'.mt')

    skat_table.order_by(skat_table.p_value).show(20)
    
    qq_plot = hl.plot.qq(
        skat_table.p_value
    )
    show(qq_plot)
    
    return(skat_table, qq_plot)

def run_skat_for_mts(mt_list):
    
    skat_tables = []
    plots = []
    options = []

    for idx, mtx in enumerate(mt_list):

        for pc in list(range(21)):
            

            print('running with '+str(pc)+' PCs and the just subsetet scores')
            
            if os.path.exists(localfs_path+'skat_table_'+str(pc)+'_scores_no_filter_parts_'+str(idx)+'.mt'):
            
                skat_table = hl.read_table(
                    localfs_path+'skat_table_'+str(pc)+'_scores_no_filter_parts_'+str(idx)+'.mt'
                )
                
                skat_tables.append(skat_table)
                
                plots.append(hl.plot.qq(
                    skat_table.p_value
                ))
                
                options.append(
                        'PCs '+str(pc)+' subseted scores subset '+str(idx)
                    )
                
            else:
                try:
                    skat_table_no_filt, qq_plot_no_filt = run_skat_log(
                        mtx,
                        pc,
                        'scores_no_filter',
                        '_parts_'+str(idx)
                    )

                    skat_tables.append(skat_table_no_filt)
                    plots.append(qq_plot_no_filt)
                    
                    options.append(
                        'PCs '+str(pc)+' no filters subseted scores subset '+str(idx)
                    )

                except Exception as e:
                    print('failed PCs '+str(pc)+' no filters subseted scores'+'subset '+str(idx))
                    print(type(e))
            
    return(skat_tables, plots, options)