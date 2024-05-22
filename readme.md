Here is simple_deseq & simple_teximport

## Introduction of simple_teximprt and simpel_deseq:

DESeq and tximport are two popular bioinformatics packages used with R. They are essential for the analysis of RNA-sequencing (RNA-seq) data, which is crucial for understanding gene expression differences across various biological samples.

However, there is a limitation with these tools. Since they are only compatible with R, users who utilize other programming environments like Python must switch to R to run DESeq, store the results, and then switch back to their preferred language. This back-and-forth can be cumbersome.

To address this issue, we developed simple_tximport and simple_deseq, two Python packages that replicate part of the functionality of tximport and DESeq. These tools enable researchers to run the entire DESeq analysis pipeline completely in Python, streamlining the process and enhancing efficiency.



## simple_teximport

Certainly! Here is a revised version for your README:

# simple_tximport

`simeple_tximport` is a Python package designed to help users convert raw table data into a format suitable for analysis with `simple_deseq`.


## Usage

`simeple_tximport` takes six arguments:

1. `list_of_def_path`: A Python list containing the paths to the table files.
2. `column_names`: A Python list specifying the column names to use for each table after conversion. It is recommended to use easily identifiable group names, such as `['old1', 'old2', 'young1', 'young2']`.
3. `gene_id_index`: An integer indicating the column number that identifies the gene. For example, if the gene is stored in the second column of the table, this number should be `1` (since the index starts from 0).
4. `count_column_index`: An integer indicating the column number that identifies the counts of each gene.
5. `abundance_column_index`: An integer or `None`, indicating the column number that identifies the abundance of each gene.
6. `length_column_index`: An integer or `None`, indicating the column number that identifies the length of each gene.

## Example

```python
import simpel_teximport

list_of_def_path = ['/path/to/file1', '/path/to/file2']
column_names = ['old1', 'young1']
gene_id_index = 1
count_column_index = 2
abundance_column_index = 3
length_column_index = 4

txi = simple_teximport.simple_texi(
    list_of_def_path,
    column_names,
    gene_id_index,
    count_column_index,
    abundance_column_index,
    length_column_index
)

# Access the dataframes
count_df = txi.count
abundance_df = txi.abundance
length_df = txi.length

# Print a brief summary of the class
print(txi)
```

## Class Attributes

After creating an instance of `simple_texi`, it will convert the data into a class that stores three DataFrames, accessible via:
- `txi.count`
- `txi.abundance`
- `txi.length`

To print a brief summary of the class, use `print(txi)`.

---
