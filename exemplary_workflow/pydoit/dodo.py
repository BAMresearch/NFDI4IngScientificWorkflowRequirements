import pathlib
from doit import get_var
from doit.action import CmdAction
from doit.tools import config_changed

ROOT = pathlib.Path(__file__).parent
SOURCE = ROOT.parent / "source"

GLOBAL_PARAMS = {"size": get_var("size", "2.0")}
DOMAIN_SIZE = GLOBAL_PARAMS["size"]

DOIT_CONFIG = {
    "action_string_formatting": "both",
    "verbosity": 2,
}


def task_generate_mesh():
    """generate the mesh with Gmsh"""
    geo = SOURCE / "unit_square.geo"
    msh = ROOT / "unit_square.msh"
    args = [
        "gmsh",
        "-2",
        "-setnumber",
        "domain_size",
        f"{DOMAIN_SIZE}",
        f"{geo}",
        "-o",
        f"{msh}",
    ]
    return {
        "file_dep": [geo],
        "actions": [CmdAction(" ".join(args), save_out="stdout")],
        "targets": [msh],
        "clean": True,
        "uptodate": [config_changed(DOMAIN_SIZE)],
    }


def task_get_domain_size():
    """parse stdout of the task `task_generate_mesh` and return domain size as float"""

    def parse(stdout):
        s = stdout.split("Used domain size:")[1]
        size = float(s.split("Used mesh size")[0])
        return {"size": size}

    return {
        "actions": [(parse,)],
        "getargs": {"stdout": ("generate_mesh", "stdout")},
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


def task_get_num_dofs():
    """reads number of degrees of freedom and returns it as integer"""

    def read(dependencies):
        with open(dependencies[0], "r") as handle:
            num_dofs = int(handle.read())

        return {"num_dofs": num_dofs}

    return {
        "file_dep": [ROOT / "numdofs.txt"],
        "actions": [(read,)],
    }


def task_plot_over_line():
    """write data using Paraview"""
    postproc = SOURCE / "postprocessing.py"
    pvdfile = ROOT / "poisson.pvd"
    vtufile = ROOT / (pvdfile.stem + "000000.vtu")
    pol = ROOT / "plotoverline.csv"
    return {
        "file_dep": [pvdfile, vtufile, postproc],
        "actions": [f"pvbatch {postproc} {pvdfile} {pol}"],
        "targets": [pol],
        "clean": True,
    }


def task_substitute_macros():
    """places the correct values into the paper macros"""
    script = SOURCE / "prepare_paper_macros.py"
    file_deps = {
        "--macro-template-file": SOURCE / "macros.tex.template",
        "--plot-data-path": ROOT / "plotoverline.csv",
    }

    def create_cmd():
        cmd = f"python {script}"
        for key, value in file_deps.items():
            cmd += f" {key} {value}"
        cmd += " --domain-size {size}"
        cmd += " --num-dofs {num_dofs}"
        cmd += " --output-macro-file {targets}"
        return cmd

    return {
        "file_dep": [script] + list(file_deps.values()),
        "actions": [create_cmd()],
        "getargs": {
            "size": ("get_domain_size", "size"),
            "num_dofs": ("get_num_dofs", "num_dofs"),
        },
        "targets": [ROOT / "macros.tex"],
        "clean": True,
    }


def task_paper():
    """compile pdf from latex source"""
    paper_source = SOURCE / "paper.tex"
    paper = ROOT / "paper.tex"
    return {
        "file_dep": [paper_source, ROOT / "macros.tex", ROOT / "plotoverline.csv"],
        "actions": [f"cp {paper_source} {paper}", f"tectonic {paper}"],
        "targets": [paper, ROOT / "paper.pdf"],
        "clean": True,
    }
