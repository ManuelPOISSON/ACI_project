#!/bin/bash

mkdir -p data/zookeeper
echo "\$ZK_ID" $ZK_ID
bin/pulsar zookeeper
