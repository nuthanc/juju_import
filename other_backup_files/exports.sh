export JUJU_CONTROLLER=10.87.79.1 #svl maas node
export JUJU_MODEL=contrail #use default for local model
export CCD_IMAGE=bng-artifactory.juniper.net/contrail-nightly/contrail-command-deployer:2002.23

echo "Ensure cluster_config.yaml is having the right tag and you have sourced this file"
