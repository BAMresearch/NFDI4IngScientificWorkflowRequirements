# Snakemake
Some notes on my user/learning experience with snakemake.

## Paper
* improved readability due to domain specific language (DSL) (+) (*transparency*, *adaptability*); assumption: for user with no prior knowledge it is easier to learn/understand DSL instead of programming language
* DSL obviates superfluous operators or boilerplate code (+, example?)
* includes deployment of software stack (conda env that is automatically installed; singularity or docker containers) (++) (*portability*)
* automatic containerization; Dockerfile that deploys all defined conda environments into the container (+); size problem with this container?
* parallel execution of the workflow is easy (+) (*scalability-parallelism*)
* how do I execute a snakemake workflow on a HPC machine? (*scalability-platform*)
* directed acyclic graph (DAG) is obtained by snakemake and can be visualized easily (+)
* automated unit test generation (?)
* automatically generated interactive reports (+)
* inclusion of other Snakefiles and workflow composition
* integration of scripts and jupyter notebooks as well as use of tool wrappers which can be shared via a central public repository (++); usually tools provide one of the two, but having both seems like a big advantage
* arbitrary python code can be used to define task metadata, but for certain use cases (presumably typical processes in data analysis) Snakemake explicitly defines directives to be used (see section 3.2 scatter/gather processes)


## Tutorial
* Snakemake wants to re-run the job after changes to the file modification date (-):
```
touch data/samples/A.fastq
```
The job is re-run although the file's contents did not change.
(With `pydoit` this is not the case.)
Isn't this contradictory to section 2.5.2 "Caching between workflows" in the snakemake paper? No, first check if outputfile with certain hash value exists in the cache. If it exists, check whether one of the inputs is newer and re-run if this is the case.

* snakemake automatically creates missing directories (+)
* when executing a the workflow one does not specify the name of the rule, but the name of the target. Hence, one can run the same workflow using different targets. This is different to e.g. pydoit, but does not make a big difference. (Think of wildcards as task generators)
* script integration: boilerplate code like parsing of CL arguments in the python script becomes unnecessary (+); this is in contrast to python script execution like `python <script.py> [options] A B`; however, this makes the script specific to the tool snakemake, I could not use the same script in another workflow tool (-); this also requires the user to use snakemake from the beginning
* Apart from filenames, Snakemake also accepts rule names as targets if the requested rule does not have wildcards.
* if no target is given at the command line, Snakemake will define the first rule of the Snakefile as the target
* How can I debug the Snakefile?
* Dependencies are on targets? (not on tasks?)
* configuration files in JSON or YAML format for customization of workflows
* using `config["samples"]` (dict) instead of `SAMPLES` (list) in rule *bcftools_call* confuses me
* How can I show info about some rule using the CLI? E.g. show all input files for rule xy?
* Step 3 of the Advanced Tutorial is unclear: normally I can use wildcards for input file definition, but not when a configuration file is used?
* expand functions are executed during initialization phase; input functions are executed during DAG phase ...
* only input files (not output!) can be specified as functions


### Wildcards
```
snakemake -np mapped_reads/B.bam
```
defines the output file `mapped_reads/B.bam` for a job generated from rule `bwa_map`. 
The wildcard `{sample}` is filled in with the value `B` given in the command.
This value is then propagated to find and check for appropriate input files (and not the other way around, like a file pattern matching ...).
* What is the point of using an input function if in the output file definition a wildcard is used?


## Test case implementation
In contrast to the `pydoit` implementation, the single conda environment is split in several environments since with `snakemake` it is possible to specify a conda environment for each rule. 
This has the benefit of modularization and later on the option to automatically write a Dockerfile (`--containerize`).
At the time of writing there is however a [bug](https://github.com/snakemake/snakemake/issues/1210) which is fixed but the PR not included in the latest version (6.10.0) of snakemake.

### Execution
```
snakemake --cores 1 --use-conda postprocessing/paper.pdf
```
The number of cores always needs to be specified. `--use-conda` is False by default.
Other useful options are `--dryrun, -n` for a dry-run and `--printshellcmds, -p` to print out shell commands that will be executed.  For more help `snakemake --help` of course.
The current Snakefile implementation requires the user to explicitly define the target `postprocessing/paper.pdf` such that an appropriate job can be generated from the rule `compile`.
