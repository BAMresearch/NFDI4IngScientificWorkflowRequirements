#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  build the docker image from the given file
baseCommand: ["docker", "build",]
arguments: ["-f", "$(inputs.file)", "-t", "$(inputs.tag)", "--iidfile", "docker_id.txt", "."]
inputs:
  file:
    type: File
    default: "Dockerfile"
    doc: "Set the dockerfile to be used for the build"
  tag:
    type: string
    default: "wftools-simpleusecase"
    doc: "Define the tag to be given to the image"
  envfile-url:
    type: string
    default: "https://raw.githubusercontent.com/BAMresearch/NFDI4IngScientificWorkflowRequirements/feature/simpleusecase-cwl/simple_use_case/cwl/docker/default_env.yml"
    doc: "The url of the conda file to use for building the environment inside the container"
outputs:
  dockerid:
    type: string
    outputBinding:
      glob: "docker_id.txt"
      loadContents: True
      outputEval: $(self[0].contents)
