Question 2 — Kafka Topic and Producer (GitHub Codespaces)

This guide consolidates the Codespaces commands, Python code, verification steps, and Git commits for the Kafka practical.

Environment: GitHub Codespaces (Linux), Kafka downloaded and run directly (no Docker), Kafka KRaft mode (no separate ZooKeeper terminal).

Project folder: /workspaces/assignment

Kafka folder: /workspaces/assignment/kafka_2.13-4.3.1

Python files (topic.py, Producer.py, consumer.py) belong in the project folder, not inside the Kafka folder.

1. Install and verify the Python library

Run from the Codespaces terminal:

cd /workspaces/assignment
python -m pip install kafka-python
python -c "import kafka; print(kafka.__version__)"

If the version prints, kafka-python is importable.

Optional Git checkpoint

Only commit if you changed or added tracked project files as part of this step. Installing a package alone generally does not create a repository change.

git status

If you added/updated a dependency file such as requirements.txt:

git add requirements.txt
git commit -m "Add kafka-python dependency"
git push

2. Start Kafka (no Docker, no ZooKeeper)

Kafka was extracted into:

/workspaces/assignment/kafka_2.13-4.3.1

Start Kafka in Terminal 1:

cd /workspaces/assignment/kafka_2.13-4.3.1
bin/kafka-server-start.sh config/server.properties

Keep this terminal open while running the Python scripts. The broker is expected at localhost:9092.

If Kafka storage has not been formatted yet, format it once before the first startup (do not repeat on an existing populated Kafka data directory):

cd /workspaces/assignment/kafka_2.13-4.3.1
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format --standalone -t "$KAFKA_CLUSTER_ID" -c config/server.properties

Use a Java version supported by your Kafka release (Kafka 4.x requires Java 17+).

3. Create topic.py

From the project folder:

cd /workspaces/assignment
nano topic.py

Paste and save this code (Ctrl+O, Enter, Ctrl+X):

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

Run:

python topic.py

Expected output is either:

Topic created successfully!

or:

Topic already exists!

Both indicate the topic is present.

Git checkpoint — topic step

git status
git add topic.py
git commit -m "Create Kafka server_metrics topic"
git push

If Git reports there is nothing to commit, the file may already be committed. Check git status.

4. Verify the topic

Run Kafka CLI commands from the Kafka folder:

cd /workspaces/assignment/kafka_2.13-4.3.1

bin/kafka-topics.sh --list --bootstrap-server localhost:9092

Confirm server_metrics appears.

Describe the topic:

bin/kafka-topics.sh --describe \
  --topic server_metrics \
  --bootstrap-server localhost:9092

5. Create Producer.py

cd /workspaces/assignment
nano Producer.py

Paste and save:

from kafka import KafkaProducer
import json
import time

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

# Send 10 messages
for i in range(10):
    message = {
        "server_id": f"server{i+1}",
        "cpu_usage": 50 + i * 4,
        "memory_usage": 60 + i
    }

    producer.send("server_metrics", value=message)
    print("Sent:", message)
    time.sleep(1)

# Make sure all messages are sent
producer.flush()
producer.close()

print("\n10 messages sent successfully!")

Run:

python Producer.py

Expected: messages for server1 through server10, followed by:

10 messages sent successfully!

CPU values range from 50% to 86%, increasing by 4 each message. Memory values range from 60% to 69%, increasing by 1 each message.

Git checkpoint — producer step

git status
git add Producer.py
git commit -m "Add Kafka metrics producer"
git push

6. Create consumer.py (useful for Question 3)

cd /workspaces/assignment
nano consumer.py

Paste and save:

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

Run the consumer in its own terminal:

cd /workspaces/assignment
python consumer.py

Expected:

Waiting for messages...

Leave it running. In another terminal, run Producer.py to stream messages to it. The consumer should print alerts for server9 (82%) and server10 (86%).

Git checkpoint — consumer step

If you are committing each completed step/question:

git status
git add consumer.py
git commit -m "Add Kafka metrics consumer and CPU alert"
git push

7. Verify published messages with Kafka Console Consumer

Open a new terminal:

cd /workspaces/assignment/kafka_2.13-4.3.1

bin/kafka-console-consumer.sh \
  --topic server_metrics \
  --from-beginning \
  --bootstrap-server localhost:9092

You should see JSON records such as:

{"server_id": "server1", "cpu_usage": 50, "memory_usage": 60}
{"server_id": "server2", "cpu_usage": 54, "memory_usage": 61}

The output continues through server10. Press Ctrl+C to stop the console consumer.

--from-beginning displays retained messages from the start of the topic. Running the producer again adds another batch of 10 messages.

8. Commit the Question 2 guide and finish the checkpoint

If this Markdown guide or other Question 2 documentation was edited:

cd /workspaces/assignment
git status
git add AIOps_Question_2_Kafka_Topic_and_Producer.md
git commit -m "Document Question 2 Kafka practical"
git push

If you want to commit all remaining changes for this question together, inspect git status first, then stage only the relevant files:

git status
git add topic.py Producer.py consumer.py AIOps_Question_2_Kafka_Topic_and_Producer.md
git commit -m "Complete Question 2 Kafka practical"
git push

Do not run both commit patterns blindly—use the one that matches what is still uncommitted. If you already made separate commits for the steps, there may be nothing left to commit.

Final check:

git status
git log -5 --oneline

A clean working tree means there are no uncommitted changes. A successful git push uploads your commits to GitHub.

9. Quick command checklist

Task

Command / action

Go to project

cd /workspaces/assignment

Install library

python -m pip install kafka-python

Check library

python -c "import kafka; print(kafka.__version__)"

Start Kafka

cd /workspaces/assignment/kafka_2.13-4.3.1 && bin/kafka-server-start.sh config/server.properties

Create topic

python topic.py

Verify topic

bin/kafka-topics.sh --list --bootstrap-server localhost:9092 (from Kafka folder)

Start consumer

python consumer.py

Send 10 messages

python Producer.py

Verify records

bin/kafka-console-consumer.sh --topic server_metrics --from-beginning --bootstrap-server localhost:9092 (from Kafka folder)

Check Git

git status

Commit changes

git add <files> && git commit -m "message"

Push commit

git push

Final flow

Kafka broker (KRaft, localhost:9092)
            ↓
   server_metrics topic
            ↑
       Producer.py
    (10 JSON messages)
            ↓
       consumer.py
 (display metrics + CPU alerts)

Question 2 essentials: topic.py, Producer.py, Kafka topic verification, and console-consumer verification. consumer.py is also useful for the next question's CPU-alert logic.
