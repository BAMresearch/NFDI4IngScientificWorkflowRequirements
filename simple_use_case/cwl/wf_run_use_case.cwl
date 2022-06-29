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
  resultvtu:
    type: File
    outputSource: run_simulation/resultvtu

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

  run_simulation:
    run: run_dolfin.cwl
    in:
      xdmfmeshfile: convert_mesh/outputmesh
      h5meshfile: convert_mesh/outputmeshdata
    out: [resultvtu, resultpvd, num_dofs]

  plot_over_line:
    run: make_paraview_plot.cwl
    in:
      vtkfile: run_simulation/resultvtu
      pvdfile: run_simulation/resultpvd
    out: [resultcsv]

  prepare_paper_macros:
    run: prepare_paper_macros.cwl
    in:
      num_dofs: run_simulation/num_dofs
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
