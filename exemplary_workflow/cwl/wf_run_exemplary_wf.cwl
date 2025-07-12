#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

outputs:
  paperpdf:
    type: File
    format: iana:application/pdf
    outputSource: compile_paper/pdf
  pol_data:
    type: File
    format: iana:text/csv
    outputSource: plot_over_line/resultcsv
  macros:
    type: File
    outputSource: prepare_paper_macros/macros_file
  resultvtu0:
    type: File
    outputSource: solvePoisson/poisson_vtu0

inputs:
  domain_size:
    type: float
    default: 1.0

steps:
  make_mesh:
    run: make_gmsh_mesh.cwl
    in:
      domain_size: domain_size
    out: [mesh]

  convert_mesh:
    run: convert_msh_to_xdmf.cwl
    in:
      inputmesh: make_mesh/mesh
    out: [outputmesh, outputmeshdata]

  solvePoisson:
    run: solvePoisson.cwl
    in:
      xdmfmeshfile: convert_mesh/outputmesh
      h5meshfile: convert_mesh/outputmeshdata
    out: [poisson_xdmf, poisson_h5, poisson_vtu, poisson_vtu0, num_dofs]

  plot_over_line:
    run: plotOverLine.cwl
    in:
      xdmf_file: solvePoisson/poisson_xdmf
      h5_file: solvePoisson/poisson_h5
      vtu_file: solvePoisson/poisson_vtu
      vtu0_file: solvePoisson/poisson_vtu0
    out: [resultcsv]

  prepare_paper_macros:
    run: prepare_paper_macros.cwl
    in:
      num_dofs: solvePoisson/num_dofs
      domain_size: domain_size
      plot_data_file: plot_over_line/resultcsv
    out: [macros_file]

  compile_paper:
    run: compile_paper.cwl
    in:
      csvfile: plot_over_line/resultcsv
      macros: prepare_paper_macros/macros_file
    out: [pdf]

$namespaces:
  iana: https://www.iana.org/assignments/media-types/
