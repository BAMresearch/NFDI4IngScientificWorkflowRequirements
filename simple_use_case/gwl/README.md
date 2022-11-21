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

Next, enable the GWL extension.

```sh
export GUIX_EXTENSIONS_PATH=$GUIX_ENVIRONMENT/share/guix/extensions
```

You should now be able to execute the workflow:

```
guix workflow run gwl/workflow.w
```

Subsequent runs should be much faster, since the computation environments for
each workflow step are cached.

> Instead of working in a temporary environment, it may be convenient to install
> GWL into your default Guix profile using `guix package -i gwl` and fix the
> configuration in your shells startup files.

## Using the authors Guix installation

Instead of using your current and probably more recent Guix installation, you
can also jump back in time to use the known good Guix installation from the
author.

> Please try this approach, if newer package versions in your Guix installation
> break this workflow.

To do this, pull your Guix installation to the following commit hash:

```sh
guix pull --commit=8e54584d4448d37ddf8ae995bb545a181ba2493c
```

Now you can follow the above commands.
