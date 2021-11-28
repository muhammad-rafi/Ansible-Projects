#!/usr/bin/env python

import ansible_runner
from getpass import getpass
import json 

username = input("Username: ")
password = getpass("Password: ")

runner = ansible_runner.run( 
                       playbook='/opt/ansible/Ansible-Projects/iosxe_ansible_project/playbooks/config_backups_playbook.yml', 
                       inventory='/opt/ansible/Ansible-Projects/iosxe_ansible_project/inventory.yml',
                       envvars='',
                       extravars={
                                    "ansible_user": username,
                                    "ansible_password": password
			                    }
                            ) 

stdout = runner.stdout.read()
stdout_lines = runner.stdout.readlines()
events = list(runner.events)
stats = runner.stats

if runner.status == 'successful':
    print("Configuration Backups are completed!\n,please check 'backups' folder \n")
    # print(json.dumps(stats, indent=4))
else: 
    print(runner.status)
    print(json.dumps(stats, indent=4))


