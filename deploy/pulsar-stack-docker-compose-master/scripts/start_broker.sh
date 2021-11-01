#!/bin/bash
export PULSAR_BROKER_CONF=/conf/broker.conf

# Apply the environment variables from the current shell to the zk configuration
/pulsar/bin/apply-config-from-env.py $PULSAR_BROKER_CONF

# Start the broker
/pulsar/bin/pulsar broker
