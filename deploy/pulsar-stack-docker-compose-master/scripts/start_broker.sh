#!/bin/bash
export PULSAR_BROKER_CONF=/conf/broker.conf
export SHARED_CONF=/conf/shared.conf.sh

# Apply the environment variables from the current shell to the zk configuration
/pulsar/bin/apply-config-from-env.py $PULSAR_BROKER_CONF
/pulsar/bin/apply-config-from-env.py $SHARED_CONF

# Start the broker
/pulsar/bin/pulsar broker
