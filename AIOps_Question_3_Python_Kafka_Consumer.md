Question 3 — Python Kafka Consumer
Objective

Write a Python Kafka consumer that consumes messages from the Kafka topic:

server_metrics

The consumer will:

Connect to Kafka broker localhost:9092
Subscribe to server_metrics
Continuously receive messages
Display server metrics
Check whether CPU usage is greater than 80%
Print an alert when CPU exceeds the threshold

We will use GitHub Codespaces + Python files only for the solution.

1. Project Structure

Use the same project from Question 2:

aiops-kafka/
├── topic.py
├── producer.py
└── consumer.py

For Question 3, the important file is:

consumer.py
2. Install Kafka Python Library

If you already installed it in Question 2, you can skip this.

Otherwise:

python -m pip install kafka-python

Verify:

python -c "from kafka import KafkaConsumer; print('kafka-python installed successfully')"

Expected:

kafka-python installed successfully
3. consumer.py

Create or replace consumer.py with this code:

from kafka import KafkaConsumer
import json

BROKER = "localhost:9092"
TOPIC = "server_metrics"
CPU_THRESHOLD = 80

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="aiops-consumer",
    value_deserializer=lambda value: json.loads(
        value.decode("utf-8")
    )
)

print("========================================")
print("       Python Kafka Consumer")
print("========================================")
print("Broker:", BROKER)
print("Topic:", TOPIC)
print("CPU Threshold:", CPU_THRESHOLD, "%")
print()
print("Waiting for messages...")
print("Press CTRL+C to stop.")
print()

try:

    for message in consumer:

        data = message.value

        server = data["server_id"]
        cpu = data["cpu_usage"]
        memory = data["memory_usage"]

        print("----------------------------------------")
        print("Received:")
        print("Server:", server)
        print("CPU:", cpu, "%")
        print("Memory:", memory, "%")

        if cpu > CPU_THRESHOLD:
            print()
            print("ALERT: High CPU detected on", server)
        else:
            print()
            print("Status: Normal")

except KeyboardInterrupt:

    print("\nConsumer stopped by user.")

finally:

    consumer.close()
    print("Kafka consumer closed.")
4. Run the Consumer

First make sure Kafka is running.

Then open a terminal in your Codespace:

cd aiops-kafka

Run:

python consumer.py

You should see:

========================================
       Python Kafka Consumer
========================================
Broker: localhost:9092
Topic: server_metrics
CPU Threshold: 80 %

Waiting for messages...
Press CTRL+C to stop.

The program will now continuously wait for Kafka messages.

5. Send Messages Using producer.py

Open another Codespace terminal.

Go to the project:

cd aiops-kafka

Run:

python producer.py

The producer sends messages to:

server_metrics

The consumer automatically receives them.

6. Example Normal Message

Suppose the producer sends:

{
    "server_id": "server01",
    "cpu_usage": 70,
    "memory_usage": 62
}

The consumer displays:

----------------------------------------
Received:
Server: server01
CPU: 70 %
Memory: 62 %

Status: Normal
7. Example Anomaly

Suppose the producer sends:

{
    "server_id": "server01",
    "cpu_usage": 85,
    "memory_usage": 62
}

The consumer displays:

----------------------------------------
Received:
Server: server01
CPU: 85 %
Memory: 62 %

ALERT: High CPU detected on server01

This satisfies the question requirement exactly.

8. Test With Your Question 2 Producer

Our Question 2 producer.py generates:

server1   CPU 50%
server2   CPU 54%
server3   CPU 58%
server4   CPU 62%
server5   CPU 66%
server6   CPU 70%
server7   CPU 74%
server8   CPU 78%
server9   CPU 82%
server10  CPU 86%

Therefore the consumer will generate alerts for:

server9  → CPU 82%
server10 → CPU 86%

Expected part of the output:

----------------------------------------
Received:
Server: server9
CPU: 82 %
Memory: 68 %

ALERT: High CPU detected on server9

and:

----------------------------------------
Received:
Server: server10
CPU: 86 %
Memory: 69 %

ALERT: High CPU detected on server10
9. Complete Execution Order

For your practical, remember this simple sequence.

Terminal 1 — Kafka

Make sure Kafka broker is running on:

localhost:9092
Terminal 2 — Create Topic

If you haven't already done Question 2:

cd aiops-kafka
python topic.py
Terminal 3 — Start Consumer
cd aiops-kafka
python consumer.py

Keep it running.

Terminal 4 — Start Producer
cd aiops-kafka
python producer.py

The consumer will receive the messages.

10. How the Code Works
Connect to Kafka
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER,

This connects the Python consumer to:

localhost:9092
Subscribe to Topic
TOPIC = "server_metrics"

and:

KafkaConsumer(TOPIC, ...)

subscribes to:

server_metrics
Deserialize JSON
value_deserializer=lambda value: json.loads(
    value.decode("utf-8")
)

Kafka receives bytes, so this converts:

bytes → UTF-8 → JSON → Python dictionary

For example:

{"server_id":"server01","cpu_usage":85,"memory_usage":62}

becomes a Python dictionary.

Continuously Receive Messages
for message in consumer:

This keeps listening for new Kafka messages.

That is why the consumer is suitable for real-time monitoring.

Read Metrics
server = data["server_id"]
cpu = data["cpu_usage"]
memory = data["memory_usage"]
Detect High CPU
if cpu > CPU_THRESHOLD:

where:

CPU_THRESHOLD = 80

So:

CPU = 80  → Normal
CPU = 81  → ALERT
CPU = 85  → ALERT
CPU = 95  → ALERT

The question specifically says greater than 80%, so we correctly use:

>

and not:

>=
11. Important Viva/MCQ Points
What is a Kafka Consumer?

A Kafka consumer is a program that reads messages from Kafka topics.

What topic are we consuming?
server_metrics
What is the broker?
localhost:9092
What is the CPU threshold?
80%
When is an alert generated?
CPU > 80%
What does for message in consumer do?

It continuously reads incoming Kafka messages.

Why use json.loads()?

To convert the JSON message received from Kafka into a Python dictionary.

Why auto_offset_reset="earliest"?

It allows the consumer to start from the earliest available messages when there is no existing offset for the consumer group.

Why group_id?
group_id="aiops-consumer"

identifies the consumer group used by Kafka to manage message offsets.

12. Final Exam Answer

If the examiner asks:

Write a Python Kafka consumer that consumes messages from server_metrics and alerts when CPU > 80%.

Your essential code is:

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "server_metrics",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="aiops-consumer",
    value_deserializer=lambda value: json.loads(
        value.decode("utf-8")
    )
)

for message in consumer:

    data = message.value

    server = data["server_id"]
    cpu = data["cpu_usage"]
    memory = data["memory_usage"]

    print("Received:")
    print("Server:", server)
    print("CPU:", cpu, "%")
    print("Memory:", memory, "%")

    if cpu > 80:
        print("ALERT: High CPU detected on", server)

Run it with:

python consumer.py

Q3 is complete when the Python consumer continuously receives server_metrics messages and prints ALERT: High CPU detected on <server> whenever CPU is greater than 80%.
