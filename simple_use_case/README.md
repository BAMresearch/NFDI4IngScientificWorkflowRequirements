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
