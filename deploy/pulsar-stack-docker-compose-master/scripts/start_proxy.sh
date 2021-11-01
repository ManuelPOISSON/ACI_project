#!/bin/bash
export PULSAR_PROXY_CONF="/conf/proxy.conf"

# Apply the environment variables from the current shell to the zk configuration
/pulsar/bin/apply-config-from-env.py $PULSAR_PROXY_CONF

# Start the proxy
/pulsar/bin/pulsar proxy 
