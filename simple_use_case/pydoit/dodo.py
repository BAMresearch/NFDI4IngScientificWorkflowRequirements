import os
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
    target = ROOT / "poisson.xdmf"
    return {
        "file_dep": [mesh, mesh.with_suffix(".h5"), poisson],
        "actions": [f"python {poisson} --mesh {mesh} --degree {degree} --output={target}"],
        "targets": [target, target.with_suffix(".h5")],
        "clean": True,
    }


def trim_it(targets):
    args = ["convert", "-trim", targets[0], targets[1]]
    os.system(" ".join(args))


def task_contourplot():
    """make a contourplot using Paraview"""
    postproc = SOURCE / "postprocessing.py"
    dep = ROOT / "poisson.xdmf"
    contour = ROOT / "contourplot.png"
    trimmed = ROOT / "contourplot_trimmed.png"
    return {
        "file_dep": [dep, dep.with_suffix(".h5"), postproc],
        "actions": [f"pvbatch {postproc} {dep} {contour}", (trim_it, [])],
        "targets": [contour, trimmed],
        "clean": True,
    }


def task_paper():
    """compile pdf from latex source"""
    latexcode = ROOT / "paper.tex"
    return {
        "file_dep": [ROOT / "contourplot_trimmed.png"],
        "actions": [f"latexmk -pdf -cd {latexcode}"],
        "targets": [ROOT / "paper.pdf"],
        "clean": True,
    }
