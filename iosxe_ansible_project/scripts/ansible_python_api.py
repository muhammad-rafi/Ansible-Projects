#!/usr/bin/env python
import os
import sys
from getpass import getpass
from ansible import context
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.module_utils.common.collections import ImmutableDict

loader = DataLoader()

inventory = InventoryManager(loader=loader, 
                            sources='/opt/ansible/Ansible-Projects/iosxe_ansible_project/inventory.yml')

variable_manager = VariableManager(loader=loader, inventory=inventory)

variable_manager._extra_vars = {
                                "ip_interfaces":
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
playbook_path = '/opt/ansible/Ansible-Projects/iosxe_ansible_project/playbooks/intf_config_playbook.yml'

if not os.path.exists(playbook_path):
    print('[ERROR] The playbook does not exist')
    sys.exit()

context.CLIARGS = ImmutableDict(tags={},
                        listtags=False,
                        listtasks=False,
                        listhosts=False,
                        syntax=False,
                        connection='smart',
                        module_path=None,
                        forks=100,
                        # remote_user='developer',
                        # remote_pass=password,
                        private_key_file=None,
                        ssh_common_args=None,
                        ssh_extra_args=None,
                        sftp_extra_args=None,
                        scp_extra_args=None,
                        become=False, # 'True'
                        become_method=None, # 'sudo'
                        become_user=None, # 'root'
                        verbosity=True,
                        check=False,
                        start_at_task=None)



play_ex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager, loader=loader, passwords={})

results = play_ex.run()

print(play_ex)