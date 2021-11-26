#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

inputs:
  dockerfile-url:
    type: string
    default: https://raw.githubusercontent.com/BAMresearch/NFDI4IngScientificWorkflowRequirements/main/simple_use_case/cwl/docker/Dockerfile
  envfile-url:
    type: string
    default: https://raw.githubusercontent.com/BAMresearch/NFDI4IngScientificWorkflowRequirements/main/simple_use_case/cwl/docker/default_env.yml

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
      envfile-url: envfile-url
    out: [dockerid]
