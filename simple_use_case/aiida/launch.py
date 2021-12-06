import os
import pathlib
from aiida.engine import submit, run

# TODO need SinglefileData as data type
from aiida.plugins import DataFactory
from simple_use_case_workchain import SimpleUseCaseWorkChain

SinglefileData = DataFactory("singlefile")

"""
If the work chain excepted, make sure the directory containing the WorkChain
definition is in the PYTHONPATH.
You can add the folder in which you have your Python file defining the
WorkChain to the PYTHONPATH through:

$ export PYTHONPATH=/path/to/workchain/directory/:$PYTHONPATH

After this, it is very important to restart the daemon:

$ verdi daemon restart --reset

Indeed, when updating an existing work chain file or adding a new one, it is
necessary to restart the daemon every time after all changes have taken place.
"""

INPUT_DIR = pathlib.Path(os.path.realpath(__file__)).parent.parent / "source"

# TODO define all input files for the entire workflow
inputs = {"geofile": SinglefileData(file=(INPUT_DIR / "unit_square.geo").as_posix())}
result = run(SimpleUseCaseWorkChain, **inputs)
