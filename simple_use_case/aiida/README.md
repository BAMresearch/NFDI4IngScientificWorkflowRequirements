AiiDA
=====

Installation
------------
TODO add installation instructions

Running the simple use case workflow
------------------------------------
To run the `SimpleUseCaseWorkChain` make sure that a suitable environment
which all required software is activated.
The workflow can then be run with
```
verdi run launch.py
```
Useful commands:
```
verdi process list -a           # lists all processes
verdi process show <PK>         # show info about process
verdi process report <PK>       # log messages if something went wrong
verdi node show <PK>            # show info about node
verdi node graph generate <PK>  # generate provenance graph for node
```
