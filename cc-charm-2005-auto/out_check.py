import subprocess
import os

# redirect_output = subprocess.run(["juju", "show-controller"])
# print(redirect_output)

# with open('ctrl.yml', 'w') as f:
#   f.write(redirect_output)
os.system("juju show-controller > ctrl.yml")