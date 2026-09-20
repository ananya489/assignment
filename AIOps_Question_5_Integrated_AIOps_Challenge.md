# Question 5 --- Integrated AIOps Challenge

## Objective

Modify the Kafka consumer from Question 3 so that it behaves like a
simple AIOps monitoring system.

The consumer must:

1.  Receive server metrics from Kafka.
2.  Check CPU usage.
3.  Detect an anomaly when CPU \> 80%.
4.  Print an alert.
5.  Maintain a count of detected anomalies.

Expected behavior:

``` text
Message received: server01 | CPU: 85%
ALERT: High CPU detected

Message received: server02 | CPU: 45%
Normal

Message received: server03 | CPU: 91%
ALERT: High CPU detected

Total anomalies detected: 2
```

------------------------------------------------------------------------

# 1. Prerequisites

You need:

-   Python 3.x
-   Apache Kafka
-   `server_metrics` Kafka topic
-   `kafka-python`

Check Python:

``` bash
python --version
```

Install the Python Kafka library:

``` bash
python -m pip install kafka-python
```

On Windows:

``` bash
py -m pip install kafka-python
```

------------------------------------------------------------------------

# 2. Start Kafka

The Python program expects the Kafka broker at:

``` text
localhost:9092
```

If using ZooKeeper-based Kafka:

## Terminal 1 --- Start ZooKeeper

``` bat
cd C:\kafka
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
```

Keep this terminal running.

## Terminal 2 --- Start Kafka

``` bat
cd C:\kafka
bin\windows\kafka-server-start.bat config\server.properties
```

Keep this terminal running.

------------------------------------------------------------------------

# 3. Verify the Kafka Topic

Open another terminal:

``` bat
cd C:\kafka
```

Run:

``` bat
bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
```

You should see:

``` text
server_metrics
```

If the topic does not exist:

``` bat
bin\windows\kafka-topics.bat --create --topic server_metrics --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

------------------------------------------------------------------------

# 4. Create the Integrated AIOps Consumer

Create:

``` text
aiops_monitor.py
```

This is the modified version of the Question 3 consumer.

Use this complete code:

``` python
import json
from kafka import KafkaConsumer


# ============================================================
# CONFIGURATION
# ============================================================

BOOTSTRAP_SERVER = "localhost:9092"

TOPIC = "server_metrics"

CPU_THRESHOLD = 80


# ============================================================
# CREATE KAFKA CONSUMER
# ============================================================

consumer = KafkaConsumer(

    TOPIC,

    bootstrap_servers=BOOTSTRAP_SERVER,

    # Read old messages if this consumer group
    # has no previous offset
    auto_offset_reset="earliest",

    enable_auto_commit=True,

    group_id="aiops-monitoring-group",

    # Convert Kafka JSON bytes into Python dictionary
    value_deserializer=lambda value:
        json.loads(value.decode("utf-8"))
)


# ============================================================
# AIOps ANOMALY COUNTER
# ============================================================

anomaly_count = 0


# ============================================================
# START MONITORING
# ============================================================

print("\n==========================================")
print("        AIOps Kafka Monitoring System")
print("==========================================")

print(f"Broker : {BOOTSTRAP_SERVER}")
print(f"Topic  : {TOPIC}")
print(f"CPU Threshold : {CPU_THRESHOLD}%")

print("\nMonitoring started...")
print("Press CTRL+C to stop.\n")


try:

    # Continuously receive Kafka messages
    for message in consumer:

        # Get JSON message
        data = message.value

        # Extract server information
        server_id = data.get("server_id")

        cpu = data.get("cpu_usage")

        memory = data.get("memory_usage")

        # ----------------------------------------------------
        # Display received message
        # ----------------------------------------------------

        print("------------------------------------------")

        print(
            f"Message received: "
            f"{server_id} | CPU: {cpu}%"
        )

        print(
            f"Memory: {memory}%"
        )

        # ----------------------------------------------------
        # AIOps anomaly detection
        # ----------------------------------------------------

        if cpu > CPU_THRESHOLD:

            # Increase anomaly counter
            anomaly_count += 1

            print(
                "ALERT: High CPU detected"
            )

            print(
                f"Server: {server_id}"
            )

            print(
                f"Total anomalies detected: "
                f"{anomaly_count}"
            )

        else:

            print("Normal")


except KeyboardInterrupt:

    print("\n")
    print("==========================================")
    print("        AIOps Monitoring Stopped")
    print("==========================================")

    print(
        f"Total anomalies detected: "
        f"{anomaly_count}"
    )


finally:

    consumer.close()

    print("\nKafka consumer closed.")
