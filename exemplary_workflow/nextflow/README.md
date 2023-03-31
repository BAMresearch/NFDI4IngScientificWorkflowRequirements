# Nextflow
This directory contains an implementation of the exemplary workflow with [nextflow](https://nextflow.io/). 
The documentation is available under [this link](https://www.nextflow.io/docs/latest/index.html).

## Installation
Nextflow is distributed as a self-installing package, which means that it does not require any special installation procedure.
You can just download the executable package following the instructions in the [documentation](https://www.nextflow.io/docs/latest/getstarted.html#installation).
Here we create a dedicated conda environment to run the exemplary workflow with nextflow.
```
conda create --name nextflow --channel bioconda nextflow=21.04.0
```

## Running the exemplary workflow
Executing the workflow is as simple as
```
nextflow run exemplarywf.nf
```
Nextflow will install all required software specified through conda environment files for you.
Any script parameter can be specified on the command line by prefixing the parameter name with
double dash characters, e.g.
```
nextflow run exemplarywf.nf --domainSize 1.0
```
