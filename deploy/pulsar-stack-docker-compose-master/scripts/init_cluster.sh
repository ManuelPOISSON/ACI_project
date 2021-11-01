#!/bin/bash
/pulsar/bin/pulsar initialize-cluster-metadata \
  --cluster $clusterName \
  --zookeeper $zkServers \
  --web-service-url $pulsarNode:$webServicePort \
  --configuration-store $configurationStore \
  --broker-service-url pulsar://$pulsarNode:brokerServicePort \