```

------------------------------------------------------------------------

# 5. Run the AIOps Monitoring System

Make sure Kafka is running.

Then execute:

``` bash
python aiops_monitor.py
```

On Windows:

``` bash
py aiops_monitor.py
```

You should see:

``` text
==========================================
        AIOps Kafka Monitoring System
==========================================

Broker : localhost:9092
Topic  : server_metrics
CPU Threshold : 80%

Monitoring started...
Press CTRL+C to stop.
```

The program now continuously monitors Kafka.

------------------------------------------------------------------------

# 6. Test Using the Question 2 Producer

You can reuse:

``` text
kafka_producer.py
```

from Question 2.

Open another terminal and run:

``` bash
python kafka_producer.py
```

The producer sends:

``` text
server01 → CPU 82
server02 → CPU 45
server03 → CPU 91
server04 → CPU 60
...
```

The AIOps consumer processes these messages.

For example:

``` text
Message received: server01 | CPU: 82%
Memory: 65%

ALERT: High CPU detected
Server: server01
Total anomalies detected: 1
```

Then:

``` text
Message received: server02 | CPU: 45%
Memory: 55%

Normal
```

Then:

``` text
Message received: server03 | CPU: 91%
Memory: 70%

ALERT: High CPU detected
Server: server03
Total anomalies detected: 2
```

------------------------------------------------------------------------

# 7. Test With Kafka Console Producer

You can also test manually.

Open another terminal:

``` bat
cd C:\kafka
```

Run:

``` bat
bin\windows\kafka-console-producer.bat --topic server_metrics --bootstrap-server localhost:9092
```

Enter:

``` json
{"server_id":"server01","cpu_usage":85,"memory_usage":62}
```

Expected:

``` text
Message received: server01 | CPU: 85%
Memory: 62%

ALERT: High CPU detected
Server: server01
Total anomalies detected: 1
```

Enter:

``` json
{"server_id":"server02","cpu_usage":45,"memory_usage":55}
```

Expected:

``` text
Message received: server02 | CPU: 45%
Memory: 55%

Normal
```

Enter:

``` json
{"server_id":"server03","cpu_usage":91,"memory_usage":70}
```

Expected:

``` text
Message received: server03 | CPU: 91%
Memory: 70%

ALERT: High CPU detected
Server: server03
Total anomalies detected: 2
```

------------------------------------------------------------------------

# 8. Stop the Monitoring System

The consumer continuously runs:

``` python
for message in consumer:
```

To stop it:

``` text
CTRL + C
```

The program prints the final anomaly count:

``` text
==========================================
        AIOps Monitoring Stopped
==========================================

Total anomalies detected: 2

Kafka consumer closed.
```

------------------------------------------------------------------------

# 9. How the Integrated AIOps System Works

The complete architecture is:

``` text
                    Kafka Producer
                         |
                         ↓
                 server_metrics
                    Kafka Topic
                         |
                         ↓
                 Python Consumer
                         |
                         ↓
                  Read JSON Data
                         |
                         ↓
                   Extract CPU
                         |
                         ↓
                    CPU > 80?
                    /         \
                  YES          NO
                   |            |
                   ↓            ↓
                ALERT         Normal
                   |
                   ↓
            anomaly_count++
                   |
                   ↓
            Final AIOps Report
```

------------------------------------------------------------------------

# 10. Core AIOps Logic

The most important part of the program is:

``` python
if cpu > CPU_THRESHOLD:

    anomaly_count += 1

    print("ALERT: High CPU detected")

else:

    print("Normal")
```

The threshold is:

``` python
CPU_THRESHOLD = 80
```

Therefore:

``` text
CPU = 85 → ANOMALY
CPU = 45 → NORMAL
CPU = 91 → ANOMALY
CPU = 80 → NORMAL
```

Notice that the question says:

``` text
CPU > 80
```

Therefore exactly `80%` is not an anomaly.

------------------------------------------------------------------------

# 11. How the Counter Works

Initially:

``` python
anomaly_count = 0
```

When an anomaly occurs:

``` python
anomaly_count += 1
```

Example:

``` text
First anomaly:
0 → 1

Second anomaly:
1 → 2

Third anomaly:
2 → 3
```

When the program stops:

``` python
print(
    f"Total anomalies detected: "
    f"{anomaly_count}"
)
```

------------------------------------------------------------------------

# 12. Important Kafka Consumer Code

## Connect to Kafka

``` python
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092"
)
```

## Consume continuously

``` python
for message in consumer:
```

## Decode JSON

``` python
value_deserializer=lambda value:
    json.loads(value.decode("utf-8"))
