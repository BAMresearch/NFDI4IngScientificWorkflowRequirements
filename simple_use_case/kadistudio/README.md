# KadiStudio
Implementation of the simple use case with KadiStudio.

## Installation
`KadiStudio` itself can be installed using debian packages provided. This software component
serves to model and visualise the workflow files in a GUI. To execute the workflow two software
components process_manager and process_engine are required.

They can be installed using debian packages using the following commands:
```sh
wget https://gitlab.com/iam-cms/workflows/process-manager/-/jobs/artifacts/master/download?job=pack_deb -O process_manager.zip
wget https://gitlab.com/iam-cms/workflows/process-engine/-/jobs/1764662488/artifacts/download -O process_engine.zip
unzip process_*.zip
apt-get install --yes ./build/*.deb
```
The tools used within KadiStudio are available in the python library workflow-nodes,
available with:

```sh
pip install workflow-nodes
```

## Running the simple use case

To ensure that all paths are found, execute the following commands inside the simple_use_case directory.
```sh
process_manager start simple_use_case.flow
```
