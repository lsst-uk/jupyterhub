# LSST UK DAC JupyterHub pilot

This is a pilot deployment of a JupyterHub environment running on a Kubernetes Cluster in an OpenStack cloud. 

## Deployment Notes

### Overview

Deployment consists of the following steps:

1. Deploy VMs
2. Install Rancher
3. Use Rancher to deploy Kubernetes.
4. Set up the OIDC client in EGI Check-in
5. Set up the local docker repository and images
6. Deploy JupyterHub
7. Set up the proxy
8. Set up ElasticStack logging

### VMs

The following VMs are required:

admin
: A VM for Rancher, local Docker reportisory etc. Requires 2GB memory (for docker builds) and plenty of disk. Should probably have a public IP and be reachable using SSH.

proxy
: an Nginx reverse proxy. Requires a public IP and to be reachable on TCP ports 80 and 443.

head
: K8s head node.

workerNN
: K8s worker nodes.

elk
: ElasticStack node for logging

The admin, head and worker VMs currently require ubuntu 16.04 in order to have compatible versions of Rancher, Docker and K8s. The proxy and elk VMs are on Ubuntu 18.04.

### Rancher

Install Docker on the admin VM:

```
sudo apt-get install docker.io
```

Install Rancher. Documentation is at https://rancher.com/docs/rancher/v2.x/en/

Use SSH port forwarding to access the GUI, e.g. `ssh 130.246.123.123 -L 8443:localhost:443`

Create and deploy a custom cluster. Configure as per the config file rancher/jupyter.yml

Create a default storage class using the manifest at k8s/sc.yml (edited for the specifics of the particular OpenStack cloud). 

### OIDC Client

Follow the instructions at https://wiki.egi.eu/wiki/AAI_guide_for_SPs to set up the OIDC client.

### Local Docker repo



### JupyterHub

Install git on the admin VM: `sudo apt-get install git`

Clone this repository: `git clone https://github.com/lsst-uk/jhub-test.git`

Create a copy of the file helm/jhub/config.yaml and edit to add/edit values as required, e.g. client ID and secret.

Follow the instructions at https://zero-to-jupyterhub.readthedocs.io/en/latest/ to first deploy Helm and then use Helm to deploy JupyterHub using the above config file.

Use SSH forwarding to test that JupyterHub is working. Login won't work yet since the callback doesn't go anywhere.


