#!/usr/bin/env runaiida
from aiida.engine import calcfunction
from aiida.orm import Float, Int
from aiida_shell import launch_shell_job
import re


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
    filenames={"geometry": "unit_square.geo"},
    outputs=["mesh.msh"],
)

# ### convert mesh from msh to xdmf format
meshio_results, meshio_node = launch_shell_job(
    "meshio",
    arguments=["convert", 
               "{mesh}", 
               "mesh.xdmf"],
    nodes={"mesh": gmsh_results["mesh_msh"]},
    filenames={"mesh": "mesh.msh"},
    outputs=["*.xdmf", "*.h5"],
)

# ### solution of the poisson problem with fenics
try:
    fenics_results, fenics_node = launch_shell_job(
        "bash",
        arguments=[
            "-c",
            (
                # Build the environment if it doesn't exist, then activate and run
                # this is due to an incompatibility between dolfinx and aiida2.7, the latter
                # requiring to downgrade packages (such as numpy) which makes the fenics job fail
                # and aiida runs the shell job in the global environment
                "mamba env create -n processing -f processing.yaml && "
                "source activate processing && "
                "python poisson.py --mesh {mesh_xdmf} --degree 2 --outputfile poisson.xdmf"
            )
        ],
        nodes={
            "script": "../source/poisson.py",
            "conda": "../source/envs/processing.yaml",
            "mesh_xdmf": meshio_results["mesh_xdmf"],  
            "mesh_h5": meshio_results["mesh_h5"]
        },
        filenames={"script": "poisson.py",
                   "mesh_xdmf": "mesh.xdmf", 
                   "mesh_h5": "mesh.h5", 
                   "conda": "processing.yaml"},  
        outputs=["poisson.xdmf", "poisson.h5", "poisson.vtu", "poisson_p0_000000.vtu"]
    )
except Exception as e:
    # Try to print stdout/stderr if available in the exception
    if 'fenics_results' in locals():
        print("=== FEniCS stdout (on error) ===")
        print(fenics_results.get("stdout", "No stdout").get_content() if fenics_results.get("stdout") else "No stdout")
        print("=== FEniCS stderr (on error) ===")
        print(fenics_results.get("stderr", "No stderr").get_content() if fenics_results.get("stderr") else "No stderr")
    print(f"FEniCS job failed: {e}")
    raise


# Check fenics outputs before postprocessing
required_keys = ["poisson_xdmf", "poisson_h5", "poisson_vtu", "poisson_p0_000000_vtu"]
missing = [k for k in required_keys if fenics_results.get(k) is None]
if missing:
    raise RuntimeError(f"Missing fenics output(s): {', '.join(missing)}")

# ### postprocessing of the fenics job
try:
    postprocessing_results, postprocessing_node = launch_shell_job(
        "python",
        arguments=[
            "{script}",      
            "{vtu0_file}", 
            "plotoverline.csv"
        ],
        nodes={
            "script": "../source/postprocessing.py",
            "xdmf_file": fenics_results["poisson_xdmf"],
            "pvd_file": fenics_results["poisson_h5"],
            "vtu_file": fenics_results["poisson_vtu"],
            "vtu0_file": fenics_results["poisson_p0_000000_vtu"],
        },
        filenames={
            "script": "postprocessing.py",
            "xdmf_file": "poisson.xdmf",
            "h5_file": "poisson.h5",
            "vtu_file": "poisson.vtu",
            "vtu0_file": "poisson_p0_000000.vtu",
        },
        outputs=["plotoverline.csv"],
    )
    # Check for output file immediately after job
    if "plotoverline_csv" not in postprocessing_results:
        print("=== Postprocessing stdout ===")
        print(postprocessing_results.get("stdout", "No stdout").get_content() if postprocessing_results.get("stdout") else "No stdout")
        print("=== Postprocessing stderr ===")
        print(postprocessing_results.get("stderr", "No stderr").get_content() if postprocessing_results.get("stderr") else "No stderr")
        raise RuntimeError("plotoverline.csv was not produced by postprocessing.py")

except Exception as e:
    if 'postprocessing_results' in locals():
        print("=== Postprocessing stdout (on error) ===")
        print(postprocessing_results.get("stdout", "No stdout").get_content() if postprocessing_results.get("stdout") else "No stdout")
        print("=== Postprocessing stderr (on error) ===")
        print(postprocessing_results.get("stderr", "No stderr").get_content() if postprocessing_results.get("stderr") else "No stderr")
    print(f"Postprocessing job failed: {e}")
    raise

@calcfunction
def get_domain_size(gmsh_stdout):
    string = gmsh_stdout.get_content().split("Used domain size:")[1]
    size = float(string.split("Used mesh size")[0])
    return Float(size)


@calcfunction
def get_num_dofs(fenics_stdout):
    stdout = fenics_stdout.get_content()
    match = re.search(r"Number of dofs used:\s*(\d+)", stdout)
    if not match:
        raise ValueError("Could not find 'Number of dofs used:' in FEniCS output.")
    ndofs = int(match.group(1))
    return Int(ndofs)


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
        "csvfile": postprocessing_results["plotoverline_csv"],
        "domain_size": get_domain_size(gmsh_results["stdout"]),
        "num_dofs": get_num_dofs(fenics_results["stdout"]),
    },
    filenames={
        "script": "prepare_paper_macros.py",
        "template": "macros.tex.template",
        "csvfile": "plotoverline.csv"
    },
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
