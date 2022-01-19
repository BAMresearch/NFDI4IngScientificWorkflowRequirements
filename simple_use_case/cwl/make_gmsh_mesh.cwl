#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  mesh generation with gmsh
baseCommand: ["gmsh"]
arguments: ["-2", "$(inputs.geofile.path)", "-o", "$(inputs.outfilename)"]
inputs:
  geofile:
    type: File
    doc: "Geometry file in a gmsh-readable format"
  outfilename:
    type: string
    doc: "The name of the mesh file to be written, including the desired extension"
outputs:
  mesh:
    type: File
    outputBinding:
      glob: $(inputs.outfilename)
