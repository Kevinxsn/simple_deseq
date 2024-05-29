import numpy as np
import pandas as pd
import os
from scipy.stats import gmean
import joblib
#import statsmodels.api as sm
#import statsmodels.formula.api as smf
import statsmodels.stats.multitest as multitest
from sklearn.preprocessing import StandardScaler


class simple_deseque:
    def __init__(self, conditions, txi):
        self.txi = txi
        self.conditions = conditions
        self.normalize = normalize(self.txi)
        
        self.base_mean = base_mean_calc(self.txi)
        self.fold_change = log2_fc(self.conditions, self.txi)
        self.dispersions = estimate_dispersion(self.txi)
        self.stat = stats(self.fold_change, self.dispersions, self.txi)
        
        dataframes = [self.base_mean, self.fold_change, self.dispersions, self.stat]

        # Initialize the result with the first DataFrame
        result = dataframes[0]

        # Merge DataFrames in a loop
        for df in dataframes[1:]:
            result = result.merge(df, on='gene_id', how='outer')
        
        self.result = result
        
        
        scaler = StandardScaler()
        predict_X = self.result.set_index('gene_id')
        predict_X = predict_X.fillna(0)
        predict_X = scaler.fit_transform(predict_X)
        
        
        best_rf = joblib.load('random_forest_model.pkl')
        y_pred = best_rf.predict(predict_X)
        
        self.result['p-value'] = y_pred
        min_val = np.min(y_pred)
        max_val = np.max(y_pred)
        normalized_data = (y_pred - min_val) / (max_val - min_val)
        self.result['p-value adjusted'] = normalized_data
        
    
#helper method, outputs a list of gene ids
def get_genes(test_txi):
    columns = test_txi.counts.columns
    genes = test_txi.counts[columns[0]].unique()
    return genes

def normalize(test_txi):
    """ Function to normalize read counts for each gene
    
    Parameters
    ----------
    test_txi: dataframe with int and string
       Table generated by teximport that combined raw counts from datasets 
    gene_lengths: list of int
       List of gene lengths for each gene. e.g. [length1, length2, ...]
    
    Returns
    -------
    normalized_data:
        dataframe with normalized read counts
    """
    columns = test_txi.counts.columns
    raw_data = test_txi.counts.set_index(columns[0])
    geometric_means = gmean(raw_data, axis=1)
    size_factors = raw_data.div(geometric_means[:, None], axis=0).replace(np.inf, np.nan).median(axis=0)
    normalized_data = raw_data / size_factors

    return normalized_data

    
def base_mean_calc(txi):
    geometric_means = txi.counts.set_index('gene_id').replace(0, np.nan).apply(np.nanmean, axis=1)
    size_factors = txi.counts.set_index('gene_id').div(geometric_means, axis=0).replace(np.inf, np.nan).median(axis=0)
    normalized_counts = txi.counts.set_index('gene_id').div(size_factors, axis=1)
    baseMean = normalized_counts.mean(axis=1)
    result = pd.DataFrame(baseMean, columns=['baseMean'])
    result.reset_index(inplace=True)
    return result


#basic log2 fold change
#need to fix: should not need the parameter condition
#basic log2 fold change



def get_conditions(conditions):
    str_1 = conditions[0]
    new_conditions = []
    for condition in conditions:
        if condition == str_1:
            new_conditions.append(0)
        else:
            new_conditions.append(1)
    return np.array(new_conditions)




def log2_fc(conditions, test_txi):
    """ Function to compute log2 fold change for each gene
    
    Parameters
    ----------
    test_txi: dataframe with int and string
       Table generated by teximport that combined raw counts from datasets 
    conditions: list of binary strings 
        Indicating the experimental conditions (treated vs. control) of the datasets
    
    Returns
    -------
    normalized_data:
        dataframe with normalized read counts
    """

    conditions = get_conditions(conditions)
    columns = test_txi.counts.columns

    #check if the conditions match the samples
    if len(conditions) != len(columns)-1:
        raise ValueError("the number of conditions does not match the number of samples!")
        
    genes = test_txi.counts[columns[0]]

    normalized_counts = normalize(test_txi)

    data = normalized_counts.rename(columns=lambda x: "")
    data = data.values

    
    # add a pseudocount to avoid log2 of zero
    pseudocount = 1
    data += pseudocount

    treated_mean = np.mean(data[:, conditions == 1], axis=1)
    control_mean = np.mean(data[:, conditions == 0], axis=1)

    log2fc = np.log2(treated_mean / control_mean)

    log2fc_df = pd.DataFrame({
        columns[0]: genes,
        'Log2FoldChange': log2fc
    })
    log2fc_df = log2fc_df.set_index(columns[0])

    return log2fc_df


def dispersion_helper(df):
    mean = df['count'].mean()
    variance = df['count'].var()  # using variance as a proxy for dispersion
    dispersion = (variance - mean) / (mean ** 2)
    if dispersion < 0:
        dispersion = np.nan
    return mean, dispersion

def estimate_dispersion(test_txi):

    columns = test_txi.counts.columns
    normalized_counts = normalize(test_txi)

    # adjust the format of the dataframe
    counts_long = normalized_counts.reset_index().melt(id_vars=columns[0], var_name='sample', value_name='count')
    
    results = []
    genes = get_genes(test_txi)
    for gene in genes:
        # get the read counts for current gene
        df_gene = counts_long[counts_long[columns[0]] == gene]
        
        # use helper to get estimated dispersion
        mean, dispersion = dispersion_helper(df_gene)
        
        # append the results
        results.append({columns[0]: gene, 'dispersion': dispersion})
    
    results_df = pd.DataFrame(results)
    results_df = results_df.set_index(columns[0])
    return results_df

def stats(log2fc, dispersions, test_txi):
    result = []
    genes = get_genes(test_txi)
    columns = test_txi.counts.columns
    for gene in genes:
        fc = log2fc.loc[gene, 'Log2FoldChange']
        se = dispersions.loc[gene, 'dispersion']
        stat = fc/se
        result.append({columns[0]: gene, 'Stats': stat})
    
    result = pd.DataFrame(result)
    result = result.set_index(columns[0])
    return result



# INCOMPLETE!!!
# finding the estimate dispersion parameter as a function of the mean using a negative binomial distribution 
"""
def negative_binomial_dispersion(test_txi):
    columns = test_txi.counts.columns
    normalized_counts = normalize(test_txi)

    
    counts_long = normalized_counts.reset_index().melt(id_vars=columns[0], var_name='sample', value_name='read_count')
    
    results = []
    genes = counts_long[columns[0]].unique()
    for gene in genes:
        df_gene = counts_long[counts_long[columns[0]] == gene]
        
        # use the negative binomial model
        model = smf.glm(formula='read_count ~ 1', data=df_gene, family=sm.families.NegativeBinomial())
        result = model.fit()
        
        # extract the dispersion parameter
        dispersion = result.scale
        mean_read_count = df_gene['read_count'].mean()
        
        # Append the results
        results.append({columns[0]: gene, 'mean': mean_read_count, 'dispersion': dispersion})

    results_df = pd.DataFrame(results)

    return results_df
"""
