Pydoit
------
Some notes about [pydoit](https://pydoit.org).

Documentation
-------------
* Task's meta-data are better described in a declarative way (i.e. CWL or DSL ...), but often you want to create this meta-data programmatically
* dependencies are on tasks, not on targets
* doit checks if *file_dep* was modified or not (by comparing the file content’s MD5) (+)

Test case implementation
------------------------
* knowledge of the python programming language (o)
* no direct integration of software packages; software deployment and execution environment are not controlled (-)
