.. _requirements:

Requirements on workflow tools
==============================

In this section, we want to translate the aspects discussed in :ref:`fairness`
into possible capabilities that workflow tools should provide in order to
fulfill these aspects.

.. contents::

.. _requirements_execution:

Execution
---------
The workflow tool should automatically execute the scientific workflow, i.e.\ the processes that make up the workflow should be executed in the correct order to satisfy dependencies between them.
To this end, a directed acyclic graph (DAG; dependency-graph) should be created and stored for later tracing and visualisation of specific instances of a workflow execution (see also :ref:`requirements_provenance`.
Moreover, the (possible) reuse of already computed results is an important feature with regard to the execution of the workflow, but also handled quite differently by the investigated tools.
Therefore, this is listed as a separate requirement (see :ref:`requirements_uptodateness`).
In this requirement, it is focused on how (easily) the execution of the workflow either locally (your computer) or on a remote machine (HPC cluster or cloud) can be integrated.
Note, that this relates to the configuration of remote machines and e.g. the ressource manager on a HPC cluster or the cloud computing service with the workflow tool rather than the actual execution, since for this a suitable compute environment needs to be instantiated which is covered in :ref:`requirements_compute_environment`.
Ideally, the workflow can be executed anywhere without changing the workflow definition script apart from small changes (one-liner) related to the workflow tool configuration file.

Evaluation criteria:

1. The workflow system supports the execution of the workflow on the local system.
2. The workflow system supports the execution of the workflow on the local system via a batch system.
3. The workflow system supports the execution of the workflow via a batch system on the local or a remote system.

.. _requirements_monitor:

Monitoring
----------
Depending on the application, the execution of scientific workflows can be very time-consuming. This can be caused by compute-intensive processes,
such as e.g. numerical simulations, or by a large number of short processes that are executed many times. In both cases, it can be very helpful to
be able to query the state of the execution, that is, which processes have been finished, which processes are currently being processed, and which
are still pending. A trivial way of such monitoring would be, for instance, when the workflow is started in a terminal which is kept open to inspect
the output written by the workflow system and the running processes. However, ideally, the workflow system allows for submission of the workflow in
the form of a process running in the background, while still providing means to monitor the state of the execution.

Evaluation criteria:

1. Only way to monitor the workflow is to watch the console output
2. The workflow system provides a way to query the execution status at any time

.. _requirements_provenance:

Data provenance
---------------
The data provenance graph contains, for a particular execution of the workflow, which data and processes participated in the generation of a particular
piece of data. Thus, this is closely related to the workflow itself, which can be thought of as a template for how that data generation should take place.
However, a concrete realization of the workflow must contain information on the exact input data and parameters that were used, possibly along with meta
information on the person that executed the workflow, the compute ressources used and the time it took to finish. Collection of all relevant information,
its storage in machine-readable formats and subsequent publication alongside the data can be very useful for future researchers in order to understand
how exactly the data was produced. Ideally, the workflow system has the means to automatically collect this information upon workflow execution.

Evaluation criteria:

1. The workflow system provides no means to export relevant information from a particular execution
2. Upon workflow execution, the tool writes metadata files alongside the results, overwriting them upon re-execution
3. Produced data is stored in a database, allowing to uniquely associate produced data with particular workflow instantiations


.. _requirements_compute_environment:

Compute environment
-------------------
In order to guarantee interoperability and reproducibility of scientific workflows, the workflows need to be executable by others.
Here, the reinstantiation of the compute environment (installation of libraries or source code) poses the main challenge.
Therefore, it is of great use that the workflow tool is able to automatically deploy the software stack (on a per workflow or per process basis) by means of a package manager (e.g. conda) or that running processes in a container (e.g. docker, singularity, etc.) is integrated in the tool.

Evaluation criteria:

1. The automatic instantiation of the compute environment is not intended.
2. The workflow system allows the automatic instantiation of the compute environment on a per workflow basis.
3. The workflow system allows the automatic instantiation of the compute environment on a per process basis.

.. _requirements_uptodateness:

Up-to-dateness
--------------
There are different areas for the application of workflows. On the one hand,
people might use a workflow to define a single piece of reproducible code
that when executed, always returns the same result. Based on that they might
start a large quantity of different jobs and use the workflow system to
perform this task. Another area of application is the constant development
within the workflow (e.g. exchanging processes, varying parameter or even
modifying the source code of a process) until a satisfactory result is
obtained. The two scenarios require a slightly different behavior of the
workflow system. In the first scenario, all runs should be kept in the data
provenance graph with a documentation of how each result instance has been
obtained (e.g. by always documenting the codes, parameters, and processes).
If identical runs (identical inputs and processes should result in the same
output) are detected, a recomputation should be avoided and the original
output should be linked in the data provenance graph. The benefit of this
behavior certainly depends on the ratio between the computation time for a
single process compared to the overhead to query the data base.

However, when changing the processes (e.g. coding a new time integration
scheme, a new constitutive model), the workflow system should rather behave
like a built system (such as make) - only recomputing the steps that are
changed or that depend on these changes. In particular for complex problems,
this allows to work with complex dependencies without manually triggering
computations and results in automatically recomputing only the relevant parts
. An example is a paper with multiple figures that each is a result of
complex simulations that in itself depend on a set of general modules that
are developed in the paper. The "erroneus" runs are usually not interesting
and should be overwritten.

How this is handled varies between the tools. Some always recompute the
complete workflow marked in the matrix by an **R**\ ecompute, others allow
to create a new entry in the data provenance graph and link the previous
result (without the need to recompute already existing results) marked in the
matrix as **L**\ ink. Finally, make-like tools recreate only the parts
that are not up-to-date labeled as **U**\ pdate. Note that the latter
usually reduces the overhead to store multiple instances of the workflow, but
at the same time also prevents - without additional effort (e.g. when
executing in different folders) computing multiple instances of the same
workflow.


.. _requirements_gui:

Graphical user interface
------------------------
Independent of a particular execution of the workflow, the workflow system may provide facilities to visualize the graph of the workflow, indicating the
mutual dependencies of the individual processes and the direction of the flow of data. One can think of this graph as the template for the data provenance
graph. This visualization can help in conveying the logic behind a particular workflow, making it easier for other researchers to understand and possibly
incorporate it into their own research. The latter requires that the workflow system is able to handle hierarchical workflows, i.e. it needs to support
sub-workflows as processes inside another workflow. Beyond a mere visualization, a graphical user interface may allow for visually connecting different
workflows into a new one by means of drag & drop. An example for this is the [Rabix Composer](https://github.com/rabix/composer), which allows for the composition of workflows
written in CWL.

Evaluation criteria:

1. The workflow system provides no means to visualize the workflow
2. The workflow system or third-party tools allow to visualize the workflow definition
3. The workflow system or third-party tools provide a graphical user interface that enables users to graphically create workflows

.. _requirements_hierarchical:

Hierarchical composition of workflows
-------------------------------------
A workflow consists of a mapping between a set of inputs (could be empty) and
a set of outputs, whereas in between a number of sequential processes are
performed. Connecting the output of one workflow to the input of another
workflow results in a new, longer workflow. This is particularly relevant in
situations, where multiple people share a common set of procedures (e.g.
common pre- and postprocessing routines). In this case, copying the
preprocessing workflow into another one is certainly always possible, but
does not allow to jointly perform modifications and work with different
versions. If the workflow system supports a hierarchical embedding of one
workflow into another one, the property is labeled as + (otherwise -). This
also requries to define separate compute environments for each sub-workflow
(e.g. docker/singularity or conda), because each sub-workflow might use
different tools or even the same tools but with different versions (e.g.
python2 vs. python3), so executing all sub-workflows in the same environment
might not be possible.

.. _requirements_interfaces:

Process interfaces
------------------
Each process in a workflow has some input and output data.
In a traditional file based pipeline the output of one process is input to the other.
However, it is often more convenient to pass non-file output (e.g. float or integer values) directly from one process to the other without the creation of intermediate files.
In this case, it is desirable that the workflow tool is able to check for the validity of the data (e.g. the correct data type) to be processed.
Furthermore, this clearly defines the interface for a process and which input values may be changed.
This way, a third person is able to understand how to work with, adapt and extend the workflow/process.
In contrast, in a file based pipeline this is usually not the case, since a dependency in form of a file does not give information about the type of data contained in that file.

Evaluation criteria:

1. The workflow system is purely file-based and does not define interface formats. 
2. The workflow system has a file and non-file based interface, where the non-file based inputs are well defined.
3. The workflow system has a file and non-file based interface, where both the file and non-file based inputs are well defined.

.. _requirements_manually_editable:

Manually editable workflow definitions
--------------------------------------
While it can be beneficial to create and edit workflows using a graphical user interface, it may be important that the
resulting workflow description is given in a human-readable format. This does not solely mean that the definition should
be a text file, but also that the structure (e.g. indentation) and the naming are comprehensive. This facilitates
version-controlling (e.g. with git), in particular the code review process. Moreover, this does not force all users and/or
developers to rely on the graphical user interface.

Evaluation criteria:

1. The workflow description is a binary file
2. The workflow description is a text file but difficult to impossible to interpret by humans
3. The workflow description file format can naturally be understood by humans


.. _requirements_platform:

Platform for publishing and sharing workflows
---------------------------------------------
The benefit of a workflow system is already significant when using it for
individual research such as the development of my paper or reproducing the
paper someone else has written, when their data processing pipeline is fully
reproducible and documented and published with the publication. However, the
benefit can be even more increased if people are able to jointly work on
(sub-)workflows together. In particular, when a hierarchical workflow system
is used. Even though workflows can easily be shared together with the work (e
.g. in a repository), it might be beneficial to provide a platform that
allows to publish documented workflows with a search and versioning
functionality. This feature is not part of the requirement matrix to compare
the different tools, but we consider a documentation of these platforms (if
existing) in the subsequent section important source of information as a good
starting point for further research (exchange).

.. _requirements_evaluation:

Evaluation
----------

.. https://www.unicode-search.net/unicode-namesearch.pl?term=CIRCLE
.. ● BLACK CIRCLE
.. ○ WHITE CIRCLE
.. 🔴 large red circle to indicate important requirement for user story

Todo: comment on reason for below evaluation results.

+----------------------------+-----------+------------+------------+---------------------+-----+-------------+--------------------+----------------+-------------------+
| Tool                       | Execution | Monitoring | Provenance | Compute Environment | GUI | Composition | Process Interfaces | Up-to-dateness | Ease-of-first-use |
+============================+===========+============+============+=====================+=====+=============+====================+================+===================+
| CWL                        | ●●○       | ●●         | ●○○        | ●●●                 | ●●● | ●●●         | ●●●                | R              | ●●○               |
+----------------------------+-----------+------------+------------+---------------------+-----+-------------+--------------------+----------------+-------------------+
| AiiDA                      | ●●●       | ●●         | ●●●        | ●○○                 | ●●○ | ●●○         | ●●○                | L/C            | ●○○               |
+----------------------------+-----------+------------+------------+---------------------+-----+-------------+--------------------+----------------+-------------------+
| Snakemake                  | ●●○       | ●○         | ●●○        | ●●●                 | ●●○ | ●●●         | ●○○                | U              | ●●●               |
+----------------------------+-----------+------------+------------+---------------------+-----+-------------+--------------------+----------------+-------------------+
| Nextflow                   | ●●○       | ●○         | ●●○        | ●●●                 | ●●○ | ●●●         | ●○○                | L/C            | ●●●               |
+----------------------------+-----------+------------+------------+---------------------+-----+-------------+--------------------+----------------+-------------------+
| Doit                       | ●○○       | ●○         | ●○○        | ●○○                 | ●○○ | ●●○         | ●○○                | U              | ●●●               |
+----------------------------+-----------+------------+------------+---------------------+-----+-------------+--------------------+----------------+-------------------+
| User Story                 | Execution | Monitoring | Provenance | Compute Environment | GUI | Composition | Process Interfaces | Up-to-dateness | Ease-of-first-use |
+----------------------------+-----------+------------+------------+---------------------+-----+-------------+--------------------+----------------+-------------------+
| Paper                      |           |            |            | 🔴                  |     |             |                    | 🔴             | 🔴                |
+----------------------------+-----------+------------+------------+---------------------+-----+-------------+--------------------+----------------+-------------------+
| Joint research             |           |            | 🔴         | 🔴                  |     | 🔴          | 🔴                 | 🔴             |                   |
+----------------------------+-----------+------------+------------+---------------------+-----+-------------+--------------------+----------------+-------------------+
| Complex hier. computations | 🔴        | 🔴         | 🔴         | 🔴                  |     | 🔴          |                    |                |                   |
+----------------------------+-----------+------------+------------+---------------------+-----+-------------+--------------------+----------------+-------------------+
