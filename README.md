# My ansible playbooks
based on ansible v1.9

I intend to write playbooks the most portable as possible. So there is few dependancies.

# cloud
require ansible-cloudstack extra module from https://github.com/resmo/ansible-cloudstack
- deploy-VM-cloudstack.yml : made to deploy an instance inside ikoula's public cloud

# Roles
- js.yml : deploy a JS script with nodeJS installation on debian 8
- ghost.yml : deploy ghostJS bloging app

# Samples
Samples are from https://github.com/ansible/ansible-examples
