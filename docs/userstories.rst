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
An essential component of this work is the development of research software in the sense of the BETTY task area.
It is aimed at enabling other scientists to comprehend and rerun each process (numerical analysis, postprocessing, etc.) of the entire workflow.

In order to meet this goal, i.e. the *reproducibilty* of computational research, the following requirements are defined.
A basic requirement is to employ version control to keep track of the code history and to be able to refer to the particular version of the code used at the time of publication.
As research software is also understood as research data, appropriate metadata regarding the code and dependencies on third-party libraries should be provided.  
This code metadata allows peers to rebuild the compute environment. 
However, since software becomes out of date rather quickly this is a minimum requirement and it is preferred to build containers that package up all required pieces of software in a way that is portable, reproducible and ensures machine-independent execution.
Finally, the fully automated implementation of the entire workflow is required to avoid any manual steps.
Ideally, the whole paper can be reproduced by running a single command and the progress of the execution is monitored by the workflow tool.


.. _user_story_2:

Research group collaboration
----------------------------
Similar to the first user story the output of the workflow could be a scientific paper. 
However, with this example interdisciplinary workflows are addressed and the reusability of single components/modules is essential. 
Each process in the workflow may require a different expertise and hence modularity and a common framework are necessary features for efficient collaboration.
Moreover, joint software development and the development of the scientific workflow itself play an important role.

Thus, it is focused on the following requirements.
- reusability
- execution, scheduling and monitoring
- machine-independent execution (but container does not work well during development?, building of the container integrated in the workflow (*task_build_container*)), emphasis on export/sharing of workflow modules
- metadata
- up-to-dateness


.. _user_story_3:

High-throughput simulations
---------------------------
In cases where screening or parameter sweeps are required, involving thousands of simulations,
running these one by one is not feasible. However, besides the *automation* of running the 
calculations their inputs and outputs need to be stored. Not only the data and calculations
should be stored to achieve *reproducibility*, but also the causal relationships between them, i.e.
the full *provenance*.

Requirements:
- relations and dependencies with portable data structures
- machine-independent execution (rather hpc system than container solution)
- execution, scheduling and monitoring (hpc connection)
- graphical visualization and documentation (provenance graph)
- metadata (FAIRness)
