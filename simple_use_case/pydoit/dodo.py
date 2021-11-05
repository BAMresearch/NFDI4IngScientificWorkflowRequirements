import pathlib

ROOT = pathlib.Path(__file__).parent
SOURCE = ROOT.parent / "source"


def task_mesh():
    """generate the mesh with Gmsh"""
    geo = SOURCE / "unit_square.geo"
    msh = ROOT / "unit_square.msh"
    args = ["gmsh", "-2", "-order", "1", "-format", "msh2", f"{geo}", "-o", f"{msh}"]
    return {
        "file_dep": [geo],
        "actions": [" ".join(args)],
        "targets": [msh],
        "clean": True,
    }


def task_convert():
    """convert the mesh file from msh to xdmf format"""
    msh = ROOT / "unit_square.msh"
    return {
        "file_dep": [msh],
        "actions": [f"meshio-convert {msh} {msh.with_suffix('.xdmf')}"],
        "targets": [msh.with_suffix(".xdmf"), msh.with_suffix(".h5")],
        "clean": True,
    }


def task_poisson():
    """solve the poisson equation with fenics"""
    poisson = SOURCE / "poisson.py"
    mesh = ROOT / "unit_square.xdmf"
    degree = 2
    pvdfile = ROOT / "poisson.pvd"
    vtufile = ROOT / (pvdfile.stem + "000000.vtu")
    return {
        "file_dep": [mesh, mesh.with_suffix(".h5"), poisson],
        "actions": [
            f"python {poisson} --mesh {mesh} --degree {degree} --outputfile {pvdfile}"
        ],
        "targets": [pvdfile, vtufile],
        "clean": True,
    }


def task_contourplot():
    """make a contourplot using Paraview"""
    postproc = SOURCE / "postprocessing.py"
    pvdfile = ROOT / "poisson.pvd"
    vtufile = ROOT / (pvdfile.stem + "000000.vtu")
    contour = ROOT / "contourplot.png"
    return {
        "file_dep": [pvdfile, vtufile, postproc],
        "actions": [f"pvbatch {postproc} {pvdfile} {contour}"],
        "targets": [contour],
        "clean": True,
    }


def task_copy_paper():
    """copy paper.tex from source directory"""
    source_code = SOURCE / "paper.tex"
    root_code = ROOT / "paper.tex"
    return {
        "actions": [f"cp {source_code} {root_code}"],
        "targets": [root_code],
        "clean": True,
    }


def task_paper():
    """compile pdf from latex source"""
    latexcode = ROOT / "paper.tex"
    return {
        "file_dep": [latexcode, ROOT / "contourplot.png"],
        "actions": [f"tectonic {latexcode}"],
        "targets": [ROOT / "paper.pdf"],
        "clean": True,
    }
