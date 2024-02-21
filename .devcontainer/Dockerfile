# https://hub.docker.com/_/fedora
FROM fedora:38

# update and install OS packages
RUN dnf -y update && dnf -y groupinstall "Development Tools" && \
    dnf -y install \
    python3-pip \
    python3-devel \
    libffi-devel \
    oniguruma-devel \
    gcc \
    wget \
    vim \
    unzip \
    curl \
    git

# install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
