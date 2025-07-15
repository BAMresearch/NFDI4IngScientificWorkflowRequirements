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
    nodes={"geometry": "../source/unit_square.geo"},
    outputs=["mesh.msh"],
)

# ### convert mesh from msh to xdmf format
meshio_results, meshio_node = launch_shell_job(
    "meshio",
    arguments=["convert", "{mesh}", "mesh.xdmf"],
    nodes={"mesh": gmsh_results["mesh_msh"]},
    filenames={"mesh": "mesh.msh"},
    outputs=["*.xdmf", "*.h5"],
)

# ### solution of the poisson problem with fenics
fenics_results, fenics_node = launch_shell_job(
    "python",
    arguments=[
        "{script}",
        "--mesh",
        "{mesh_xdmf}",  
        "--degree",
        "2",
        "--outputfile",
        "poisson.xdmf",
    ],
    nodes={
        "script": "../source/poisson.py",
        "mesh_xdmf": meshio_results["mesh_xdmf"],  
        "mesh_h5": meshio_results["mesh_h5"]
    },
    filenames={"mesh_xdmf": "mesh.xdmf", "mesh_h5": "mesh.h5"},  
    outputs=["poisson.xdmf", "poisson.h5"],  # <-- only list files actually produced
)

# Check fenics outputs before postprocessing
required_keys = ["poisson_xdmf", "poisson_h5"]  # <-- only check for files that exist
missing = [k for k in required_keys if fenics_results.get(k) is None]
if missing:
    raise RuntimeError(f"Missing fenics output(s): {', '.join(missing)}")

# ### postprocessing of the fenics job
postprocessing_results, postprocessing_node = launch_shell_job(
    "python",
    arguments=["{script}", "{pvdfile}", "plotoverline.csv"],
    nodes={
        "script": "../source/postprocessing.py",
        "xdmf_file": fenics_results["poisson_xdmf"],
        "pvd_file": fenics_results["poisson_h5"],
        # "vtu_file": fenics_results["poisson_vtu"],  # <-- remove if not produced
        # "vtu0_file": fenics_results["poisson_p0_000000_vtu"]  # <-- remove if not produced
    },
    filenames={"xdmf_file": "poisson.xdmf", 
                "h5_file": "poisson.h5"},
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
        "{domain_size}",
        "--num-dofs",
        "{num_dofs}",
        "--output-macro-file",
        "macros.tex",
    ],
    nodes={
        "script": "../source/prepare_paper_macros.py",
        "template": "../source/macros.tex.template",
        "csvfile": postprocessing_results["plotoverline_csv"],  # <-- fix here
        "domain_size": get_domain_size(gmsh_results["stdout"]),
        "num_dofs": get_num_dofs(fenics_results["stdout"]),
    },
    filenames={"csvfile": "plotoverline.csv"},
    outputs=["macros.tex"],
)

# ### compile paper
paper, paper_node = launch_shell_job(
    "tectonic",
    arguments=["{texfile}"],
    nodes={
        "texfile": "../source/paper.tex",
        "macros": macros["macros_tex"],
        "csvfile": postprocessing_results["plotoverline_csv"],
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
    handle.write(paper["paper_pdf"].get_object_content(path="./paper.pdf", mode="rb"))
    handle.write(paper["paper_pdf"].get_object_content(path="./paper.pdf", mode="rb"))
    handle.write(paper["paper_pdf"].get_object_content(path="./paper.pdf", mode="rb"))
    handle.write(paper["paper_pdf"].get_object_content(path="./paper.pdf", mode="rb"))
