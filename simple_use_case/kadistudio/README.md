# KadiStudio
Implementation of the simple use case with KadiStudio. `KadiStudio` is a software component of the
Kadi4Mat research data infrastructure, that is dedicated to model, visualise and execute scientific workflows using a GUI.

## Installation
`KadiStudio` can be installed using the debian package provided [here](https://bwsyncandshare.kit.edu/s/cJSZrE6fDTR6cLQ).
To execute a workflow in KadiStudio, the two software components `process-manager` and `process-engine` are
required. They are available as debian packages and can be installed using the following commands:

```sh
wget https://gitlab.com/iam-cms/workflows/process-manager/-/jobs/artifacts/master/download?job=pack_deb -O process_manager.zip
wget https://gitlab.com/iam-cms/workflows/process-engine/-/jobs/1764662488/artifacts/download -O process_engine.zip
unzip process_*.zip
apt-get install --yes ./build/*.deb
```

The process-manager is a software component dedicated to orchestrate the execution of workflows. It does not read or interpret
workflow files but only delegates their execution to a suitable process-engine and checks the execution status frequently. This
serves as a layer of abstraction between the workflow editor KadiStudio and the process-engines and allows the use of different
process-engines depending on the current use case.

The process-engine on the other hand is responsible for reading, interpreting and executing the workflow file that it is handed by
the process-manager. Different implementations of the process-engine are conceivable that are suitable for certain use cases such as
parallel execution, remote execution etc.. The currently available process-engine, used in this example, executes all tools contained
in the workflow file sequentially in the order derived from the green dependency ports visible in the image below.

The tools used within KadiStudio are collected in the python library `workflow-nodes`, that can be installed with:

```sh
pip install workflow-nodes
```
This library is necessary, as KadiStudio needs a machine readable description of the used tools to be able to visualise them inside
the GUI. Adding this description to existing tools can be implemented using wrapper scripts. Already implemented wrapper scripts for
certain tools can be found inside the workflow-nodes library which can be extended by users as desired. A more detailed documentation
of the workflow-nodes project as well as the description of how to add new tools can be found [here](https://pypi.org/project/workflow-nodes/).

## Creating workflows

Workflows can be created in KadiStudio using a GUI to which tools can be added using a point-and-click interface.
In the gif below this is exemplified by the simple use case.

![workflow creation](workflowCreation.gif)

Each added tool represents a command that is run when the workflow is executed. Using the input ports on the
left-hand side the corresponding tool can be parameterised. Connecting the green dependency ports of the tools
nodes defines the order of execution making the modelled workflow easier to grasp for the user.

The complete workflow saved in the simple_use_case.flow file is shown in the following image.
![workflow creation](WorkflowNFDI4Ing.png)

## Running the simple_use_case workflow

The execution of a workflow is recommended to be started inside the GUI of KadiStudio, as it offers the possiblity to easily
track its status and to interact with the workflow in case a user input is required. When starting a workflow inside KadiStudio the
following command is executed:

```sh
process_manager start simple_use_case.flow
```

Thus, if KadiStudio is not available or its GUI cannot be displayed, it is also possible to start a workflow directly from a terminal
using the command above. Alternatively, it is also possible to start a workflow directly by passing it to a process-engine using
the command:

```sh
process_engine run simple_use_case.flow -p /path/to/execution_folder
```

However, using the process-engine directly is not recommended, as the background tasks initiated by the process-manager when executing a
workflow are omitted in this case. This can lead to overwriting data when executing a workflow several times.

### Command line execution -- Necessary configuration

The workflow saved in the simple_use_case.flow file was specifically modelled to run inside the actions of this github project.
For this the variable GITHUB_WORKSPACE was used to reliably access the folder structure of the container that runs the workflow.
To be able to run the workflow manually it is therefore necessary to set this variable on your machine as well. This can
be done using the command:

```sh
export GITHUB_WORKSPACE="/path/to/NFDI4IngScientificWorkflowRequirements"
```

This path might vary depending on your folder structure. Its only essential point is that it directs to the folder in which
the simple_use_case folder is located. When executing the simple_use_case workflow inside the GUI of KadiStudio, setting this variable
can be omitted as a check whether the $GITHUB_WORKSPACE is known is performed before execution. In case it is unknown, the user will
be prompted to enter the path to the NFDI4IngScientificWorkflowRequirements folder interactively.


## Visualisation of the workflow

The workflow files can be visualised inside KadiStudio or on Kadi4Mat.
A screenshot of the workflow can be seen in the image above.
