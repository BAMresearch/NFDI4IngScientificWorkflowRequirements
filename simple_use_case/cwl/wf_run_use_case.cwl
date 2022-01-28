#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

outputs:
  paperpdf:
    type: File
    outputSource: compile_paper/pdf

inputs:
  geometryfile:
    type: File
    default:
      class: File
      location: ../source/unit_square.geo

steps:

  make_mesh:
    run: make_gmsh_mesh.cwl
    in:
      geofile: geometryfile
    out: [mesh, domain_size]

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
      domainsize: make_mesh/domain_size
    out: [resultvtu, resultpvd]

  plot_over_line:
    run: make_paraview_plot.cwl
    in:
      vtkfile: run_simulation/resultvtu
      pvdfile: run_simulation/resultpvd
    out: [resultcsv]

  prepare_paper_macros:
    run: prepare_paper_macros.cwl
    in:
      domain_size: make_mesh/domain_size
    out: [macros_file]

  compile_paper:
    run: compile_paper.cwl
    in:
      csvfile: plot_over_line/resultcsv
      macros: prepare_paper_macros/macros_file
    out: [pdf]
