# juju deploy ./tf-charms/contrail-command --to 3 --config docker-registry='bng-artifactory.juniper.net/contrail-nightly' --config image-tag=master.1159
juju deploy /root/tf-charms/contrail-command --constraints "tags=contrail-command" --config docker-registry="bng-artifactory.juniper.net/contrail-nightly" --config image-tag=2011.L2.311 --config docker-registry-insecure=true
juju add-relation contrail-command contrail-controller
juju change-user-password
juju show-controller
# Copy certificate to cert.pem
cat cert.pem | base64 > "cert.pem.b64"

juju show-controller --format json | jq -r '.["myjujucontroller"].details["ca-cert"]' | base64 > cert.pem.b64

# Need to create config file
cat config.yaml 

juju run-action contrail-command/0 import-cluster --params config.yaml
juju run-action contrail-command/2 import-cluster --params config.yaml
# Action queued with id: "1"

juju show-action-status 1
juju show-action-status 4
juju status
juju show-action-output 1 | grep result
juju show-action-output 4 | grep result

# juju remove-application contrail-command --force
# To access g20 in localhost, had to delete

ssh -L 8079:192.168.7.17:8079 root@10.204.216.194
# when the above doesn't work, try clientspecified
sudo ip route delete default

juju show-controller --format json | jq -r '.[\"myjujucontroller\"].details[\"ca-cert\"]'