Question 5 — Integrated AIOps Challenge

We will modify the Python Kafka consumer from Question 3 and turn it into a simple AIOps monitoring system.

We will use:

GitHub Codespaces
Python
kafka-python
Kafka topic: server_metrics
Python files only
CPU threshold: 80%

The flow is:

Kafka Producer
      ↓
server_metrics
      ↓
AIOps Python Consumer
      ↓
Check CPU
      ↓
CPU > 80% ?
   ↙       ↘
 YES       NO
  ↓         ↓
ALERT     Normal
  ↓
anomaly_count++
1. Project Structure

Use the same project:

aiops-kafka/
├── topic.py
├── producer.py
├── consumer.py
└── aiops_monitor.py

For Question 5, the new file is:

aiops_monitor.py
2. Install Kafka Python Library

If you already installed it in Questions 2 and 3, skip this.

Otherwise:

python -m pip install kafka-python

Verify:

python -c "from kafka import KafkaConsumer; print('kafka-python installed successfully')"

Expected:

kafka-python installed successfully
3. Create aiops_monitor.py

Create:

aiops-kafka/aiops_monitor.py

Use this complete code:

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
    group_id="aiops-monitor",
    value_deserializer=lambda value: json.loads(
        value.decode("utf-8")
    )
)

anomaly_count = 0

print("==========================================")
print("        AIOps Monitoring System")
print("==========================================")
print("Broker:", BROKER)
print("Topic:", TOPIC)
print("CPU Threshold:", CPU_THRESHOLD, "%")
print()
print("Monitoring started...")
print("Press CTRL+C to stop.")
print()

try:

    for message in consumer:

        data = message.value

        server = data["server_id"]
        cpu = data["cpu_usage"]
        memory = data["memory_usage"]

        print("------------------------------------------")
        print(
            f"Message received: {server} | CPU: {cpu}%"
        )
        print(f"Memory: {memory}%")

        if cpu > CPU_THRESHOLD:

            anomaly_count += 1

            print("ALERT: High CPU detected")
            print(
                f"Total anomalies detected: {anomaly_count}"
            )

        else:

            print("Normal")

except KeyboardInterrupt:

    print()
    print("==========================================")
    print("       AIOps Monitoring Stopped")
    print("==========================================")
    print(
        f"Total anomalies detected: {anomaly_count}"
    )

finally:

    consumer.close()
    print("Kafka consumer closed.")
4. Run the AIOps Monitor

Make sure you're inside the project:

cd aiops-kafka

Run:

python aiops_monitor.py

You should see:

==========================================
        AIOps Monitoring System
==========================================
Broker: localhost:9092
Topic: server_metrics
CPU Threshold: 80 %

Monitoring started...
Press CTRL+C to stop.

The program will continuously monitor Kafka.

5. Start the Producer

Open another Codespace terminal.

cd aiops-kafka

Run:

python producer.py

The producer sends the 10 messages from Question 2.

6. Expected Monitoring Output

For example:

------------------------------------------
Message received: server1 | CPU: 50%
Memory: 60%
Normal

Then:

------------------------------------------
Message received: server2 | CPU: 54%
Memory: 61%
Normal

And eventually:

------------------------------------------
Message received: server9 | CPU: 82%
Memory: 68%
ALERT: High CPU detected
Total anomalies detected: 1

Then:

------------------------------------------
Message received: server10 | CPU: 86%
Memory: 69%
ALERT: High CPU detected
Total anomalies detected: 2

So with our Question 2 producer:

Total anomalies detected: 2

because:

server9  → CPU 82% → ANOMALY
server10 → CPU 86% → ANOMALY
7. Test With Custom Messages

You can also modify producer.py to send specific test values.

For example:

from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

messages = [
    {
        "server_id": "server01",
        "cpu_usage": 85,
        "memory_usage": 62
    },
    {
        "server_id": "server02",
        "cpu_usage": 45,
        "memory_usage": 55
    },
    {
        "server_id": "server03",
        "cpu_usage": 91,
        "memory_usage": 70
    }
]

for message in messages:

    producer.send(
        "server_metrics",
        value=message
    )

    print("Sent:", message)

    time.sleep(1)

producer.flush()
producer.close()

Run:

python producer.py

The AIOps monitor should produce:

