#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  Create the paper as pdf, given the correct images
hints:
  DockerRequirement:
    dockerPull: wftools-simpleusecase
baseCommand: ["tectonic"]
arguments: ["$(inputs.texfile)"]
requirements:
  InitialWorkDirRequirement:
      listing:
        - $(inputs.csvfile)
        - $(inputs.texfile)
inputs:
  csvfile:
    type: File
  texfile:
    type: File
outputs:
  pdf:
    type: File
    outputBinding:
      glob: ["*.pdf"]
