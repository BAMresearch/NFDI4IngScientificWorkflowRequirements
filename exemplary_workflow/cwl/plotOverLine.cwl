#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool

doc: Create plot-over-line data with paraview`s pvbatch

baseCommand: [python]

arguments: [ $(inputs.script), $(inputs.vtu0_file.path), plotoverline.csv ]

hints:
  SoftwareRequirement:
   packages:
     vtk:
       version: [ "9.3" ]
       specs:
         - https://anaconda.org/conda-forge/vtk
         - https://bio.tools/vtk

requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
      listing:
        - $(inputs.xdmf_file)
        - $(inputs.h5_file)
        - $(inputs.vtu_file)
        - $(inputs.vtu0_file)

inputs:
  script:
    type: File
    default:
      class: File
      location: ../source/postprocessing.py
  xdmf_file:
    type: File
  h5_file:
    type: File
  vtu_file:
    type: File
  vtu0_file:
    type: File

outputs:
  resultcsv:
    type: File
    format: https://www.iana.org/assignments/media-types/text/csv
    outputBinding:
      glob: plotoverline.csv
