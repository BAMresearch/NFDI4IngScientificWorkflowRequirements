Introduction
============

Software-driven scientific workflows are often characterized by a complex interplay
of various pieces of software executed in a particular order. The software involved
in the workflows may consist of well-established software packages as well as self-
written or open-source code developed by other researchers. With increasing complexity,
a comprehensive documentation of the workflow, possibly aided by a graphical visualization,
is necessary in order to communicate the underlying rationale to other researchers.

Moreover, for the research to be as transparent as possible, the results obtained
with the workflow at a particular point in time, for instance for a scientific
publication, must be reproducible by other researchers in the future. To this end,
it is necessary to provide metadata on the exact versions used for all the software
involved. Such a "snapshot" of the workflow should be published side-by-side with
scientific papers.

In this documentation, we want to evaluate if, or which, currently existing workflow
tools can provide the means to accomplish the above-mentioned challenges, that is:

- comprehensive documentation of the individual processing steps of a workflow,
  their interaction and the flow of data
- version-controlling the workflow and publishing it side-by-side with a scientific publication
- packaging of the workflow together with the involved software packages to make it
  shareable with and executable by other researchers

The aim of this document is to collect, in a community effort, the requirements
of scientific workflows on such tools, and to document user experiences on how to
set up workflows using existing tools.
