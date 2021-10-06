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
up-to-date results (see :ref:`_requirements_uptodateness`). The workload may
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
about the workflow has to be provided. In addition to the provenance graph mentioned
in the previous point, workflow tools may provide the possibility to export more
detailed information on the used software components, for instance, the exact versions,
the chosen parameters, etc. This metadata should be exportable into widely-used
data formats such as JSON.


.. _requirements_compute_environment:

Compute environment specification/supply
----------------------------------------
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
A graphical user interface to visualize the workflow together with the flow of data
between computational components may be a valuable form of documentation.


.. _requirements_gui:

Graphical user interface
------------------------
In addition to simply visualizing the workflow (see :ref:`requirements_visualization`),
a user interface may also provide the means to define a workflow graphically
in a user-friendly way without having to know the details about the underlying API.
This GUI may also be capable of plugging together components defined in other workflows,
which may address the capability described in :ref:`requirements_reusability`.
