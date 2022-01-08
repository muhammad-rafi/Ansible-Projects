#!/usr/bin/env python

import ansible_runner
import json 


def main():
    """
    Run the playbook defined inside the function,
    and backup the configuration of iosxe device.
    """
    playbook = "/opt/ansible/Ansible-Projects/iosxe_ansible_project/playbooks/rest_loop_playbook.yml"
    inventory = "/opt/ansible/Ansible-Projects/iosxe_ansible_project/inventory.yml"
    
    kwargs = {
        "playbook": playbook, 
        "inventory": inventory,
        "envvars": '',
        "extravars": ''
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
            print("Loopback interface(s) have been configure successfully.")
            # print(json.dumps(stats, indent=4))
        else: 
            print(runner.status)
            print(json.dumps(stats, indent=4))
            
    except Exception as e: 
        print(e) 
        
if __name__ == '__main__':
    main()