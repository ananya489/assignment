# Question 2 --- Kafka Topic and Producer

## Objective

Set up a Kafka environment and create a topic called:

``` text
server_metrics
```

The practical must:

1.  Start the Kafka server/cluster.
2.  Create the `server_metrics` topic.
3.  Configure a Kafka producer.
4.  Send at least 10 server metric messages.
5.  Verify that the messages were successfully published.

Each message contains:

``` json
{
    "server_id": "server01",
    "cpu_usage": 82,
    "memory_usage": 65
}
```

------------------------------------------------------------------------

# 1. Prerequisites

You need:

-   Java
-   Apache Kafka
-   Python
-   `kafka-python`

Check Java:

``` bash
java -version
```

Check Python:

``` bash
python --version
```

Install the Python Kafka library:

``` bash
python -m pip install kafka-python
```

On Windows, if `python` does not work:

``` bash
py -m pip install kafka-python
```

------------------------------------------------------------------------

# 2. Kafka Folder

Assume Kafka is extracted somewhere such as:

``` text
C:\kafka
```

Open a terminal in the Kafka directory:

``` bat
cd C:\kafka
```

Your Kafka directory should contain folders similar to:

``` text
bin
config
libs
```

On Windows, Kafka command files are normally inside:

``` text
bin\windows
```

------------------------------------------------------------------------

# 3. Start Kafka

There are two common Kafka setups.

## Option A --- ZooKeeper-based Kafka

If your Kafka installation contains:

``` text
config\zookeeper.properties
config\server.properties
```

start ZooKeeper first.

### Terminal 1 --- ZooKeeper

``` bat
cd C:\kafka
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
```

Keep this terminal running.

------------------------------------------------------------------------

### Terminal 2 --- Kafka Broker

Open another terminal:

``` bat
cd C:\kafka
bin\windows\kafka-server-start.bat config\server.properties
```

Keep this terminal running.

The Kafka broker should now be available at:

``` text
localhost:9092
```

------------------------------------------------------------------------

# 4. Create the Kafka Topic

Open a third terminal.

Run:

``` bat
cd C:\kafka
```

Create the required topic:

``` bat
bin\windows\kafka-topics.bat --create --topic server_metrics --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

Expected output will be similar to:

``` text
Created topic server_metrics.
```

The important part is:

``` text
server_metrics
```

------------------------------------------------------------------------

# 5. Verify the Topic

Run:

``` bat
bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
```

Expected:

``` text
server_metrics
```

You can also inspect the topic:

``` bat
bin\windows\kafka-topics.bat --describe --topic server_metrics --bootstrap-server localhost:9092
```

You should see information about:

-   Topic
-   Partition
-   Leader
-   Replicas
-   ISR

For a single-broker practical setup, one partition and replication
factor 1 are sufficient.

------------------------------------------------------------------------

# 6. Create the Python Producer

Create a file:

``` text
kafka_producer.py
```

Use this complete code:

``` python
import json
from kafka import KafkaProducer


# ============================================================
# CONFIGURATION
# ============================================================

BOOTSTRAP_SERVER = "localhost:9092"
TOPIC = "server_metrics"


# ============================================================
# CREATE KAFKA PRODUCER
# ============================================================

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVER,

    value_serializer=lambda value:
        json.dumps(value).encode("utf-8")
)


# ============================================================
# SERVER METRIC MESSAGES
# ============================================================

messages = [
    {
        "server_id": "server01",
        "cpu_usage": 82,
        "memory_usage": 65
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
    },
    {
        "server_id": "server04",
        "cpu_usage": 60,
        "memory_usage": 50
    },
    {
        "server_id": "server05",
        "cpu_usage": 75,
        "memory_usage": 68
    },
    {
        "server_id": "server06",
        "cpu_usage": 88,
        "memory_usage": 72
    },
    {
        "server_id": "server07",
        "cpu_usage": 40,
        "memory_usage": 45
    },
    {
        "server_id": "server08",
        "cpu_usage": 95,
        "memory_usage": 80
    },
    {
        "server_id": "server09",
        "cpu_usage": 55,
        "memory_usage": 52
    },
    {
        "server_id": "server10",
        "cpu_usage": 85,
        "memory_usage": 63
    }
]


# ============================================================
# SEND MESSAGES
# ============================================================

