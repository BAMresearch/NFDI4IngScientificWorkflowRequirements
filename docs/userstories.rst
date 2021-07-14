.. _userstories:

User Stories
============
In this section, the :ref:`requirements` defined in the previous section are illustrated
with examples given below. Each *user story* pursues a different goal to show the 
diversity in requirements on the workflow tool and at the same time which requirements
are safe to be assumed common for most use cases.

.. _user_story_1:

Reproducible (computational) research
-------------------------------------
In this user story, the output of the workflow is a scientific paper describing the research results.
But not only the final manuscript should be provided. It is aimed at enabling other scientists to
comprehend and redo the *processing steps* (numerical analysis, postprocessing, etc.) the workflow consists of.

Reproducibility?:
* automation 
.. The workflow should be implemented in a fully automated way, such that *reproducibilty* is ensured.
* version control
* archive computer environment (at least software + versions, but: becomes out of date easily) --> container


.. _user_story_2:

Research group collaboration
----------------------------
With this example we would like to address workflows, where joint software development and the development
of the scientific workflow itself play an important role.
Each process in the workflow may require a different expertise and hence modularity and a common
framework are required for the tool to be used.


.. _user_story_3:

High-throughput simulations
---------------------------
In cases where screening or parameter sweeps are required, involving thousands of simulations,
running these one by one is not feasible. However, besides the *automation* of running the 
calculations their inputs and outputs need to be stored. Not only the data and calculations
should be stored to achieve *reproducibility*, but also the causal relationships between them, i.e.
the full *provenance*.
