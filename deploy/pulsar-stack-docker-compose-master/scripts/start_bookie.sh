#!/bin/bash
export BOOKIE_CONF=/conf/bookkeeper.conf

# Apply the environment variables from the current shell to the zk configuration
/pulsar/bin/apply-config-from-env.py $BOOKIE_CONF

# Start the BookKeeper server
/pulsar/bin/bookkeeper bookie 
