import yaml
import base64
import pexpect
import os

os.system("juju show-controller > controller.yml")
try:
  change_command = pexpect.spawn('juju change-user-password')
  change_command.expect('new password: ', timeout=5)
  change_command.sendline('c0ntrail123')
  change_command.expect('type new password again: ', timeout=5)
  change_command.sendline('c0ntrail123')
except Exception as e:
  print(str(e))
else:
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

  with open('/root/juju_import/cc-charm-2005-auto/auto_config.yml', 'w') as file:
    documents = yaml.dump(juju_config, file)