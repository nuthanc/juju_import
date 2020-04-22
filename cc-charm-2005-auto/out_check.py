import os
import yaml
import subprocess

def gen_cert_and_b64():
  """
  Take controller.yml as input and generate cert.pem and cert.pem.b64
  """
  with open('/root/juju_import/cc-charm-2005-auto/controller.yml') as file:
      controller = yaml.load(file, Loader=yaml.FullLoader)
      cert = controller['myjujucontroller']['details']['ca-cert']
      with open('cert.pem','w') as file:
        file.write(cert)
  os.system("cat cert.pem | base64 > 'cert.pem.b64'")
# End of gen_cert_and_b64

# os.system("juju status")
# os.system("cat cmd.sh")
out = subprocess.run(["juju", "status"],stdout=subprocess.PIPE, universal_newlines=True)
print(out.stdout)