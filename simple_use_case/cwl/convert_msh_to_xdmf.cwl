#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  Convert gmsh mesh file format to xdmf
baseCommand: ["meshio", "convert"]
arguments: ["$(inputs.inputmesh.path)", "mesh_converted.xdmf"]
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
