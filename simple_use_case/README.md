# Simple use case
As a minimal working example representative of workflows in computational science,
the poisson equation is solved using the finite element method.
The workflow consists of the following processes:

1. Partition of the computational domain using [Gmsh](http://gmsh.info/),
2. Conversion of the file format (into one readable by [FEniCS](https://fenicsproject.org/)) using [meshio](https://github.com/nschloe/meshio),
3. Solution of the poisson equation using [FEniCS](https://fenicsproject.org/),
4. Postprocessing using [ParaView](https://www.paraview.org/),
5. Preparation of macro definitions,
6. Generation of a PDF using [LaTeX](https://www.latex-project.org/), [Tectonic](https://tectonic-typesetting.github.io/en-US/) respectively.

A more extensive description can be found in the [documentation](https://nfdi4ingscientificworkflowrequirements.readthedocs.io/en/latest/docs/simpleusecase.html).

## Compute environment
Details about how the compute environment is built (using [conda](https://docs.conda.io/en/latest/)) can be found in the respective sub-directory for each tool.

## Headless operation
The ParaView version used in the examples (see the [conda environment specification file](https://github.com/BAMresearch/NFDI4IngScientificWorkflowRequirements/blob/main/simple_use_case/source/envs/default_env.yaml)) is linked against EGL to also support offscreen rendering.
Usually, these libraries exist in case of a desktop pc where an actual screen or monitor is available.
However, for headless operation, i.e. when executing the simple use case in a container, it is necessary to install aforementioned libraries since these are not installed automatically as a dependency by conda.
We refer to the installation of the basic dependencies in our [github action](https://github.com/BAMresearch/NFDI4IngScientificWorkflowRequirements/blob/main/.github/actions/install-basic-deps/action.yml) to give an example.
For more information about offscreen rendering with ParaView go to the [ParaView documentation](https://kitware.github.io/paraview-docs/latest/cxx/Offscreen.html).
