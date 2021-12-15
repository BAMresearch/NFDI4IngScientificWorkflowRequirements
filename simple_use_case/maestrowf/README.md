# Maestrowf
Implementation of the simple use case with [maestrowf](https://github.com/LLNL/maestrowf).

## Installation
`maestrowf` itself can be installed via pip. It does not deploy the software stack for you, so
installing all required software first is required. You can do so by running the following commands.
```sh
conda env create --file ../source/envs/default_env.yml --prefix ./simpleusecase
conda activate simpleusecase
pip install maestrowf
```

## Running the simple use case
```sh
maestro run simpleusecase.yaml
```
