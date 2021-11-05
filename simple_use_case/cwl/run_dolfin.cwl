#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  poisson solver with dolfin
hints:
  DockerRequirement:
    dockerPull: simpleusecase
baseCommand: ["python3"]
arguments: ["$(inputs.script)", "--mesh", "$(inputs.xdmfmeshfile.path)",
                                "--degree", "2",
                                "--output", "result.pvd"]
requirements:
  InitialWorkDirRequirement:
      listing:
        - $(inputs.xdmfmeshfile)
        - $(inputs.h5meshfile)
inputs:
  script:
    type: File
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
