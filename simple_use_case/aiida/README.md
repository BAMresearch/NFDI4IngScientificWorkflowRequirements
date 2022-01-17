# AiiDA
This directory contains an implementation of the simple use case with [AiiDA](https://www.aiida.net/).

## Implementation
Since the implementation of workflows in AiiDA is quite different from the other file
based workflow managers (like e.g. snakemake or nextflow), we briefly comment on the different options
and design choices in AiiDA.

### Calculation functions
According to the [documentation](https://aiida.readthedocs.io/projects/aiida-core/en/latest/topics/calculations/concepts.html#calculation-functions): 
> The calcfunction in AiiDA is a function decorator that transforms a regular python function in a calculation process, which automatically stores the provenance of its output in the provenance graph when executed.

Typically `calcfunction`s are used for short running processes to be run on the local machine, like preprocessing and postprocessing steps.
One could think of a workaround, using `os.subprocess` inside a `calcfunction` to run the processes of the simple use case.
However, `calcfunction`s are not intended to be used to run external codes and the use of `os.subprocess` is discouraged since in this case the provenance cannot be properly captured by AiiDA.    

### Calculation jobs
> ... not all computations are well suited to be implemented as a python function, but rather are implemented as a separate code, external to AiiDA. To interface an external code with the engine of AiiDA, the CalcJob process class was introduced

The `CalcJob` is designed to run a `Code` on *any* computer through AiiDA. 
While this is very powerful, apart from installing the `Code` on the other computer it is necessary to setup the `code` with AiiDA and [write a plugin](https://aiida.readthedocs.io/projects/aiida-core/en/latest/howto/plugin_codes.html) which instructs AiiDA how to run the external `Code`.
For long running processes (computationally expensive tasks) this is worth the while, but for simple
shell commands the effort is too high.

### Shell functions
The `shellfunction` was introduced in December 2021 to easily run shell commands through AiiDA.
For more information see the associated [AiiDA Enhancement Proposal](https://github.com/aiidateam/AEP/tree/aep/shell-functions/xxx_shell_functions).

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
However, in the implementation of the simple use case we make use of the `shellfunction` which
makes it possible to easily run shell commands through `AiiDA` (without the need to write a plugin).
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
