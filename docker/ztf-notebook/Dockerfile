FROM jupyter/base-notebook

RUN conda install --quiet --yes \
    'mysql-connector-python' \
    'matplotlib'

RUN jupyter labextension install @jupyterlab/git

RUN mkdir /opt/conda/lib/python3.6/site-packages/ztf

COPY settings.py /opt/conda/lib/python3.6/site-packages/ztf

USER root

RUN apt-get update && apt-get -yq dist-upgrade \
 && apt-get install -yq --no-install-recommends \
    git \
 && apt-get clean \
&& rm -rf /var/lib/apt/lists/*

USER $NB_UID

