#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: Convert the produced gmsh mesh to xdmf

hints:
  SoftwareRequirement:
   packages:
     meshio:
       version: [ 5.0.5=pyhd8ed1ab_0, 5.0.5 ]
       specs:
         - https://anaconda.org/conda-forge/meshio
         - https://doi.org/10.5281/zenodo.1173115

baseCommand: [ meshio, convert]
arguments: [ $(inputs.inputmesh.path), mesh_converted.xdmf ]
inputs:
  inputmesh:
    type: File
outputs:
  outputmesh:
    type: File
    outputBinding:
      glob: "mesh_converted.xdmf"
  outputmeshdata:
    type: File
    outputBinding:
       glob: "mesh_converted.h5"
