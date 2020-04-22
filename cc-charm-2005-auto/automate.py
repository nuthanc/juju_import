import yaml
import base64
import pexpect
import os
import time
import subprocess

def change_user_password():
  try:
    change_command = pexpect.spawn('juju change-user-password')
    change_command.expect('new password: ', timeout=5)
    change_command.sendline('c0ntrail123')
    change_command.expect('type new password again: ', timeout=5)
    change_command.sendline('c0ntrail123')
  except Exception as e:
    print(str(e))


def prepare_config_file():
  os.system("juju show-controller > /root/juju_import/cc-charm-2005-auto/controller.yml")

  with open('/root/juju_import/cc-charm-2005-auto/controller.yml') as file:
    controller = yaml.load(file, Loader=yaml.FullLoader)
    juju_config = {}
    cert = controller['myjujucontroller']['details']['ca-cert']
    cert_bytes = cert.encode('ascii')
    base64_bytes = base64.b64encode(cert_bytes)
    juju_config['juju-ca-cert'] = base64_bytes.decode('ascii')
    juju_config['juju-controller'] = controller['myjujucontroller']['details']['api-endpoints'][0].split(":")[0]
    juju_config['juju-model-id'] = controller['myjujucontroller']['models']['default']['model-uuid']
    juju_config['juju-controller-password'] = 'c0ntrail123'

    with open('/root/juju_import/cc-charm-2005-auto/config.yaml', 'w') as file:
      documents = yaml.dump(juju_config, file)


def deploy(charm_path='/root/tf-charms/contrail-command'):
  deploy_output = subprocess.run(['juju', 'deploy', charm_path, '--constraints', 'tags=g20', '--config', 'docker-registry=bng-artifactory.juniper.net/contrail-nightly', '--config', 'image-tag=master.1186', '--config', 'docker-registry-insecure=true'], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines=True)
  
  cc = deploy_output.stdout.split("-")[2].split("\"")[0]

  juju_status = subprocess.run(['juju', 'status'], stdout=subprocess.PIPE, universal_newlines=True)

  while('Missing cloud orchestrator' not in juju_status.stdout):
    juju_status = subprocess.run(['juju', 'status'], stdout=subprocess.PIPE, universal_newlines=True)
    print(juju_status.stdout)
    time.sleep(10)

  subprocess.run(['juju', 'add-relation', 'contrail-command', 'contrail-controller'])

  cc = "contrail-command/" + cc
  out = subprocess.run(['juju', 'run-action', cc, 'import-cluster', '--params', 'config.yaml'], stdout=subprocess.PIPE, universal_newlines=True)
  id = out.stdout.split(":")[1].strip()
  subprocess.run(['juju', 'show-action-status', id])
  result = subprocess.run(['juju', 'show-action-status', id], stdout=subprocess.PIPE, universal_newlines=True)
  while('Success' not in result.stdout):
    result = subprocess.run(['juju', 'show-action-status', id], stdout=subprocess.PIPE, universal_newlines=True)
    print(result.stdout[-15:])
  


if __name__ == '__main__':
  change_user_password()
  prepare_config_file()
  deploy()

  