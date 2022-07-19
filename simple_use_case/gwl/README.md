# Workflow implementation with GWL

[`GWL`](https://guixwl.org) requires a [`Guix`](https://guix.gnu.org)
installation on your system.

The following steps assume that your current working directory is the
[gwl](.) directory of this repository:

```sh
cd simple_use_case/gwl
```

## Using your Guix installation

You are encouraged to execute the workflow with your current Guix installation
(potentially using recent packages).

First, create a temporary environment with GWL:

```sh
guix shell gwl
```

> If your Guix installation doesn't support the `shell` command, please upgrade
> your installation via `guix pull`.

This will spawn a new shell, in which GWL is available.

Next, configure both GWL and Guix.

```sh
export GUIX_EXTENSIONS_PATH=$GUIX_ENVIRONMENT/share/guix/extensions
export GUIX_PACKAGE_PATH=../build-aux/gwl guix workflow run gwl/workflow.w
```

GWL will use Guix to construct the compute environment on your system. At the
time of this writing, the packages `cgns` and `paraview` are not available in
Guix upstream. These packages are provided locally via the `GUIX_PACKAGE_PATH`
environment variable in [sigfwtools.scm](../../build-aux/gwl/sigwftools.scm) for
the time being. Upstreaming these packages is work-in-progress.

You should now be able to execute the workflow. Since `cgns` and `paraview` need
to be compiled, this will take a long time:

```
guix workflow run gwl/workflow.w
```

Subsequent runs should be much faster, since the compilation results are cached.

> Instead of working in a temporary environment, it may be convenient to install
> GWL into your default Guix profile using `guix package -i gwl` and fix the
> configuration in your shells startup files.

## Using the authors Guix installation

Instead of using your current and probably more recent Guix installation, you
can also jump back in time to use the known good Guix installation from the
author.

> Please try this approach, if newer package versions in your Guix installation
> break this workflow.

Replace the `guix shell gwl` step with this:

```sh
guix time-machine --commit=5f856c595479c30d9ccdb0063c9124248fdcf5c2 -- shell guix gwl
```

This will spawn a shell with the Guix and GWL versions of the author, in which
you can follow the remaining commands from above.
