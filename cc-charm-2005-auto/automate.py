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


def wait_till_machine_is_deployed():
  juju_status = subprocess.run(['juju', 'status'], stdout=subprocess.PIPE, universal_newlines=True)
  print("Sleep for 300s while waiting for machine to get deployed")
  time.sleep(300)
  while('Missing cloud orchestrator' not in juju_status.stdout):
    juju_status = subprocess.run(['juju', 'status'], stdout=subprocess.PIPE, universal_newlines=True)
    print(juju_status.stdout)
    time.sleep(10)


def add_relation_to_contrail_controller():
  subprocess.run(['juju', 'add-relation', 'contrail-command', 'contrail-controller'])


def run_action_config(deploy_unit):
  out = subprocess.run(['juju', 'run-action', deploy_unit, 'import-cluster', '--params', 'config.yaml'], stdout=subprocess.PIPE, universal_newlines=True)
  print(out.stdout)
  id = out.stdout.split(":")[1].strip().split("\"")[1]
  print("id",id)
  return id


def action_status_and_result(id):
  subprocess.run(['juju', 'show-action-status', id])
  action_status = subprocess.run(['juju', 'show-action-status', id], stdout=subprocess.PIPE, universal_newlines=True)
  print(action_status.stdout)
  while 'status: completed' not in action_status.stdout:
    action_status = subprocess.run(['juju', 'show-action-status', id], stdout=subprocess.PIPE, universal_newlines=True)
    print(action_status.stdout)
    time.sleep(10)
    
  action_result = subprocess.run(['juju', 'show-action-output', id], stdout=subprocess.PIPE, universal_newlines=True)
  print(action_result.stdout)
  while 'Success' not in action_result.stdout:
    action_result = subprocess.run(['juju', 'show-action-output', id], stdout=subprocess.PIPE, universal_newlines=True)
    print(action_result.stdout[-250:])
    time.sleep(10)


def parse_deploy_unit():
  deploy_unit_output = subprocess.check_output('juju status|grep "contrail-command/"', shell=True, universal_newlines=True)
  if "*" in deploy_unit_output:
    deploy_unit = deploy_unit_output.split("*")[0].strip()
  else:
    deploy_unit = deploy_unit_output.split()[0].strip()
  return deploy_unit


def deploy(charm_path='/root/tf-charms/contrail-command', image_tag='2005.1'):
  image_tag_config = f"image-tag={image_tag}"
  juju_deploy = subprocess.run(['juju', 'deploy', charm_path, '--constraints', 'tags=contrail-command', '--config', 'docker-registry=bng-artifactory.juniper.net/contrail-nightly', '--config', image_tag_config, '--config', 'docker-registry-insecure=true'], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines=True)
  print(juju_deploy.stdout)
  
  wait_till_machine_is_deployed()
  add_relation_to_contrail_controller()
  prepare_config_file()
  print("Sleeping for 90s for the Unit to get Ready")
  time.sleep(90)
  deploy_unit = parse_deploy_unit()
  id = run_action_config(deploy_unit)
  action_status_and_result(id)



if __name__ == '__main__':
  change_user_password()
  deploy(image_tag='2008.29')
  # The below 3 for debugging
  # deploy_unit = parse_deploy_unit()
  # id = run_action_config(deploy_unit)
  # action_status_and_result(id)

