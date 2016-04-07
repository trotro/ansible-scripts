# My ansible playbooks
based on ansible v2.x

I intend to write playbooks the most portable as possible. So there is few dependancies.

# Dockerfile
In order to play the playbooks in the same environment everywhere, I've written a Dockerfile.
To build the container
```Shell
docker build --quiet --rm=true -t myAnsible .
```

# Roles
- js-scripts.yml
  deploy JS scripts based on csclient https://www.npmjs.com/package/csclient
- nodeJS-debian8
  install latest nodeJS engine on debian 8
- ghost.yml
  deploy ghostJS bloging app

## cloudstack
Playbooks with the "cs-" suffix are designed to run on cloudstack cloud platforms.
- cs-deploy.yml
  deploy an instance inside cloudstack. Some variables has to be defined in the inventory
- cs-keypair
  deploy a SSH keypair in cloudstack

To run the cloudstack plays, you have to add a cloudstack.ini file with your credentials.
```
[cloudstack]
endpoint = https://cloudstack.ikoula.com/client/api
key = your_API_key
secret = you_API_secret_key
```

## docker
Plays with the "docker-" suffix are designed to deploy docker containers.
- docker-wordpress.yml
  install docker engine (based on [jgeusebroek.docker](https://galaxy.ansible.com/jgeusebroek/docker/) playbook)
  deploy wordpress on 3 containers : db ; app ; nginx

# Samples
Samples are from https://github.com/ansible/ansible-examples
