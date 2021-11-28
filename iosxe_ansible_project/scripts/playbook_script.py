#!/usr/bin/env python

import ansible_runner
import json 

runner = ansible_runner.run(private_data_dir='/home/appdeveloper/iosxe-ansible/', 
                       playbook='intf_playbook.yml', 
                       inventory='inventory.yml',
                       envvars='',
                       extravars={"ip_interfaces": [
                                   {
                                    "intf_name": "GigabitEthernet 2",
                                    "intf_description": "Configured via Ansible",
                                    "intf_ipv4": "10.1.1.1",
                                    "intf_ipv4_mask": "255.255.255.0",
                                    "intf_speed": 1000,
                                    "port_status": "up"
                                    }
                                  ]
                                }
                            )

stdout = runner.stdout.read()
stdout_lines = runner.stdout.readlines()
events = list(runner.events)
stats = runner.stats

print(stdout)
print(runner.status)
print(json.dumps(stats, indent=4))

