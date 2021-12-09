Workflow implemetation with CWL
===============================

The implementation with CWL requires that all the dependencies are provided by the environment.
If you have [`miniconda`](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
installed, you can simply create a respective environment by typing

```sh
conda env create --file default_env.yml --prefix ./simpleusecase
conda activate simpleusecase
```

Note that by specifying the `--prefix` option you can simply remove all downloaded packages afterwards
by removing the folder given to `prefix`. To execute the workflow after activating the environment,
simply type

```sh
cwltool wf_run_use_case.cwl
```

into your terminal.
