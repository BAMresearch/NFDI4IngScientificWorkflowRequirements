#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

inputs:
  dockerfile-url: string

outputs:
  dockerid:
    type: string
    outputSource: build_dockerimage/dockerid

steps:
  fetch_dockerfile:
    run: fetch_dockerfile.cwl
    in:
      url: dockerfile-url
    out: [dockerfile]

  build_dockerimage:
    run: build_docker_image.cwl
    in:
      file: fetch_dockerfile/dockerfile
    out: [dockerid]
