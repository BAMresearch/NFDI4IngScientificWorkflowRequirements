
.. _simpleusecase:

Simple use case
===============
This simple use case is regarded as a minimal working example representative of workflows in computational science.
The (directed acyclic graph of the) workflow is shown below and consists of the following processes:

1. Partition of the computational domain using `Gmsh <http://gmsh.info/>`_,
2. Conversion of the file format (into one readable by `FEniCS`) using `meshio <https://github.com/nschloe/meshio>`_,
3. Solution of the poisson equation using `FEniCS <https://fenicsproject.org/>`_,
4. Postprocessing using `ParaView <https://www.paraview.org/>`_,
5. Generation of a PDF using `LaTex <https://www.latex-project.org/>`_.

.. image:: ./../img/g1948.png
  :width: 500
  :alt: TODO: caption

Details on the specific versions used for each software package can be found in the `conda environment specification file <https://github.com/BAMresearch/NFDI4IngScientificWorkflowRequirements/blob/main/simple_use_case/source/envs/default_env.yaml>`_.
