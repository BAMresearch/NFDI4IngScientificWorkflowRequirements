# Planemo

Planemo is a SDK for Galaxy. You can do all of `planemo's` functionality without `planemo` by just using the Galaxy API, but it is more fun with `planemo` :)

## Installation

`planemo` can be installed via `pip` or `conda`.
See the [docs](https://planemo.readthedocs.io/en/latest/installation.html) for more information.

## GitHub integration

There is a planemo-ci-action (https://github.com/galaxyproject/planemo-ci-action) that can be used in tool repos. This is for example used by various tool communities, like [IUC](https://github.com/galaxyproject/tools-iuc) or the [Muon tools](https://github.com/muon-spectroscopy-computational-project/muon-galaxy-tools).

# Visual Studio Code Integration

`planemo` is a CLI / SDK for Galaxy, but its also integrated as a language server in VSC. Check out https://github.com/galaxyproject/galaxy-language-server

## Log

The following Dockerfile can be used to reproduce the installation and expected results.
It also contains some comments that might be useful.

```
FROM python:3.10

RUN useradd -m -s /bin/bash testuser -d /home/testuser && \
    apt update && apt install -y time
USER testuser
WORKDIR /home/testuser
RUN python3 -m venv testenv
RUN . testenv/bin/activate && \
    python3 -m pip install planemo

RUN . testenv/bin/activate && \
    planemo project_init --template=demo mytools

# You can run Galaxy tools in conda, Docker, Singularity etc ... this can be configured via params.
RUN . testenv/bin/activate && \
    time planemo test --no_conda_auto_install --no_conda_auto_init --biocontainers mytools/randomlines.xml ;\
    echo "Random file returns random results, so test fails and gives a correct error message. ;)"

# Run a second time to check if the speed and if any installations are redone.
RUN . testenv/bin/activate && \
    time planemo test --biocontainers mytools/randomlines.xml ; \
    echo "Seem like everything is fine, test is done in less than a minute."

# Test the second tool.
RUN . testenv/bin/activate && \
    time planemo test --biocontainers mytools/cat.xml ; \
    echo "Seem like everything is fine, all tests passed in less than a second."

# Does linting work?
RUN . testenv/bin/activate && \
    time planemo lint mytools/randomlines.xml && \
    echo "Linting also works, nice."
```


### How to add tools

There are multiple ways how you can add tools to Galaxy. In production and the best practice is to publish your tool into the Galaxy ToolShed - this is the Galaxy Appstore with over 8000 tools.
You can use `planemo` to upload tools to the Galaxy ToolShed, e.g. with `planemo shed_upload ...`. 

Manually you can add Galaxy tools by registering the path in a config file:

[add-tool-tutorial](https://galaxyproject.org/admin/tools/add-tool-tutorial/)

In this example the tool is a perl script `toolExample.pl`. The corresponding wrapper is `toolExample.xml`.
Both are placed under `galaxyroot/tools/myTools` (need to `mkdir galaxyroot/tools/myTools`)
Add new lines to `galaxyroot/config/tool_conf.xml` to make Galaxy aware of the new tool.

You could also register directly and then Galaxy loads all tools in this directory automatically. You can also use `planemo serve` to add a tool to a temporary Galaxy instance.

### Galaxy Root

If you have a checkout of a local Galaxy git repo, you can also point `planemo` to this local checkout. This is recommended if you want to have more control over the Galaxy
version, or if you want to check against local changes to Galaxy etc. This can also save time, e.g. if you run `planemo` the first time it does not need to clone the Galaxy git repo again.

```sh
planemo test --galaxy_root /path/to/your/galaxy/
```


