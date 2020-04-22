import yaml
import base64
import pexpect
import os
import time

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


def deploy():
  os.system('juju deploy /root/tf-charms/contrail-command --constraints "tags=g20" --config docker-registry="bng-artifactory.juniper.net/contrail-nightly" --config image-tag=master.1167 --config docker-registry-insecure=true')
  # subprocess.run(['juju', 'deploy', '/root/tf-charms/contrail-command', '--constraints', 'tags=g20', '--config', 'docker-registry=bng-artifactory.juniper.net/contrail-nightly', '--config', 'image-tag=master.1167', '--config', 'docker-registry-insecure=true'])
  time.sleep(2)
  os.system("juju add-relation contrail-command contrail-controller")
  time.sleep(900)
  os.system("juju run-action contrail-command/0 import-cluster --params config.yaml")
  os.system("juju show-action-status 1")


if __name__ == '__main__':
  change_user_password()
  prepare_config_file()
  deploy()

  