Message received: server01 | CPU: 85%
Memory: 62%
ALERT: High CPU detected
Total anomalies detected: 1

Message received: server02 | CPU: 45%
Memory: 55%
Normal

Message received: server03 | CPU: 91%
Memory: 70%
ALERT: High CPU detected
Total anomalies detected: 2

When you stop the monitor with:

CTRL + C

you get:

==========================================
       AIOps Monitoring Stopped
==========================================
Total anomalies detected: 2
Kafka consumer closed.
8. How the AIOps Logic Works
Step 1 — Receive Kafka message
for message in consumer:

The consumer continuously receives messages.

Step 2 — Convert JSON
data = message.value

The JSON is already converted into a Python dictionary by:

value_deserializer=lambda value: json.loads(
    value.decode("utf-8")
)
Step 3 — Read CPU
cpu = data["cpu_usage"]
Step 4 — Check for anomaly
if cpu > CPU_THRESHOLD:

where:

CPU_THRESHOLD = 80

Therefore:

CPU 50% → Normal
CPU 70% → Normal
CPU 80% → Normal
CPU 81% → Anomaly
CPU 90% → Anomaly

Remember that the question says greater than 80%, so we use:

>

not:

>=
9. Maintaining the Anomaly Count

Initially:

anomaly_count = 0

When an anomaly occurs:

anomaly_count += 1

So:

First anomaly  → 1
Second anomaly → 2
Third anomaly  → 3

This directly satisfies the requirement:

Maintain a count of detected anomalies.

10. Complete Execution Order

For the practical, use this order.

Terminal 1

Make sure your Kafka broker is running on:

localhost:9092
Terminal 2 — Create Topic
cd aiops-kafka
python topic.py
Terminal 3 — Start AIOps Monitor
cd aiops-kafka
python aiops_monitor.py

Keep it running.

Terminal 4 — Start Producer
cd aiops-kafka
python producer.py

The monitoring system will now receive the messages and detect anomalies.

11. Complete Architecture
                    Kafka Producer
                         │
                         │ JSON metrics
                         ▼
                ┌──────────────────┐
                │  server_metrics   │
                │      Topic        │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ aiops_monitor.py │
                │  Python Consumer  │
                └────────┬─────────┘
                         │
                         ▼
                    Check CPU
                         │
                  ┌──────┴──────┐
                  │             │
               CPU > 80      CPU <= 80
                  │             │
                  ▼             ▼
                ALERT         Normal
                  │
                  ▼
          anomaly_count += 1
                  │
                  ▼
          Total Anomalies
12. Important Viva/MCQ Points
What is the Kafka topic?
server_metrics
What is the Kafka broker?
localhost:9092
What is the CPU threshold?
80%
When is an anomaly detected?
CPU > 80%
What happens when an anomaly is detected?
anomaly_count += 1

and:

ALERT: High CPU detected

is printed.

What happens when CPU is normal?
Normal

is printed.

What does the final count represent?

The total number of Kafka messages whose CPU usage exceeded 80% during that monitor process's run.

13. Final Exam Code

If you need to write the answer quickly in the practical exam, this is the core version:

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "server_metrics",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="aiops-monitor",
    value_deserializer=lambda value: json.loads(
        value.decode("utf-8")
    )
)

anomaly_count = 0

try:

    for message in consumer:

        data = message.value

        server = data["server_id"]
        cpu = data["cpu_usage"]

        print(
            f"Message received: {server} | CPU: {cpu}%"
        )

        if cpu > 80:

            anomaly_count += 1

            print("ALERT: High CPU detected")

        else:

            print("Normal")

except KeyboardInterrupt:

    print()
    print(
        f"Total anomalies detected: {anomaly_count}"
    )

finally:

    consumer.close()

Run:

python aiops_monitor.py
Q5 expected result

For:

server01 → 85%
server02 → 45%
server03 → 91%

the monitor produces:

Message received: server01 | CPU: 85%
ALERT: High CPU detected

Message received: server02 | CPU: 45%
Normal

Message received: server03 | CPU: 91%
ALERT: High CPU detected

Total anomalies detected: 2

Q5 is complete when the Python Kafka consumer continuously monitors server_metrics, detects CPU values above 80%, prints alerts, and maintains the total anomaly count.
