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
Details about how the compute environment is built can be found in the respective sub-directory for each tool.