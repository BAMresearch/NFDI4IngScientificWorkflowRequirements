# Maestrowf
Implementation of the exemplary workflow with [maestrowf](https://github.com/LLNL/maestrowf).

## Installation
`maestrowf` itself can be installed via pip. It does not deploy the software stack for you, so
installing all required software first is required. You can do so by running the following commands.
```sh
conda env create --file ../source/envs/default_env.yml --prefix ./exemplarywf
conda activate exemplarywf
pip install maestrowf
```

## Running the simple use case
```sh
maestro run exemplarywf.yaml -o ./output
```
It is recommended to specify the workspace with the `-o` option.
