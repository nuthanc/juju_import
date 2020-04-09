# juju deploy ./tf-charms/contrail-command --to 3 --config docker-registry='bng-artifactory.juniper.net/contrail-nightly' --config image-tag=master.1159
juju deploy ./tf-charms/contrail-command --constraints "tags=g20" --config docker-registry='bng-artifactory.juniper.net/contrail-nightly' --config image-tag=master.1159

juju status
juju add-relation contrail-command contrail-controller
juju status
juju change-user-password
juju show-controller
# Copy certificate to cert.pem
cat cert.pem | base64 > "cert.pem.b64"
# Need to create config file
cat config.yaml 

juju run-action contrail-command/2 import-cluster --params config.yaml
# Action queued with id: "3"
juju status
juju show-action-status 4
juju status
juju show-action-output 4 | grep result

# juju remove-application contrail-command --force
