#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  Generate the computational mesh with gmsh
baseCommand: ["gmsh"]
arguments: ["-2", "$(inputs.geofile.path)", "-o", "mesh.msh"]
stdout: output.txt
requirements:
  InlineJavascriptRequirement: {}
inputs:
  geofile:
    type: File
    doc: "Geometry file in a gmsh-readable format"
outputs:
  mesh:
    type: File
    outputBinding:
      glob: "mesh.msh"
  domain_size:
    type: float
    outputBinding:
      glob: "output.txt"
      loadContents: true
      outputEval: |
        ${
            var output = self[0].contents;
            var size_string = output.split("Used domain size:")[1];
            size_string = size_string.split("Used mesh size")[0];
            return parseFloat(size_string);
        }
