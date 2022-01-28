#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  Create the paper as pdf, given the produced csv file
baseCommand: ["python3"]
arguments: ["$(inputs.compilation_script)", "--domain-size", "$(inputs.domain_size)"]
requirements:
  InitialWorkDirRequirement:
      listing:
        - $(inputs.csvfile)
        - $(inputs.compilation_script)
        - $(inputs.paper_template)
inputs:
  csvfile:
    type: File
  domain_size:
    type: float
  paper_template:
    type: File
    default:
      class: File
      location: ../source/paper.tex.template
  compilation_script:
    type: File
    default:
      class: File
      location: ../source/compile_paper.py
outputs:
  pdf:
    type: File
    outputBinding:
      glob: ["*.pdf"]
