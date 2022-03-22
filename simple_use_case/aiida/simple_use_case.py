#!/usr/bin/env runaiida
import pathlib

from aiida import orm
from aiida_shell import launch_shell_job

results, node = launch_shell_job(
    "python",
    arguments=[
        "{script}",
        "--mesh",
        "{mesh}",
        "--degree",
        "2",
        "--output",
        "poisson.pvd",
    ],
    files={"script": "resources/poisson.py", "mesh": converted_mesh["mesh_xdmf"]},
    filenames={"mesh": "mesh.xdmf"},
    outputs=["poisson.pvd", "poisson000000.vtu"],
    context_files={"mesh_h5": converted_mesh["mesh_h5"]},
    context_filenames={"mesh_h5": "mesh.h5"},
)


@shellfunction(command="gmsh", output_filenames=["*.msh"])
def gmsh(**kwargs):
    """Run the ``gmsh`` command."""


@shellfunction(command="meshio", output_filenames=["*.xdmf", "*.h5"])
def meshio(**kwargs):
    """Run the ``meshio`` command to convert to XDMF format."""


@shellfunction(command="python", output_filenames=["*.pvd", "*.vtu"])
def poisson(**kwargs):
    """Run the ``poisson`` step."""


@shellfunction(command="pvbatch", output_filenames=["*.csv"])
def pvbatch(**kwargs):
    """Run the ``pvbatch`` command."""


@workfunction
def workflow(geometry, poisson_script, post_processing_script):
    """Simple workflow to solve Poisson equation for a geometry."""

    # Generate the mesh from the geometry.
    arguments = List(
        ["-2", "-order", "1", "-format", "msh2", "{geometry}", "-o", "mesh.msh"]
    )
    results_gmsh = gmsh(arguments=arguments, geometry=geometry)

    # Convert the mesh to XDMF format
    arguments = List(["convert", "{mesh}", "mesh.xdmf"])
    # Note that the output link label was converted from "mesh.msh" to "mesh_msh"
    results_meshio = meshio(arguments=arguments, mesh=results_gmsh["mesh_msh"])
    # For more information see section "Design choices" > "Output files" in the AiiDA
    # Enhancement Proposal https://github.com/aiidateam/AEP/tree/aep/shell-functions/xxx_shell_functions

    # Solve poisson equation
    # The additional argument '--h5' is necessary to specify the .h5 file as input,
    # such that it is copied to the temporary directory as well.
    # See https://github.com/sphuber/aiida-core/blob/feature/5287/shell-function/aiida/engine/processes/functions/shell.py#L156-L189
    arguments = List(
        [
            "{script}",
            "--mesh",
            "{mesh}",
            "--h5",
            "{mesh_data}",
            "--degree",
            "2",
            "--outputfile",
            "poisson.pvd",
        ]
    )
    results_poisson = poisson(
        arguments=arguments,
        script=poisson_script,
        mesh=results_meshio["mesh_xdmf"],
        mesh_data=results_meshio["mesh_h5"],
    )

    # Postprocessing: plot over line
    # With the .pvd and corresponding .vtu file, the same issue as with the .xdmf and .h5 files occurs.
    arguments = List(["{script}", "{pvd}", "plotoverline.csv", "--vtu", "{vtu}"])
    results_pvbatch = pvbatch(
        arguments=arguments,
        script=post_processing_script,
        pvd=results_poisson["poisson_pvd"],
        vtu=results_poisson["poisson000000_vtu"],
    )

    return results_pvbatch


if __name__ == "__main__":
    # declare inputs as AiiDA data types
    geometry = SinglefileData(Path("../source/unit_square.geo").resolve())
    poisson_script = SinglefileData(Path("../source/poisson.py").resolve())
    post_processing_script = SinglefileData(
        Path("../source/postprocessing.py").resolve()
    )
    # run the workflow and return the process node and the results
    results, node = workflow.run_get_node(
        geometry, poisson_script, post_processing_script
    )
    print(f"Workflow {node} finished.")
    print(f"Results: {results}")
    """
    the output should look something like this:
    ```sh
    ❯❯ verdi run simple_use_case.py
    Workflow uuid: 8f8ad841-feb4-42a9-a546-fe48342d91a7 (pk: 683) (__main__.workflow) finished.
    Results: {'plotoverline_csv': <SinglefileData: uuid: 4a805be6-27b4-4518-b5c9-29dcc041c31e (pk: 697)>}
    ```
    The primary key can be used to show information (e.g. inputs and outputs) about the workflow:
    ```sh
    verdi process show 683
    ```
    """
