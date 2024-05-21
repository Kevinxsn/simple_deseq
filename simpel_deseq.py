import numpy as np
import pandas as pd

class simple_deseque:
    def __init__(self, txi):
        self.txi = txi
        self.base_mean = base_mean_calc(self.txi)
    
    
    
def base_mean_calc(txi):
    geometric_means = txi.counts.set_index('gene_id').replace(0, np.nan).apply(np.nanmean, axis=1)
    size_factors = txi.counts.set_index('gene_id').div(geometric_means, axis=0).replace(np.inf, np.nan).median(axis=0)
    normalized_counts = txi.counts.set_index('gene_id').div(size_factors, axis=1)
    baseMean = normalized_counts.mean(axis=1)
    result = pd.DataFrame(baseMean, columns=['baseMean'])
    result.reset_index(inplace=True)
    return result