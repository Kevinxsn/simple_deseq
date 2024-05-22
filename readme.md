Here is simple_deseq & simple_teximport

## Introduction of simple_teximprt and simpel_deseq:

Deseq and tximport is are two popular bioinformatics package worked with R. They can be used in the analysis of RNA-sequencing (RNA-seq) data, which is crucial for understanding gene expression differences across different biological samples. 

However, there is a problem with this two tools. Since they are the packages only caompatible with R, that means if some are using some other programming package pipeline such as python, they


## simple_teximport

simple_texi in simple_teximport takes two arguments, the list of path that gene result has, and the list of column names that given to each of the dataframe. 

It will create three dataframe, abundance, counts and length. 

Can be accssed by .dataframe, .abundance, .length


