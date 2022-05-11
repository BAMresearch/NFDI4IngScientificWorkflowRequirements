#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: Create plot-over-line data with paraview`s pvbatch
baseCommand: [pvbatch]
arguments: ["$(inputs.script)", "$(inputs.pvdfile.path)", "plotoverline.csv"]

hints:
  SoftwareRequirement:
   packages:
     paraview:
       version: [ 5.9.1=hfc1cbd4_3_egl, 5.9.1 ]
       specs:
         - https://anaconda.org/conda-forge/paraview
         - https://identifiers.org/rrid/RRID:SCR_002516
         - https://bio.tools/paraview

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
