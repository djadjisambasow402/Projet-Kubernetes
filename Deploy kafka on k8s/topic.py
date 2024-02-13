from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer, KafkaConsumer

bootstrap_servers = '192.168.2.240:9092'
topic_name = 'domodatopic'
num_partitions = 3
replication_factor = 1

# Create a topic with the Admin API
admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
topic_spec = {
    "name": topic_name,
    "num_partitions": num_partitions,
    "replication_factor": replication_factor
}
admin_client.create_topics([NewTopic(**topic_spec)])

# Produce a test message
message_value = "Test message from outside the cluster"
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
producer.send(topic_name, value=message_value.encode("utf-8"))  # Encode the value to bytes

# Consume the test message
consumer = KafkaConsumer(topic_name, bootstrap_servers=bootstrap_servers, auto_offset_reset="earliest")
for message in consumer:
    print(message.value.decode("utf-8"))

