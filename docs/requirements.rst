.. _requirements:

Requirements on workflow tools
==============================

In this section, we want to translate the aspects discussed in :ref:`fairness`
into possible capabilities that workflow tools should provide in order to
fulfill these aspects.

.. contents::

.. _requirements_monitoring:

Execution, scheduling and monitoring
------------------------------------
The complete workflow has to be scheduled and executed, maybe reusing
up-to-date results (see :ref:`requirements_uptodateness`). The workload may
be distributed among different machines, and it may be necessary to use an HPC
system for intensive computations. The workflow system should provide the means
to monitor the progress of the workflow execution at any time.

.. _provenance:

Data provenance graph
---------------------
After the successful execution of a workflow, it should be possible to obtain
the provenance graph for all produced or modified data within the workflow.


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


.. _requirements_visualization:

Graphical visualization
-----------------------
A workflow tool may be able to export the workflow graph into a format that can
be visualized, or provide visualization capabilities itself. A visual representation
of the flow of data between computational components can be a valuable form of
documentation, making it easier for users to understand the underlying logic.


.. _requirements_gui:

Graphical user interface
------------------------
In addition to simply visualizing the workflow (see :ref:`requirements_visualization`),
a user interface may also provide the means to define a workflow graphically
in a user-friendly way without having to know the details about the underlying API.
This GUI may also be capable of plugging together components defined in other workflows,
which may address the capability described in :ref:`requirement_platform`.


.. _requirement_platform:

Platform for publishing and sharing workflows
---------------------------------------------
Ideally, workflows are continuously developed, reused independently by others and shared on a platform.
Other researchers should have the possibility to search for existing workflows, embed a component into
their own workflow that addresses a different research question, and publish these modified or extended
workflows with appropriate metadata and permissions. To this end, it is important that the components'
inputs and outputs are standardized, portable across compute environments and versioned.
