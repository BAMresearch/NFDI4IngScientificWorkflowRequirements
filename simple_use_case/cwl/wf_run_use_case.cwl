#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

outputs:
  mesh:
    type: File
    outputSource: make_mesh/mesh
  resultvtu:
    type: File
    outputSource: run_simulation/resultvtu
  resultpvd:
    type: File
    outputSource: run_simulation/resultpvd
  resultimage:
    type: File
    outputSource: plot_over_line/resultcsv
  paperpdf:
    type: File
    outputSource: compile_paper/pdf

inputs:
  geometryfile:
    type: File
    default:
      class: File
      location: ../source/unit_square.geo
  dolfinscript:
    type: File
    default:
      class: File
      location: ../source/poisson.py
  pvbatchscript:
    type: File
    default:
      class: File
      location: ../source/postprocessing.py

steps:

  make_mesh:
    run: make_gmsh_mesh.cwl
    in:
      geofile: geometryfile
      outfilename:
        default: "unit_square.msh"
    out: [mesh]

  convert_mesh:
    run: convert_msh_to_xdmf.cwl
    in:
      inputmesh: make_mesh/mesh
      outfilename:
        default: "unit_square"
    out: [outputmesh, outputmeshdata]

  run_simulation:
    run: run_dolfin.cwl
    in:
      script: dolfinscript
      xdmfmeshfile: convert_mesh/outputmesh
      h5meshfile: convert_mesh/outputmeshdata
    out: [resultvtu, resultpvd]

  plot_over_line:
    run: make_paraview_plot.cwl
    in:
      script: pvbatchscript
      vtkfile: run_simulation/resultvtu
      pvdfile: run_simulation/resultpvd
      outputfile:
        default: "plotoverline.csv"
    out: [resultcsv]

  compile_paper:
    run: compile_paper.cwl
    in:
      csvfile: plot_over_line/resultcsv
    out: [pdf]
