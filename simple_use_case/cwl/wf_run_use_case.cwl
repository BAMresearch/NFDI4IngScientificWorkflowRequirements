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
    outputSource: render_image/resultimage
  paperpdf:
    type: File
    outputSource: compile_paper/pdf

inputs:
  geometryfile: File
  dolfinscript: File
  pvbatchscript: File
  papersource: File

steps:

  make_mesh:
    run: make_gmsh_mesh.cwl
    in:
      dimension:
        default: 2
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

  render_image:
    run: make_paraview_rendering.cwl
    in:
      script: pvbatchscript
      vtkfile: run_simulation/resultvtu
      pvdfile: run_simulation/resultpvd
      outputfile:
        default: "contourplot.png"
    out: [resultimage]

  compile_paper:
    run: compile_paper.cwl
    in:
      pngfile: render_image/resultimage
      texfile: papersource
    out: [pdf]
