# juju deploy ./tf-charms/contrail-command --to 3 --config docker-registry='bng-artifactory.juniper.net/contrail-nightly' --config image-tag=master.1159
juju deploy ./tf-charms/contrail-command --constraints "tags=g20" --config docker-registry="bng-artifactory.juniper.net/contrail-nightly" --config image-tag=master.1167 --config docker-registry-insecure=true
juju add-relation contrail-command contrail-controller
juju change-user-password
juju show-controller
# Copy certificate to cert.pem
cat cert.pem | base64 > "cert.pem.b64"
# Need to create config file
cat config.yaml 

juju run-action contrail-command/0 import-cluster --params config.yaml
# Action queued with id: "1"

juju show-action-status 1
juju status
juju show-action-output 1 | grep result

# juju remove-application contrail-command --force
# To access g20 in localhost, had to delete
sudo ip route delete default