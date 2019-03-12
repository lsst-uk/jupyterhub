FROM jupyter/base-notebook

RUN conda update -n base conda

RUN conda install --quiet --yes \
    'mysql-connector-python' \
    'matplotlib' \
    'astropy'

RUN jupyter labextension install @jupyterlab/git \
 && pip install jupyterlab-git \
 && jupyter serverextension enable --py jupyterlab_git --sys-prefix

RUN mkdir /opt/conda/lib/python3.7/site-packages/ztf

COPY settings.py /opt/conda/lib/python3.7/site-packages/ztf

USER root

RUN apt-get update && apt-get -yq dist-upgrade \
 && apt-get install -yq --no-install-recommends \
    git \
 && apt-get clean \
&& rm -rf /var/lib/apt/lists/*

USER $NB_UID

