#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  Create rendering from vtk file using pvbatch
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
    default:
      class: File
      location: ../source/postprocessing.py
  vtkfile:
    type: File
  pvdfile:
    type: File
  outputfile:
    type: string
outputs:
  resultcsv:
    type: File
    outputBinding:
      glob: $(inputs.outputfile)
