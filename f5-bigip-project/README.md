# Ansible Project for F5 BIG-IP LTM 
## Introduction
This repository focuses on F5 BIG-IP configurations automation 
via Ansible, this project can also be imported/added onto the Tower/AWX 
and then call the Tower APIs via CURL or Postman to launch the jobs to automate
the BIG-IP configurations, which gives the opportunity to integrate this with 
third part tool for orchestration.

This project covers the followings configurations items 
- BIG-IP Base config (e.g. ntp/dns/syslog etc.)
- BIG-IP HA Failover Setup
- BIG-IP Tenant onboarding 
- BIG-IP Config Backup
- Partition 
- Nodes/Pool/Virtual Servers
- VLAN and Self-IP 
- Static Routes 
- More …

Here are the screenshots of the pair of F5 BIG-IPs used during the
project, you can see one is active and other one is in standby mode. 

#### BIG-IP Active 
![App Screenshot](https://github.com/muhammad-rafi/Ansible-Projects/blob/main/f5-bigip-project/images/bigip_active.PNG)

#### BIG-IP Standby 
![App Screenshot](https://github.com/muhammad-rafi/Ansible-Projects/blob/main/f5-bigip-project/images/bigip_standby.PNG)

### Versions 
```
Ansible: 2.9.16
Python: 3.6.8
F5 BIG-IP: 15.1.2.1
f5-icontrol-rest: 1.3.13
f5-sdk: 3.0.21
```
## Usage: 

Clone the repository and create a virtual environment then 
install the required packages from the requirement.txt 
```
$ git clone https://github.com/muhammad-rafi/Ansible-Projects
$ sudo yum install python3-virtualenv
$ virtualenv .venv
$ source .venv/bin/activate

(.venv) $ cd Ansible-Projects/f5-bigip-project/
(.venv) $ $ pip3 install -r requirements.txt
```

## Topology 
Here is the topology used for this project 
![App Screenshot](https://github.com/muhammad-rafi/Ansible-Projects/blob/main/f5-bigip-project/images/bigip_topology.PNG)

### Ansible Config File (ansible.cfg)
```bash
[defaults]

inventory = inventory.yml
forks=10
callback_whitelist = profile_tasks
host_key_checking = False
roles_path = ~/f5-bigip-project/roles/
timeout = 300
log_path = ~/f5-bigip-project/ansible.log
deprecation_warnings=False
ansible_python_interpreter = /usr/bin/python3
collections_paths = ~/.ansible/collections
retry_files_enabled = False
#retry_files_save_path = ~/.ansible/retry-files
vault_password_file = .vault_pass
```
### Ansible inventory File (inventory.yml)

```bash
all:
  children:
    eve_bigip:
      hosts:
        eve-bigip01.devnetbro.com:
        eve-bigip02.devnetbro.com:
```
### Ansible variables
Ansible variable for BIG-IP defined in three ways for this project
- host_vars directory for the hosts defined in inventory
- Specific variable file for particular playbook 
- Pass the variables via extra vars via CLI or Postman/curl 

Here is example of variables defined in bigip_basic_vars_file.yml 
for bigip-basic-config-ha-vars.yml playbook
```bash
---

# F5 BIG-IP Initial configuration variables 
initial_setup: "no"

# Variable for bigip-basic-config.yml playbook
# bigip_name: eve-bigip01.devnetbro.com
bigip_names:
  name:
    - eve-bigip01.devnetbro.com
    - eve-bigip02.devnetbro.com

timezone: UTC

users:
  - username: devnetbro
    password: myP@ssw0rd!23
    full_name: Devnet Bro
    partition: Common
    access: all:admin # Parition:Role
    update_password: always
    shell: bash # choices: tmsh, bash, none
    state: present

ntp_servers:
  servers:
    - 192.168.56.9
    - 192.168.56.10
  state: present 

name_servers:
  servers:
    - 192.168.56.3
    - 192.168.56.4
  domains: 
    - devnetbro.com
  cache: disabled
  ip_version: 4
  state: present 

remote_host:
  hosts:
    - host: 192.168.56.5
      port: '514'
      local_ip: none
    - host: 192.168.56.6
      port: '514'
      local_ip: none
  state: present
```

### Ansible Playbook 
This is one of the playbook from this project to create the nodes
on F5 BIG-IP 
```bash
- name: CREATE F5 BIGIP NODES
  hosts: eve_bigip
  gather_facts: false  
  connection: local
  collections: 
    - f5networks.f5_modules
    
  vars:
    cli:
      server: "{{ inventory_hostname }}"
      user: "{{ ansible_user }}"
      password: "{{ ansible_pass }}"
      server_port: "{{ port }}"
      validate_certs: no

  tasks:
    - name: CONFIGURE BIGIP NODES
      include_role: 
        name: bigip-vip-pool
        tasks_from: nodes.yml
```
### Running the playbook
To run the playbooks exist in the project main folder 
`ansible-playbook bigip-nodes.yml` 
```bash
[ansible@vCentOS f5-bigip-project]$ ansible-playbook bigip-nodes.yml

PLAY [CREATE F5 BIGIP NODES] ***************************************************************************************

TASK [CONFIGURE BIGIP NODES] ***************************************************************************************
Friday 01 October 2021  01:25:43 +0100 (0:00:00.197)       0:00:00.197 ********

TASK [bigip-vip-pool : Create nodes] *******************************************************************************
Friday 01 October 2021  01:25:43 +0100 (0:00:00.583)       0:00:00.781 ********
changed: [eve-bigip02.devnetbro.com] => (item={'name': 'http_pool_member_1', 'description': 'http_pool_member_1', 'partition': 'TENANT_2', 'address': '192.168.20.11', 'port': 80, 'state': 'enabled'})
changed: [eve-bigip01.devnetbro.com] => (item={'name': 'http_pool_member_1', 'description': 'http_pool_member_1', 'partition': 'TENANT_2', 'address': '192.168.20.11', 'port': 80, 'state': 'enabled'})
changed: [eve-bigip02.devnetbro.com] => (item={'name': 'http_pool_member_2', 'description': 'http_pool_member_2', 'partition': 'TENANT_2', 'address': '192.168.20.12', 'port': 80, 'state': 'enabled'})
changed: [eve-bigip01.devnetbro.com] => (item={'name': 'http_pool_member_2', 'description': 'http_pool_member_2', 'partition': 'TENANT_2', 'address': '192.168.20.12', 'port': 80, 'state': 'enabled'})

PLAY RECAP *********************************************************************************************************
eve-bigip01.devnetbro.com  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
eve-bigip02.devnetbro.com  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  

Friday 01 October 2021  01:25:59 +0100 (0:00:15.456)       0:00:16.237 ********
===============================================================================
bigip-vip-pool : Create nodes ------------------------------------------------------------------------------ 15.46s
CONFIGURE BIGIP NODES --------------------------------------------------------------------------------------- 0.58s
```
### Add project onto the Ansible Tower/AWX 
This project can be added on Ansible Tower/AWX via GIT source control URL 
`https://github.com/muhammad-rafi/Ansible-Projects.git`,
see the screenshot below. 
![App Screenshot](https://github.com/muhammad-rafi/Ansible-Projects/blob/main/f5-bigip-project/images/bigip_awx_project.PNG)

### Create a Job Template on Ansible Tower/AWX 
Once you added the project onto the Tower/AWX, you can now create job
templates for the playbooks it has in the project. Here are some job templates  
I have created for this project. 
![App Screenshot](https://github.com/muhammad-rafi/Ansible-Projects/blob/main/f5-bigip-project/images/bigip_awx_templates.PNG)

You can either run the job templates from Tower/AWX directly or utilise the
Tower APIs via curl or Postman to lanuch those templates. I have added
postman collection in the main folder along with the environmen variables
Here are the screens for both Tower/AWX Jobs and via Postman. 

#### Via Tower/AWX Jobs 
![App Screenshot](https://github.com/muhammad-rafi/Ansible-Projects/blob/main/f5-bigip-project/images/bigip_awx_job_run.PNG)

#### via Postman
![App Screenshot](https://github.com/muhammad-rafi/Ansible-Projects/blob/main/f5-bigip-project/images/bigip_postman.PNG)

## Environment Variables

As you can see from my ansible config file `ansible.cfg`, I 
am using a vault for password protection `vault_password_file = .vault_pass`, 
therefore, you will need to create your own vault if you like to use one. 

## ISSUES

You may find some of the plays are not idempotent as this is how they are 
and I have already raised few issues with [F5Networks/f5-ansible](https://github.com/F5Networks/f5-ansible)


## Authors

[Muhammad Rafi](https://github.com/muhammad-rafi)

## License

The source code is released under the [MIT](https://choosealicense.com/licenses/mit/).
