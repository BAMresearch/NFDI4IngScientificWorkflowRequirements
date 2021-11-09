Nextflow
========
Some notes about [nextflow](https://nextflow.io/). The documentation is available under [this link](https://www.nextflow.io/docs/latest/index.html).

Wratten et Al.
--------------
* domain specific language (DSL) based on the groovy programming language
* steps of a pipeline split into modular components and connected through channels that determine pipeline execution (dataflow paradigm)
* ability to create reusable modules for steps of the workflow
* active community with a large number of published ready-to-use pipelines (refs. 63-66)
* nf-core project: community-curated pipelines; framework to host nextflow pipelines, which requires best practices and sets standards for pipeline implementations to guarantee their maintenance, documentation, portability, scalability, and reproducibility
* curated pipelines are citable (often with Zenodo DOI) 

Di Tommaso et Al.
-----------------
* sources of irreproducibility: lack of good practice pertaining to software and database usage, variations across computational platforms
* nextflow uses Docker technology for the multi-scale handling of containerized computation
* another challenge: handling a large number of software packages and conflicting requirements of frequent software updates and maintaining the reproducibility of original results
* high-throughput: how to deal with intermediate files?
* nextflow is designed to address numerical instability, efficient parallel execution, error tolerance, execution provenance and traceability
* existing pipelines written in any scripting language
* multi-scale containerization, which makes it possible to bundle entire pipelines, subcomponents and individual tools into their own containers, is essential for numerical stability
* containers can be produced *ad hoc* by users or by following recently proposed standards (BioBoxes, Bioshadock and AlgoRun)
* integration with software repositories (GitHub, BitBucket)
* native support for cloud systems
* consequence of the prior 2 points: ability to run any current or previous version of a pipeline/workflow
* nextflow relies on the dataflow programming paradigm, which, according to the authors, is superior to alternative solutions based on a Make-like approach (such as Snakemake, pyDoit, ...)
* Make-like procedure requires a DAG while nextflow does not ("top to bottom processing model follows the natural flow of data")
* unclear: how does nextflow determine which processes are not uptodate? skip certain tasks?
* outputs are not limited to files but can also include in-memory values and data objects
* example genomic analysis: differences in "native" workflow execution and containerization as solution; what is the truth? docker image is also based on some operating system ...
* table 1 is not up to date (by now Snakemake supports Docker)
