# gentree_builder

## Background
These scripts communicate with the EMSEMBL API to pull gene trees using a list of species names

## Input file format

## Usage
```
#!/bin/bash

#SBATCH --job-name=TREES     # Set the job name
#SBATCH --nodes 1
#SBATCH --tasks-per-node 1
#SBATCH --cpus-per-task 1
#SBATCH --mem 64gb
#SBATCH --time 72:00:00

cd /scratch/ffeltus/emily_ensembl_20250522/trees 
python ensembl_gene_tree_v0-6.py species_ensembl-metazoa.txt 
```