print("\n========================================")
print("       Kafka Server Metrics Producer")
print("========================================")

print(f"Broker : {BOOTSTRAP_SERVER}")
print(f"Topic  : {TOPIC}")

print("\nSending messages...\n")


for message in messages:

    future = producer.send(
        TOPIC,
        value=message
    )

    # Wait for Kafka acknowledgement
    metadata = future.get(timeout=10)

    print(
        f"Sent: {message}"
    )

    print(
        f"Partition: {metadata.partition} "
        f"| Offset: {metadata.offset}"
    )

    print()


# Make sure all messages are sent
producer.flush()

# Close producer
producer.close()


print("========================================")
print("10 messages successfully published.")
print("========================================")
```

------------------------------------------------------------------------

# 7. Run the Producer

Make sure Kafka is still running.

From the directory containing `kafka_producer.py`, run:

``` bash
python kafka_producer.py
```

On Windows:

``` bash
py kafka_producer.py
```

Expected output:

``` text
========================================
       Kafka Server Metrics Producer
========================================

Broker : localhost:9092
Topic  : server_metrics

Sending messages...

Sent: {'server_id': 'server01', 'cpu_usage': 82, 'memory_usage': 65}
Partition: 0 | Offset: 0

Sent: {'server_id': 'server02', 'cpu_usage': 45, 'memory_usage': 55}
Partition: 0 | Offset: 1

Sent: {'server_id': 'server03', 'cpu_usage': 91, 'memory_usage': 70}
Partition: 0 | Offset: 2

...

Sent: {'server_id': 'server10', 'cpu_usage': 85, 'memory_usage': 63}
Partition: 0 | Offset: 9

========================================
10 messages successfully published.
========================================
```

The offsets confirm that Kafka acknowledged the messages.

------------------------------------------------------------------------

# 8. Verify Messages Were Published

This is an important part of the question.

Use Kafka's console consumer.

Open another terminal:

``` bat
cd C:\kafka
```

Run:

``` bat
bin\windows\kafka-console-consumer.bat --topic server_metrics --from-beginning --bootstrap-server localhost:9092
```

You should see the messages:

``` json
{"server_id": "server01", "cpu_usage": 82, "memory_usage": 65}
{"server_id": "server02", "cpu_usage": 45, "memory_usage": 55}
{"server_id": "server03", "cpu_usage": 91, "memory_usage": 70}
{"server_id": "server04", "cpu_usage": 60, "memory_usage": 50}
{"server_id": "server05", "cpu_usage": 75, "memory_usage": 68}
{"server_id": "server06", "cpu_usage": 88, "memory_usage": 72}
{"server_id": "server07", "cpu_usage": 40, "memory_usage": 45}
{"server_id": "server08", "cpu_usage": 95, "memory_usage": 80}
{"server_id": "server09", "cpu_usage": 55, "memory_usage": 52}
{"server_id": "server10", "cpu_usage": 85, "memory_usage": 63}
```

This proves that the producer successfully published the messages to:

``` text
server_metrics
```

Press:

``` text
CTRL + C
```

to stop the console consumer.

------------------------------------------------------------------------

# 9. Complete Practical Command Sequence

Use these commands in this order.

## Terminal 1 --- Start ZooKeeper

``` bat
cd C:\kafka
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
```

Keep it running.

------------------------------------------------------------------------

## Terminal 2 --- Start Kafka

``` bat
cd C:\kafka
bin\windows\kafka-server-start.bat config\server.properties
```

Keep it running.

------------------------------------------------------------------------

## Terminal 3 --- Create Topic

``` bat
cd C:\kafka
bin\windows\kafka-topics.bat --create --topic server_metrics --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

Verify:

``` bat
bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
```

Expected:

``` text
server_metrics
```

------------------------------------------------------------------------

## Terminal 4 --- Run Python Producer

Install the library once:

``` bash
python -m pip install kafka-python
```

Then:

``` bash
python kafka_producer.py
```

------------------------------------------------------------------------

## Terminal 5 --- Verify Messages

``` bat
cd C:\kafka
bin\windows\kafka-console-consumer.bat --topic server_metrics --from-beginning --bootstrap-server localhost:9092
```

You should see all 10 messages.

------------------------------------------------------------------------

