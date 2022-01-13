# AiiDA
This directory contains an implementation of the simple use case with [AiiDA](https://www.aiida.net/).

## Installation
Please follow the instructions in the [documentation](https://aiida.readthedocs.io/projects/aiida-core/en/latest/)
to make yourself familiar with the installation process.
It is recommended to use the system-wide installation method, where you first install prerequisite
services using a package manager (e. g. on Ubuntu)
```sh
sudo apt install \
    git python3-dev python3-pip \
    postgresql postgresql-server-dev-all postgresql-client rabbitmq-server
```
and then install `aiida-core` using `pip+venv` or `conda`.
However, in the implementation of the simple use case we make use of the `shell_function` which
makes it possible to easily run shell commands through `AiiDA` (without the need to write a plugin).
For more information see the associated [AiiDA Enhancement Proposal](https://github.com/aiidateam/AEP/tree/aep/shell-functions/xxx_shell_functions).
This new feature is being developed at the time of writing and therefore we need to clone the repository,
checkout the respective branch and install `aiida-core` via `pip`.
Furthermore, the software packages to run the simple use case need to be installed as well.
We start by preparing a conda environment
```sh
conda env create --name aiida_simplecase --file ../source/envs/default_env.yaml
conda activate aiida_simplecase
```
and install `aiida-core` in it with
```sh
git clone https://github.com/sphuber/aiida-core.git 
cd aiida-core
git checkout feature/5287/shell-function
pip install -e .
```
The installation is completed with running
```sh
reentry scan
```
and setting up a profile with
```sh
verdi quicksetup
```
Finally, you can check your setup with
```sh
verdi status
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
