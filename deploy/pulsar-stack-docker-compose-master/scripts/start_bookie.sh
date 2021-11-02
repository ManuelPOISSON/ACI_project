#!/bin/bash
export BOOKIE_CONF=/conf/bookkeeper.conf
export SHARED_CONF=/conf/shared.conf.sh

# Apply the environment variables from the current shell to the zk configuration
/pulsar/bin/apply-config-from-env.py $BOOKIE_CONF
/pulsar/bin/apply-config-from-env.py $SHARED_CONF

# Start the BookKeeper server
/pulsar/bin/bookkeeper bookie 
