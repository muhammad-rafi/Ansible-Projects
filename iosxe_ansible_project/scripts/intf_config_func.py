#!/usr/bin/env python

import ansible_runner
from getpass import getpass
import json

def intf_config(config_data) -> dict:
    """
    Run the playbook defined inside the function,
    extravars will come via config_date dict 
    variable. 
    """
    kwargs = {
        # 'private_data_dir': '/opt/ansible/Ansible-Projects/iosxe_ansible_project/', 
        'playbook': '/opt/ansible/Ansible-Projects/iosxe_ansible_project/playbooks/intf_config_playbook.yml',
        'inventory': '/opt/ansible/Ansible-Projects/iosxe_ansible_project/inventory.yml',
        'envvars': '',
        'extravars': config_data
    }
    
    try: 
        runner = ansible_runner.run(**kwargs)
        
        stdout = runner.stdout.read()
        stdout_lines = runner.stdout.readlines()
        events = list(runner.events)
        stats = runner.stats
        job_status = runner.status

        # print(json.dumps(stats, indent=4))
        # print(job_status)

        for event in events:
            if 'event_data' in event:
                event_data = event['event_data']
            if 'host' in event_data:
                host = event_data['host']

        for event in events:
            if 'event_data' in event:
                event_data = event['event_data']
                if 'res' in event_data:
                    resp = event_data['res']
                    if 'intf_config.updates' in resp:
                        updates = resp['intf_config.updates']
                        # msg_data = json.dumps(updates, indent=4) ## green
                    if 'msg' in resp:
                        updates = resp['msg']
                        # msg_data = json.dumps(updates, indent=4) ## red

        if job_status == 'successful':
            status = f"{host} has been configured successfully." ## green

        if job_status == 'failed':
            status = f"[Error]: {host} changes are failed" ## red

        return_data = {"host": host, "status": job_status, "data": updates}
        
        return json.dumps(return_data, indent=4)
    
    except Exception as e: 
        print(e)
    
if __name__ == '__main__':
    
    username = input("Username: ")
    password = getpass("Password: ")
       
    config_data = {"ip_interfaces":
                    [{
                        "intf_name": "Loopback 998",
                        "intf_description": "Configured via Ansible",
                        "intf_ipv4": "10.98.98.98",
                        "intf_ipv4_mask": "255.255.255.0",
                        # "intf_speed": 1000,
                        "port_status": "up"
                    },
                    {
                        "intf_name": "Loopback 999",
                        "intf_description": "Configured via Ansible",
                        "intf_ipv4": "10.99.99.99",
                        "intf_ipv4_mask": "255.255.255.0",
                        # "intf_speed": 1000,
                        "port_status": "up"
                    }],
                    "ansible_user": username,
                    "ansible_password": password
                    }
    
    results = intf_config(config_data)
    print(results)