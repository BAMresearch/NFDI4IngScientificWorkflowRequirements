from pathlib import Path

from aiida.orm import List, SinglefileData
from aiida.engine.processes.functions import shellfunction, workfunction


@shellfunction(command="gmsh", output_filenames=["mesh"])
def gmsh(**kwargs):
    """Run the ``gmsh`` command."""


@shellfunction(command="meshio", output_filenames=["mesh*"])
def meshio(**kwargs):
    """Run the ``meshio`` command."""


@shellfunction(command="python", output_filenames=["poisson.pvd"])
def poisson(**kwargs):
    """Run the ``poisson`` step."""


@shellfunction(command="pvbatch", output_filenames=["plotoverline.csv"])
def pvbatch(**kwargs):
    """Run the ``pvbatch`` command."""


@workfunction
def workflow(geometry):
    """Simple workflow to solve Poisson equation for a geometry."""

    # Generate the mesh from the geometry.
    arguments = List(
        ["-2", "-order", "1", "-format", "msh2", "{geometry}", "-o", "mesh"]
    )
    results_gmsh = gmsh(arguments=arguments, geometry=geometry)

    # Convert the mesh to XDMF format
    arguments = List(["convert", "{mesh}"])
    results_meshio = meshio(arguments=arguments, mesh=results_gmsh["output"])

    # Solve Poisson
    # arguments = List(["{script}", "--mesh", "{mesh}", "--degree", "2"])
    # results_poisson = poisson(
    #     arguments=arguments, script=poisson_script, mesh=results_meshio["output"]
    # )

    # Postprocessing: plot over line
    # arguments = List(["{script}", "{pvd}"])
    # results_pvbatch = pvbatch(
    #     script=post_processing_script, pvd=results_poisson["output"]
    # )

    # return results_pvbatch["output"]
    return results_gmsh


if __name__ == "__main__":
    geometry = SinglefileData(Path("../source/unit_square.geo").resolve())
    # poisson_script = SinglefileData(Path("../source/poisson.py").resolve())
    # post_processing_script = SinglefileData(
    #     Path("../source/postprocessing.py").resolve()
    # )
    # results, node = workflow.run_get_node(
    #     geometry, poisson_script, post_processing_script
    # )
    results, node = workflow.run_get_node(geometry)
    print(f"Workflow {node} finished.")
    print(f"Results: {results}")
