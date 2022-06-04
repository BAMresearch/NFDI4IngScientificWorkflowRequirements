#!/usr/bin/env runaiida
from aiida.engine import calcfunction
from aiida.orm import Float, Int
from aiida_shell import launch_shell_job

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


@calcfunction
def get_domain_size(gmsh_stdout):
    string = gmsh_stdout.get_content().split("Used domain size:")[1]
    size = float(string.split("Used mesh size")[0])
    return Float(size)


@calcfunction
def get_num_dofs(fenics_stdout):
    stdout = fenics_stdout.get_content()
    ndofs = stdout.split("Number of dofs used:")[1]
    return Int("".join(ndofs.split()))


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
        get_domain_size(gmsh_results["stdout"]),
        "--num-dofs",
        get_num_dofs(fenics_results["stdout"]),
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
with open("paper.pdf", "wb") as handle:
    handle.write(paper["paper_pdf"].get_object_content(path="./paper.pdf", mode='rb'))

