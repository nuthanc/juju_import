juju deploy ./tf-charms/contrail-command --to g20 --config docker-registry='bng-artifactory.juniper.net/contrail-nightly' --config image-tag=master.1159
juju status
juju add-relation contrail-command contrail-controller
juju status
juju change-user-password
juju show-controller
# Copy certificate to cert.pem
cat cert.pem | base64 > "cert.pem.b64"
# Need to create config file
cat config.yaml 

juju run-action contrail-command/0 import-cluster --params config.yaml
# Action queued with id: "65"
juju status
juju show-action-status 65
juju status
juju show-action-output 65 | grep result