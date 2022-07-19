;; Variables
define domain-size 1


;; Define workflow process templates
process make-gmsh-mesh (with geofile domainsize)
  synopsis "Generate the computational mesh with gmsh"
  packages "gmsh"
  inputs
    . geofile: (file geofile)
  outputs
    . mesh: (file "mesh.msh")
  # { gmsh -setnumber domainsize {{domainsize}} -2 {{inputs}} -o {{outputs}} }


process convert-msh-to-xdmf (with inputmesh)
  synopsis "Convert the produced gmsh mesh to xdmf"
  packages "python" "python-meshio"
  inputs
    . inputmesh: (file inputmesh)
  outputs
    . xdmf: (file (basename inputmesh ".msh") "_converted.xdmf")
    . h5: (file (basename inputmesh ".msh") "_converted.h5")
  # { meshio convert {{inputs}} {{outputs:xdmf}} }


process run-dolfin (with xdmfmeshfile h5meshfile)
  synopsis "Run the poisson solver in dolfin"
  packages "python" "fenics" "pkg-config" "python-pkgconfig" "openmpi"
    . "openssh" "gcc-toolchain"
  inputs
    . script: (file "source/poisson.py")
    . xdmf: (file xdmfmeshfile)
    . h5: (file h5meshfile)
  outputs
    . pvd: (file "result.pvd")
    . vtu: (file "result000000.vtu")
    . num-dof: (file "num-dof")
  # {
    python3 {{inputs:script}} --mesh {{inputs:xdmf}} --degree 2 \
            --output {{outputs:pvd}} --num-dofs {{outputs:num-dof}}
  }


process make-paraview-plot (with pvd vtu)
  synopsis "Create plot-over-line data with paraview's pvbatch"
  packages "paraview"
  inputs
    . script: (file "source/postprocessing.py")
    . pvd: (file pvd)
    . vtu: (file vtu)
  outputs
    . csv: (file "plotoverline.csv")
  # { pvbatch {{inputs:script}} {{inputs:pvd}} {{outputs}} }


process prepare-paper-macros (with domain_size num_dofs plot_data_file)
  synopsis "Update the macros of the paper with values from this run"
  packages "python"
  inputs
    . substitution_script: (file "source/prepare_paper_macros.py")
    . macros_template: (file "source/macros.tex.template")
    . num_dofs: (file num_dofs)
    . plot_data_file: (file plot_data_file)
  outputs
    . macros_file: (file "macros.tex")
  # bash {
    python3 {{inputs:substitution_script}} \
            --domain-size {{domain_size}} \
            --macro-template-file {{inputs:macros_template}} \
            --num-dofs $(<{{inputs:num_dofs}}) \
            --plot-data-path {{inputs:plot_data_file}} \
            --output-macro-file {{outputs:macros_file}}
  }

process compile-paper (with macros csvfile)
  synopsis "Create the paper as pdf, given the produced csv file"
  packages "tectonic" "coreutils"
  inputs
    . macros: (file macros)
    . csvfile: (file csvfile)
    . texfile: (file "source/paper.tex")
  outputs
    . pdf: (file "paper.pdf")
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
    pick mesh: (process-outputs make-mesh with-tags:)


define run-simulation
  run-dolfin
    pick xdmf: (process-outputs convert-mesh with-tags:)
    pick h5: (process-outputs convert-mesh with-tags:)


define plot-over-line
  make-paraview-plot
    pick pvd: (process-outputs run-simulation with-tags:)
    pick vtu: (process-outputs run-simulation with-tags:)


define paper-macros
  prepare-paper-macros domain-size
    pick num-dof: (process-outputs run-simulation with-tags:)
    pick csv: (process-outputs plot-over-line with-tags:)


define paper
  compile-paper
    pick macros_file: (process-outputs paper-macros with-tags:)
    pick csv: (process-outputs plot-over-line with-tags:)


;; Define simple-use-case workflow by auto-connecting processes.
workflow simple-use-case
  processes
    auto-connect make-mesh convert-mesh run-simulation plot-over-line
      . paper-macros paper
