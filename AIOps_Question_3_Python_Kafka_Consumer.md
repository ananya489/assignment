# Question 3 --- Python Kafka Consumer

## Objective

Write a Python Kafka consumer that consumes messages from:

``` text
server_metrics
```

The consumer must:

1.  Connect to the Kafka broker.
2.  Subscribe to the `server_metrics` topic.
3.  Continuously receive messages.
4.  Display the received server metrics.
5.  Detect whether CPU usage is greater than **80%**.
6.  Print:

``` text
ALERT: High CPU detected on server01
```

when the CPU is greater than 80%.

------------------------------------------------------------------------

# 1. Prerequisites

You need:

-   Kafka running
-   `server_metrics` topic created
-   Python 3.x
-   `kafka-python`

Check Python:

``` bash
python --version
```

Install the Python Kafka library:

``` bash
python -m pip install kafka-python
```

On Windows, if required:

``` bash
py -m pip install kafka-python
```

------------------------------------------------------------------------

# 2. Kafka Must Be Running

The Python consumer connects to:

``` text
localhost:9092
```

So Kafka must already be running.

If using ZooKeeper-based Kafka:

### Terminal 1 --- Start ZooKeeper

``` bat
cd C:\kafka
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
```

Keep this terminal running.

### Terminal 2 --- Start Kafka

``` bat
cd C:\kafka
bin\windows\kafka-server-start.bat config\server.properties
```

Keep this terminal running.

------------------------------------------------------------------------

# 3. Verify the Topic

Open another terminal:

``` bat
cd C:\kafka
```

Check that the topic exists:

``` bat
bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
```

You should see:

``` text
server_metrics
```

If it does not exist, create it:

``` bat
bin\windows\kafka-topics.bat --create --topic server_metrics --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

------------------------------------------------------------------------

# 4. Make Sure There Are Messages

Question 2 sends messages to this topic.

For example:

``` json
{
    "server_id": "server01",
    "cpu_usage": 85,
    "memory_usage": 62
}
```

You can also send the 10 messages from Question 2 before starting the
consumer.

Run the Question 2 producer:

``` bash
python kafka_producer.py
```

------------------------------------------------------------------------

# 5. Create the Python Consumer

Create a file:

``` text
kafka_consumer.py
```

Put this complete code inside it:

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

    # Start from the earliest available message
    auto_offset_reset="earliest",

    # Commit offsets automatically
    enable_auto_commit=True,

    # Consumer group
    group_id="server-monitor-group",

    # Convert JSON bytes back into Python dictionary
    value_deserializer=lambda value:
        json.loads(value.decode("utf-8"))
)


# ============================================================
# START CONSUMING
# ============================================================

print("\n========================================")
print("       Kafka Server Metrics Consumer")
print("========================================")

print(f"Broker : {BOOTSTRAP_SERVER}")
print(f"Topic  : {TOPIC}")
print(f"CPU Threshold : {CPU_THRESHOLD}%")

print("\nWaiting for messages...")
print("Press CTRL+C to stop.\n")


try:

    for message in consumer:

        data = message.value

        server_id = data.get("server_id")
        cpu = data.get("cpu_usage")
        memory = data.get("memory_usage")

        print("----------------------------------------")

        print("Received:")

        print(f"Server: {server_id}")
        print(f"CPU: {cpu}%")
        print(f"Memory: {memory}%")

        # ====================================================
        # CPU ANOMALY DETECTION
        # ====================================================

        if cpu > CPU_THRESHOLD:

            print(
                f"\nALERT: High CPU detected on "
                f"{server_id}"
            )

        else:

            print("\nStatus: Normal")


except KeyboardInterrupt:

    print("\n")
    print("Consumer stopped by user.")


finally:

    consumer.close()

    print("Kafka consumer closed.")
```

------------------------------------------------------------------------

# 6. Run the Consumer

Make sure Kafka is running.

Run:

``` bash
python kafka_consumer.py
```

On Windows:

``` bash
py kafka_consumer.py
```

The consumer will continuously listen to:

``` text
server_metrics
```

------------------------------------------------------------------------

