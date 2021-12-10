# Snakemake
This directory contains an implementation of the simple use case with [Snakemake](https://snakemake.github.io/).

## Installation
For more detailed information we refer to the official [documentation](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html).
The recommended way of installing snakemake is via conda, because it also enables Snakemake
to handle software dependencies of your workflow.
```
conda create -c conda-forge -c bioconda -n snakemake snakemake
```

## Running the simple use case
The workflow can be run with
```
snakemake --cores 1 --use-conda postprocessing/paper.pdf
```
