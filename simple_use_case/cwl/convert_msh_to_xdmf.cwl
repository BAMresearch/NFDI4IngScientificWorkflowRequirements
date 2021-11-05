#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  Convert gmsh mesh file format to xdmf
baseCommand: ["meshio-convert"]
hints:
  DockerRequirement:
    dockerPull: simpleusecase
arguments: ["$(inputs.inputmesh.path)", "$(inputs.outfilename).xdmf"]
inputs:
  inputmesh:
    type: File
  outfilename:
    type: string
outputs:
  outputmesh:
    type: File
    outputBinding:
      glob: $(inputs.outfilename).xdmf
  outputmeshdata:
    type: File
    outputBinding:
       glob: $(inputs.outfilename).h5
