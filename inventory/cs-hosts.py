#!/usr/bin/env python
# based on https://github.com/resmo/ansible-cloudstack-routers

import os
import sys
import argparse

try:
    import json
except:
    import simplejson as json

try:
    from cs import CloudStack, CloudStackException, read_config
except ImportError:
    print >> sys.stderr, "Error: CloudStack library must be installed: pip install cs."
    sys.exit(1)

class CloudStackInventory(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--host')
        parser.add_argument('--list', action='store_true')

        options = parser.parse_args()
        try:
            self.cs = CloudStack(**read_config())
        except CloudStackException, e:
            print >> sys.stderr, "Error: Could not connect to CloudStack API"

        if options.host:
            data = self.get_host(options.host)
            print json.dumps(data, indent=2)

        elif options.list:
            data = self.get_list()
            print json.dumps(data, indent=2)
        else:
            print >> sys.stderr, "usage: --list | --host <hostname>"
            sys.exit(1)

    def add_group(self, data, group_name, host_name):
        if group_name not in data:
            data[group_name] = {
                'hosts': []
            }
        data[group_name]['hosts'].append(host_name)
        return data

    def get_host(self, name):
        hosts = []

        hosts_projects = self.cs.listVirtualMachines(listall=True)
        if hosts_projects and 'host' in hosts_projects:
            hosts = hosts + hosts_projects['host']

        hosts_accounts = self.cs.listVirtualMachines(listall=True)
        if hosts_accounts and 'host' in hosts_accounts:
            hosts = hosts + hosts_accounts['host']

        data = {}
        for host in hosts:
            host_name = host['name']
            if name == host_name:
                data['zone'] = host['zonename']
                if 'linklocalip' in host:
                    data['ansible_ssh_host'] = host['linklocalip']
                data['state'] = host['state']
                if 'account' in host:
                    data['account'] = host['account']
                if 'project' in host:
                    data['project'] = host['project']
                data['service_offering'] = host['serviceofferingname']
                data['role'] = host['role']
                data['nic'] = []
                for nic in host['nic']:
                    data['nic'].append({
                        'ip': nic['ipaddress'],
                        'mac': nic['macaddress'],
                        'netmask': nic['netmask'],
                    })
                    if nic['isdefault']:
                        data['default_ip'] = nic['ipaddress']
                break;
        return data

    def get_list(self):
        data = {
            'all': {
                'hosts': [],
                },
            '_meta': {
                'hostvars': {},
                },
            }
        hosts = []

        hosts_projects = self.cs.listVirtualMachines()
        if hosts_projects and 'virtualmachine' in hosts_projects:
            hosts = hosts + hosts_projects['virtualmachine']

        for host in hosts:
            if host['state'] != 'Running':
                continue
            host_name = host['name']
            data['all']['hosts'].append(host_name)
            # Make a group per domain
            data = self.add_group(data, host['domain'], host_name)
            data['_meta']['hostvars'][host_name] = {}
            data['_meta']['hostvars'][host_name]['group'] = host['domain']
            data['_meta']['hostvars'][host_name]['domain'] = host['domain']
            if 'networkdomain' in host:
                data['_meta']['hostvars'][host_name]['networkdomain'] = host['networkdomain']

            data['_meta']['hostvars'][host_name]['zone'] = host['zonename']
            # Make a group per zone
            data = self.add_group(data, host['zonename'], host_name)

            if 'project' in host:
                data['_meta']['hostvars'][host_name]['project'] = host['project']
                # Make a group per project
                data = self.add_group(data, host['project'], host_name)

            if 'account' in host:
                data['_meta']['hostvars'][host_name]['account'] = host['account']
                # Make a group per account
                data = self.add_group(data, host['account'], host_name)

            data['_meta']['hostvars'][host_name]['state'] = host['state']
            data['_meta']['hostvars'][host_name]['service_offering'] = host['serviceofferingname']
            data['_meta']['hostvars'][host_name]['nic'] = []
            for nic in host['nic']:
                data['_meta']['hostvars'][host_name]['nic'].append({
                    'ip': nic['ipaddress'],
                    'mac': nic['macaddress'],
                    'netmask': nic['netmask'],
                    })
                if nic['isdefault']:
                    data['_meta']['hostvars'][host_name]['default_ip'] = nic['ipaddress']
        return data

if __name__ == '__main__':
    CloudStackInventory()