#!/usr/bin/env nextflow

params.domainSize = 1.0

// for now simply add dependent files as Channels
geofile = Channel.fromPath("$PWD/../source/unit_square.geo")
fenics_code = Channel.fromPath("$PWD/../source/poisson.py")
paraview_script = Channel.fromPath("$PWD/../source/postprocessing.py")
macro_template = Channel.fromPath("$PWD/../source/macros.tex.template")
prepare_macros = Channel.fromPath("$PWD/../source/prepare_paper_macros.py")
paper_source = Channel.fromPath("$PWD/../source/paper.tex")


process generateMesh {
    // generate mesh using Gmsh

    // use conda directive to specify environment file
    conda "../source/envs/preprocessing.yaml"

    input:
    file geofile

    output:
    file "unit_square.msh" into mesh_msh

    """
    gmsh -2 -setnumber domain_size ${params.domainSize} $geofile -o unit_square.msh
    """
}


process convertToXDMF {
    // convert .msh file to .xdmf

    conda "../source/envs/preprocessing.yaml"

    input:
    file mesh from mesh_msh

    output:
    file "unit_square.h5" into mesh_h5
    file "unit_square.xdmf" into mesh_xdmf

    """
    meshio convert $mesh unit_square.xdmf
    """
}


process solvePoisson {
    // solve poisson equation using fenics

    conda "../source/envs/processing.yaml"

    // multiple inputs from different channels
    input:
    file fenics_code
    file meshdata from mesh_h5
    file mesh from mesh_xdmf

    output:
    file "poisson.pvd" into poisson_pvd
    file "poisson*.vtu" into poisson_vtu
    stdout poisson_stdout

    """
    python $fenics_code --mesh $mesh --degree 2 --outputfile poisson.pvd
    """
}


process readNumberOfDofs {
    input:
    val x from poisson_stdout

    output:
    stdout number_of_dofs

    """
    #!/usr/bin/python3
    s = '''${x.replaceAll("\\n", "&")}'''
    dof_string = s.split("Number of dofs used:")[1]
    num_dofs = dof_string.split("&")[0]
    print(int(num_dofs))
    """
}


process makePlotOverLine {

    conda "../source/envs/postprocessing.yaml"

    input:
    file paraview_script
    file vtu from poisson_vtu
    file pvd from poisson_pvd

    output: 
    file "plotoverline.csv" into plot_over_line

    """
    pvbatch $paraview_script $pvd plotoverline.csv
    """
}


process substituteMacros {
    // place the correct value into the paper macros

    conda "../source/envs/postprocessing.yaml"

    input:
    file prepare_macros
    file macro_template
    val number_of_dofs

    output:
    file "macros.tex" into macros

    """
    python $prepare_macros --macro-template-file $macro_template \
        --plot-data-path "./plotoverline.csv" \
        --domain-size ${params.domainSize} \
        --num-dofs ${number_of_dofs.replaceAll("\\s", "")} \
        --output-macro-file macros.tex
    """
}


process compilePaper {

    conda "../source/envs/postprocessing.yaml"
    publishDir "$PWD"

    input:
    file paper_source
    file plot_over_line
    file macros

    output:
    file "paper.pdf" 

    """
    tectonic $paper_source
    """
}
