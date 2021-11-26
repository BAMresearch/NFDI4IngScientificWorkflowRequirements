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
# and activating the conda environment needs write-access to the environment folder.
# Containers to be used with cwl should therefore probably have the environment set
# up system-wide instead of using conda. For our purposes this should be ok, as we
# want to inject/test different environment files on our workflow.
RUN groupadd --gid 1000 conda && \
    useradd --gid 1000 -m --home-dir /environments --uid 1000 condauser
USER condauser
ENV CONDA_PKGS_DIRS=/environments/pkgs
WORKDIR /environments

# create environment with conda and substitute ParaView by version without x-server
# - TODO: change link to the .yml file after branch has been merged
ARG ENVFILEURL=https://raw.githubusercontent.com/BAMresearch/NFDI4IngScientificWorkflowRequirements/main/simple_use_case/cwl/docker/default_env.yml
RUN echo "using environment file with url $ENVFILEURL" && \
    wget $ENVFILEURL -O my_env.yml && \
    conda env create --file my_env.yml --prefix ./myenv && \
    conda clean --all -y && \
    wget --no-check-certificate "https://www.paraview.org/paraview-downloads/download.php?submit=Download&version=v5.9&type=binary&os=Linux&downloadFile=ParaView-5.9.1-osmesa-MPI-Linux-Python3.8-64bit.tar.gz" \
         --output-document=/environments/paraview.tar.gz && \
    tar -xvf /environments/paraview.tar.gz && \
    rm /environments/paraview.tar.gz
ENV PATH=$PATH:/environments/ParaView-5.9.1-osmesa-MPI-Linux-Python3.8-64bit/bin

# make sure environment is loaded when commands are executed
ENTRYPOINT ["conda", "run", "--no-capture-output", "-p", "/environments/myenv"]
CMD ["/bin/bash"]
