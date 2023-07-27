import os
import hail as hl

localfs_path = os.environ.get('SCRATCH_LOCAL') + '/'

def run_pca(mtx, mtx_path, suffix):
    mtx = hl.variant_qc(mtx)
    mtx = mtx.checkpoint(localfs_path+'variant_qced_'+suffix+mtx_path)
    mtx = hl.read_matrix_table(localfs_path+'variant_qced_'+suffix+mtx_path)
    for_pca = mtx.filter_rows(mtx.variant_qc.AF[1] > 0.05)
    pruned_variant_table = hl.ld_prune(for_pca.GT, r2=0.2, bp_window_size=500000)
    for_pca = for_pca.filter_rows(hl.is_defined(pruned_variant_table[for_pca.row_key]))

    for_pca = for_pca.checkpoint(localfs_path+'for_pca_20_'+suffix+mtx_path)
    for_pca = hl.read_matrix_table(localfs_path+'for_pca_20_'+suffix+mtx_path)
    eigenvalues, pcs, _ = hl.hwe_normalized_pca(for_pca.GT, k=20)
    
    mtx = mtx.annotate_cols(pruned_scores = pcs[mtx.s].scores)
    mtx = mtx.checkpoint(localfs_path+'after_pca_20_'+suffix+mtx_path)
    
    return(mtx)

def run_pca_no_filter(mtx, mtx_path, suffix):
    
    for_pca = mtx.sample_rows(0.1)

    for_pca = for_pca.checkpoint(localfs_path+'subset_'+suffix+mtx_path)
    for_pca = hl.read_matrix_table(localfs_path+'subset_'+suffix+mtx_path)
    eigenvalues, pcs, _ = hl.hwe_normalized_pca(for_pca.GT, k=20)
    
    mtx = mtx.annotate_cols(scores_no_filter = pcs[mtx.s].scores)
    mtx = mtx.checkpoint(localfs_path+'after_pca_no_filters_'+suffix+mtx_path)
    
    return(mtx)

def remove_pca_outliers(mtx, field, last_score, mtx_path, suffix):
    
    mtx = mtx.annotate_globals(
            st = mtx.aggregate_cols(
                hl.agg.array_agg(
                    lambda pc: hl.agg.stats(pc),
                    mtx[field])
            )
        )

    mtx = mtx.annotate_cols(
            pc_outliers=hl.map(
                lambda s, st: hl.int((s > st['mean'] + (10 * st['stdev'])) | (s < st['mean'] - (10 * st['stdev']))),
                mtx[field][0:last_score],
                mtx.st
            )
        )

    mtx = mtx.filter_cols(
        hl.sum(mtx.pc_outliers) ==  0
    )
    
    mtx = mtx.checkpoint(localfs_path+'no_outliers'+mtx_path+suffix+'.mt')
    
    return(mtx)