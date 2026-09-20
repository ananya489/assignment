from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

# Connect to Kafka
admin = KafkaAdminClient(
    bootstrap_servers="localhost:9092"
)

# Create topic
topic = NewTopic(
    name="server_metrics",
    num_partitions=1,
    replication_factor=1
)

try:
    admin.create_topics(new_topics=[topic])
    print("Topic created successfully!")

except TopicAlreadyExistsError:
    print("Topic already exists!")

finally:
    admin.close()