# 7. Expected Output --- High CPU

Suppose Kafka receives:

``` json
{
    "server_id": "server01",
    "cpu_usage": 85,
    "memory_usage": 62
}
```

The consumer prints:

``` text
========================================
       Kafka Server Metrics Consumer
========================================

Broker : localhost:9092
Topic  : server_metrics
CPU Threshold : 80%

Waiting for messages...

----------------------------------------
Received:

Server: server01
CPU: 85%
Memory: 62%

ALERT: High CPU detected on server01
```

Because:

``` text
85 > 80
```

the alert is generated.

------------------------------------------------------------------------

# 8. Expected Output --- Normal CPU

For:

``` json
{
    "server_id": "server02",
    "cpu_usage": 45,
    "memory_usage": 55
}
```

the output is:

``` text
----------------------------------------
Received:

Server: server02
CPU: 45%
Memory: 55%

Status: Normal
```

Because:

``` text
45 < 80
```

there is no alert.

------------------------------------------------------------------------

# 9. Test the Consumer

A good way to demonstrate the practical is to run the consumer and
producer in separate terminals.

## Terminal 1 --- Kafka

Keep Kafka running.

``` bat
bin\windows\kafka-server-start.bat config\server.properties
```

## Terminal 2 --- Consumer

Run:

``` bash
python kafka_consumer.py
```

It will show:

``` text
Waiting for messages...
```

## Terminal 3 --- Producer

Run:

``` bash
python kafka_producer.py
```

The producer sends the server metrics.

The consumer immediately receives them.

For example:

``` text
Message 1:
server01 | CPU 82%
→ ALERT

Message 2:
server02 | CPU 45%
→ Normal

Message 3:
server03 | CPU 91%
→ ALERT
```

This demonstrates real-time monitoring.

------------------------------------------------------------------------

# 10. How the Consumer Works

The complete flow is:

``` text
Kafka Producer
      |
      | JSON message
      ↓
server_metrics Topic
      |
      ↓
Kafka Consumer
      |
      ↓
Read JSON
      |
      ↓
Extract server_id
Extract cpu_usage
Extract memory_usage
      |
      ↓
CPU > 80?
    /     \
  YES      NO
   |        |
 ALERT     Normal
```

------------------------------------------------------------------------

# 11. Important Code Sections

## Connect to Kafka

``` python
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092"
)
```

This connects the consumer to the Kafka broker.

------------------------------------------------------------------------

## Subscribe to Topic

The topic is passed to `KafkaConsumer`:

``` python
KafkaConsumer(
    "server_metrics",
    ...
)
```

Therefore, the consumer listens to:

``` text
server_metrics
```

------------------------------------------------------------------------

## Deserialize JSON

Kafka sends data as bytes.

This converts it back into a Python dictionary:

``` python
value_deserializer=lambda value:
    json.loads(value.decode("utf-8"))
```

------------------------------------------------------------------------

## Continuously Receive Messages

``` python
for message in consumer:
```

This keeps listening for new Kafka messages.

------------------------------------------------------------------------

## Read Server Metrics

``` python
data = message.value

server_id = data.get("server_id")
cpu = data.get("cpu_usage")
memory = data.get("memory_usage")
```

------------------------------------------------------------------------

## Detect High CPU

``` python
if cpu > 80:
    print(
        f"ALERT: High CPU detected on {server_id}"
    )
```

This is the main anomaly detection logic.

------------------------------------------------------------------------

# 12. Important Kafka Consumer Settings

## `auto_offset_reset`

``` python
auto_offset_reset="earliest"
```

This tells Kafka to start from the earliest available messages when the
consumer group has no previous offset.

This is useful during a practical because you can see the messages
already produced by Question 2.

------------------------------------------------------------------------

## `group_id`

``` python
group_id="server-monitor-group"
```

This identifies the consumer group.

Kafka uses consumer groups to manage message consumption and offsets.

------------------------------------------------------------------------

## `enable_auto_commit`

``` python
enable_auto_commit=True
```

Kafka automatically commits the consumer's offsets.

------------------------------------------------------------------------

