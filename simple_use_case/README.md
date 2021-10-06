A simple use case
=================
This use case is meant as a minimal working example representative of workflows in computational science.
We plan to implement it in several workflow tools to compare them.
The workflow consists of the following processes:
* partition of the computational domain using `Gmsh`,
* conversion of the file format (into one readable by `dolfin`) using `meshio`,
* solution of the poisson equation using `fenics`,
* postprocessing using `ParaView`,
* and finally generation of a PDF using `Latex`.

Compute environment
-------------------
The compute environment may be re-instantiated by using [Conda](https://docs.conda.io/projects/conda/en/latest/) and
the file `conda_env.yml` containing all packages and their versions.
```
conda env create --file conda_env.yml --name <env> --prefix <your-prefix>
```
The file `conda_info.txt` provides additinoal information about the `conda` version used.

TODO
----
* other ways of providing the compute environment?
* installation of `Paraview` and `Latex` currently not covered by conda environment
