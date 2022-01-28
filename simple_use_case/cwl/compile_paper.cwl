#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  Create the paper as pdf, given the produced csv file
baseCommand: ["tectonic"]
arguments: ["$(inputs.texfile)"]
requirements:
  InitialWorkDirRequirement:
      listing:
        - $(inputs.csvfile)
        - $(inputs.texfile)
        - $(inputs.macros)
inputs:
  macros:
    type: File
  csvfile:
    type: File
  texfile:
    type: File
    default:
      class: File
      location: ../source/paper.tex
outputs:
  pdf:
    type: File
    outputBinding:
      glob: ["*.pdf"]
