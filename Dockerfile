FROM williamyeh/ansible:alpine3-onbuild

# ==> Install cs library to deploy on cloudstack
RUN pip install cs
# /!\ require cloudstack.ini /!\
# ==> Specify requirements filename;  default = "requirements.yml"
#ENV REQUIREMENTS  requirements.yml

# ==> Specify playbook filename;      default = "playbook.yml"
#ENV PLAYBOOK      playbook.yml

# ==> Specify inventory filename;     default = "/etc/ansible/hosts"
#ENV INVENTORY     inventory.ini

# ==> Executing Ansible (with a simple wrapper)...
#RUN ansible-playbook-wrapper
# Install roles from galaxy
RUN ansible-galaxy install abaez.docker

CMD ["sh"]
