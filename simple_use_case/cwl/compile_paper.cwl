#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: Create the paper as pdf, given the produced csv file
baseCommand: tectonic
arguments: [ $(inputs.texfile) ]
requirements:
  InitialWorkDirRequirement:
      listing:
        - $(inputs.csvfile)
        - $(inputs.texfile)
        - $(inputs.macros)
hints:
  SoftwareRequirement:
   packages:
     tectonic:
       version: [ 0.8.0=ha1fef3e_1, 0.8.0 ]
       specs: [ https://anaconda.org/conda-forge/tectonic ]
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
