FROM williamyeh/ansible:alpine3

# Install cs library to deploy on cloudstack
RUN pip install cs
# /!\ require cloudstack.ini /!\

WORKDIR /tmp
COPY . /tmp
RUN chmod -R -X /tmp/*
# Install roles from galaxy
RUN ansible-galaxy install abaez.docker

CMD ["sh"]
