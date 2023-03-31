# Pydoit
This directory contains an implementation of the exemplary workflow with [pydoit](https://pydoit.org).

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
conda env create --name doit_env --file ../source/envs/default_env.yaml
```
to create a conda environment with all required software and then install `doit` in the
same environment with
```
conda install --name doit_env --channel conda-forge doit=0.33.1
```


## Running the exemplary workflow
If you are using `conda`, activate your environment.
```
conda activate doit_env
```
Then run the workflow with
```
doit
```
