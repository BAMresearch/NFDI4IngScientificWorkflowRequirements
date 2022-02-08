# Snakemake
This directory contains an implementation of the simple use case with [Snakemake](https://snakemake.github.io/).

## Installation
For more detailed information we refer to the official [documentation](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html).
The recommended way of installing snakemake is via conda, because it also enables Snakemake
to handle software dependencies of your workflow.
In the documentation the use of the [Mambaforge](https://github.com/conda-forge/miniforge#mambaforge) Python 3 distribution (Mambaforge is a Conda based distribution like [Miniconda](https://docs.conda.io/en/latest/miniconda.html), which however uses [Mamba](https://github.com/mamba-org/mamba) a fast and more robust replacement for the Conda package manager) is recommended.
If you don't have the Mamba command because you used a different conda distribution than Mambaforge, you can also first install Mamba in your base environment with
```sh
conda install -n base -c conda-forge mamba
```
You can then install snakemake with
```sh
mamba env create -c conda-forge -c bioconda -n snakemake snakemake
```
If you don't want to use Mamba, install snakemake with the usual command
```sh
conda env create -c conda-forge -c bioconda -n snakemake snakemake
```

## Running the simple use case
The workflow can be run with
```sh
snakemake --cores 1 --use-conda ./paper.pdf
```
with Mamba as the default conda frontend.
If you don't want to use Mamba, you need to specify conda as the frontend for installing environments with
```sh
snakemake --cores 1 --use-conda --conda-frontend conda ./paper.pdf
```
