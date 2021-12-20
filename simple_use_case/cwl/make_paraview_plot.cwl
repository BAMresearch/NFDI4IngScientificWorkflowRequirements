#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  Create rendering from vtk file using pvbatch
hints:
  DockerRequirement:
    dockerPull: wftools-simpleusecase
baseCommand: ["pvbatch"]
arguments: ["$(inputs.script)", "$(inputs.pvdfile.path)", "$(inputs.outputfile)"]
requirements:
  InitialWorkDirRequirement:
      listing:
        - $(inputs.vtkfile)
        - $(inputs.pvdfile)
inputs:
  script:
    type: File
  vtkfile:
    type: File
  pvdfile:
    type: File
  outputfile:
    type: string
outputs:
  resultimage:
    type: File
    outputBinding:
      glob: $(inputs.outputfile)
