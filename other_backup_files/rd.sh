docker run -ti --net host --privileged -e action=import_cluster -e orchestrator=juju \
-e juju_controller=$JUJU_CONTROLLER \
-e juju_controller_user=root -e juju_model=$JUJU_MODEL \
-e juju_controller_password=c0ntrail123 \
-v /root/cluster_config.yaml:/cluster_config.yml $CCD_IMAGE
