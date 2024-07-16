import os
import shutil
from pyiron_base import Project

# input parameter 
domain_size = 2.0

# create pyiron project 
pr = Project("workflow")

# create conda environments for the proprocessing, processing and postprocessing stage 
for k, v in {
    "preprocessing": "../source/envs/preprocessing.yaml",
    "processing": "../source/envs/processing.yaml",
    "postprocessing": "../source/envs/postprocessing.yaml"
}.items():
    pr.conda_environment.create(env_name=k, env_file=v, global_installation=False)


# Preprocessing
## generate mesh
gmsh = pr.wrap_executable(
    executable_str=f"gmsh -2 -setnumber domain_size {domain_size} unit_square.geo -o square.msh",
    conda_environment_path=pr.conda_environment.preprocessing,
    input_file_lst=["../source/unit_square.geo"],
    delayed=True,
    output_file_lst=["square.msh"],
)

## convert mesh to xdmf
meshio = pr.wrap_executable(
    executable_str="meshio convert square.msh square.xdmf",
    conda_environment_path=pr.conda_environment.preprocessing,
    input_file_lst=[gmsh.files.square_msh],
    delayed=True,
    output_file_lst=["square.xdmf", "square.h5"],
)


# Processing
## poisson
def collect_output(working_directory):
    with open(os.path.join(working_directory, "numdofs.txt"), "r") as f:
        return {"numdofs": int(f.read())}

poisson = pr.wrap_executable(
    executable_str="python poisson.py --mesh square.xdmf --degree 2 --outputfile poisson.pvd --num-dofs numdofs.txt",
    conda_environment_path=pr.conda_environment.processing,
    input_file_lst=["../source/poisson.py", meshio.files.square_xdmf, meshio.files.square_h5],
    delayed=True,
    collect_output_funct=collect_output,
    output_key_lst=["numdofs"],
    output_file_lst=["poisson.pvd", "poisson000000.vtu"],
)


# Postprocessing
## plot over line
pvbatch = pr.wrap_executable(
    executable_str="pvbatch postprocessing.py poisson.pvd plotoverline.csv",
    conda_environment_path=pr.conda_environment.postprocessing,
    input_file_lst=["../source/postprocessing.py", poisson.files.poisson_pvd, poisson.files.poisson000000_vtu],
    delayed=True,
    output_file_lst=["plotoverline.csv"],
)

## substitute macros
def write_input(input_dict, working_directory):
    script_name = os.path.join(working_directory, "macros.sh")
    with open(script_name, "w") as f:
        f.writelines(f"python prepare_paper_macros.py --macro-template-file macros.tex.template --plot-data-path plotoverline.csv --domain-size {domain_size} --num-dofs {input_dict["numdofs"]} --output-macro-file macros.tex")
    os.chmod(script_name, 0o744)

macros = pr.wrap_executable(
    input_dict={"numdofs": poisson.output.numdofs},
    write_input_funct=write_input,
    executable_str="./macros.sh",
    conda_environment_path=pr.conda_environment.postprocessing,
    input_file_lst=["../source/macros.tex.template", "../source/prepare_paper_macros.py", pvbatch.files.plotoverline_csv],
    delayed=True,
    output_file_lst=["macros.tex"],
)

## compile paper
tectonic = pr.wrap_executable(
    executable_str="tectonic paper.tex",
    conda_environment_path=pr.conda_environment.postprocessing,
    input_file_lst=["../source/paper.tex", macros.files.macros_tex, pvbatch.files.plotoverline_csv],
    delayed=True,
    output_file_lst=["paper.pdf"],
)

# Execute Workflow Graph and copy output
tectonic.pull()
shutil.copyfile(str(tectonic.files.paper_pdf), "paper.pdf")
