# gentree_builder

## Background
These scripts communicate with the ENSEMBL API to pull gene trees using a list of species names

## Input file format
Strongylocentrotus purpuratus
Daphnia pulex
Octopus bimaculoides
Lingula anatina
Aplysia californica
Crassostrea gigas
Nematostella vectensis
Clytia hemisphaerica
Mnemiopsis leidyi
Amphimedon queenslandica

## Usage
```
biomart_url = "https://www.ensembl.org/biomart/martservice"

Anole specific to generalizable with metadata support:

obgca001194135v2rs_eg_gene - Octopus bimaculoides (California two-spot octopus, UCB-OBI-ISO-001) genes (ASM119413v2)
mscalaris_eg_gene - Megaselia scalaris (Coffin fly) genes (Msca1)

Moved Ciona savignyi to ensembl species list
__________________________________________________________
ensembl_dataset_finder.py
__________________________________________________________

# With a file containing species names (one per line)
python ensembl_dataset_finder.py species_list.txt

# Interactive mode
python ensembl_dataset_finder.py --interactive

# Specify output filename
python ensembl_dataset_finder.py species_list.txt --output my_results.csv

__________________________________________________________

fetch_ensembl_genes.py
__________________________________________________________

# For standard Ensembl
python fetch_ensembl_genes.py species_list.txt

# For Ensembl Metazoa
python fetch_ensembl_genes.py species_list.txt --metazoa

# To list available datasets (helpful for troubleshooting)
python fetch_ensembl_genes.py --list --metazoa

# Interactive mode
python fetch_ensembl_genes.py --interactive --metazoa

__________________________________________________________
gene_tree_fetcher.py
__________________________________________________________
Basic usage:

python ensembl_gene_tree.py species_list.txt

To force a specific API (bypassing auto-detection):

python ensembl_gene_tree.py species_list.txt --force Metazoa
```

```
#!/bin/bash

#SBATCH --job-name=TREES     # Set the job name
#SBATCH --nodes 1
#SBATCH --tasks-per-node 1
#SBATCH --cpus-per-task 1
#SBATCH --mem 64gb
#SBATCH --time 72:00:00

cd /scratch/ffeltus/emily_ensembl_20250522/trees 
python ensembl_gene_tree.py species_ensembl-metazoa.txt 
```
