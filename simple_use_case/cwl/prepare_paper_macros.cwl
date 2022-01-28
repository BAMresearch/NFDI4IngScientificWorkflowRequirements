#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  Update the macros of the paper with values from this run
baseCommand: ["python3"]
arguments: ["$(inputs.substitution_script)", "--domain-size", "$(inputs.domain_size)"]
requirements:
  InitialWorkDirRequirement:
      listing:
        - $(inputs.substitution_script)
        - $(inputs.macros_template)
inputs:
  domain_size:
    type: float
  substitution_script:
    type: File
    default:
      class: File
      location: ../source/prepare_paper_macros.py
  macros_template:
    type: File
    default:
      class: File
      location: ../source/macros.tex.template
outputs:
  macros_file:
    type: File
    outputBinding:
      glob: ["macros.tex"]
