FROM jupyterhub/k8s-hub:0.8.2

USER root

RUN apt-get update \
  && apt-get -yq dist-upgrade \
  && apt-get -yq install python3-nacl

RUN mkdir /usr/local/share/jupyterhub/custom_templates 
COPY login.html /usr/local/share/jupyterhub/custom_templates

USER $NB_UID


