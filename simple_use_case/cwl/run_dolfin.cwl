#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  Run the poisson solver in dolfin
baseCommand: ["python3"]
arguments: ["$(inputs.script)", "--domain-size", "$(inputs.domainsize)",
                                "--mesh", "$(inputs.xdmfmeshfile.path)",
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
    default:
      class: File
      location: ../source/poisson.py
  xdmfmeshfile:
    type: File
  h5meshfile:
    type: File
  domainsize:
    type: float
outputs:
  resultvtu:
    type: File
    outputBinding:
      glob: ["result000000.vtu"]
  resultpvd:
    type: File
    outputBinding:
      glob: ["result.pvd"]
