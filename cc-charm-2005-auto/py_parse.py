import yaml
import base64

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

print(juju_config)
print(cert)
print(juju_config['juju-ca-cert'])
# with open('/root/juju_import/cc-charm-2005-auto/auto_config.yml', 'w') as file:
#   documents = yaml.dump(juju_config, file)