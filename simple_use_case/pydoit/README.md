# Pydoit
Some notes about [pydoit](https://pydoit.org).

## Compute environment
The compute environment may be re-instantiated by using [Conda](https://docs.conda.io/projects/conda/en/latest/) and
the file `conda_env.yaml` containing all packages and their versions.
```
conda env create --file conda_env.yaml --name <env> --prefix <your-prefix>
```
* I had to add `importlib_metadata` and `superlu_dist` explicitly because conda was not able to figure out the dependencies correctly (resulting in `ImportError` or `ModuleNotFoundError`)

## Documentation
* Task's meta-data are better described in a declarative way (i.e. CWL or DSL ...), but often you want to create this meta-data programmatically
* dependencies are on tasks, not on targets
* doit checks if *file_dep* was modified or not (by comparing the file content’s MD5) (+)

## Test case implementation
* knowledge of the python programming language (o)
* no direct integration of software packages; software deployment and execution environment are not controlled (-); However, doit is very flexible and tasks like checking whether conda is installed (and installing it if this is not the case) or building a docker container for the current (conda) environment could be implemented
