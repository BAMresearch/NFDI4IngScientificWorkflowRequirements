#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  mesh generation with gmsh
baseCommand: ["gmsh"]
arguments: ["-$(inputs.dimension)", "$(inputs.geofile.path)", "-o", "$(inputs.outfilename)"]
inputs:
  geofile:
    type: File
    doc: "Geometry file in a gmsh-readable format"
  outfilename:
    type: string
    doc: "The name of the mesh file to be written, including the desired extension"
  dimension:
    type: int
    doc: "The desired dimension of the mesh"
outputs:
  mesh:
    type: File
    outputBinding:
      glob: $(inputs.outfilename)
