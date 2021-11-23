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
outputs:
  dockerid:
    type: string
    outputBinding:
      glob: "docker_id.txt"
      loadContents: True
      outputEval: $(self[0].contents)
