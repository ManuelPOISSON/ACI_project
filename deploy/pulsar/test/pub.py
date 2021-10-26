import pulsar

client = pulsar.Client('pulsar://pulsar1:6650')

producer = client.create_producer('persistent://my-tenant/my-namespace/my-topic')
# producer = client.create_producer('my-topic')

for i in range(10):
    producer.send(('Hello-%d' % i).encode('utf-8'))

client.close()


# from pulsar import Function

# # Example function that uses the built in publish function in the context
# # to publish to a desired topic based on config
# class PublishFunction(Function):
#   def __init__(self):
#     pass

#   def process(self, input, context):
#     publish_topic = "publishtopic"
#     if "publish-topic" in context.get_user_config_map():
#       publish_topic = context.get_user_config_value("publish-topic")
#     context.publish(publish_topic, input + '!')
#     return