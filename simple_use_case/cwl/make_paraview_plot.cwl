#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  Create plot-over-line data with paraview`s pvbatch
baseCommand: ["pvbatch"]
arguments: ["$(inputs.script)", "$(inputs.pvdfile.path)", "plotoverline.csv"]
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
outputs:
  resultcsv:
    type: File
    outputBinding:
      glob: "plotoverline.csv"
