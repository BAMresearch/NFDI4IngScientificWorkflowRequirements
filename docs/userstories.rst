.. _userstories:

User Stories
============

Reproducible research
---------------------
In this user story, the final result of the workflow is a paper describing the research results.
The workflow should be implemented in a fully automated way, such that *reproducibilty* is ensured.


Research group collaboration
----------------------------
With this example we would like to address workflows, where joint software development and the development
of the scientific workflow itself play an important role.
Each process in the workflow may require a different expertise and hence modularity and a common
framework are required for the tool to be used.


High-throughput simulations
---------------------------
In cases where screening or parameter sweeps are required, involving thousands of simulations,
running these one by one is not feasible. However, besides the *automation* of running the 
calculations their inputs and outputs need to be stored. Not only the data and calculations
should be stored to achieve *reproducibility*, but also the causal relationships between them, i.e.
the full *provenance*.
