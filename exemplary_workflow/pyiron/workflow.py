import os
from pyiron_base import Project


# create pyiron project 
pr = Project("workflow")

# create conda environments for the proprocessing, processing and postprocessing stage 
for k, v in {
    "preprocessing": "../source/envs/preprocessing.yaml",
    "processing": "../source/envs/processing.yaml",
    "postprocessing": "../source/envs/postprocessing.yaml"
}.items():
    pr.conda_environment.create(env_name=k, env_file=v)


# Preprocessing

## generate mesh
def write_input(input_dict, working_directory):
    script_name = os.path.join(working_directory, "gmsh.sh")
    with open(script_name, "w") as f:
        f.writelines("gmsh -2 -setnumber domain_size " + str(input_dict["domain_size"]) + " unit_square.geo -o square.msh")
    os.chmod(script_name, 0o744)

gmsh = pr.wrap_executable(
    job_name="gmsh",
    executable_str="./gmsh.sh",
    write_input_funct=write_input,
    input_dict={"domain_size": 2.0},
    conda_environment_path=pr.conda_environment.preprocessing,
    input_file_lst=["source/unit_square.geo"],
    execute_job=True,
)


## convert mesh to xdmf
meshio = pr.wrap_executable(
    job_name="meshio",
    executable_str="meshio convert square.msh square.xdmf",
    conda_environment_path=pr.conda_environment.preprocessing,
    input_file_lst=[gmsh.files.square_msh],
    execute_job=True,
)


# Processing
## poisson
def collect_output(working_directory):
    with open(os.path.join(working_directory, "numdofs.txt"), "r") as f:
        return {"numdofs": int(f.read())}

poisson = pr.wrap_executable(
    job_name="poisson",
    executable_str="python poisson.py --mesh square.xdmf --degree 2 --outputfile poisson.pvd --num-dofs numdofs.txt",
    collect_output_funct=collect_output,
    conda_environment_path=pr.conda_environment.processing,
    input_file_lst=["source/poisson.py", meshio.files.square_xdmf, meshio.files.square_h5],
    execute_job=True,
)


# Postprocessing
## plot over line
pvbatch = pr.wrap_executable(
    job_name="pvbatch",
    executable_str="pvbatch postprocessing.py poisson.pvd plotoverline.csv",
    conda_environment_path=pr.conda_environment.postprocessing,
    input_file_lst=["source/postprocessing.py", poisson.files.poisson_pvd, poisson.files.poisson000000_vtu],
    execute_job=True,
)

## substitute macros
def write_input(input_dict, working_directory):
    script_name = os.path.join(working_directory, "macros.sh")
    with open(script_name, "w") as f:
        f.writelines("python prepare_paper_macros.py --macro-template-file macros.tex.template --plot-data-path plotoverline.csv --domain-size " + str(input_dict["domain_size"]) + " --num-dofs " + str(input_dict["numdofs"]) + " --output-macro-file macros.tex")
    os.chmod(script_name, 0o744)

macros = pr.wrap_executable(
    job_name="macros",
    executable_str="./macros.sh",
    write_input_funct=write_input,
    input_dict={"domain_size": 2.0, "numdofs": 100},
    conda_environment_path=pr.conda_environment.postprocessing,
    input_file_lst=["source/macros.tex.template", "source/prepare_paper_macros.py", pvbatch.files.plotoverline_csv],
    execute_job=True,
)

## compile paper
tectonic = pr.wrap_executable(
    job_name="tectonic",
    executable_str="tectonic paper.tex",
    conda_environment_path=pr.conda_environment.postprocessing,
    input_file_lst=["source/paper.tex", macros.files.macros_tex, pvbatch.files.plotoverline_csv],
    execute_job=True,
)


