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
from argparse import ArgumentParser
import dolfin as df


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
    with df.XDMFFile(meshfile) as instream:
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


def solve_and_write_output(mesh, degree, outputfile):
    u = solve_poisson(mesh, degree)
    u.rename("u", u.name())
    resultfile = df.XDMFFile(outputfile)
    resultfile.write(u, 0)


if __name__ == "__main__":
    PARSER = ArgumentParser(description="run script for the poisson problem")
    PARSER.add_argument("-m", "--mesh",
                        required=True, help="mesh file to be used")
    PARSER.add_argument("-d", "--degree",
                        required=True,
                        help="polynomial order to be used")
    PARSER.add_argument("-o", "--outputfile",
                        required=True,
                        help="file name for the output to be written")
    ARGS = vars(PARSER.parse_args())

    solve_and_write_output(
        ARGS["mesh"], int(ARGS["degree"]), ARGS["outputfile"]
    )