```

## Extract CPU

``` python
cpu = data.get("cpu_usage")
```

## Detect anomaly

``` python
if cpu > 80:
```

## Count anomaly

``` python
anomaly_count += 1
```

## Generate alert

``` python
print("ALERT: High CPU detected")
```

------------------------------------------------------------------------

# 13. Complete Practical Command Sequence

## Terminal 1 --- ZooKeeper

``` bat
cd C:\kafka
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
```

## Terminal 2 --- Kafka Broker

``` bat
cd C:\kafka
bin\windows\kafka-server-start.bat config\server.properties
```

## Terminal 3 --- Verify Topic

``` bat
cd C:\kafka
bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
```

Expected:

``` text
server_metrics
```

## Terminal 4 --- Start AIOps Monitor

``` bash
python aiops_monitor.py
```

## Terminal 5 --- Send Metrics

Use the Question 2 producer:

``` bash
python kafka_producer.py
```

Or use the Kafka console producer:

``` bat
bin\windows\kafka-console-producer.bat --topic server_metrics --bootstrap-server localhost:9092
```

------------------------------------------------------------------------

# 14. WSL/Linux Commands

If Kafka is running in WSL/Linux:

### Start ZooKeeper

``` bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

### Start Kafka

``` bash
bin/kafka-server-start.sh config/server.properties
```

### Check topic

``` bash
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

### Start AIOps monitor

``` bash
python aiops_monitor.py
```

### Run producer

``` bash
python kafka_producer.py
```

------------------------------------------------------------------------

# 15. Troubleshooting

## Error: `NoBrokersAvailable`

Make sure Kafka is running:

``` text
localhost:9092
```

Start the broker before starting:

``` bash
python aiops_monitor.py
```

------------------------------------------------------------------------

## Error: `No module named kafka`

Install:

``` bash
python -m pip install kafka-python
```

------------------------------------------------------------------------

## No messages appear

Check the topic:

``` bat
bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
```

Then send a test message:

``` bat
bin\windows\kafka-console-producer.bat --topic server_metrics --bootstrap-server localhost:9092
```

Use:

``` json
{"server_id":"server01","cpu_usage":85,"memory_usage":62}
```

------------------------------------------------------------------------

## Old messages appear

The consumer uses:

``` python
auto_offset_reset="earliest"
```

This is useful for the practical because the consumer can read messages
already published to the topic.

If you want only new messages for a fresh consumer group, you can use:

``` python
auto_offset_reset="latest"
```

------------------------------------------------------------------------

# 16. Exam Explanation

> This integrated AIOps monitoring system uses a Python Kafka consumer
> to continuously receive server metrics from the `server_metrics`
> topic. It extracts the CPU usage from each message and compares it
> with an 80% threshold. If CPU usage is greater than 80%, the system
> generates a high-CPU alert and increments the anomaly counter.
> Otherwise, it reports the server as normal. When monitoring is
> stopped, the system displays the total number of detected anomalies.

------------------------------------------------------------------------

# 17. Quick Revision

### Kafka topic

``` text
server_metrics
```

### Broker

``` text
localhost:9092
```

### CPU threshold

``` python
CPU_THRESHOLD = 80
```

### Counter

``` python
anomaly_count = 0
```

### Receive message

``` python
for message in consumer:
```

### Get CPU

``` python
cpu = data.get("cpu_usage")
```

### Detect anomaly

``` python
if cpu > 80:
```

### Increment counter

``` python
anomaly_count += 1
```

### Alert

``` python
print("ALERT: High CPU detected")
```

### Normal

``` python
print("Normal")
```

### Run

``` bash
python aiops_monitor.py
```

### Stop

``` text
CTRL + C
```

### Final output

``` text
Total anomalies detected: 2
```

------------------------------------------------------------------------

# 18. Final Workflow

``` text
┌───────────────────────┐
│   Kafka Producer      │
│                       │
│ server01 CPU = 85     │
│ server02 CPU = 45     │
│ server03 CPU = 91     │
└───────────┬───────────┘
            │
            ↓
┌───────────────────────┐
│  server_metrics       │
│  Kafka Topic          │
└───────────┬───────────┘
            │
            ↓
┌───────────────────────┐
│  Python AIOps         │
│  Consumer             │
└───────────┬───────────┘
            │
            ↓
       CPU > 80?
        /      \
      YES       NO
       ↓         ↓
    ALERT      Normal
       ↓
 anomaly_count++
       ↓
Total anomalies
detected
```

This completes the integrated Kafka + Python + metrics + anomaly
detection + AIOps monitoring practical.
