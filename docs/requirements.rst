.. _requirements:

Requirements
================================

This section discusses potential requirements on workflow tools to reach the
goals mentioned in the :ref:`introduction`.

.. contents::

.. _portable_data_structures:

Relations and dependencies with portable data structures
--------------------------------------------------------
A workflow consist of heterogeneous models (e.g. HPC computational model, calibration model, data preprocessing of
experimental data potentially even running on different machines or operating systems). They should be embedded into
a common framework. The relations and dependencies between the modules should be defined with a portable data
structure. The workflow system should handle and document the provenance graph.

.. _machine-independent:

Machine-independent execution
-----------------------------
Research workflows should be executable by others in order to guarantee reproducible
research. Thus, it must be possible to export/share the workflow/modules in such a way that
it no longer depends on machine-local installations of libraries or source code, for
instance, by bundling all required components into a container.

.. _doc:

Documentation
-------------
Scientific workflows may be complex, and therefore, it is important to provide a
comprehensive documentation that describes the individual computational steps and
how they are interconnected. Thus, a beneficial feature of workflow tools can be
the automated generation of a documentation based on descriptions of individual
components and the flow of data between them.

.. _uptodateness:

Up-to-dateness
--------------
It may be required that the tool not only documents all steps of the workflow and
executes them in sequence, but also that it is capable of checking for up-to-dateness.
In case of changes somewhere in the *pipeline* it determines and only executes the *tasks*
which are not up-to-date, without the need to rerun everything from scratch.
A task is referred to as up-to-date if execution of the task would produce the same result
as the previous execution.

.. _metadata:

Metadata
--------
To make a published workflow compliant with the
`FAIR principles <https://www.go-fair.org/fair-principles/>`_, appropriate metadata
about the workflow has to be provided. Workflow tools may provide the possibility
to automatically export the complete provenance graph including the involved
software components, their versions, their inputs, outputs and parameters, etc.

.. _reusability:

Reusable components
-------------------
Ideally, individual components of the workflow may be reused independently of others.
This gives other researchers the possibility to embed a component into a new workflow
that addresses a different research question. To this end, it is important that the
components' inputs and outputs are properly documented (see :ref:`doc`) and
defined via portable data structures
(see :ref:`portable_data_structures`).

.. _gui:

Graphical visualization
-----------------------
A graphical user interface to visualize the workflow together with the flow of data
between computational components may be a valuable form of documentation. Besides
this, a user interface may also provide the means to define a workflow graphically
in a user-friendly way without having to know the details about the underlying API.


.. _monitoring:

Execution, scheduling and monitoring
------------------------------------
A complete workflow has to be scheduled and executed (eventually reusing
up-to-date results) by the workflow system and in particular monitor and
document the progress of the execution. This is in particular relevant for
compute intensive computations that might fail or where manual interaction (e
.g. adding experimental data) is required.
