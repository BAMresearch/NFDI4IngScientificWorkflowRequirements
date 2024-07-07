# pyiron
This directory contains an implementation of the exemplary workflow with [pyiron](https://pyiron.org/) or more specifically the [pyiron_base](https://pyiron-base.readthedocs.io) workflow manager.

## Installation
For more detailed information we refer to the official [documentation](https://pyiron-base.readthedocs.io/en/latest/installation.html).
The recommended way of installing `pyiron_base` is via conda, because it also enables `pyiron_base` to handle software dependencies of your workflow using the [conda_subprocess](https://github.com/pyiron/conda_subprocess) package.

You can then install `pyiron_base` with
```sh
mamba create -c conda-forge -n pyiron_base pyiron_base=0.9.6 conda_subprocess=0.0.4
```

## Running the exemplary workflow
The workflow can be run with
```sh
python workflow.py
```
The final output `paper.pdf` created using the `tectonic` package is then stored in the working direcrtory of last workflow step:
```sh
./workflow/tectonic_hdf5/tectonic/paper.pdf
```
This is a general feature of the `pyiron_base` workflow manager, each step of the workflow - called job - is executed in a separate working directory. 
