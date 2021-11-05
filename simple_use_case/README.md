A simple use case
=================
This use case is meant as a minimal working example representative of workflows in computational science.
We plan to implement it in several workflow tools to compare them.
The workflow consists of the following processes:
* partition of the computational domain using `Gmsh` (version 4.6.0),
* conversion of the file format (into one readable by `dolfin`) using `meshio` (version 4.3.1),
* solution of the poisson equation using `fenics` (version 2019.1.0),
* postprocessing using `ParaView` (version 5.9.1),
* and finally generation of a PDF using `Latex` (version 3.141592653-2.6-1.40.23 (TeX Live 2021)) / `tectonic`.

Compute environment
-------------------
Details about how the compute environment is built can be found in the respective sub-directory for each tool.
