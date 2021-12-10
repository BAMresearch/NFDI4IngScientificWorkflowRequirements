# Pydoit
This directory contains an implementation of the simple use case with [pydoit](https://pydoit.org).

## Installation
Doit can be installed with `pip` or `conda`.
```
pip install doit=0.33.1
```
```
conda install --channel conda-forge doit=0.33.1
```
However, it does not handle the installation of the required software for you.
Here, we assume that all required software and `doit` are already installed.
For example you could do
```
conda env create --name doit_simplecase --file ../source/envs/conda_env_explicit.yaml
```
to create a conda environment with all required software and then install `doit` in the
same environment with
```
conda install --name doit_simplecase --channel conda-forge doit=0.33.1
```


## Running the simple use case
If you are using `conda`, activate your environment.
```
conda activate doit_simplecase
```
Then run the workflow with
```
doit
```