# 10. If You Are Using Kafka in WSL/Linux

The Python producer code does not change.

The Kafka commands change from:

``` text
bin\windows\...
```

to:

``` text
bin/...
```

For example:

### Start ZooKeeper

``` bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

### Start Kafka

``` bash
bin/kafka-server-start.sh config/server.properties
```

### Create topic

``` bash
bin/kafka-topics.sh --create \
    --topic server_metrics \
    --bootstrap-server localhost:9092 \
    --partitions 1 \
    --replication-factor 1
```

### List topics

``` bash
bin/kafka-topics.sh --list \
    --bootstrap-server localhost:9092
```

### Verify messages

``` bash
bin/kafka-console-consumer.sh \
    --topic server_metrics \
    --from-beginning \
    --bootstrap-server localhost:9092
```

------------------------------------------------------------------------

# 11. If Your Kafka Version Uses KRaft

Newer Kafka installations can run without ZooKeeper using KRaft.

If your Kafka setup provides a KRaft configuration such as:

``` text
config/kraft/server.properties
```

the setup is different.

First generate a cluster ID:

``` bash
bin/kafka-storage.sh random-uuid
```

Format the storage:

``` bash
bin/kafka-storage.sh format -t <CLUSTER_ID> -c config/kraft/server.properties
```

Then start Kafka:

``` bash
bin/kafka-server-start.sh config/kraft/server.properties
```

On Windows, use the corresponding `.bat` files:

``` bat
bin\windows\kafka-storage.bat random-uuid
```

and:

``` bat
bin\windows\kafka-storage.bat format -t <CLUSTER_ID> -c config\kraft\server.properties
```

Then:

``` bat
bin\windows\kafka-server-start.bat config\kraft\server.properties
```

For the exam, use whichever Kafka setup your installed environment
already uses.

------------------------------------------------------------------------

# 12. Troubleshooting

## Error: Connection refused

Example:

``` text
NoBrokersAvailable
```

Check that Kafka is running:

``` text
localhost:9092
```

Start the broker before running the Python producer.

------------------------------------------------------------------------

## Error: No module named kafka

Run:

``` bash
python -m pip install kafka-python
```

Then verify:

``` bash
python -c "import kafka; print(kafka.__version__)"
```

------------------------------------------------------------------------

## Topic already exists

If you see:

``` text
Topic 'server_metrics' already exists
```

that is not a problem.

Verify it:

``` bat
bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
```

If it shows:

``` text
server_metrics
```

continue with the producer.

------------------------------------------------------------------------

# 13. What Each Part Demonstrates

``` text
Kafka Cluster
      ↓
Kafka Broker
      ↓
server_metrics Topic
      ↓
Python Producer
      ↓
10 JSON Messages
      ↓
Kafka Partition
      ↓
Console Consumer
      ↓
Verify Messages
```

The Python producer uses:

``` python
producer.send(
    TOPIC,
    value=message
)
```

The JSON serializer converts the Python dictionary into JSON bytes:

``` python
value_serializer=lambda value:
    json.dumps(value).encode("utf-8")
```

The producer waits for Kafka acknowledgement:

``` python
metadata = future.get(timeout=10)
```

This gives you the partition and offset, which helps demonstrate that
Kafka accepted the message.

------------------------------------------------------------------------

# 14. Exam Answer --- Short Explanation

> First, start the Kafka broker and create the `server_metrics` topic.
> Then configure a Python `KafkaProducer` using `localhost:9092`. The
> producer sends 10 JSON messages containing `server_id`, `cpu_usage`,
> and `memory_usage`. Finally, use the Kafka console consumer with
> `--from-beginning` to verify that all messages were successfully
> published to the topic.

------------------------------------------------------------------------

# 15. Quick Revision

### Topic

``` text
server_metrics
```

### Broker

``` text
localhost:9092
```

### Producer

``` python
KafkaProducer(...)
```

### Send

``` python
producer.send(
    "server_metrics",
    value=message
)
```

### Verify

``` bat
kafka-console-consumer.bat --topic server_metrics --from-beginning --bootstrap-server localhost:9092
```

### Required message

``` json
{
    "server_id": "server01",
    "cpu_usage": 82,
    "memory_usage": 65
}
```

### Required number of messages

``` text
10
```
