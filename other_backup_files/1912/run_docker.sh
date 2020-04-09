export JUJU_CONTROLLER=192.168.30.18
export JUJU_MODEL=default
export CCD_IMAGE=bng-artifactory.juniper.net/contrail-nightly/contrail-command-deployer:1912.37

docker run -ti --net host --privileged -e action=import_cluster -e orchestrator=juju \
-e juju_controller=$JUJU_CONTROLLER \
-e juju_controller_user=root -e juju_model=$JUJU_MODEL \
-e juju_controller_password=c0ntrail123 \
-v /root/cluster_config.yaml:/cluster_config.yml $CCD_IMAGE
