;; Variables
define domain-size 1


;; Define workflow process templates
process make-gmsh-mesh (with geofile domain-size)
  synopsis "Generate the computational mesh with gmsh"
  packages "gmsh"
  inputs geofile: geofile
  outputs mesh: "mesh.msh"
  # { gmsh -setnumber domainsize {{domain-size}} -2 {{inputs}} -o {{outputs}} }


process convert-msh-to-xdmf (with inputmesh)
  synopsis "Convert the produced gmsh mesh to xdmf"
  packages "python" "python-meshio"
  inputs inputmesh: inputmesh
  outputs
    . xdmf: : file (basename inputmesh ".msh") "_converted.xdmf"
    . h5: : file (basename inputmesh ".msh") "_converted.h5"
  # { meshio convert {{inputs}} {{outputs:xdmf}} }


process run-dolfin (with xdmfmeshfile h5meshfile)
  synopsis "Run the poisson solver in dolfin"
  packages "python" "fenics" "pkg-config" "python-pkgconfig" "openmpi"
    . "openssh" "gcc-toolchain"
  inputs script: "source/poisson.py" xdmf: xdmfmeshfile h5: h5meshfile
  outputs pvd: "result.pvd" vtu: "result000000.vtu" num-dof: "num-dof"
  # {
    python3 {{inputs:script}} --mesh {{inputs:xdmf}} --degree 2 \
            --output {{outputs:pvd}} --num-dofs {{outputs:num-dof}}
  }


process make-paraview-plot (with pvd vtu)
  synopsis "Create plot-over-line data with paraview's pvbatch"
  packages "paraview"
  inputs script: "source/postprocessing.py" pvd: pvd vtu: vtu
  outputs csv: "plotoverline.csv"
  # { pvbatch {{inputs:script}} {{inputs:pvd}} {{outputs:csv}} }


process prepare-paper-macros (with domain-size num_dofs plot_data_file)
  synopsis "Update the macros of the paper with values from this run"
  packages "python"
  inputs substitution_script: "source/prepare_paper_macros.py"
    . macros_template: "source/macros.tex.template" num_dofs: num_dofs
    . plot_data_file: plot_data_file
  outputs macros_file: "macros.tex"
  # bash {
    python3 {{inputs:substitution_script}} \
            --domain-size {{domain-size}} \
            --macro-template-file {{inputs:macros_template}} \
            --num-dofs $(<{{inputs:num_dofs}}) \
            --plot-data-path {{inputs:plot_data_file}} \
            --output-macro-file {{outputs:macros_file}}
  }

process compile-paper (with macros csvfile)
  synopsis "Create the paper as pdf, given the produced csv file"
  packages "tectonic" "coreutils"
  inputs macros: macros csvfile: csvfile texfile: "source/paper.tex"
  outputs "paper.pdf"
  # { cp {{inputs:texfile}} paper.tex; tectonic paper.tex }


;; Define workflow process

;; Workflow process templates are invoked with parameters. These are either
;; variables (see make-mesh) or some outputs picked from other workflow
;; processes. For example, convert-mesh picks the mesh output from the make-mesh
;; process.
define make-mesh
  make-gmsh-mesh "source/unit_square.geo" domain-size


define convert-mesh
  convert-msh-to-xdmf
    pick mesh: : process-outputs make-mesh with-tags:


define run-simulation
  run-dolfin
    pick xdmf: : process-outputs convert-mesh with-tags:
    pick h5: : process-outputs convert-mesh with-tags:


define plot-over-line
  make-paraview-plot
    pick pvd: : process-outputs run-simulation with-tags:
    pick vtu: : process-outputs run-simulation with-tags:


define paper-macros
  prepare-paper-macros domain-size
    pick num-dof: : process-outputs run-simulation with-tags:
    pick csv: : process-outputs plot-over-line with-tags:


define paper
  compile-paper
    pick macros_file: : process-outputs paper-macros with-tags:
    pick csv: : process-outputs plot-over-line with-tags:


;; Define exemplary workflow by auto-connecting processes.
workflow exemplary-wf
  processes
    auto-connect make-mesh convert-mesh run-simulation plot-over-line
      . paper-macros paper
