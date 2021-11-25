#!/usr/bin/env nextflow

params.degree = 2

// for now simply add dependent files as Channels
geo_ch = Channel.fromPath("$PWD/../source/unit_square.geo")
fenics_ch = Channel.fromPath("$PWD/../source/poisson.py")
pv_ch = Channel.fromPath("$PWD/../source/postprocessing.py")
tex_ch = Channel.fromPath("$PWD/../source/paper.tex")

process generateMesh {
    // generate mesh using Gmsh

    // use conda directive to specify environment file
    conda "./envs/preprocessing.yaml"

    input:
    file geo from geo_ch

    output:
    file 'unit_square.msh' into msh_ch

    """
    gmsh -2 -order 1 -format msh2 $geo -o unit_square.msh
    """
}


process convertToXDMF {
    // convert any msh file to xdmf

    conda "./envs/preprocessing.yaml"

    input:
    file msh from msh_ch

    output:
    file 'unit_square.h5' into h5_ch
    file 'unit_square.xdmf' into xdmf_ch

    """
    meshio-convert $msh unit_square.xdmf
    """
}


process solvePoisson {
    // solve poisson equation using fenics code

    conda "./envs/processing.yaml"

    // multiple inputs from different channels
    input:
    file fenics_code from fenics_ch
    file meshdata from h5_ch
    file mesh from xdmf_ch

    output:
    file 'poisson.pvd' into pvd_ch
    file 'poisson*.vtu' into vtu_ch

    """
    python $fenics_code --mesh $mesh --degree ${params.degree} --outputfile poisson.pvd
    """
}


process makeContourplot {

    conda "./envs/postprocessing.yaml"

    input:
    file postproc from pv_ch
    file vtu from vtu_ch
    file pvd from pvd_ch

    output: 
    file 'contourplot.png' into png_ch

    """
    pvbatch $postproc $pvd contourplot.png
    """
}


process compile {

    conda "./envs/postprocessing.yaml"

    input:
    file tex_code from tex_ch
    file png from png_ch

    output:
    file 'paper.pdf' 

    """
    tectonic $tex_code
    """
}
