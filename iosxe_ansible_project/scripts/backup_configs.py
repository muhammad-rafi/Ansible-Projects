#!/usr/bin/env python

import ansible_runner
from getpass import getpass
import json 


def main():
    """
    Run the playbook defined inside the function,
    and backup the configuration of iosxe device.
    """
    username = input("Username: ")
    password = getpass("Password: ")

    kwargs = {
        "playbook": "/opt/ansible/Ansible-Projects/iosxe_ansible_project/playbooks/config_backups_playbook.yml", 
        "inventory": "/opt/ansible/Ansible-Projects/iosxe_ansible_project/inventory.yml",
        "envvars": '',
        "extravars": {
                    "ansible_user": username,
                    "ansible_password": password
             }
            }

    try: 
        runner = ansible_runner.run(**kwargs)
                        
        stdout = runner.stdout.read()
        stdout_lines = runner.stdout.readlines()
        events = list(runner.events)
        stats = runner.stats

        # for event in events:
        #     print(event['event'])
        
        if runner.status == 'successful':
            print("Configuration Backups are completed!\nplease check the 'backups' folder \n")
            # print(json.dumps(stats, indent=4))
        else: 
            print(runner.status)
            print(json.dumps(stats, indent=4))
            
    except Exception as e: 
        print(e) 
        
if __name__ == '__main__':
    main()
    