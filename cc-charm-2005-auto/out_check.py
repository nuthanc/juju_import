import os
import yaml

with open('/root/juju_import/cc-charm-2005-auto/controller.yml') as file:
    controller = yaml.load(file, Loader=yaml.FullLoader)
    cert = controller['myjujucontroller']['details']['ca-cert']
    with open('cert.pem','w') as file:
      file.write(cert)

os.system("cat cert.pem | base64 > 'cert.pem.b64'")
