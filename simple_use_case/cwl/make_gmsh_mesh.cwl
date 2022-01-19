#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  mesh generation with gmsh
baseCommand: ["gmsh"]
arguments: ["-2", "$(inputs.geofile.path)", "-o", "mesh.msh"]
inputs:
  geofile:
    type: File
    doc: "Geometry file in a gmsh-readable format"
outputs:
  mesh:
    type: File
    outputBinding:
      glob: "mesh.msh"
