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

RUN groupadd --gid 1000 conda
RUN useradd --gid 1000 -m --home-dir /environments --uid 1000 condauser
USER condauser
ENV CONDA_PKGS_DIRS=/environments/pkgs
WORKDIR /environments

COPY complete.yml .
RUN conda env create --file ./complete.yml --prefix ./complete

# remove paraview and install version without x-server requirement instead (suitable for container)
RUN conda remove --prefix ./complete paraview
RUN wget --no-check-certificate "https://www.paraview.org/paraview-downloads/download.php?submit=Download&version=v5.9&type=binary&os=Linux&downloadFile=ParaView-5.9.1-osmesa-MPI-Linux-Python3.8-64bit.tar.gz" \
         --output-document=/environments/paraview.tar.gz
RUN tar -xvf /environments/paraview.tar.gz && rm /environments/paraview.tar.gz
ENV PATH=$PATH:/environments/ParaView-5.9.1-osmesa-MPI-Linux-Python3.8-64bit/bin

# make sure environment is loaded when commands are executed
ENTRYPOINT ["conda", "run", "--no-capture-output", "-p", "/environments/complete"]
CMD ["/bin/bash"]
