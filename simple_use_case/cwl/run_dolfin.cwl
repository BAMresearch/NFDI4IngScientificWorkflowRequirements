#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: Run the poisson solver in dolfin
baseCommand: python3
arguments: ["$(inputs.script)", "--mesh", "$(inputs.xdmfmeshfile.path)",
                                "--degree", "2",
                                "--output", "result.pvd"]
stdout: output.txt
hints:
  SoftwareRequirement:
   packages:
     fenics:
       version: [ 2019.1.0=py39hf3d152e_26, 2019.1.0 ]
       specs:
         - https://anaconda.org/conda-forge/fenics
         - https://bio.tools/fenics

requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
      listing:
        - $(inputs.xdmfmeshfile)
        - $(inputs.h5meshfile)
inputs:
  script:
    type: File
    default:
      class: File
      location: ../source/poisson.py
  xdmfmeshfile:
    type: File
  h5meshfile:
    type: File
outputs:
  resultvtu:
    type: File
    outputBinding:
      glob: ["result000000.vtu"]
  resultpvd:
    type: File
    outputBinding:
      glob: ["result.pvd"]
  num_dofs:
    type: float
    outputBinding:
      glob: "output.txt"
      loadContents: true
      outputEval: |
        ${
            var output = self[0].contents;
            var dofs_string = output.split("Number of dofs used:")[1];
            dofs_string = dofs_string.split("\n")[0];
            return parseFloat(dofs_string);
        }
