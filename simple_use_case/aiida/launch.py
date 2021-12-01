from aiida.engine import run, submit
# TODO need SinglefileData as data type
from aiida.plugins import DataFactory
from simple_use_case_workchain import SimpleUseCaseWorkChain
SinglefileData = DataFactory("singlefile")

# TODO define all input files for the entire workflow
inputs = {}
result = submit(SimpleUseCaseWorkChain, **inputs)
