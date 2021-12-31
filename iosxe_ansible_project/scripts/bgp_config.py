#!/usr/bin/env python

import ansible_runner

def bgp_config() -> dict:
    """
    Run the playbook defined inside the function,
    variable will be parsed via var files.
    """
    kwargs = {
        'playbook': '/opt/ansible/Ansible-Projects/iosxe_ansible_project/playbooks/bgp_config_playbook.yml',
        'inventory': '/opt/ansible/Ansible-Projects/iosxe_ansible_project/inventory.yml'
    }
    
    try: 
        runner = ansible_runner.run(**kwargs)
        
        events = list(runner.events)
        job_status = runner.status

        for event in events:
            if 'event_data' in event:
                event_data = event['event_data']
            if 'host' in event_data:
                host = event_data['host']

        if job_status == 'successful':
            status = f"{host} has been configured successfully.\n"

        if job_status == 'failed':
            status = f"[Error]: {host} changes are failed\n"

        return status 
    
    except Exception as e: 
        print(e)
    
if __name__ == '__main__':
    
    results = bgp_config()
    print(results)