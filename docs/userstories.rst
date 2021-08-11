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
Names:

* Sylvester (John Rambo)
* Jean Reno (Leon der Profi, Mathilda)

In this user story, the output of the workflow is a scientific paper describing the research results.
An essential component of this work is the development of research software in line with the task area `BETTY <https://nfdi4ing.de/archetypes/betty/>`_.
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
Names: 

* George (John "Hannibal" Smith)
* Patrick (Jean-Luc Picard)
* Swetlana Tichanowskaja

Similar to the first user story the output of the workflow could be a scientific paper. 
However, with this example interdisciplinary workflows are addressed and the reusability of single components/modules is essential. 
Each process in the workflow may require a different expertise and hence modularity and a common framework are necessary features for efficient collaboration.
Moreover, joint software development and the development of the scientific workflow itself play an important role.

Thus, it is focused on the following requirements.
First, the heterogeneous models of the workflow should be embedded into a common framework and should be executable independent of the local machine. 
Without a common framework/interface the exchange of data between processes is not possible (except for file based workflows).
The workflow tool must provide means to control (automatically install) the compute environment for specific processes of the workflow.
This greatly enhances the reusability of a process and/or modules (chain of processes) of the workflow and guarantees the machine-independent execution.
For complex workflows containing computationally expensive processes a check for up-to-dateness is required, as this leads to significant speed up in the time needed for development of the workflow and minimizes errors in manual execution of some part of the workflow. 


.. _user_story_3:

High-throughput simulations
---------------------------
Names:

* Giuseppe (Verdi)
* Antonio (Ghislanzoni)

In cases where screening or parameter sweeps are required, involving thousands of simulations,
running these one by one is not feasible. Moreover, besides the *automation* of running the 
calculations their inputs and outputs need to be stored. Not only the data and calculations
should be stored to achieve *reproducibility*, but also the causal relationships between them, i.e.
the full *provenance*.

Given the large amount of data (inputs/outputs) manually keeping track of the full provenance becomes infeasible.
Therefore, the workflow tool must automatically track and record inputs, outputs and metadata of all processes in a database.
Furthermore, fast queries of the database and automatic generation of the provenance graph are required features of the workflow tool.
Due to the large computational effort the seamless integration of HPC systems is as well vital for this use case.
