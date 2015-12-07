# My ansible playbooks
based on ansible v1.9

I intend to write playbooks the most portable as possible. So there is few dependancies.

# cloud
require ansible-cloudstack extra module from https://github.com/resmo/ansible-cloudstack
- cs-deploy.yml : deploy an instance inside ikoula's public cloud

# Roles
- cs-js-scripts.yml : deploy JS scripts based on csclient https://www.npmjs.com/package/csclient
- nodeJS-debian8 : install latest nodeJS engine on
- ghost.yml : deploy ghostJS bloging app

# Samples
Samples are from https://github.com/ansible/ansible-examples
