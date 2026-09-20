# Question 2 — Kafka Topic, Producer & Consumer in GitHub Codespaces

## Purpose

Create a Kafka topic named `server_metrics`, publish 10 JSON server-metric messages, verify them, and optionally consume them with a CPU-threshold alert.

**Project folder:** `/workspaces/assignment`

Python files:
- `topic.py`
- `Producer.py`
- `consumer.py`

> Choose **one Kafka startup method** below: Docker Compose OR direct Kafka installation. Do not start both against port `9092` at the same time. The Python scripts work with either setup because both use `localhost:9092`.

---

# A. Kafka using Docker Compose (Codespaces)

## A1. Check Docker

```bash
cd /workspaces/assignment
docker --version
docker compose version
```

Stop any manually running Kafka broker first (`Ctrl+C` in its broker terminal), so port `9092` is free.

## A2. Create `docker-compose.yml`

```bash
cd /workspaces/assignment
nano docker-compose.yml
```

Paste:

```yaml
services:
  kafka:
    image: apache/kafka:latest
    container_name: kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_LISTENERS: PLAINTEXT://:9092,CONTROLLER://:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_NUM_PARTITIONS: 1
    volumes:
      - kafka_data:/var/lib/kafka/data

volumes:
  kafka_data:
```

Save in nano: `Ctrl+O`, `Enter`, `Ctrl+X`.

### Git checkpoint — Docker configuration

```bash
git status
git add docker-compose.yml
git commit -m "Add Docker Compose Kafka setup"
git push
```

## A3. Start Kafka

```bash
docker compose up -d
docker compose ps
docker compose logs -f kafka
```

Wait for Kafka to start. Press `Ctrl+C` to exit the log view; the container remains running.

Check:

```bash
docker ps
```

---

# B. Kafka installed directly (without Docker)

Use this option if Kafka has already been downloaded and extracted in your Codespace.

## B1. Install/check Python library

```bash
cd /workspaces/assignment
python -m pip install kafka-python
python -c "import kafka; print(kafka.__version__)"
```

## B2. Start Kafka broker

Kafka directory:

`/workspaces/assignment/kafka_2.13-4.3.1`

If this is a **fresh Kafka data directory that has not been formatted**, format it once:

```bash
cd /workspaces/assignment/kafka_2.13-4.3.1
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format --standalone -t "$KAFKA_CLUSTER_ID" -c config/server.properties
```

Do not reformat an existing populated data directory.

Start broker in a terminal and keep it running:

```bash
cd /workspaces/assignment/kafka_2.13-4.3.1
bin/kafka-server-start.sh config/server.properties
```

Kafka 4.x requires Java 17 or newer. This KRaft setup does not require a separate ZooKeeper terminal.

---

# C. Python files (work with either Kafka setup)

## C1. `topic.py`

Create/edit:

```bash
cd /workspaces/assignment
nano topic.py
```

Code:

```python
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
```

Run:

```bash
python topic.py
```

Expected: `Topic created successfully!` or `Topic already exists!`

### Git checkpoint — topic

```bash
git status
git add topic.py
git commit -m "Create Kafka server_metrics topic"
git push
```

## C2. Verify topic

### If using Docker:

```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh \
  --list --bootstrap-server localhost:9092
```

### If using direct Kafka:

```bash
cd /workspaces/assignment/kafka_2.13-4.3.1
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

Expected topic: `server_metrics`

Describe it:

```bash
bin/kafka-topics.sh --describe \
  --topic server_metrics \
  --bootstrap-server localhost:9092
```

(For Docker, prefix the command with `docker exec -it kafka /opt/kafka/` and use the full script path.)

## C3. `Producer.py`

Create/edit:

```bash
cd /workspaces/assignment
nano Producer.py
```

Code:

```python
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

# Ensure all messages are sent
producer.flush()
producer.close()

