#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
doc: |
  wrapper around wget to fetch the docker file from the specified url
baseCommand: ["wget",]
arguments: ["$(inputs.url)", "-O", "Dockerfile"]
inputs:
  url:
    type: string
outputs:
  dockerfile:
    type: File
    outputBinding:
      glob: ["Dockerfile"]
