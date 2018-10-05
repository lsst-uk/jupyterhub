FROM jupyter/base-notebook

RUN conda install --quiet --yes \
    'mysql-connector-python' \
    'matplotlib'

RUN mkdir /opt/conda/lib/python3.6/site-packages/ztf

COPY settings.py /opt/conda/lib/python3.6/site-packages/ztf

