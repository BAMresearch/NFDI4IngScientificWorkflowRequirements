"""
solution of the poisson equation on the unit square
"""

from argparse import ArgumentParser
import numpy as np
import dolfinx
import dolfinx.io
import dolfinx.fem as fem
from dolfinx.fem.petsc import LinearProblem as LinearProblem
import dolfinx.mesh as mesh
import ufl
from mpi4py import MPI
from petsc4py import PETSc
import sys


def boundary_expression():
    """Defines the function to be used for the boundary conditions"""
    return lambda x: 1.0 + x[0] ** 2 + 2.0 * x[1] ** 2


def solve_poisson(
    meshfile: str, degree: int, bc_expression=boundary_expression()
):
    """solves the poisson equation

    Parameters
    ----------
    meshfile : str
        FilePath to the mesh in xdmf format.
    degree : int
        Degree of the finite element space.

    Returns
    -------
    solution : dolfinx.fem.Function
    """
    with dolfinx.io.XDMFFile(MPI.COMM_WORLD, meshfile, "r") as xdmf:
        mesh = xdmf.read_mesh(name="Grid")
    V = fem.functionspace(mesh, ("CG", degree))

    # Boundary condition
    u_bc = fem.Function(V)
    u_bc.interpolate(bc_expression)

    def boundary(x):
        return np.full(x.shape[1], True, dtype=bool)

    facets = dolfinx.mesh.locate_entities_boundary(mesh, mesh.topology.dim - 1, boundary)
    bc = fem.dirichletbc(u_bc, fem.locate_dofs_topological(V, mesh.topology.dim - 1, facets))

    # Variational problem
    u = ufl.TrialFunction(V)
    v = ufl.TestFunction(V)
    f = fem.Constant(mesh, PETSc.ScalarType(-6.0))
    a = ufl.dot(ufl.grad(u), ufl.grad(v)) * ufl.dx
    L = f * v * ufl.dx

    # Solve
    uh = fem.Function(V)
    problem = LinearProblem(a, L, bcs=[bc], u=uh, petsc_options={"ksp_type": "cg", "pc_type": "hypre"})
    uh = problem.solve()
    return uh


def solve_and_write_output(
    meshfile: str, degree: int, outputfile: str, numdofs=None, return_dofs=False
):
    """solves the poisson equation and writes the solution
    and the number of degrees of freedom to the given file

    Parameters
    ----------
    meshfile : str
        FilePath to the mesh in xdmf format.
    degree : int
        Degree of the finite element space.
    outputfile : str
        FilePath to the output file into which the solution is written.
    numdofs : optional, str
        FilePath to which the number of degrees of freedom is written.
    return_dofs : optional, bool
        If True, return number of degrees of freedom.
    """
    uh = solve_poisson(meshfile, degree)
    V = uh.function_space
    dofs = V.dofmap.index_map.size_global * V.dofmap.index_map_bs
    print(f"Number of dofs used: {dofs}")
    sys.stdout.flush()

    # Set the solution field name to "u"
    uh.name = "u"

    # write XDMF using dolfinx native writer for compatibility
    xdmf_filename = outputfile.replace('.vtu', '.xdmf').replace('.vtk', '.xdmf')
    if not xdmf_filename.endswith('.xdmf'):
        xdmf_filename = outputfile + '.xdmf'
    
    # write VTK for visualization and postprocessing
    vtk_filename = outputfile.replace('.xdmf', '.vtu').replace('.vtk', '.vtu')
    if not vtk_filename.endswith('.vtu'):
        vtk_filename = outputfile + '.vtu'
    
    # Get mesh geometry degree (fallback to 1 if not found)
    mesh_degree = getattr(V.mesh.geometry, "degree", 1)

    # Write VTK output
    try:
        with dolfinx.io.VTKFile(MPI.COMM_WORLD, vtk_filename, "w") as vtk:
            if mesh_degree != degree:
                # Interpolate uh to a function space matching the mesh degree
                V1 = fem.functionspace(V.mesh, ("CG", mesh_degree))
                uh1 = fem.Function(V1)
                uh1.interpolate(uh)
                uh1.name = "u"
                vtk.write_function(uh1)
            else:
                vtk.write_function(uh)
    except Exception as e:
        print(f"Error writing vtk files: {e}", file=sys.stderr)
        sys.stderr.flush()

    try:        
        with dolfinx.io.XDMFFile(MPI.COMM_WORLD, xdmf_filename, "w") as xdmf:
            import os
            print("xdmf_filename", xdmf_filename)
            print(f"Opened XDMF file for writing at: {os.path.abspath(xdmf_filename)}")
            xdmf.write_mesh(V.mesh)
            
            if mesh_degree != degree:
                # Interpolate uh to a function space matching the mesh degree
                V1 = fem.functionspace(V.mesh, ("CG", mesh_degree))
                uh1 = fem.Function(V1)
                uh1.interpolate(uh)
                uh1.name = "u"
                xdmf.write_function(uh1)
            else:
                xdmf.write_function(uh)
    except Exception as e:
        print(f"Error writing xdmf/h5 files: {e}", file=sys.stderr)
        sys.stderr.flush()

    import os
    print("Current working directory:", os.getcwd())

   # Check that output files actually exist and are readable
    import os
    # Generate expected output filenames
    outdir = os.path.dirname(outputfile)
    required_files = [
        os.path.join(outdir, "poisson.xdmf"),
        os.path.join(outdir, "poisson.h5"),
        os.path.join(outdir, "poisson.vtu"),
        os.path.join(outdir, "poisson_p0_000000.vtu")]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        raise RuntimeError(f"Missing output file(s): {', '.join(missing_files)}")
    
    # Try to open each file to verify they're readable
    for file_path in required_files:
        try:
            with open(file_path, 'rb') as f:
                # Just attempt to read a small part to verify file is accessible
                f.read(10)
        except Exception as e:
            print(f"Warning: File {file_path} exists but cannot be read: {e}", file=sys.stderr)
            sys.stderr.flush()

    if numdofs is not None and MPI.COMM_WORLD.rank == 0:
        with open(numdofs, "w") as handle:
            handle.write("{}\n".format(dofs))
    if return_dofs:
        return dofs


if __name__ == "__main__":
    PARSER = ArgumentParser(description="run script for the poisson problem")
    PARSER.add_argument("-m", "--mesh", required=True, help="mesh file to be used")
    PARSER.add_argument(
        "-d", "--degree", required=True, help="polynomial order to be used"
    )
    PARSER.add_argument(
        "-o",
        "--outputfile",
        required=True,
        help="file name for the output to be written",
    )
    PARSER.add_argument(
        "-n",
        "--num-dofs",
        required=False,
        default=None,
        help="file name for the number of DoFs to be written",
    )
    ARGS = vars(PARSER.parse_args())

    solve_and_write_output(
        ARGS["mesh"], int(ARGS["degree"]), ARGS["outputfile"], ARGS["num_dofs"]
    )