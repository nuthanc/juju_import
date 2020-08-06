2020-08-06 09:57:29,200 p=50 u=root |  fatal: [192.168.30.60]: UNREACHABLE! => {"changed": false, "msg": "SSH Error: data could not be sent to remote host \"192.168.30.60\". Make sure this host can be reached over ssh", "unreachable": true}
2020-08-06 09:57:29,202 p=50 u=root |   to retry, use: --limit @/root/contrail-ansible-deployer/playbooks/configure_instances.retry


2020-08-06 09:57:29,202 p=50 u=root |  PLAY RECAP *********************************************************************
2020-08-06 09:57:29,203 p=50 u=root |  192.168.30.60              : ok=0    changed=0    unreachable=1    failed=0
2020-08-06 09:57:29,203 p=50 u=root |  localhost                  : ok=66   changed=7    unreachable=0    failed=0