1. Install Kafka Python library

Run:

python -m pip install kafka-python

Check:

python -c "import kafka; print(kafka.__version__)"
2. Start Kafka

If you're using your existing Windows Kafka setup:

Terminal 1 — ZooKeeper
cd C:\kafka
bin\windows\zookeeper-server-start.bat config\zookeeper.properties

Keep this terminal open.

Terminal 2 — Kafka Broker
cd C:\kafka
bin\windows\kafka-server-start.bat config\server.properties

Keep this terminal open.

Kafka should now be available at:

localhost:9092
3. topic.py

Create:

topic.py

Use:

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

    admin.create_topics(
        new_topics=[topic]
    )

    print("Topic created successfully!")

except TopicAlreadyExistsError:

    print("Topic already exists!")


admin.close()

The TopicAlreadyExistsError handling is useful because if you run the file a second time, your program won't crash just because the topic already exists.

4. Producer.py

Create:

Producer.py

Use your requested producer:

from kafka import KafkaProducer
import json
import time


# Create Kafka producer
producer = KafkaProducer(

    bootstrap_servers="localhost:9092",

    value_serializer=lambda x:
        json.dumps(x).encode("utf-8")
)


# Send 10 messages
for i in range(10):

    message = {

        "server_id": f"server{i+1}",

        "cpu_usage": 50 + i * 4,

        "memory_usage": 60 + i
    }


    producer.send(
        "server_metrics",
        value=message
    )


    print("Sent:", message)

    time.sleep(1)


# Make sure all messages are sent
producer.flush()

producer.close()

print("\n10 messages sent successfully!")

This produces:

server1  CPU 50
server2  CPU 54
server3  CPU 58
server4  CPU 62
server5  CPU 66
server6  CPU 70
server7  CPU 74
server8  CPU 78
server9  CPU 82
server10 CPU 86

So 10 messages are sent.

5. consumer.py

Create:

consumer.py

Use:

from kafka import KafkaConsumer
import json


# Create Kafka consumer
consumer = KafkaConsumer(

    "server_metrics",

    bootstrap_servers="localhost:9092",

    auto_offset_reset="earliest",

    enable_auto_commit=True,

    group_id="aiops-monitor",

    value_deserializer=lambda value:
        json.loads(value.decode("utf-8"))
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

        print(
            "ALERT: High CPU detected on",
            server
        )

This consumer is also useful for Question 3, because it already checks:

if cpu > 80:
6. Execute in the Correct Order

You need three additional terminals after Kafka is running.

Your setup will look like:

Terminal 1
    ↓
ZooKeeper

Terminal 2
    ↓
Kafka Broker

Terminal 3
    ↓
topic.py

Terminal 4
    ↓
consumer.py

Terminal 5
    ↓
Producer.py
Terminal 3 — Create Topic

Go to your Python project folder:

cd path\to\aiops_kafka

Run:

python topic.py

Expected:

Topic created successfully!

If you already created it:

Topic already exists!

Both are fine.

7. Verify Topic

Before running the producer, you can verify the topic.

cd C:\kafka
bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092

You should see:

server_metrics

You can also check its configuration:

bin\windows\kafka-topics.bat --describe --topic server_metrics --bootstrap-server localhost:9092
8. Terminal 4 — Start Consumer

Run:

python consumer.py

You should see:

Waiting for messages...

The consumer will wait for Kafka messages.

Do not close this terminal.

9. Terminal 5 — Run Producer

Run:

python Producer.py

Expected:

Sent: {'server_id': 'server1', 'cpu_usage': 50, 'memory_usage': 60}

Sent: {'server_id': 'server2', 'cpu_usage': 54, 'memory_usage': 61}

Sent: {'server_id': 'server3', 'cpu_usage': 58, 'memory_usage': 62}

...

Until:

Sent: {'server_id': 'server10', 'cpu_usage': 86, 'memory_usage': 69}

10 messages sent successfully!
10. Consumer Output

At the same time, the consumer will receive the messages.

For example:

Received:
Server: server1
CPU: 50 %
Memory: 60 %

For server9:

Received:
Server: server9
CPU: 82 %
Memory: 68 %

ALERT: High CPU detected on server9

For server10:

Received:
Server: server10
CPU: 86 %
Memory: 69 %

ALERT: High CPU detected on server10

Because:

82 > 80
86 > 80
11. Verify Published Messages Directly

You can also verify the messages using Kafka's console consumer.

Open another terminal:

cd C:\kafka

Run:

bin\windows\kafka-console-consumer.bat --topic server_metrics --from-beginning --bootstrap-server localhost:9092

You should see:

{"server_id":"server1","cpu_usage":50,"memory_usage":60}
{"server_id":"server2","cpu_usage":54,"memory_usage":61}
{"server_id":"server3","cpu_usage":58,"memory_usage":62}
{"server_id":"server4","cpu_usage":62,"memory_usage":63}
{"server_id":"server5","cpu_usage":66,"memory_usage":64}
{"server_id":"server6","cpu_usage":70,"memory_usage":65}
{"server_id":"server7","cpu_usage":74,"memory_usage":66}
{"server_id":"server8","cpu_usage":78,"memory_usage":67}
{"server_id":"server9","cpu_usage":82,"memory_usage":68}
{"server_id":"server10","cpu_usage":86,"memory_usage":69}

This directly proves that the producer published the messages to:

server_metrics
12. Complete Execution Commands
Install library
python -m pip install kafka-python
Start ZooKeeper
cd C:\kafka
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
Start Kafka
cd C:\kafka
bin\windows\kafka-server-start.bat config\server.properties
Create topic
python topic.py
Verify topic
bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
Start consumer
python consumer.py
Start producer
python Producer.py
Verify messages
bin\windows\kafka-console-consumer.bat --topic server_metrics --from-beginning --bootstrap-server localhost:9092
13. Final Flow for Question 2
                  Kafka Cluster
                       │
                       ↓
              localhost:9092
                       │
                       ↓
              ┌────────────────┐
              │ server_metrics │
              │     Topic      │
              └───────┬────────┘
                      ↑
                      │
                Producer.py
                      │
              10 JSON messages
                      │
                      ↓
                Consumer.py
                      │
                      ↓
              Display metrics
Files you need
topic.py
Producer.py
consumer.py
Most important commands
python topic.py
python consumer.py
python Producer.py

For the actual Question 2 requirement, topic.py + Producer.py + Kafka console consumer verification are the essential parts. Your consumer.py is useful for the next question and also demonstrates that the published metrics can be consumed.
