import pathlib
from doit.action import CmdAction

ROOT = pathlib.Path(__file__).parent
SOURCE = ROOT.parent / "source"


def task_generate_mesh():
    """generate the mesh with Gmsh"""
    geo = SOURCE / "unit_square.geo"
    msh = ROOT / "unit_square.msh"
    args = ["gmsh", "-2", "-setnumber", "domain_size", "2.0", f"{geo}", "-o", f"{msh}"]
    return {
        "file_dep": [geo],
        "actions": [CmdAction(" ".join(args), save_out="stdout")],
        "targets": [msh],
        "clean": True,
    }


def task_convert():
    """convert the mesh file from msh to xdmf format"""
    msh = ROOT / "unit_square.msh"
    return {
        "file_dep": [msh],
        "actions": [f"meshio convert {msh} {msh.with_suffix('.xdmf')}"],
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
    txtfile = ROOT / "numdofs.txt"
    return {
        "file_dep": [mesh, mesh.with_suffix(".h5"), poisson],
        "actions": [
            f"python {poisson} --mesh {mesh} --degree {degree} --outputfile {pvdfile} --num-dofs {txtfile}"
        ],
        "targets": [pvdfile, vtufile, txtfile],
        "clean": True,
    }


def task_plot_over_line():
    """write data using Paraview"""
    postproc = SOURCE / "postprocessing.py"
    pvdfile = ROOT / "poisson.pvd"
    vtufile = ROOT / (pvdfile.stem + "000000.vtu")
    pol = ROOT / "plotoverline.csv"
    return {
        "file_dep": [pvdfile, vtufile, postproc],
        "actions": [f"pvbatch {postproc} -i {pvdfile} -o {pol}"],
        "targets": [pol],
        "clean": True,
    }


def task_write_paper_source():
    """write paper source to file"""

    def write_source(gmsh_stdout, dependencies, targets):
        # file names in correct order
        fnames = ["lineplot.tex", "plotoverline.csv", "numdofs.txt"]
        deps = fix_deps(dependencies, fnames)
        preamble = """\\documentclass[12pt]{article}
\\usepackage{pgfplots}
\\usepackage{graphicx}

\\title{A simple use case}

\\newcommand\\inputplot[4]{%
    \\def\\DATA{#2}%
    \\def\\SIZE{#3}%
    \\def\\NUMDOFS{#4}%
    \\input{#1}%
}
        
\\begin{document}
\\maketitle\n
"""
        # parse stdout from task_generate_mesh to determine domain size
        s = gmsh_stdout.split("Used domain size:")[1]
        size = s.split("Used mesh size")[0]

        # read file written by task_poisson to determine number of DoFs
        with open(deps[2], "r") as handle:
            ndofs = handle.read()

        body = "\\inputplot{{{}}}{{{}}}{{{}}}{{{}}}\n".format(deps[0], deps[1], float(size), int(ndofs))
        end = "\\end{document}"
        with open(targets[0], "w") as handle:
            handle.write(preamble)
            handle.write(body)
            handle.write(end)
    return {
        "file_dep": [SOURCE / "lineplot.tex", ROOT / "plotoverline.csv", ROOT / "numdofs.txt"],
        "actions": [(write_source, [])],
        "getargs": {"gmsh_stdout": ("generate_mesh", "stdout"),},
        "targets": [ROOT / "paper.tex"],
        "clean": True,
        "verbosity": 2,
    }


def fix_deps(dependencies, fnames):
    """unfortunately the order of the `file_dep` is not guaranteed
    see https://github.com/pydoit/doit/issues/254

    Parameters
    ----------
    fnames : list of str
        The filenames in the correct order.
    """
    from pathlib import Path
    deps = [Path(d).name for d in dependencies]
    order = [deps.index(fn) for fn in fnames]
    return [dependencies[i] for i in order]


def task_paper():
    """compile pdf from latex source"""
    latexcode = ROOT / "paper.tex"
    return {
        "file_dep": [latexcode, ROOT / "plotoverline.csv", SOURCE / "lineplot.tex"],
        "actions": [f"tectonic {latexcode}"],
        "targets": [ROOT / "paper.pdf"],
        "clean": True,
    }
