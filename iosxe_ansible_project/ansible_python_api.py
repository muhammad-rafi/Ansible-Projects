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

inventory = InventoryManager(loader=loader, sources='/home/appdeveloper/iosxe-ansible/inventory.yml')

variable_manager = VariableManager(loader=loader, inventory=inventory)

variable_manager._extra_vars = {"ip_interfaces": [
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
playbook_path = '/home/appdeveloper/iosxe-ansible/intf_playbook.yml'

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
                        #remote_user='developer',
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


print(dir(play_ex))

