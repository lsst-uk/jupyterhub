## Deployment 

### Prerequisites
* uwsgi
* uwsgi-plugin-python
* python-flask-restful

### Installation (CentOS 7)
* Copy jhubacct.py to /opt/jhubacct/
* Create /opt/jhubacct/jobs.db
* Set ownership and permissions (uwsgi runs as user uwsgi by default)
* Copy jhubacct.ini to /etc/uwsgi.d/
* Set uwsgi emperor-tyrant mode to false in /etc/uwsgi.ini
* Test and enable uwsgi service

