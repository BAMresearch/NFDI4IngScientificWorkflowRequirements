#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

outputs:
  mesh:
    type: File
    outputSource: run_computations/mesh
  resultvtu:
    type: File
    outputSource: run_computations/resultvtu
  resultpvd:
    type: File
    outputSource: run_computations/resultpvd
  resultimage:
    type: File
    outputSource: run_computations/resultimage
  paperpdf:
    type: File
    outputSource: run_computations/paperpdf

requirements:
  - class: SubworkflowFeatureRequirement

inputs:
  dockerfile-url: string
  geometryfile: File
  dolfinscript: File
  pvbatchscript: File
  papersource: File

steps:

  build_image:
    run: wf_build_docker_image.cwl
    in:
      dockerfile-url: dockerfile-url
    out: [dockerid]

  run_computations:
    run: wf_computations.cwl
    in:
      geometryfile: geometryfile
      dolfinscript: dolfinscript
      pvbatchscript: pvbatchscript
      papersource: papersource
    out: [mesh, resultvtu, resultpvd, resultimage, paperpdf]
