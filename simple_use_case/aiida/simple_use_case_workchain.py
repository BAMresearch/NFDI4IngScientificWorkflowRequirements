import sys
import pathlib
import subprocess
import voluptuous as vol

from aiida.engine import WorkChain, calcfunction
from aiida.orm import Dict
from aiida.plugins import DataFactory

SinglefileData = DataFactory("singlefile")

# set filepaths
# unfortunately this seems necessary
# I haven't figured out how to specify the absolute path
# from the SinglefileData object yet (if possible)
CWD = pathlib.Path(__file__).parent.absolute()
SOURCE = CWD.parent / "source"

# add SOURCE to path for fenics imports
sys.path.append(SOURCE.absolute().as_posix())


"""Outline
use calcfunction for mesh generation, conversion
and the postprocessing tasks. These are usually no
long running processes.
The fenics simulation should be submitted to some
other machine as a CalcJob as this can be a
computationally expensive task.
"""


def get_executable_path(env_name, executable):
    """get executable path

    Parameters
    ----------
    env_name : str
        The name of the locally installed conda environment.
    executable : str
        The name of the executable

    Returns
    -------
    exec_path : str
    """
    exec_path = subprocess.check_output(
        ["conda", "run", "-n", env_name, "which", executable], encoding="UTF-8"
    )
    return exec_path.strip("\n")


@calcfunction
def gmsh_subprocess(cmdline_parameters, geofile):
    """

    Parameters
    ----------
    cmdline_parameters : aiida.orm.nodes.data.dict.Dict
        A AiiDA data Node of type Dict defining Gmsh cmdline parameters.

    Returns
    -------
    output: aiida.orm.nodes.data.singlefile.SinglefileData
        The solution of the poisson problem stored in a .pvd file.

    """
    # subset of gmsh's command line options
    cmdline_options = {
        vol.Optional("-1"): bool,
        vol.Optional("-2"): bool,
        vol.Optional("-3"): bool,
        vol.Optional("-format", default="auto"): str,
        vol.Optional("-order", default=1): int,
        vol.Optional("-o"): str,
    }
    schema = vol.Schema(cmdline_options)
    parameters = schema(cmdline_parameters.get_dict())

    # build subprocess call
    executable = get_executable_path("aiida_simplecase_dev", "gmsh")
    args = [executable]
    # FIXME how to return absolute path of geofile?
    args += [SOURCE / geofile.filename]
    for key, value in parameters.items():
        if isinstance(value, bool) and value:
            args.append(key)
        elif isinstance(value, (str, int)):
            args.append(key)
            args.append(str(value))

    # default output
    if "-o" not in args:
        outputfile = (CWD / geofile.filename).with_suffix(".msh")
        args.append("-o")
        args.append(outputfile.absolute())
    else:
        outputfile = pathlib.Path(args[args.index("-o") + 1])

    subprocess.call(args)

    output = SinglefileData(outputfile.absolute())
    return output


