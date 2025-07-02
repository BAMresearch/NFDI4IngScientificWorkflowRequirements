#!/usr/bin/env nextflow

nextflow.enable.dsl=2

workflow {
    params.domainSize = 1.0

    Channel
        .fromPath("$PWD/../source/unit_square.geo")
        .set { geofile }

    Channel
        .fromPath("$PWD/../source/poisson.py")
        .set { fenics_code }

    Channel
        .fromPath("$PWD/../source/postprocessing.py")
        .set { postprocessing_script }

    Channel
        .fromPath("$PWD/../source/macros.tex.template")
        .set { macro_template }

    Channel
        .fromPath("$PWD/../source/prepare_paper_macros.py")
        .set { prepare_macros }

    Channel
        .fromPath("$PWD/../source/paper.tex")
        .set { paper_source }

    // Generate mesh and convert
    generateMesh(geofile)

    convertToXDMF(generateMesh.out.mesh)

    solvePoisson(
        fenics_code, 
        convertToXDMF.out.mesh_xdmf,
        convertToXDMF.out.mesh_h5        )


    // Extract number of dofs from stdout
    readNumberOfDofs(
        solvePoisson.out.poisson_stdout)

    // Plot over line
    makePlotOverLine(
        postprocessing_script, 
        solvePoisson.out.poisson_xdmf,
        solvePoisson.out.poisson_h5,
        solvePoisson.out.poisson_vtu,
        solvePoisson.out.poisson_vtu0)

    // Substitute macros
    substituteMacros(
        makePlotOverLine.out.plot_over_line,
        readNumberOfDofs.out.number_of_dofs,
        macro_template,
        prepare_macros)

    // Compile paper
    compilePaper(
        substituteMacros.out.macros,
        makePlotOverLine.out.plot_over_line,
        paper_source)
}

process generateMesh {
    conda '../source/envs/full_default_env.yaml'

    input:
    path geofile

    output:
    path "unit_square.msh", emit: mesh

    script:
    """
    gmsh -2 -setnumber domain_size ${params.domainSize} $geofile -o unit_square.msh
    """
}

process convertToXDMF {
    conda '../source/envs/full_default_env.yaml'

    input:
    path mesh

    output:
    path "unit_square.h5", emit: mesh_h5
    path "unit_square.xdmf", emit: mesh_xdmf

    script:
    """
    meshio convert $mesh unit_square.xdmf
    """
}

process solvePoisson {

    publishDir "./results", mode: "copy"

    conda "../source/envs/processing.yaml"

    input:
    path fenics_code
    path mesh_xdmf
    path mesh_h5

    output:
    path "poisson.xdmf", emit: poisson_xdmf
    path "poisson.h5", emit: poisson_h5
    path "poisson.vtu", emit: poisson_vtu
    path "poisson_p0_000000.vtu", emit: poisson_vtu0

    stdout emit: poisson_stdout

    script:
    """
    python $fenics_code --mesh $mesh_xdmf --degree 2 --outputfile poisson.xdmf
    """
}


process readNumberOfDofs {
    conda '../source/envs/full_default_env.yaml'

    input:
    val x

    output:
    stdout emit: number_of_dofs

    script:
    """
    #!/usr/bin/python3
    s = '''${x.replaceAll("\\n", "&")}'''
    dof_string = s.split("Number of dofs used:")[1]
    num_dofs = dof_string.split("&")[0]
    print(int(num_dofs))
    """
}

process makePlotOverLine {

    publishDir "./results", mode: "copy"

    conda "../source/envs/postprocessing.yaml"

    input:
    path postprocessing_script
    path xdmf
    path h5
    path vtu
    path vtu0

    output:
    path "plotoverline.csv", emit: plot_over_line

    script:
    """
    echo "Python executable: \$(which python)"
    echo "Conda env: \$CONDA_PREFIX"
    python $postprocessing_script $vtu0 plotoverline.csv
    """
}

process substituteMacros {

    input:
    path plotOverLine
    val number_of_dofs
    path macro_template
    path prepare_macros

    output:
    path "macros.tex", emit: macros

    script:
    """
    python $prepare_macros --macro-template-file $macro_template \
        --plot-data-path $plotOverLine \
        --domain-size ${params.domainSize} \
        --num-dofs ${number_of_dofs.replaceAll("\\s", "")} \
        --output-macro-file macros.tex
    """
}

process compilePaper {

    publishDir "./results", mode: "copy"

    input:
    path macros
    path plot_over_line
    path paper_source

    output:
    path "paper.pdf"

    script:
    """
    tectonic $paper_source
    """
}
