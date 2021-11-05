Workflow implemetation with CWL
===============================

The implementation with CWL relies on a suitable [Docker](docker.com) image being present, which is
not yet hosted online, but you will have to build it locally for now. Please note that also for the
execution of the workflow [Docker](docker.com) is required.

The .cwl files use a docker image with the tat `simpleusecase`. To build that image from within this
folder, type in the following commands into your terminal:

```
mkdir tmp && cd tmp
cp ../../environments/complete.yml .
cp ../../docker/Dockerfile .
docker build . -t simpleusecase
cd .. && rm -rf tmp
```

This may take some time. After a successful image build, you can execute the workflow with a CWL
interpreter. For instance, with `cwltool`:

```
cwltool --no-read-only workflow.cwl \
        --geometryfile ../source/unit_square.geo \
        --dolfinscript ../source/poisson.py \
        --pvbatchscript ../source/postprocessing.py \
        --papersource ../source/paper.tex
```
