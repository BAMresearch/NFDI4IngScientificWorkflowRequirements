# AiiDA
This directory contains an implementation of the simple use case with [AiiDA](https://www.aiida.net/).

## Installation
To install `AiiDA` please follow the instructions in the [documentation](https://aiida.readthedocs.io/projects/aiida-core/en/latest/).
It is recommended to use the system-wide installation method, where you first install prerequisite
services using a package manager and then install `aiida-core` using `pip+venv` or `conda`.
Using `conda` it is easy to also install all other packages needed to run the simple use case.
```sh
conda env create --name aiida_simplecase --file ../source/envs/default_env.yaml
conda install --name aiida_simplecase --channel conda-forge aiida-core
```

## Running the simple use case
If you are using `conda`, activate your environment.
```
conda activate aiida_simplecase
```
Then run the workflow with
```
verdi run simple_use_case.py
```
Useful commands:
```
verdi process list -a           # lists all processes
verdi process show <PK>         # show info about process
verdi process report <PK>       # log messages if something went wrong
verdi node show <PK>            # show info about node
verdi node graph generate <PK>  # generate provenance graph for node
```
