import pandas as pd
import numpy as np


class simple_texi:
    def __init__(self, list_df_path, column_names):
        self.df = [pd.read_table(i) for i in list_df_path]
        self.column_names = column_names
        self.abundance = merge_dataframes_on_column(self.df, 'gene_id', [['TPM'] for _ in self.df], column_names)
        self.counts = merge_dataframes_on_column(self.df, 'gene_id', [['expected_count'] for _ in self.df], column_names)
        self.length = merge_dataframes_on_column(self.df, 'gene_id', [['effective_length'] for _ in self.df], column_names)
        
    def __str__(self):
        abundance_info = str([self.abundance.shape, self.abundance.columns])
        counts_info = str([self.counts.shape, self.counts.columns])
        length_info = str([self.length.shape, self.length.columns])
        ans = f'abundance information: {abundance_info} \n count information: {counts_info} \n length information: {length_info}'
        return ans
    
    def filter(self, threshold, min_samples):
        self.counts = filter_genes(self.counts, threshold, min_samples)
        self.length = self.length[self.length['gene_id'].isin(self.counts['gene_id'])]
        self.abundance = self.abundance[self.abundance['gene_id'].isin(self.counts['gene_id'])]
    
    
        



def merge_dataframes_on_column(dfs, join_column, columns_to_keep, column_name):
    """
    Merge multiple DataFrames on a specified join column and keep only specified columns.

    Args:
    dfs (list of pd.DataFrame): List of DataFrames to merge.
    join_column (str): Name of the column to join on.
    columns_to_keep (list of list of str): List of lists, where each sublist contains the names of the columns
                                           to keep from the corresponding DataFrame.

    Returns:
    pd.DataFrame: A DataFrame resulting from merging all input DataFrames on the join_column and 
                  keeping only the specified columns from each.
    """
    # Ensure columns_to_keep is valid
    if len(dfs) != len(columns_to_keep):
        raise ValueError("Each DataFrame must have a corresponding list of columns to keep.")

    # Reduce the dataframes to only the columns to keep and the join column
    reduced_dfs = [
        df[[join_column] + columns] for df, columns in zip(dfs, columns_to_keep)
        if join_column in df.columns and all(col in df.columns for col in columns)
    ]
    
    # Merge all dataframes on the join column
    merged_df = reduced_dfs[0]
    for df in reduced_dfs[1:]:
        merged_df = pd.merge(merged_df, df, on=join_column, how='inner')
    merged_df.columns = [merged_df.columns[0]] + column_name
    
    return merged_df


def filter_genes(dataframe, threshold, min_samples):
    counts = dataframe.set_index('gene_id')
    
    sufficient_counts = (counts >= threshold).sum(axis=1)
    
    filtered_genes = sufficient_counts[sufficient_counts >= min_samples].index
    
    return dataframe[dataframe['gene_id'].isin(filtered_genes)]
