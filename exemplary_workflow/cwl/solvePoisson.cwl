#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool

doc: Run the poisson solver in dolfin

baseCommand: python3

arguments:
 - $(inputs.script)
 - --mesh
 - $(inputs.xdmfmeshfile.path)
 - --degree
 - "2"
 - --output
 - poisson.xdmf

stdout: output.txt

hints:
  SoftwareRequirement:
   packages:
     fenics-dolfinx:
       version: [ 0.9.* ]
       specs:
         - https://anaconda.org/conda-forge/fenics-dolfinx
         - https://bio.tools/fenics-dolfinx

requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
      listing:
        - $(inputs.xdmfmeshfile)
        - $(inputs.h5meshfile)

inputs:
  script:
    type: File
    default:
      class: File
      location: ../source/poisson.py
  xdmfmeshfile:
    type: File
  h5meshfile:
    type: File

outputs:
  poisson_xdmf:
    type: File
    outputBinding:
      glob: poisson.xdmf  
  poisson_h5:
    type: File
    outputBinding:
      glob: poisson.h5  
  poisson_vtu:
    type: File
    outputBinding:
      glob: poisson.vtu  
  poisson_vtu0:
    type: File
    outputBinding:
      glob: poisson_p0_000000.vtu
  num_dofs:
    type: float
    outputBinding:
      glob: output.txt
      loadContents: true
      outputEval: |
        ${
            var output = self[0].contents;
            var dofs_string = output.split("Number of dofs used:")[1];
            dofs_string = dofs_string.split("\n")[0];
            return parseFloat(dofs_string);
        }
