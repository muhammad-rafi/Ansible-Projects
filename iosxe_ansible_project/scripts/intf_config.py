#!/usr/bin/env python

import ansible_runner
import json 

runner = ansible_runner.run(#private_data_dir='/opt/ansible/Ansible-Projects/iosxe_ansible_project/', 
                       playbook='/opt/ansible/Ansible-Projects/iosxe_ansible_project/playbooks/intf_config_playbook.yml', 
                       inventory='/opt/ansible/Ansible-Projects/iosxe_ansible_project/inventory.yml',
                       envvars='',
                       extravars={"ip_interfaces":
			                              [{
				                              "intf_name": "Loopback 999",
				                              "intf_description": "Configured via Ansible",
				                              "intf_ipv4": "10.99.99.99",
				                              "intf_ipv4_mask": "255.255.255.0",
				                              # "intf_speed": 1000,
				                              "port_status": "up"
                                    },
                                    {
                                      "intf_name": "Loopback 998",
				                              "intf_description": "Configured via Ansible",
				                              "intf_ipv4": "10.98.98.98",
				                              "intf_ipv4_mask": "255.255.255.0",
				                              # "intf_speed": 1000,
				                              "port_status": "up"
				                            }],
                                    "ansible_user": "developer",
                                    "ansible_password": "C1sco12345"
			                            }
                                ) 

stdout = runner.stdout.read()
stdout_lines = runner.stdout.readlines()
events = list(runner.events)
stats = runner.stats

print(stdout)
print(runner.status)
print(json.dumps(stats, indent=4))

