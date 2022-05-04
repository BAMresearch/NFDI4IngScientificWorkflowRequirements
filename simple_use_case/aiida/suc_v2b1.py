#!/usr/bin/env runaiida

from aiida_shell import launch_shell_job
import PyPDF2

# ### generate mesh with gmsh
gmsh_results, gmsh_node = launch_shell_job(
    "gmsh",
    arguments=[
        "-2",
        "-setnumber",
        "domain_size",
        "2.0",
        "{geometry}",
        "-o",
        "mesh.msh",
    ],
    files={"geometry": "../source/unit_square.geo"},
    outputs=["mesh.msh"],
)

# ### convert mesh from msh to xdmf format
meshio_results, meshio_node = launch_shell_job(
    "meshio",
    arguments=["convert", "{mesh}", "mesh.xdmf"],
    files={"mesh": gmsh_results["mesh_msh"]},
    filenames={"mesh": "mesh.msh"},
    outputs=["*.xdmf", "*.h5"],
)

# ### solution of the poisson problem with fenics
fenics_results, fenics_node = launch_shell_job(
    "python",
    arguments=[
        "{script}",
        "--mesh",
        "{mesh}",
        "--degree",
        "2",
        "--outputfile",
        "poisson.pvd",
    ],
    files={
        "script": "../source/poisson.py",
        "mesh": meshio_results["mesh_xdmf"],
        "mesh_h5": meshio_results["mesh_h5"],
    },
    filenames={"mesh": "mesh.xdmf", "mesh_h5": "mesh.h5"},
    outputs=["poisson.pvd", "poisson000000.vtu"],
)

# ### postprocessing of the fenics job
paraview_results, paraview_node = launch_shell_job(
    "pvbatch",
    arguments=["{script}", "{pvdfile}", "plotoverline.csv"],
    files={
        "script": "../source/postprocessing.py",
        "pvdfile": fenics_results["poisson_pvd"],
        "vtufile": fenics_results["poisson000000_vtu"],
    },
    filenames={"pvdfile": "poisson.pvd", "vtufile": "poisson000000.vtu"},
    outputs=["plotoverline.csv"],
)


def read_domain_size():
    stdout = gmsh_results["stdout"].get_content()
    s = stdout.split("Used domain size:")[1]
    size = float(s.split("Used mesh size")[0])
    return str(size)


def read_num_dofs():
    stdout = fenics_results["stdout"].get_content()
    ndofs = stdout.split("Number of dofs used:")[1]
    return "".join(ndofs.split())


# ### prepare latex macros
macros, macros_node = launch_shell_job(
    "python",
    arguments=[
        "{script}",
        "--macro-template-file",
        "{template}",
        "--plot-data-path",
        "{csvfile}",
        "--domain-size",
        read_domain_size(),
        "--num-dofs",
        read_num_dofs(),
        "--output-macro-file",
        "macros.tex",
    ],
    files={
        "script": "../source/prepare_paper_macros.py",
        "template": "../source/macros.tex.template",
        "csvfile": paraview_results["plotoverline_csv"],
    },
    filenames={"csvfile": "plotoverline.csv"},
    outputs=["macros.tex"],
)

# ### compile paper
paper, paper_node = launch_shell_job(
    "tectonic",
    arguments=["{texfile}"],
    files={
        "texfile": "../source/paper.tex",
        "macros": macros["macros_tex"],
        "csvfile": paraview_results["plotoverline_csv"],
    },
    filenames={
        "texfile": "paper.tex",
        "macros": "macros.tex",
        "csvfile": "plotoverline.csv",
    },
    outputs=["paper.pdf"],
)

# ### extract final PDF from database
outstream = open("./paper.pdf", "wb")
PdfWriter = PyPDF2.PdfFileWriter()

with paper["paper_pdf"].open(mode="rb") as handle:
    reader = PyPDF2.PdfFileReader(handle)
    PdfWriter.appendPagesFromReader(reader)
    PdfWriter.write(outstream)
outstream.close()
