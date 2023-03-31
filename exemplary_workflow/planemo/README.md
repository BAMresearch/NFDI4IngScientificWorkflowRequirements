# Planemo

## Installation

`planemo` can be installed via `pip` or `conda` (experimental).
See the [docs](https://planemo.readthedocs.io/en/latest/installation.html)
for more information.


## Log

### Attempt 1 via conda
The following commands were executed.
If not stated explicitly everything worked as intended.

Creation of the conda env:
```sh
mamba create -n planemo -c bioconda planemo
```
Init demo project:
```sh
planemo project_init --template=demo mytools
cd mytools
```

```sh
planemo lint
planemo lint randomlines.xml
```
This gives an AttributeError.

```sh
planemo test randomlines.xml
```
raises ImportError.

Installation via `conda` seems to be broken.

### Attempt 2 via pip

1. deactivate conda.
2. follow install guide for pip.

```sh
planemo l randomlines.xml
```
seems to be okay.

```sh
planemo test randomlines.xml
```
git clone bare repos into `/home/pdiercks/.planemo/gx_repo`
downloads a whole lot of packages ...
... it installs miniconda3 ... wtf
... there is a lot of useless output.
... in the end 1 of 2 tests fails. nice demo.

```sh
planemo l ./run_dolfin.cwl
```
does not work because Node.js engine is required to
evaluate and validate JavaScript Expressions

+ Loading cwltool is also experimental.
+ Linting of xml fails without hint why this might be the case.

### What worked for me

1. `git clone git@github.com:galaxyproject/galaxy.git ./galaxyroot`
2. `export GR=/home/pdiercks/repos/galaxyroot`
3. `cd /home/pdiercks/projects/planemo_demo/seqtk_example`
4. `planemo test --galaxy_root $GR`
5. `planemo serve --galaxy_root $GR`

Any command like `planemo test | serve | run` will spin
up the galaxy instance. This takes quite some time even
if `--galaxy_root` is specified.
Basically all packages are uninstalled and installed again each time.

#### Problem with planemo run

FileNotFoundError: [Errno 2] No such file or directory: '/home/pdiercks/repos/galaxyroot/.venv/bin/galaxyctl'

after I tried running one of the test workflows via:
```sh
 ❯ planemo run --galaxy_root $GR tutorial.ga tutorial-job.yml --download_outputs --output_directory . --output_json output.json
```

### How to add tools

[add-tool-tutorial](https://galaxyproject.org/admin/tools/add-tool-tutorial/)

in this example the tool is a perl script `toolExample.pl`.
the corresponding wrapper is `toolExample.xml`.
Both are placed under `galaxyroot/tools/myTools` (need to `mkdir galaxyroot/tools/myTools`)
Add new lines to `galaxyroot/config/tool_conf.xml` to make galaxy aware of the new tool.

### Galaxy Root

```sh
cd $galaxy_root && sh run.sh
```
can also be used to setup a Galaxy instance ...
it found my installation of mambaforge and installed
a virtualenv using that. (`~/mambaforge/envs/_galaxy_`)

However, there were several errors and it fails.
This does not work.
Probably because one has to set the path for non-conda
python somehow and the virtualenv is faulty.

I guess `planemo serve --galaxy_root` shoud be equivalent
to `sh run.sh` only that here I have the virtualenv setup correctly.


### Purge

Delete the following to remove galaxy later on:
1. `~/repos/galaxyroot`
2. `~/.planemo`
3. `~/mambaforge/envs/_galaxy_`
