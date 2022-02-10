import sys
import os
from pathlib import Path

from aiida.orm import Int, Float, List, SinglefileData
from aiida.engine.processes.functions import calcfunction, shellfunction, workfunction


@shellfunction(command="gmsh", output_filenames=["*.msh"])
def gmsh(**kwargs):
    """Run the ``gmsh`` command."""


@shellfunction(command="meshio", output_filenames=["*.xdmf", "*.h5"])
def meshio(**kwargs):
    """Run the ``meshio`` command to convert to XDMF format."""


@calcfunction
def solve_poisson(mesh_h5, mesh_xdmf):
    """solve the poisson problem using fenics"""
    import tempfile

    # make source available in path
    cwd = Path.cwd()
    source = cwd.parent / "source"
    sys.path.append(source.absolute().as_posix())
    from poisson import solve_and_write_output

    # Similar to the shellfunction implementation
    # a temporary directory to write input SinglefileData
    # is used. Therefore, the additional argument 'mesh_h5'
    # is necessary.
    # See https://github.com/sphuber/aiida-core/blob/feature/5287/shell-function/aiida/engine/processes/functions/shell.py#L156-L189
    with tempfile.TemporaryDirectory() as tempdir:
        dirpath = Path(tempdir)

        # process inputs of type SinglefileData
        for single_file in [mesh_h5, mesh_xdmf]:
            filename = single_file.filename
            filepath = dirpath / filename

            with single_file.open(mode="rb") as handle:
                filepath.write_bytes(handle.read())

        # change current working directory to dirpath
        os.chdir(dirpath)
        degree = 2  # not exposed as input
        pvd_file = dirpath / "poisson.pvd"
        dofs = solve_and_write_output(
            (dirpath / mesh_xdmf.filename).resolve().as_posix(),
            degree,
            pvd_file.resolve().as_posix(),
            return_dofs=True,
        )

        # store outputs
        outputs = {}
        outputs["pvd"] = SinglefileData(pvd_file.resolve())
        outputs["vtu"] = SinglefileData(
            (dirpath / (pvd_file.stem + "000000.vtu")).resolve()
        )
        outputs["num_dofs"] = Int(dofs)

    os.chdir(cwd)
    return outputs


@shellfunction(command="pvbatch", output_filenames=["*.csv"])
def pvbatch(**kwargs):
    """Run the ``pvbatch`` command."""


@shellfunction(command="python", output_filenames=["*.tex"])
def substitute(**kwargs):
    """Run a python script to substitute macros."""


@shellfunction(command="tectonic", output_filenames=["*.pdf"])
def tectonic(**kwargs):
    """Run the ``tectonic`` command."""


@workfunction
def workflow(
    domain_size,
    geometry,
    poisson_script,
    post_processing_script,
    prepare_macros,
    macro_template,
    paper,
):
    """Simple workflow to solve Poisson equation for a geometry."""

    # Generate the mesh from the geometry.
    arguments = List(
        [
            "-2",
            "-setnumber",
            "domain_size",
            str(domain_size.value),
            "{geometry}",
            "-o",
            "mesh.msh",
        ]
    )
    results_gmsh = gmsh(arguments=arguments, geometry=geometry)

    # Convert the mesh to XDMF format
    arguments = List(["convert", "{mesh}", "mesh.xdmf"])
    # Note that the output link label was converted from "mesh.msh" to "mesh_msh"
    results_meshio = meshio(arguments=arguments, mesh=results_gmsh["mesh_msh"])
    # For more information see section "Design choices" > "Output files" in the AiiDA
    # Enhancement Proposal https://github.com/aiidateam/AEP/tree/aep/shell-functions/xxx_shell_functions

    # Solve poisson problem with fenics
    results_poisson = solve_poisson(
        results_meshio["mesh_h5"], results_meshio["mesh_xdmf"]
    )

    # Postprocessing: plot over line
    # As in the poisson step, all dependent files must be declared as arguments, such that
    # they will be copied to the temporary working directory.
    arguments = List(["{script}", "{pvd}", "plotoverline.csv", "--vtu", "{vtu}"])
    results_pvbatch = pvbatch(
        arguments=arguments,
        script=post_processing_script,
        pvd=results_poisson["pvd"],
        vtu=results_poisson["vtu"],
    )

    # Substitute macros
    arguments = List(
        [
            "{script}",
            "--macro-template-file",
            "{template}",
            "--plot-data-path",
            "./plotoverline.csv",
            "--domain-size",
            str(domain_size.value),
            "--num-dofs",
            str(results_poisson["num_dofs"].value),
            "--output-macro-file",
            "macros.tex",
        ]
    )
    results_macros = substitute(
        arguments=arguments,
        script=prepare_macros,
        template=macro_template,
        plotdata=results_pvbatch["plotoverline_csv"],
    )

    # Compile paper
    # FIXME implicit file dependencies do not work
    # I would need macros.tex and plotoverline.csv to be present in the
    # temporary working directory for the compilation to work.
    # However, the command 'tectonic paper.tex' does not allow
    # these files to be passed as arguments such that they would
    # be copied to the temporary working directory.
    # possible workaround: use calcfunction and subprocess.call

    return results_macros


if __name__ == "__main__":
    # declare inputs as AiiDA data types
    domain_size = Float(2.0)
    geometry = SinglefileData(Path("../source/unit_square.geo").resolve())
    poisson_script = SinglefileData(Path("../source/poisson.py").resolve())
    post_processing_script = SinglefileData(
        Path("../source/postprocessing.py").resolve()
    )
    prepare_macros = SinglefileData(Path("../source/prepare_paper_macros.py").resolve())
    macro_template = SinglefileData(Path("../source/macros.tex.template").resolve())
    paper = SinglefileData(Path("../source/paper.tex").resolve())

    # run the workflow and return the process node and the results
    results, node = workflow.run_get_node(
        domain_size,
        geometry,
        poisson_script,
        post_processing_script,
        prepare_macros,
        macro_template,
        paper,
    )
    print(f"Workflow {node} finished.")
    print(f"Results: {results}")
