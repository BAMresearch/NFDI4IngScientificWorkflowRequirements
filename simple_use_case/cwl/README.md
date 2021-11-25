Workflow implemetation with CWL
===============================

The implementation with CWL relies on a suitable [Docker](docker.com) image being present, which is
not yet hosted online, but you will have to build it locally for now. Please note that also for the
execution of the workflow [Docker](docker.com) is required.

Two workflow files are contained in this folder, namely `wf_build_docker_image.cwl` and
`wf_run_use_case.cwl`. Execute the first one with a cwl interpreter, e.g.
`cwltool wf_build_docker_image.cwl`, to prepare the docker image on your machine. This may take
some time, but has to be done only once. The workflow accepts urls for the dockerfile and conda
environment file to be used upon image creation, settable via the command line parameters
`dockerfile-url` and `envfile-url`. This allows testing e.g. different environment files that
we host in this repository.

After a successful image build, you can execute the workflow. For instance, with
`cwltool --no-read-only wf_run_use_case.cwl`. The `no-read-only` flag is necessary because inside
the container a conda environment is activated, which requires write access.
