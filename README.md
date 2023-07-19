# Clustering Significance Test

Permutation Test is a powerful Python program designed to assess the statistical significance of clustering patterns in phylogenetic trees. It provides researchers and scientists with a reliable tool to analyze and interpret the clustering of metadata annotations within the context of evolutionary relationships.

## Overview
Permutation Test program provides a reliable and efficient method to evaluate the clustering of different metadata annotations in a phylogenetic tree. It aims to determine whether the observed clustering is statistically significant or likely to have occurred by chance.

The program works by utilizing a permutation test methodology. It takes as input a phylogenetic tree file in Nexus format, which represents the evolutionary relationships among samples. Additionally, it can incorporate a metadata file in TSV format, containing annotations or characteristics of the samples.

The program calculates cluster purity, which measures the proportion of samples within clusters that share the same annotation. It then generates a null distribution by randomly permuting the metadata labels and compares the observed cluster purity to this null distribution.

By performing a large number of permutations, the program obtains a distribution of cluster purity values under the null hypothesis. It calculates a p-value, representing the probability of observing a cluster purity as extreme as or more extreme than the observed value. If the p-value is below a significance threshold (default: 0.05), the program concludes that the observed clustering is statistically significant.

The program offers several customizable parameters, including the indices of the columns containing tree labels and labels to test in the metadata file. It also allows users to adjust the significance level and the number of permutation replicates.

The output of the program includes cluster purity scores, statistical metrics (p-values), and significance levels. It provides researchers with valuable information to interpret and understand the clustering patterns in their phylogenetic trees.

For more detailed information, usage examples, and documentation, please refer to the Clustering Significance Test GitHub repository at [https://github.com/Yasas1994/Clustering-significance-test](https://github.com/Yasas1994/Clustering-significance-test).

## Dependencies
- pandas (v1.0.0 or later)
- numpy (v1.18.0 or later)
- treeswift (v1.0.0 or later)
- tqdm (v4.0.0 or later)
- seaborn (v0.10.0 or later)
- matplotlib (v3.0.0 or later)

## Usage

To use the Clustering Significance Test program, simply follow the provided command-line instructions:

```
python permutation_test.py -t <tree_file> <optional parameters>
python permutation_test.py -t <tree_file> -m <meta_file> -i1 <index_tree_labels> -i2 <index_test_labels> <other optional parameters>
```

### Mandatory Parameters

- `-t --tree <tree_file>`: Specifies the path to the tree file in Nexus format. The tree file represents the phylogenetic relationships between the samples.

### Optional Parameters

- `-i1 <integer>`: Index of the column in the metadata file that contains the labels corresponding to the tree (e.g., genus names). This parameter is mandatory if `-m` is specified.
- `-i2 <integer>`: Index of the column in the metadata file that contains the labels to test (e.g., random numbers). This parameter is mandatory if `-m` is specified.
- `-m --meta <tsv_file>`: Specifies the path to the metadata file in TSV (Tab-Separated Values) format. The metadata file should contain additional information about the samples in the tree, such as annotations or characteristics.
- `-o --out <string | path>`: Specifies the output directory path where the results and generated files will be saved. By default, the output directory is set to 'output_dir'.
- `-p --p_value <float>`: Specifies the significance level (p-value) for cluster selection. This value determines the threshold for determining whether a cluster is statistically significant. The default value is 0.05.
- `-r --replicates <integer>`: Specifies the number of permutation replicates to perform. Permutations are used to generate a null distribution for comparison. The default value is 10000.
- `-v`: Prints the version information of the program.
- `-h --help`: Displays the help message and usage instructions.

## License

This project is licensed under the [MIT License](https://github.com/Yasas1994/Clustering-significance-test/blob/main/LICENSE). Please review the license file for more details.

## Authors
- Bas E. Dutilh
- Yasas Wijesekara: [GitHub](https://github.com/Yasas1994)
- Giuliana Pola: [GitHub](https://github.com/GiulianaPola)