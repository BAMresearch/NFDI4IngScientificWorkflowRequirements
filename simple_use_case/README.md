Simple use case
=================
This simple use case is regarded as a minimal working example representative of workflows in computational science.
The (directed acyclic graph of the) workflow is shown below and consists of the following processes:

1. Partition of the computational domain using [Gmsh](http://gmsh.info/),
2. Conversion of the file format (into one readable by `FEniCS`) using [meshio](https://github.com/nschloe/meshio),
3. Solution of the poisson equation using [FEniCS](https://fenicsproject.org/),
4. Postprocessing using [ParaView](https://www.paraview.org/),
5. Generation of a PDF using [LaTeX](https://www.latex-project.org/).

