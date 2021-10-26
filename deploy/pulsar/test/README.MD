# Dev

To dev, be sure to open this part of the project from the docker remote extension. This will enable you to work from a controlled Python 3.7 environnement with `pulsar-client` installed in it.


<!-- # Test

```sh
sed -i "s/localhost/broker-beijing/g" /pulsar/conf/client.conf
/pulsar/bin/pulsar-admin tenants create my-tenant  --allowed-clusters beijing
/pulsar/bin/pulsar-admin namespaces create my-tenant/my-namespace --clusters beijing
``` -->

# Test 2

```sh
docker run --name client  -it --rm  --network test_pulsar apachepulsar/pulsar-test-latest-version:latest /bin/bash 
```
## Inside the container
```sh
sed -i "s/localhost/pulsar-rennes/g" /pulsar/conf/client.conf
/pulsar/bin/pulsar-admin tenants create my-tenant  --allowed-clusters cluster-rennes
/pulsar/bin/pulsar-admin namespaces create my-tenant/my-namespace --clusters cluster-rennes
```
## To start a consumer/publisher
```sh
/pulsar/bin/pulsar-client consume -s "sub-rennes" my-tenant/my-namespace/t1 -n 0
/pulsar/bin/pulsar-client produce  my-tenant/my-namespace/t1  --messages "hello-from-rennes" -n 10
```
/pulsar/bin/pulsar-client consume -s "sub-rennes" my-tenant/my-namespace/my-topic-excl -n 0

# Functions 
```sh
pulsar/bin/pulsar-admin functions create \
    --py sub.py \
    --classname PublishFunction \
    --inputs persistent://my-namespace/my-tenant/my-topic \
    --output persistent://my-namespace/my-tenant/my-excla \
    --name excla
```

```sh
/pulsar/bin/pulsar-client consume -s "sub-rennes" my-tenant/my-namespace/my-excla -n 0
/pulsar/bin/pulsar-client produce  my-tenant/my-namespace/my-topic  --messages "hello-from-rennes" -n 10
```