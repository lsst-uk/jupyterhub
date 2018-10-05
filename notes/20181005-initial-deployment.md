Notes from a Slack conversation, 20181005

Dave : 

I'm curious about basic architecture stuff ..
How many VMs do you have ?
How do you create them ?
What is on each of them and how is that installed ?

Gareth:

Right now I have 3 VMs created using the browser interface (Horizon)

All run Ubuntu 16.04 (since Rancher/Kubernetes doesn't work with the version of Docker in 18.04 yet)

One VM runs rancher and misc stuff like a local docker repository that will later go elsewhere

One is a head node (control plane/etcd in Kubernetes speak)

The other is a worker node

Installation process for the head and worker is: login; apt-get update; apt-get dist-upgrade; apt-get install docker.io; install the rancher client (it's a docker container) and let rancher take it from there

The rancher config is also created interactively, but without any customisation initially, then apply the config file that;s in the git repo

Helm/Tiller installation is completely standard (it's a couple of commands)
Then use helm to deploy jupyterhub using the config file in git

That config file is where pretty much all the customisation is done
Plus I'm building a custom docker image for accessing the ZTF database - dockerfile also in git
So there's a bunch of steps there that each automatically do a lot of stuff, but they all have to be kicked off manually in the right order at the moment
I'm hoping to use something like Ansible to replace the interactive bits of that

Dave :

What IP addresses do they get ?

Gareth :

They're all on VM network private, they get IP addresses in the range 192.168.1.0/24 which they can use to talk to each other.
Rancher and head have a floating IP assigned from the 172.16.0.0/16 range that is accessible from within the university network.
Rancher and worker are small instances, head is a medium. Rancher and head require a fair bit of disk space for docker images.
User storage lives on separate volumes that get created dynamically.
