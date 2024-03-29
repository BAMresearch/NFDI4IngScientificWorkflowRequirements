import os
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
    pr.conda_environment.create(env_name=k, env_file=v)


# Preprocessing
## generate mesh
gmsh = pr.wrap_executable(
    job_name="gmsh",
    executable_str=f"gmsh -2 -setnumber domain_size {domain_size} unit_square.geo -o square.msh",
    conda_environment_path=pr.conda_environment.preprocessing,
    input_file_lst=["../source/unit_square.geo"],
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
poisson = pr.wrap_executable(
    job_name="poisson",
    executable_str="python poisson.py --mesh square.xdmf --degree 2 --outputfile poisson.pvd --num-dofs numdofs.txt",
    conda_environment_path=pr.conda_environment.processing,
    input_file_lst=["../source/poisson.py", meshio.files.square_xdmf, meshio.files.square_h5],
    execute_job=True,
)


# Postprocessing
## plot over line
pvbatch = pr.wrap_executable(
    job_name="pvbatch",
    executable_str="pvbatch postprocessing.py poisson.pvd plotoverline.csv",
    conda_environment_path=pr.conda_environment.postprocessing,
    input_file_lst=["../source/postprocessing.py", poisson.files.poisson_pvd, poisson.files.poisson000000_vtu],
    execute_job=True,
)

## substitute macros
macros = pr.wrap_executable(
    job_name="macros",
    executable_str=f"python prepare_paper_macros.py --macro-template-file macros.tex.template --plot-data-path plotoverline.csv --domain-size {domain_size} --num-dofs {int(poisson.output['stdout'].split()[-1])} --output-macro-file macros.tex",
    conda_environment_path=pr.conda_environment.postprocessing,
    input_file_lst=["../source/macros.tex.template", "../source/prepare_paper_macros.py", pvbatch.files.plotoverline_csv],
    execute_job=True,
)

## compile paper
tectonic = pr.wrap_executable(
    job_name="tectonic",
    executable_str="tectonic paper.tex",
    conda_environment_path=pr.conda_environment.postprocessing,
    input_file_lst=["../source/paper.tex", macros.files.macros_tex, pvbatch.files.plotoverline_csv],
    execute_job=True,
)
