.. _userstories:

User Stories
============

TODO: introductory text

.. contents::

.. _usera:
User A
------

Writes application code on top of well-established open-source software libraries
to tackle domain-specific problems. Moreover, User A writes scripts for pre-
and post-processing of input/output data. The written code is domain- and
project-specific and does not have substantial potential for reusability.

.. _userb:
User B
------

Helps in the development and maintenance of an open-source software framework.
User B's research activities involve the development of new algorithms, which are
implemented into the framework in the scope of research projects, and which are
presented to the community in the form of scientific papers. The content presented
in the papers is produced by separate application code that runs a series of tests.

.. _userc:
User C
------

In the scope of a research project, user C writes application-specific code.
During the development, it becomes clear that a major part of the implemented
functionality could be useful for the community in various contexts. User C then
decides to separate the generic parts of the code into a standalone framework,
while moving the project-specific parts into an applications module.

.. _philipp:

Philipp (PhD student, engineer, self-taught programmer)
-------------------------------------------------------
The final result of this workflow is a *paper* describing the research results. Research should be
accessible by everyone and thus it is required that all software used is available under an open source license.
With the aim of making the paper reproducible by other researchers it is required that the used compute environment
is either provided as a *container* (docker) or all packages and their respective versions used need to be documented and this 
metadata published along with the code.
The tool used to define the workflow (chain of tasks), where each task consists of actions, dependencies and
targets, should give *documentation* of the implemented workflow in itself and have means of exploring this interactively. 
It is required that the tool is able to check for *up-to-dateness* of the tasks and handles execution of tasks automatically,
without the user having to decide if he needs to run/rerun a certain task. This greatly improves productivity during development
of the code, especially for computationally demanding tasks and minimizes errors. 
It is noted however that once the paper is published and archived, the main requirement is to reproduce the results as at the time
of publication. In contrast to other user stories no continuous integration (beyond the time of publication) of testing and
development of modules in the workflow system is required.
A *graphical visualization* of the workflow is not mandatory, but should be very useful to share with and explain the
workflow to others.
If possible the individual components of the workflow should be general/modular, such that these are *reusable* by others.
Others include members of the research group or other researchers in the same field who then quickly can pick up work from
some point in the pipeline/workflow. While this is not necessary for the paper itself, this is highly desirable to increase 
efficiency in the research group and / or community.

.. _bamgroup:

BAM Group (structural reliability)
----------------------------------
The objective is to guarantee the safety of a construction by determining the failure probability.
This is done by repeated evaluation of a structural model in a probabilistic approach (*adaptive importance sampling*).
Herein, an approximation of the probability of failure is computed from a joint distribution function of the
material parameters. Usually within this framework a large number of evaluations of the structural model are required which is
why the replacement of the structural model by a surrogate / *reduced order model* is necessary to increase efficiency.

Another aspect of the probabilistic approach is the calibration of the model by means of *Bayesian Inference* in which
the distribution function is determined based on the prior knowledge and the likelihood function. The likelihood
describes the probability that the numerical model of the lab experiment reproduces the experimental data for given model parameters.
Therefore, the numerical model has to be evaluated for various parameter values and the experimental data has to be processed. Here, for each of the different lab experiments a model and corresponding *metadata* should exist, such that these
are evaluated collectively. At the same time a query of the *database* should extract the relevant metadata and process the raw
data accordingly.

With the above example we would like to address workflows which consist of several modules, where each module
requires a different expertise (FEM, ROM, Bayesian Inference, ...), leading to the implementation and development of the
workflow being a group effort.

Collaborators taking part in the presented workflow could be grouped by *developers* and *users*.

Developers
^^^^^^^^^^
It is important that all modules (heterogeneous models) are embedded into a common framework and that the 
*relations and dependencies* between modules should be defined with a *portable data structure*.
For collaboration with others within the group automation of the installation of potentially complex
software environments (up to *machine-independent execution*) within the workflow tool is thought to be a great but
not compulsory feature.
The *reusability* of each module in several workflows is a basic requirement to avoid duplication of work (code).
Another fundamental feature for effective teamwork is a comprehensive *documentation* of the API of the workflow tool as well as
documentation of the implemented workflow (automatically generated).
The role of *metadata* as described above is twofold. On the one hand, for the compute environment software packages and
versions used (preferably automatically handled by the workflow system) need to be documented. On the other hand, metadata should 
be provided to describe and process experimental data in an automated way. In general metadata and data should comply with
the FAIR principles.

Users
^^^^^
In additon to the requirements for a *developer*, for an user dealing with computationally demanding tasks a connection to HPC systems is required.
In contrast to the developer, the *graphical visualization* of the workflow as a particularly user friendly form of documentation
and especially the definition of pipelines, without the need to understand the underlying API, through a GUI are important features.
For the user the definition and automatic installation of the software environment within the workflow tool is highly favorable to
avoid loosing time during the installation process.