@calcfunction
def meshio_convert_subprocess(cmdline_parameters, infile):
    """Convert mesh file

    Parameters
    ----------
    cmdline_parameters : aiida.orm.nodes.data.dict.Dict
        A AiiDA data Node of type Dict defining meshio cmdline parameters.
    infile : aiida.orm.nodes.data.singlefile.SinglefileData
        The meshfile to be read from.

    Returns
    -------
    output: aiida.orm.nodes.data.singlefile.SinglefileData
        The meshfile that was written to.

    """
    input_formats = [
        "abaqus",
        "ansys",
        "avsucd",
        "cgns",
        "dolfin-xml",
        "exodus",
        "flac3d",
        "gmsh",
        "h5m",
        "mdpa",
        "med",
        "medit",
        "nastran",
        "neuroglancer",
        "obj",
        "off",
        "permas",
        "ply",
        "stl",
        "su2",
        "tecplot",
        "tetgen",
        "ugrid",
        "vtk",
        "vtu",
        "wkt",
        "xdmf",
    ]
    output_formats = [
        "abaqus",
        "ansys",
        "avsucd",
        "cgns",
        "dolfin-xml",
        "exodus",
        "flac3d",
        "gmsh",
        "gmsh22",
        "h5m",
        "mdpa",
        "med",
        "medit",
        "nastran",
        "neuroglancer",
        "obj",
        "off",
        "permas",
        "ply",
        "stl",
        "su2",
        "svg",
        "tecplot",
        "tetgen",
        "ugrid",
        "vtk",
        "vtu",
        "wkt",
        "xdmf",
    ]
    # A subset of meshio-convert's command line options
    cmdline_options = {
        vol.Optional("--prune"): bool,
        vol.Optional("--prune-z-0"): bool,
        vol.Optional("--input-format"): vol.All(
            str, vol.Length(min=1), vol.In(input_formats)
        ),
        # output format is required since output file
        # (nonexistent SinglefileData) cannot be specified by the user
        vol.Required("--output-format"): vol.All(
            str, vol.Length(min=1), vol.In(output_formats)
        ),
    }
    schema = vol.Schema(cmdline_options)
    parameters = schema(cmdline_parameters.get_dict())

    # build subprocess call
    executable = get_executable_path("aiida_simplecase_dev", "meshio-convert")
    args = [executable]
    for key, value in parameters.items():
        if isinstance(value, bool) and value:
            args.append(key)
        elif isinstance(value, (str, int)):
            args.append(key)
            args.append(value)

    args.append(CWD / infile.filename)
    outputfilename = CWD / "outfile"
    args.append(outputfilename)

    subprocess.call(args)
    output = SinglefileData(file=pathlib.Path(outputfilename).absolute())
    return output


@calcfunction
def fenics_subprocess(cmdline_parameters, meshfile):
    """Run a fenics problem as a subprocess

    Parameters
    ----------
    cmdline_parameters : aiida.orm.nodes.data.dict.Dict
        A AiiDA data Node of type Dict defining meshio cmdline parameters.
    meshfile : aiida.orm.nodes.data.singlefile.SinglefileData
        The meshfile to be read from.

    Returns
    -------
    output: aiida.orm.nodes.data.singlefile.SinglefileData
        The solution of the fenics problem.

    """
    from poisson import solve_and_write_output

    cmdline_options = {
        vol.Required("--degree"): vol.All(int, vol.Range(min=1, max=3)),
        vol.Required("--outputfile"): str,
    }
    schema = vol.Schema(cmdline_options)
    parameters = schema(cmdline_parameters.get_dict())

    mesh = CWD / meshfile.filename
    solve_and_write_output(
        mesh.as_posix(), int(parameters["--degree"]), str(parameters["--outputfile"])
    )

    output = SinglefileData(
        file=pathlib.Path(str(parameters["--outputfile"])).absolute()
    )
    return output


class SimpleUseCaseWorkChain(WorkChain):
    """WorkChain defining the simple use case."""

    @classmethod
    def define(cls, spec):
        """Specify inputs, outputs, and the workchain outline."""
        super().define(spec)

        spec.input("geofile", valid_type=SinglefileData)
        # spec.input("fenics_code", valid_type=SinglefileData)
        # spec.input("postprocessing", valid_type=SinglefileData)
        # spec.input("latex_code", valid_type=SinglefileData)
        spec.outline(
            cls.generate_mesh,
            cls.convert_mesh,
            cls.fenics_solve,
        )
        spec.output("solution", valid_type=SinglefileData)

    def generate_mesh(self):
        """generate the mesh using Gmsh"""
        cmdline_parameters = Dict(dict={"-2": True, "-format": "msh2"})
        self.ctx.mshfile = gmsh_subprocess(cmdline_parameters, self.inputs.geofile)

    def convert_mesh(self):
        """convert the mesh to dolfin format using meshio-convert"""
        cmdline_parameters = Dict(dict={"--output-format": "xdmf"})
        self.ctx.converted_mesh = meshio_convert_subprocess(
            cmdline_parameters, self.ctx.mshfile
        )

    def fenics_solve(self):
        """solve the poisson equation using fenics"""
        cmdline_parameters = Dict(dict={"--degree": 2, "--outputfile": "poisson.pvd"})
        solution = fenics_subprocess(cmdline_parameters, self.ctx.converted_mesh)
        self.out("solution", solution)