print("\\n10 messages sent successfully!")
```

Run:

```bash
python Producer.py
```

Expected: 10 `Sent:` lines, ending with `10 messages sent successfully!`

CPU values: 50, 54, 58, 62, 66, 70, 74, 78, 82, 86.
Memory values: 60 through 69.

### Git checkpoint — producer

```bash
git status
git add Producer.py
git commit -m "Add Kafka metrics producer"
git push
```

## C4. `consumer.py` (useful for Question 3)

Create/edit:

```bash
cd /workspaces/assignment
nano consumer.py
```

Code:

```python
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

    print("\\nReceived:")
    print("Server:", server)
    print("CPU:", cpu, "%")
    print("Memory:", memory, "%")

    # High CPU detection
    if cpu > 80:
        print("ALERT: High CPU detected on", server)
```

Run in its own terminal:

```bash
cd /workspaces/assignment
python consumer.py
```

Keep it running. In another terminal, run `python Producer.py`. Alerts should appear for server9 (82%) and server10 (86%).

### Git checkpoint — consumer

```bash
git status
git add consumer.py
git commit -m "Add Kafka metrics consumer and CPU alert"
git push
```

---

# D. Verify published messages with Kafka Console Consumer

## Docker Kafka

```bash
docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh \
  --topic server_metrics \
  --from-beginning \
  --bootstrap-server localhost:9092
```

## Direct Kafka installation

```bash
cd /workspaces/assignment/kafka_2.13-4.3.1

bin/kafka-console-consumer.sh \
  --topic server_metrics \
  --from-beginning \
  --bootstrap-server localhost:9092
```

You should see the JSON messages from `server1` through `server10`. Press `Ctrl+C` to stop the console consumer.

> Running `Producer.py` again publishes another 10 messages. The console consumer's `--from-beginning` option can show retained messages from earlier runs too.

---

# E. Git commit after each completed step

Check status before staging:

```bash
cd /workspaces/assignment
git status
```

Stage and commit only the relevant changed files for that checkpoint, then push:

```bash
git add <file1> <file2>
git commit -m "Describe completed step"
git push
```

Example: commit the Question 2 guide if you updated it:

```bash
git add AIOps_Question_2_Kafka_Topic_and_Producer.md
git commit -m "Document Question 2 Kafka practical"
git push
```

If all Question 2 changes remain uncommitted, you can stage the relevant files together:

```bash
git add docker-compose.yml topic.py Producer.py consumer.py AIOps_Question_2_Kafka_Topic_and_Producer.md
git commit -m "Complete Question 2 Kafka practical"
git push
```

Do not repeat commits blindly if you already committed those changes. Check:

```bash
git status
git log -5 --oneline
```

A successful `git push` uploads the commits to GitHub.

---

# F. Stop Kafka

## Docker

```bash
cd /workspaces/assignment
docker compose down
```

This stops/removes the container while preserving the named data volume. To also delete Kafka's stored data:

```bash
docker compose down -v
```

**Warning:** `-v` deletes the Kafka data volume and stored messages.

## Direct Kafka

Stop the broker using `Ctrl+C` in the terminal where `kafka-server-start.sh` is running.

---

# G. Execution order — quick reference

1. Start Kafka (Docker Compose **or** direct installation).
2. `cd /workspaces/assignment`
3. `python topic.py`
4. Verify topic with Kafka CLI.
5. Start `python consumer.py` in a separate terminal (optional for Question 2; useful for Question 3).
6. Run `python Producer.py`.
7. Verify messages with Kafka console consumer.
8. `git status`, stage changed files, `git commit`, and `git push`.

## Final flow

```text
Kafka broker at localhost:9092
             ↓
      server_metrics topic
             ↑
        Producer.py
      (10 JSON messages)
             ↓
        consumer.py
             ↓
    Display CPU/memory metrics
             ↓
       CPU alert if > 80%
```

**Question 2 essentials:** create `server_metrics`, publish 10 messages, and verify them. The Python consumer demonstrates message consumption and CPU alerting for the next question.
