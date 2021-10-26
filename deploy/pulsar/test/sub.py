# import pulsar

# client = pulsar.Client('pulsar://pulsar-rennes:6650')

# consumer = client.subscribe('my-tenant/my-namespace/my-topic', 'my-subscription')

# while True:
#     msg = consumer.receive()
#     try:
#         print("Received message '{}' id='{}'".format(msg.data(), msg.message_id()))
#         # Acknowledge successful processing of the message
#         consumer.acknowledge(msg)
#     except:
#         # Message failed to be processed
#         consumer.negative_acknowledge(msg)

# client.close()

from pulsar import Function

# Example function that uses the built in publish function in the context
# to publish to a desired topic based on config
class PublishFunction(Function):
  def __init__(self):
    pass

  def process(self, input, context):
    # publish_topic = "excla"
    # if "publish-topic" in context.get_user_config_map():
    #   publish_topic = context.get_user_config_value("publish-topic")
    # context.publish(publish_topic, input + '!')
    return input + '!'