FROM continuumio/miniconda3
MAINTAINER dennis.glaeser@iws.uni-stuttgart.de

# install basic dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends --yes \
    libgomp1 \
    libgl1-mesa-glx \
    libglu1-mesa \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# we use the user/group 1000/1000, since this is the pair of user/gid that
# cwltool uses to spin up the container for execution of the cwl workflow
RUN groupadd --gid 1000 conda && \
    useradd --gid 1000 -m --home-dir /environments --uid 1000 condauser
USER condauser
ENV CONDA_PKGS_DIRS=/environments/pkgs
WORKDIR /environments

# create environment with conda
# - remove paraview after installation and substitute by version without x-server (see below)
# - TODO: change link after the .yml file has been placed correctly
ARG ENVFILE=https://raw.githubusercontent.com/BAMresearch/NFDI4IngScientificWorkflowRequirements/feature/simpleusecase-cwl/simple_use_case/cwl/docker/default_env.yml
ADD ENVFILE .
RUN wget https://raw.githubusercontent.com/BAMresearch/NFDI4IngScientificWorkflowRequirements/feature/simpleusecase-cwl/simple_use_case/environments/complete.yml && \
    conda env create --file ENVFILE --prefix ./myenv && \
    conda remove --prefix ./myenv paraview && \
    wget --no-check-certificate "https://www.paraview.org/paraview-downloads/download.php?submit=Download&version=v5.9&type=binary&os=Linux&downloadFile=ParaView-5.9.1-osmesa-MPI-Linux-Python3.8-64bit.tar.gz" \
         --output-document=/environments/paraview.tar.gz && \
    tar -xvf /environments/paraview.tar.gz && \
    rm /environments/paraview.tar.gz
ENV PATH=$PATH:/environments/ParaView-5.9.1-osmesa-MPI-Linux-Python3.8-64bit/bin

# make sure environment is loaded when commands are executed
ENTRYPOINT ["conda", "run", "--no-capture-output", "-p", "/environments/myenv"]
CMD ["/bin/bash"]
