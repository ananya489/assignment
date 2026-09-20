from kafka import KafkaConsumer
import json

# Create Kafka consumer
consumer = KafkaConsumer(
    "server_metrics",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="aiops-monitor",
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)

print("Waiting for messages...")

# Continuously consume messages
for message in consumer:
    data = message.value

    server = data["server_id"]
    cpu = data["cpu_usage"]
    memory = data["memory_usage"]

    print("\nReceived:")
    print("Server:", server)
    print("CPU:", cpu, "%")
    print("Memory:", memory, "%")

    # High CPU detection
    if cpu > 80:
        print("ALERT: High CPU detected on", server)