"""
solution of the poisson equation on the unit square

Usage:
    poisson.py [options] MESH DEG

Arguments:
    MESH         The partition of the unit square.
    DEG          The degree of the finite element space.

Options:
    -h, --help               Show this message and exit.
    -o FILE, --output=FILE   Write solution to FILE.
"""

import sys
from pathlib import Path
from docopt import docopt
import dolfin as df


def parse_args(args):
    args = docopt(__doc__, args)
    args["MESH"] = Path(args["MESH"])
    args["DEG"] = int(args["DEG"])
    args["--output"] = Path(args["--output"]) if args["--output"] is not None else None
    return args


def solve_poisson(meshfile, degree):
    """solves the poisson equation

    Parameters
    ----------
    meshfile : str, Path
        FilePath to the mesh in xdmf format.
    degree : int
        Degree of the finite element space.

    Returns
    -------
    solution : df.Function
    """
    mesh = df.Mesh()
    with df.XDMFFile(meshfile.as_posix()) as instream:
        instream.read(mesh)
    V = df.FunctionSpace(mesh, "CG", degree)
    boundary_data = df.Expression("1.0 + x[0] * x[0] + 2.0 * x[1] * x[1]", degree=2)

    def boundary(x, on_boundary):
        return on_boundary

    bc = df.DirichletBC(V, boundary_data, boundary)
    u = df.TrialFunction(V)
    v = df.TestFunction(V)
    f = df.Constant(-6.0)
    a = df.dot(df.grad(u), df.grad(v)) * df.dx
    L = f * v * df.dx

    solution = df.Function(V)
    df.solve(a == L, solution, bc)
    return solution


def main(args):
    args = parse_args(args)
    u = solve_poisson(args["MESH"], args["DEG"])
    if args["--output"] is not None and args["--output"].suffix == ".xdmf":
        resultfile = df.XDMFFile(args["--output"].as_posix())
        resultfile.write(u, 0)


if __name__ == "__main__":
    main(sys.argv[1:])
