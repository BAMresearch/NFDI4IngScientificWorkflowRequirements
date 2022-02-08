#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  Generate the computational mesh with gmsh
baseCommand: ["gmsh"]
arguments: ["-setnumber", "domain_size", "$(inputs.domain_size)",
            "-2", "$(inputs.geofile.path)",
            "-o", "mesh.msh"]
inputs:
  geofile:
    type: File
    doc: "Geometry file in a gmsh-readable format"
    default:
      class: File
      location: ../source/unit_square.geo
  domain_size:
    type: float
    doc: "Specify the size of the domain to be meshed"
outputs:
  mesh:
    type: File
    outputBinding:
      glob: "mesh.msh"
