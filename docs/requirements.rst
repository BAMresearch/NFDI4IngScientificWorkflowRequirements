.. _requirements:

Requirements on workflow tools
==============================

In this section, we want to translate the aspects discussed in :ref:`fairness`
into possible capabilities that workflow tools should provide in order to
fulfill these aspects.

.. contents::

.. _requirements_execution:

Execution and scheduling
------------------------------------
The complete workflow has to be scheduled and executed, maybe reusing
up-to-date results (see :ref:`requirements_uptodateness`). The workload may
be distributed among different machines, and it may be necessary to use an HPC
system for intensive computations.

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

.. _provenance:

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

.. _requirements_metadata:

Metadata
--------
To make a published workflow compliant with the
`FAIR principles <https://www.go-fair.org/fair-principles/>`_, appropriate metadata
about the workflow has to be provided. Workflow tools may provide the possibility
to export detailed information on the used software components, for instance, the
exact versions, the chosen parameters, etc. This metadata should be exportable into
widely-used data formats such as JSON.


.. _requirements_compute_environment:

Compute environment
-------------------
Research workflows should be executable by others in order to guarantee reproducible
research. Thus, it must be possible to export/share the workflow/modules in such a way that
it no longer depends on machine-local installations of libraries or source code, for
instance, by bundling all required components into a container.


.. _requirements_uptodateness:

Up-to-dateness
--------------
It may be required that the tool not only documents all steps of the workflow and
executes them in sequence, but also that it is capable of checking for up-to-dateness.
In case of changes somewhere in the *pipeline* it determines and only executes the *tasks*
which are not up-to-date, without the need to rerun everything from scratch.
A task is referred to as up-to-date if execution of the task would produce the same result
as the previous execution.


.. _requirements_gui:

Graphical user interface
-----------------------

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

.. _requirements_manually_editable:


.. _requirement_platform:

Platform for publishing and sharing workflows
---------------------------------------------
Ideally, workflows are continuously developed, reused independently by others and shared on a platform.
Other researchers should have the possibility to search for existing workflows, embed a component into
their own workflow that addresses a different research question, and publish these modified or extended
workflows with appropriate metadata and permissions. To this end, it is important that the components'
inputs and outputs are standardized, portable across compute environments and versioned.
