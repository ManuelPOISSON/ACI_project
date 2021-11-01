#!/bin/bash
export PULSAR_ZK_CONF=/conf/zookeeper.conf 

# Apply the environment variables from the current shell to the zk configuration
/pulsar/bin/apply-config-from-env.py $PULSAR_ZK_CONF
/pulsar/bin/generate-zookeeper-config.sh $PULSAR_ZK_CONF

# Load the zookeeper
/pulsar/bin/pulsar zookeeper
