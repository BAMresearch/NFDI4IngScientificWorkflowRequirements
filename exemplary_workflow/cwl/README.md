Workflow implemetation with CWL
===============================

The implementation with CWL requires that all the dependencies are provided by the environment.
If you have [`miniconda`](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
installed, you can simply create a respective environment by typing

```sh
conda env create --file default_env.yml --prefix ./exemplarywf
conda activate ./exemplarywf
```

Note that by specifying the `--prefix` option you can simply remove all downloaded packages afterwards
by removing the folder given to `prefix`. To execute the workflow after activating the environment,
simply type

```sh
cwltool wf_run_exemplary_wf.cwl
```

into your terminal.

Or you can use the conda dependency feature of the CWL reference runner to obtain
the dependencies dynamically:

```sh
cwltool --beta-conda-dependencies wf_run_exemplary_wf.cwl
```

Note that there exist tools to visualize, edit or create cwl workflows. For instance, you can
visualize workflows contained in git repositories with [view.commonwl.org](https://view.commonwl.org/),
or you can use the [Rabix Composer](https://github.com/rabix/composer) to compose workflows locally
on your machine.

Example: ![Workflow Diagram](workflow.svg)
[source](https://view.commonwl.org/workflows/github.com/BAMresearch/NFDI4IngScientificWorkflowRequirements/blob/main/exemplary_workflow/cwl/wf_run_exemplary_wf.cwl)
