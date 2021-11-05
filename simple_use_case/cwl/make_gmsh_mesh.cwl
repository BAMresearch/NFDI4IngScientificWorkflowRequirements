#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  mesh generation with gmsh
hints:
  DockerRequirement:
    dockerPull: simpleusecase
baseCommand: ["gmsh"]
arguments: ["-$(inputs.dimension)", "$(inputs.geofile.path)", "-o", "$(inputs.outfilename)"]
inputs:
  geofile:
    type: File
  outfilename:
    type: string
  dimension:
    type: int
outputs:
  mesh:
    type: File
    outputBinding:
      glob: $(inputs.outfilename)