# 13. Testing With Kafka Console Producer

You can test without the Python producer.

Open another terminal:

``` bat
cd C:\kafka
```

Run:

``` bat
bin\windows\kafka-console-producer.bat --topic server_metrics --bootstrap-server localhost:9092
```

Then enter:

``` json
{"server_id":"server01","cpu_usage":85,"memory_usage":62}
```

Press Enter.

The Python consumer should immediately print:

``` text
Received:

Server: server01
CPU: 85%
Memory: 62%

ALERT: High CPU detected on server01
```

Try a normal server:

``` json
{"server_id":"server02","cpu_usage":45,"memory_usage":55}
```

The consumer should print:

``` text
Received:

Server: server02
CPU: 45%
Memory: 55%

Status: Normal
```

Press:

``` text
CTRL + C
```

to stop the console producer.

------------------------------------------------------------------------

# 14. Complete Practical Command Sequence

## Terminal 1 --- Start ZooKeeper

``` bat
cd C:\kafka
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
```

## Terminal 2 --- Start Kafka

``` bat
cd C:\kafka
bin\windows\kafka-server-start.bat config\server.properties
```

## Terminal 3 --- Check Topic

``` bat
cd C:\kafka
bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
```

Expected:

``` text
server_metrics
```

## Terminal 4 --- Start Consumer

``` bash
python kafka_consumer.py
```

## Terminal 5 --- Start Producer

``` bash
python kafka_producer.py
```

Now the consumer receives the producer's messages.

------------------------------------------------------------------------

# 15. WSL/Linux Commands

If Kafka is running in WSL/Linux, use:

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

### Start consumer

``` bash
python kafka_consumer.py
```

The Python consumer code itself does not need to change if Kafka is
accessible at:

``` text
localhost:9092
```

------------------------------------------------------------------------

# 16. Troubleshooting

## `NoBrokersAvailable`

Example:

``` text
kafka.errors.NoBrokersAvailable
```

Kafka is probably not running or is not accessible at:

``` text
localhost:9092
```

Start the Kafka broker first.

------------------------------------------------------------------------

## `No module named kafka`

Run:

``` bash
python -m pip install kafka-python
```

------------------------------------------------------------------------

## Consumer shows no messages

Check the topic:

``` bat
bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
```

Then produce a test message:

``` bat
bin\windows\kafka-console-producer.bat --topic server_metrics --bootstrap-server localhost:9092
```

Enter:

``` json
{"server_id":"server01","cpu_usage":85,"memory_usage":62}
```

------------------------------------------------------------------------

## Consumer reads old messages

This code uses:

``` python
auto_offset_reset="earliest"
```

so a new consumer group can read existing messages.

If you want to start from only new messages, change it to:

``` python
auto_offset_reset="latest"
```

For this practical, `earliest` is useful for demonstrating the messages
from Question 2.

------------------------------------------------------------------------

# 17. Exam Explanation

> A Python Kafka consumer connects to the Kafka broker at
> `localhost:9092` and consumes messages from the `server_metrics`
> topic. Each JSON message is deserialized into a Python dictionary. The
> consumer extracts the server ID, CPU usage, and memory usage. If CPU
> usage is greater than 80%, it generates a high-CPU alert. Otherwise,
> it reports the server as normal. The consumer continuously listens for
> new messages, providing basic real-time monitoring.

------------------------------------------------------------------------

# 18. Quick Revision

### Topic

``` text
server_metrics
```

### Broker

``` text
localhost:9092
```

### Library

``` bash
python -m pip install kafka-python
```

### Consumer

``` python
KafkaConsumer(...)
```

### Receive

``` python
for message in consumer:
```

### Extract CPU

``` python
cpu = data.get("cpu_usage")
```

### Detect anomaly

``` python
if cpu > 80:
    print(
        f"ALERT: High CPU detected on {server_id}"
    )
```

### Run

``` bash
python kafka_consumer.py
```

### Test message

``` json
{
    "server_id": "server01",
    "cpu_usage": 85,
    "memory_usage": 62
}
```

### Expected alert

``` text
ALERT: High CPU detected on server01
```
