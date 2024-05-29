import pandas as pd
import numpy as np


class simple_texi:
    def __init__(self, list_df_path, column_names, gene_id_index, count_column_index, abundance_column_index, length_column_index):
        self.df = [pd.read_table(i) for i in list_df_path]
        self.column_names = column_names
        gene_id = self.df[0].columns[gene_id_index]
        self.gene_id = gene_id
        
        ## Make sure every datafrom having a different column name
        # Assuming self.df is a list of DataFrames
        for i in range(len(self.df)):
            # Rename the column at count_column_index by appending the column name
            column_to_rename = self.df[i].columns[count_column_index]
            new_column_name = column_to_rename + column_names[i]
            self.df[i].rename(columns={column_to_rename: new_column_name}, inplace=True)

        
        self.counts = merge_dataframes_on_column(self.df, gene_id, [[_.columns[count_column_index]] for _ in self.df], column_names)
        
        if abundance_column_index is not None:
            #abundance_id = self.df[0].columns[abundance_column_index]
            for i in range(len(self.df)):
            # Rename the column at abundance_column_index by appending the column name
                column_to_rename = self.df[i].columns[abundance_column_index]
                new_column_name = column_to_rename + column_names[i]
                self.df[i].rename(columns={column_to_rename: new_column_name}, inplace=True)
            
            self.abundance = merge_dataframes_on_column(self.df, gene_id, [[_.columns[abundance_column_index]] for _ in self.df], column_names)
        else:
            self.abundance = None
            
        if length_column_index is not None:
            #length_id = self.df[0].columns[length_column_index]
            for i in range(len(self.df)):
            # Rename the column at length_column_index by appending the column name
                column_to_rename = self.df[i].columns[length_column_index]
                new_column_name = column_to_rename + column_names[i]
                self.df[i].rename(columns={column_to_rename: new_column_name}, inplace=True)
            self.length = merge_dataframes_on_column(self.df, gene_id, [[_.columns[length_column_index]] for _ in self.df], column_names)
        else:
            self.length = None
        
        
    
        
    def __str__(self):
        
        counts_info = str([self.counts.shape, self.counts.columns])
        
        if self.length is not None:
            length_info = str([self.length.shape, self.length.columns])
        else:
            length_info = 'There is no length data for this simple_texi class'
        
        if self.abundance is not None:
            abundance_info = str([self.abundance.shape, self.abundance.columns])
        else:
            abundance_info = 'There is no abundance data for this simple_texi class'
            
            
        ans = f'count information: {counts_info} \n abundance information: {abundance_info} \n length information: {length_info}'
        return ans
    
    def filter(self, threshold, min_samples):
        self.counts = filter_genes(self, self.counts, threshold, min_samples)
        if self.length is not None:
            self.length = self.length[self.length[self.gene_id].isin(self.counts[self.gene_id])]
        if self.abundance is not None:
            self.abundance = self.abundance[self.abundance[self.gene_id].isin(self.counts[self.gene_id])]
    
    
        



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


def filter_genes(self, dataframe, threshold, min_samples):
    counts = dataframe.set_index(self.gene_id)
    
    sufficient_counts = (counts >= threshold).sum(axis=1)
    
    filtered_genes = sufficient_counts[sufficient_counts >= min_samples].index
    
    return dataframe[dataframe[self.gene_id].isin(filtered_genes)]
