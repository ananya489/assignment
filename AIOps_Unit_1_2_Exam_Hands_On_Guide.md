# AIOps & Model Deployment --- Unit 1 & Unit 2 Exam + Hands-On Guide

**Course:** AIOps & Model Deployment (CS308E)\
**Focus:** Unit 1 --- Introduction to AIOps and Intelligent Automation\
**Focus:** Unit 2 --- Data Pipelines and Model Infrastructure\
**Use case:** Virtual-environment / sandbox practical exam

------------------------------------------------------------------------

## 0. What this guide covers

This guide follows the syllabus shown in the provided course-booklet
image.

### Unit 1

-   AIOps concepts, architecture, and evolution from DevOps to AIOps
-   AI in IT operations
-   Anomaly detection
-   Root-cause analysis
-   Predictive maintenance
-   AIOps lifecycle: data ingestion → analytics → correlation →
    automation
-   AIOps platforms: Moogsoft, Dynatrace, Splunk, IBM Watson AIOps
-   Python/shell log analysis
-   Rule-based anomaly detection
-   ML-based anomaly detection
-   Automatic service restart
-   Basic visualization with Matplotlib/Grafana

### Unit 2

-   Automated data pipelines for AI/ML
-   Batch vs real-time processing
-   Apache Kafka
-   Apache Airflow
-   Apache Spark
-   Feature stores: Feast, Hopsworks
-   Scalable data management
-   TensorFlow Extended (TFX)
-   Kubeflow Pipelines
-   Dataset/model versioning with DVC
-   Experiment/model tracking with MLflow
-   End-to-end Kafka + Airflow practical workflow

------------------------------------------------------------------------

# PART I --- UNIT 1: AIOps

## 1. What is AIOps?

**AIOps = Artificial Intelligence for IT Operations.**

It applies machine learning, statistics, automation, and data analysis
to operational IT data such as:

-   application logs
-   server logs
-   CPU/memory metrics
-   network metrics
-   traces
-   alerts
-   events
-   deployment information

The goal is to move from:

``` text
Human manually watches systems
        ↓
Human notices problem
        ↓
Human investigates
        ↓
Human fixes problem
```

toward:

``` text
Collect data
    ↓
Detect abnormal behavior
    ↓
Correlate related events
    ↓
Find probable cause
    ↓
Predict failures
    ↓
Automate an appropriate action
```

### Simple definition for an exam

> AIOps uses AI/ML and automation to collect, analyze, correlate, and
> act on IT operational data.

------------------------------------------------------------------------

# 2. DevOps vs AIOps

## DevOps

DevOps connects development and operations.

Main ideas:

``` text
Development
     +
Operations
     ↓
CI/CD
Automation
Monitoring
Fast releases
```

## AIOps

AIOps adds intelligent analysis and automated decision support to
operational data.

``` text
DevOps
  +
Logs
Metrics
Traces
Events
  +
AI/ML
  ↓
AIOps
```

### Key difference

  DevOps                          AIOps
  ------------------------------- ----------------------------------------------------
  Development + Operations        AI + Operations
  CI/CD is central                Observability + intelligence + automation
  Automation                      Intelligent automation
  Monitoring                      Analysis and correlation of large operational data
  Human investigation is common   AI can help detect/correlate/predict

Do not say that AIOps replaces DevOps. AIOps can complement DevOps.

------------------------------------------------------------------------

# 3. AIOps architecture

Remember this pipeline:

``` text
              AIOps
                │
       ┌────────┴────────┐
       │                 │
   Data Sources      IT Systems
       │                 │
       └────────┬────────┘
                ↓
          DATA INGESTION
                ↓
       DATA PROCESSING
                ↓
      ANALYTICS / ML
                ↓
      EVENT CORRELATION
                ↓
      ROOT-CAUSE ANALYSIS
                ↓
      PREDICTION / ALERT
                ↓
          AUTOMATION
                ↓
       IT OPERATIONS
```

### Main stages

1.  **Ingestion**
2.  **Processing**
3.  **Detection**
4.  **Correlation**
5.  **Root-cause analysis**
6.  **Prediction**
7.  **Automation**
8.  **Feedback**

------------------------------------------------------------------------

# 4. AIOps lifecycle

The syllabus explicitly gives this flow:

``` text
Data Ingestion
      ↓
Analytics
      ↓
Correlation
      ↓
Automation
```

Expand it for an exam:

``` text
Logs / Metrics / Events / Traces
             ↓
          Ingestion
             ↓
      Cleaning / Parsing
             ↓
         Analytics
             ↓
 Anomaly / Pattern Detection
             ↓
     Event Correlation
             ↓
   Root Cause Analysis
             ↓
Prediction / Alerting
             ↓
        Automation
             ↓
       Feedback Loop
```

------------------------------------------------------------------------

# 5. Data ingestion

Data ingestion means collecting operational data from different sources.

Examples:

``` text
Application logs
System logs
Kafka events
CPU metrics
Memory metrics
Network metrics
Database metrics
Cloud monitoring data
```

Typical ingestion technologies:

``` text
Kafka
Fluent Bit
Logstash
Filebeat
APIs
Cloud agents
```

------------------------------------------------------------------------

# 6. Logs, metrics, traces and events

These are commonly confused.

## Logs

Discrete text records describing events.

Example:

``` text
2026-09-20 10:30:01 INFO User login successful
2026-09-20 10:31:12 ERROR Database connection failed
```

Logs answer:

> What happened?

------------------------------------------------------------------------

## Metrics

Numerical measurements over time.

Example:

``` text
CPU = 82%
Memory = 74%
Latency = 320 ms
Requests/sec = 1500
```

Metrics answer:

> How much? How fast? How often?

------------------------------------------------------------------------

## Traces

Follow a request across multiple services.

Example:

``` text
Client
  ↓
API Gateway
  ↓
Auth Service
  ↓
Order Service
  ↓
Database
```

A trace helps identify where time was spent.

------------------------------------------------------------------------

## Events

Something happened at a particular time.

Example:

``` text
Deployment started
Server restarted
Database failed
Configuration changed
```

------------------------------------------------------------------------

# 7. Anomaly detection

An anomaly is an observation that significantly differs from expected
behavior.

Example:

Normal CPU:

``` text
40
42
41
43
39
44
```

Suddenly:

``` text
97
```

Potential anomaly.

But remember:

> An unusual value is not automatically proof of a system failure.

You need context, baseline, thresholds, trends, and duration.

------------------------------------------------------------------------

# 8. Types of anomaly detection

## A. Threshold/rule-based

Example:

``` python
if cpu > 90:
    print("ALERT: High CPU")
```

Advantages: - Simple - Fast - Easy to understand

Disadvantages: - Requires manual thresholds - May create false alarms -
Poor for changing patterns

------------------------------------------------------------------------

## B. Statistical

Use statistics such as:

-   mean
-   standard deviation
-   z-score
-   moving average
-   percentile

Example:

``` text
mean = 50
std = 5

value = 80
```

The value is far from the normal range.

------------------------------------------------------------------------

## C. Machine-learning based

Possible algorithms:

-   Isolation Forest
-   One-Class SVM
-   Local Outlier Factor
-   Autoencoders
-   clustering-based methods

For a simple practical exam, **Isolation Forest** is a useful example.

------------------------------------------------------------------------

# 9. Simple log anomaly detector --- rule based

Create:

``` text
logs.txt
```

Example:

``` text
2026-09-20 10:00:01 INFO CPU=42
2026-09-20 10:01:01 INFO CPU=45
2026-09-20 10:02:01 INFO CPU=43
2026-09-20 10:03:01 INFO CPU=95
2026-09-20 10:04:01 INFO CPU=47
```

Python:

``` python
import re

THRESHOLD = 90

with open("logs.txt", "r") as f:
    for line in f:
        match = re.search(r"CPU=(\d+)", line)

        if match:
            cpu = int(match.group(1))

            if cpu > THRESHOLD:
                print("ANOMALY:", line.strip())
```

Output:

``` text
ANOMALY: 2026-09-20 10:03:01 INFO CPU=95
```

------------------------------------------------------------------------

# 10. Better log analysis with Python

``` python
import re
from collections import Counter

levels = Counter()

with open("logs.txt", "r") as f:
    for line in f:
        match = re.search(r"\b(INFO|WARNING|ERROR)\b", line)

        if match:
            levels[match.group(1)] += 1

print("Log summary:")
print(levels)
```

Example:

``` text
Log summary:
Counter({'INFO': 100, 'WARNING': 12, 'ERROR': 5})
```

This gives a simple operational summary.

------------------------------------------------------------------------

# 11. ML anomaly detection with Isolation Forest

Install:

``` bash
pip install pandas scikit-learn
```

Code:

``` python
import numpy as np
from sklearn.ensemble import IsolationForest

# Normal CPU values
X = np.array([
    [40],
    [42],
    [41],
    [43],
    [45],
    [39],
    [44],
    [46],
    [98],   # possible anomaly
    [42],
    [41]
])

model = IsolationForest(
    contamination=0.1,
    random_state=42
)

model.fit(X)

predictions = model.predict(X)

for value, prediction in zip(X.flatten(), predictions):
    if prediction == -1:
        print(value, "ANOMALY")
    else:
        print(value, "NORMAL")
```

Important:

``` text
1  = normal
-1 = anomaly
```

The exact result depends on the data and model parameters.

------------------------------------------------------------------------

# 12. Root Cause Analysis (RCA)

Anomaly detection tells you:

> Something unusual happened.

RCA asks:

> What caused it?

Example:

``` text
Database CPU ↑
      ↓
Database latency ↑
      ↓
API latency ↑
      ↓
Request failures ↑
```

Possible root cause:

``` text
Database overload
```

AIOps can correlate events to avoid treating every downstream symptom as
an independent incident.

------------------------------------------------------------------------

# 13. Event correlation

Suppose the system produces:

``` text
10:00 Database CPU high
10:01 Database latency high
10:01 API latency high
10:02 API errors high
10:02 User complaints
```

A naive monitoring system may produce five alerts.

Correlation tries to recognize:

``` text
Database problem
      ↓
Database latency
      ↓
API latency
      ↓
API failures
```

So the system can group related events.

------------------------------------------------------------------------

# 14. Predictive maintenance

Traditional maintenance:

``` text
Wait for failure
     ↓
Repair
```

Preventive maintenance:

``` text
Schedule maintenance periodically
```

Predictive maintenance:

``` text
Collect sensor/operational data
          ↓
Detect degradation pattern
          ↓
Predict possible failure
          ↓
Schedule maintenance
```

Example:

``` text
Disk temperature
Disk errors
Read/write latency
SMART metrics
       ↓
ML model
       ↓
Failure-risk estimate
```

------------------------------------------------------------------------

# 15. AIOps platforms from your syllabus

Know their role at a high level.

### Moogsoft

Focuses on AIOps/event management and event correlation.

### Dynatrace

Observability platform covering application, infrastructure, traces,
logs, metrics, and automated analysis.

### Splunk

Strong in log/event data analysis, search, monitoring, security and
observability.

### IBM Watson AIOps

IBM's AIOps approach/platform for operational event analysis,
correlation and automation.

For MCQs, remember:

``` text
AIOps platforms
→ ingest operational data
→ analyze/correlate events
→ detect problems
→ help automate response
```

------------------------------------------------------------------------

# 16. Automatic service restart

The Unit 1 practical specifically mentions detecting and restarting
failed services.

A simple Linux shell example:

``` bash
#!/bin/bash

SERVICE="nginx"

if systemctl is-active --quiet "$SERVICE"; then
    echo "$SERVICE is running"
else
    echo "$SERVICE is down"
    sudo systemctl restart "$SERVICE"
fi
```

Check status:

``` bash
systemctl status nginx
```

Check whether it is running:

``` bash
systemctl is-active nginx
```

Restart:

``` bash
sudo systemctl restart nginx
```

Enable on boot:

``` bash
sudo systemctl enable nginx
```

### Important exam idea

A production system should not blindly restart services forever.

A safer automation design is:

``` text
Detect failure
     ↓
Check recent restart count
     ↓
Restart if policy allows
     ↓
Verify service
     ↓
Alert if still failing
```

------------------------------------------------------------------------

# PART II --- UNIT 2: DATA PIPELINES

# 17. What is a data pipeline?

A data pipeline moves data from source to destination while performing
processing.

Basic example:

``` text
Source
  ↓
Ingestion
  ↓
Processing
  ↓
Storage
  ↓
ML / Analytics
```

Example:

``` text
Application
    ↓
Kafka
    ↓
Python/Spark
    ↓
Data Lake
    ↓
Feature Store
    ↓
ML Model
```

------------------------------------------------------------------------

# 18. Batch vs real-time processing

## Batch

Process data in groups.

Example:

``` text
Every night:
10 million records
        ↓
Process together
```

Good for: - daily reports - historical analysis - large periodic jobs

Examples: - Spark batch jobs - scheduled Airflow jobs

------------------------------------------------------------------------

## Real-time / streaming

Process data continuously or with low latency.

``` text
Event 1 → process
Event 2 → process
Event 3 → process
Event 4 → process
```

Kafka is commonly used for event streaming.

### Quick comparison

  Batch                         Streaming
  ----------------------------- --------------------------------
  Data processed in groups      Data processed continuously
  Higher latency                Lower latency
  Scheduled jobs common         Event-driven processing common
  Airflow/Spark commonly used   Kafka commonly used

------------------------------------------------------------------------

# PART III --- KAFKA

# 19. What is Apache Kafka?

Kafka is a distributed event-streaming platform.

It is commonly used to:

-   publish events
-   consume events
-   build streaming pipelines
-   decouple applications
-   process large event volumes
-   retain event data for consumers

Think:

``` text
Producer
    ↓
Kafka
    ↓
Consumer
```

------------------------------------------------------------------------

# 20. Kafka architecture

``` text
                 Kafka Cluster

       ┌──────────────┐
       │   Broker 1   │
       └──────────────┘

       ┌──────────────┐
       │   Broker 2   │
       └──────────────┘

       ┌──────────────┐
       │   Broker 3   │
       └──────────────┘
```

A Kafka cluster can contain multiple brokers.

A topic is divided into partitions.

``` text
Topic: sensor-data

Partition 0:
0  1  2  3  4  5

Partition 1:
0  1  2  3  4

Partition 2:
0  1  2  3
```

------------------------------------------------------------------------

# 21. Kafka terms you must know

## Producer

Writes records to Kafka.

``` text
Producer → Topic
```

## Consumer

Reads records.

``` text
Topic → Consumer
```

## Broker

Kafka server.

## Topic

Logical category/stream.

Example:

``` text
orders
payments
logs
sensor-data
```

## Partition

Ordered log inside a topic.

## Offset

Position of a record within a partition.

Example:

``` text
Offset 0 → A
Offset 1 → B
Offset 2 → C
```

## Consumer group

Group of consumers cooperating to consume a topic.

------------------------------------------------------------------------

# 22. Important Kafka rule

Within a consumer group:

> A partition is assigned to at most one consumer at a time.

Example:

``` text
Topic
P0
P1
P2

Consumer Group G

C1 → P0
C2 → P1
C3 → P2
```

If:

``` text
3 partitions
5 consumers
```

then not every consumer can receive a partition simultaneously.

At least two consumers will have no partition assigned for that topic at
that moment.

------------------------------------------------------------------------

# 23. Kafka message flow

``` text
Application
     │
     ▼
Producer
     │
     ▼
Kafka Topic
     │
     ├── Partition 0
     ├── Partition 1
     └── Partition 2
            │
            ▼
       Consumer Group
            │
            ▼
        Processing
```

------------------------------------------------------------------------

# 24. Kafka installation concepts

Your exact sandbox may already have Kafka installed.

First check:

``` bash
kafka-topics.sh --help
```

On Windows:

``` cmd
kafka-topics.bat --help
```

If the command is not found, locate the Kafka installation and run the
script from its `bin` directory.

Modern Kafka installations may use **KRaft** instead of ZooKeeper. Older
labs may use ZooKeeper.

For an exam, first identify which architecture the sandbox provides.

------------------------------------------------------------------------

# 25. Kafka KRaft concept

Modern Kafka can run without ZooKeeper using KRaft.

Conceptually:

``` text
Kafka
  ↓
KRaft metadata quorum
```

Older Kafka labs often look like:

``` text
ZooKeeper
    ↓
Kafka Broker
```

Do not mix the startup commands from the two setups.

------------------------------------------------------------------------

# 26. Step-by-step Kafka practical

## Step 1 --- Check Kafka

Linux:

``` bash
kafka-topics.sh --help
```

Windows:

``` cmd
kafka-topics.bat --help
```

------------------------------------------------------------------------

## Step 2 --- Start Kafka

Use the startup procedure supplied by your sandbox.

For a KRaft installation, the distribution normally provides
configuration under:

``` text
config/
```

and a server configuration file.

For older ZooKeeper-based installations, you may need ZooKeeper first
and then the Kafka broker.

**Exam rule:** use the commands/configuration supplied by your installed
Kafka version. Do not blindly mix KRaft and ZooKeeper commands.

------------------------------------------------------------------------

# 27. Step 3 --- Create a topic

Example:

``` bash
kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --topic sensor-data \
  --partitions 3 \
  --replication-factor 1
```

Windows:

``` cmd
kafka-topics.bat --bootstrap-server localhost:9092 --create --topic sensor-data --partitions 3 --replication-factor 1
```

If the broker uses another port, replace:

``` text
localhost:9092
```

with the sandbox's bootstrap server.

------------------------------------------------------------------------

# 28. Step 4 --- List topics

Linux:

``` bash
kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --list
```

Windows:

``` cmd
kafka-topics.bat --bootstrap-server localhost:9092 --list
```

You should see:

``` text
sensor-data
```

------------------------------------------------------------------------

# 29. Step 5 --- Describe topic

``` bash
kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --topic sensor-data
```

Look for:

``` text
Partition
Leader
Replicas
ISR
```

### Important meanings

**Leader:** broker currently handling writes/reads for that partition.

**Replicas:** copies of the partition.

**ISR:** in-sync replicas.

------------------------------------------------------------------------

# 30. Step 6 --- Start a producer

``` bash
kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic sensor-data
```

Enter:

``` text
temperature=25
temperature=26
temperature=27
temperature=95
```

Each entered line becomes a Kafka record.

------------------------------------------------------------------------

# 31. Step 7 --- Start a consumer

Open another terminal:

``` bash
kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic sensor-data
```

You should receive new messages.

To read old messages too:

``` bash
kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic sensor-data \
  --from-beginning
```

------------------------------------------------------------------------

# 32. Step 8 --- Consumer group

``` bash
kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic sensor-data \
  --group sensor-group
```

Now Kafka tracks the consumer group's offsets.

------------------------------------------------------------------------

# 33. Step 9 --- Inspect consumer group

``` bash
kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --group sensor-group
```

Important columns:

``` text
CURRENT-OFFSET
LOG-END-OFFSET
LAG
```

Conceptually:

``` text
LAG = LOG-END-OFFSET - CURRENT-OFFSET
```

Example:

``` text
CURRENT = 850
LOG-END = 1000

LAG = 150
```

------------------------------------------------------------------------

# 34. Kafka Python producer

Install:

``` bash
pip install kafka-python
```

Python:

``` python
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

for i in range(10):
    data = {
        "sensor_id": "S1",
        "temperature": 25 + i
    }

    producer.send("sensor-data", value=data)
    print("Sent:", data)

    time.sleep(1)

producer.flush()
producer.close()
```

------------------------------------------------------------------------

# 35. Kafka Python consumer

``` python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "sensor-data",
    bootstrap_servers="localhost:9092",
    group_id="sensor-python-group",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

for message in consumer:
    print(
        "partition =", message.partition,
        "offset =", message.offset,
        "value =", message.value
    )
```

Run producer in one terminal and consumer in another.

------------------------------------------------------------------------

# 36. Kafka anomaly detector

Producer sends:

``` json
{
  "sensor_id": "S1",
  "temperature": 95
}
```

Consumer detects:

``` python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "sensor-data",
    bootstrap_servers="localhost:9092",
    group_id="anomaly-detector",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

THRESHOLD = 80

for message in consumer:
    data = message.value
    temperature = data["temperature"]

    if temperature > THRESHOLD:
        print("ANOMALY:", data)
    else:
        print("NORMAL:", data)
```

This directly connects **Unit 1 anomaly detection** with **Unit 2 Kafka
streaming**.

------------------------------------------------------------------------

# 37. Kafka troubleshooting

## Problem: connection refused

Possible causes:

``` text
Broker not running
Wrong host
Wrong port
Firewall/network issue
Incorrect bootstrap-server
```

Check:

``` bash
kafka-topics.sh --bootstrap-server localhost:9092 --list
```

------------------------------------------------------------------------

## Problem: topic does not exist

Check:

``` bash
kafka-topics.sh --bootstrap-server localhost:9092 --list
```

Create it if appropriate.

------------------------------------------------------------------------

## Problem: consumer receives nothing

Check:

``` text
Topic name
Broker address
Consumer group
Whether producer actually sent messages
Whether the consumer started from the desired offset
```

Try:

``` bash
kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic sensor-data \
  --from-beginning
```

------------------------------------------------------------------------

## Problem: consumer lag increases

Think:

``` text
Producer rate > Consumer processing rate
```

Investigate:

``` text
Consumer CPU
Consumer processing time
Number of partitions
Consumer count
Broker performance
Network
Errors/retries
```

------------------------------------------------------------------------

# PART IV --- APACHE AIRFLOW

# 38. What is Airflow?

Apache Airflow is a workflow orchestration platform.

It is used to:

-   define workflows as DAGs
-   schedule tasks
-   execute tasks
-   manage dependencies
-   retry failed tasks
-   monitor workflows
-   view logs

Think:

``` text
Airflow = Workflow Orchestration
```

Kafka is not a replacement for Airflow.

``` text
Kafka
→ event streaming

Airflow
→ workflow orchestration
```

------------------------------------------------------------------------

# 39. Airflow architecture

``` text
                 Airflow UI
                    │
                    ▼
               API/Web layer
                    │
                    ▼
                Scheduler
                    │
                    ▼
                 Executor
                    │
                    ▼
                Task Worker
                    │
                    ▼
             Metadata Database
```

Airflow also uses:

``` text
DAG files
Logs
Connections
Variables
XCom
```

------------------------------------------------------------------------

# 40. DAG

DAG means:

> Directed Acyclic Graph

Example:

``` text
extract
   ↓
transform
   ↓
load
```

Directed:

``` text
A → B
```

Acyclic:

``` text
A → B → C
```

not:

``` text
A → B → C → A
```

------------------------------------------------------------------------

# 41. DAG vs task vs task instance

### DAG

Entire workflow.

### Task

One operation.

### Task instance

One execution of one task for a particular DAG run.

Example:

``` text
DAG
 ├── extract
 ├── transform
 └── load
```

A particular run creates task instances for those tasks.

------------------------------------------------------------------------

# 42. Airflow task states

Know these:

``` text
scheduled
queued
running
success
failed
up_for_retry
upstream_failed
skipped
removed
```

Typical flow:

``` text
scheduled
    ↓
queued
    ↓
running
   / \
  /   \
success failed
          ↓
    up_for_retry
```

If:

``` text
A → B
```

and A fails, B may become:

``` text
upstream_failed
```

------------------------------------------------------------------------

# 43. Airflow installation

In a Linux/WSL virtual environment, a typical setup is:

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

Upgrade packaging tools:

``` bash
pip install --upgrade pip setuptools wheel
```

For Airflow, use the constraints file appropriate for the exact Airflow
and Python versions installed in the sandbox.

Example pattern:

``` bash
export AIRFLOW_VERSION=3.1.0
export PYTHON_VERSION=3.12
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

Windows PowerShell uses different environment-variable syntax.

If Airflow is already installed in the exam sandbox, do not reinstall
it.

------------------------------------------------------------------------

# 44. AIRFLOW_HOME

Check:

``` bash
echo $AIRFLOW_HOME
```

If not set:

``` bash
export AIRFLOW_HOME=~/airflow
```

The metadata database is commonly located under the Airflow home
directory.

------------------------------------------------------------------------

# 45. Initialize/migrate Airflow database

For the Airflow version installed in your environment, use its
documented database initialization/migration command.

For modern Airflow:

``` bash
airflow db migrate
```

Check:

``` bash
airflow version
```

------------------------------------------------------------------------

# 46. Create a DAG directory

Example:

``` bash
mkdir -p ~/airflow/dags
```

If your environment uses another DAG folder:

``` bash
airflow config get-value core dags_folder
```

This command is very useful in a sandbox.

------------------------------------------------------------------------

# 47. First Airflow DAG

Create:

``` text
hello_dag.py
```

Code:

``` python
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def hello():
    print("Hello from Airflow")


with DAG(
    dag_id="hello_dag",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    hello_task = PythonOperator(
        task_id="hello_task",
        python_callable=hello,
    )
```

------------------------------------------------------------------------

# 48. DAG with dependencies

``` python
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def extract():
    print("Extracting data")


def transform():
    print("Transforming data")


def load():
    print("Loading data")


with DAG(
    dag_id="etl_dag",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform,
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load,
    )

    extract_task >> transform_task >> load_task
```

Workflow:

``` text
extract
   ↓
transform
   ↓
load
```

------------------------------------------------------------------------

# 49. Parallel Airflow tasks

You can create:

``` text
       extract
       /     \
      ↓       ↓
 clean      validate
      \       /
       ↓     ↓
        load
```

Code:

``` python
extract_task >> [clean_task, validate_task]
[clean_task, validate_task] >> load_task
```

This is important for DAG questions.

------------------------------------------------------------------------

# 50. Useful Airflow CLI commands

Check version:

``` bash
airflow version
```

List DAGs:

``` bash
airflow dags list
```

List tasks:

``` bash
airflow tasks list <dag_id>
```

Trigger a DAG:

``` bash
airflow dags trigger <dag_id>
```

List DAG runs:

``` bash
airflow dags list-runs -d <dag_id>
```

Check import errors:

``` bash
airflow dags list-import-errors
```

Test a task:

``` bash
airflow tasks test <dag_id> <task_id> <logical_date>
```

Check configuration:

``` bash
airflow config list
```

Check the DAG folder:

``` bash
airflow config get-value core dags_folder
```

------------------------------------------------------------------------

# 51. Airflow task testing

Suppose:

``` text
DAG ID = etl_dag
Task ID = extract
```

A task-level test can be run with the appropriate logical date:

``` bash
airflow tasks test etl_dag extract 2026-09-20
```

Task testing is useful because it helps isolate task code from the
complete DAG scheduling workflow.

------------------------------------------------------------------------

# 52. Airflow logs

If a task fails:

``` text
DAG
 ↓
Task
 ↓
Task Instance
 ↓
Logs
 ↓
Traceback
 ↓
Root cause
```

Look for:

``` text
ERROR
Exception
Traceback
```

Example:

``` text
ModuleNotFoundError: No module named 'pandas'
```

Interpretation:

> The environment executing that task does not have the required package
> available.

------------------------------------------------------------------------

# 53. Airflow retry

A task can be configured with retries.

Example:

``` python
from datetime import timedelta

default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}
```

Then:

``` python
with DAG(
    dag_id="retry_example",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
) as dag:
    ...
```

Concept:

``` text
Task fails
   ↓
Retry
   ↓
Retry
   ↓
Retry
   ↓
Final failure if unsuccessful
```

Retries are useful for transient failures such as temporary
network/database problems.

They are not a solution for every permanent code error.

------------------------------------------------------------------------

# 54. Airflow scheduling

A DAG can be manually triggered or scheduled.

Examples of concepts:

``` text
Manual
Hourly
Daily
Weekly
Cron-based
```

For an exam, understand:

``` text
schedule
start_date
catchup
DAG run
logical date
```

### catchup=False

Generally means Airflow should not automatically create all missed
historical scheduled runs when the DAG becomes active.

------------------------------------------------------------------------

# 55. Airflow XCom

XCom = cross-communication between tasks.

It is useful for **small pieces of metadata/results**, not large
datasets.

Example:

``` python
from airflow.decorators import dag, task
from datetime import datetime


@dag(
    dag_id="xcom_example",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
)
def xcom_example():

    @task
    def produce():
        return {"status": "ok", "count": 100}

    @task
    def consume(data):
        print(data)

    consume(produce())


xcom_example()
```

Concept:

``` text
Task A
  ↓
XCom
  ↓
Task B
```

Do not use XCom to pass huge DataFrames or model files.

------------------------------------------------------------------------

# 56. Airflow Variables vs Connections

### Variable

Stores configuration/value data.

Example concept:

``` text
environment = production
```

### Connection

Stores information required to connect to an external system.

Examples:

``` text
PostgreSQL
AWS
Kafka
HTTP API
```

Think:

``` text
Variable → configuration/value
Connection → external system credentials/configuration
```

------------------------------------------------------------------------

# PART V --- AIRFLOW + KAFKA PRACTICAL

# 57. End-to-end architecture

This is one of the most important diagrams for your course.

``` text
                   PRODUCER
                      │
                      ▼
                Kafka Topic
                      │
            ┌─────────┼─────────┐
            ▼         ▼         ▼
           P0        P1        P2
            │         │         │
            └─────────┼─────────┘
                      ▼
                  Consumer
                      │
                      ▼
              Processed Dataset
                      │
                      ▼
                  Airflow
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       Validate     Train       Evaluate
          │           │           │
          └───────────┼───────────┘
                      ▼
                 Model/Report
```

Kafka handles streaming ingestion.

Airflow orchestrates the workflow.

------------------------------------------------------------------------

# 58. Airflow DAG that processes Kafka output

A simple educational DAG can execute a Python program/script.

``` python
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="kafka_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    check_kafka = BashOperator(
        task_id="check_kafka",
        bash_command="echo 'Checking Kafka pipeline'",
    )

    process_data = BashOperator(
        task_id="process_data",
        bash_command="python /path/to/process_data.py",
    )

    generate_report = BashOperator(
        task_id="generate_report",
        bash_command="echo 'Generating report'",
    )

    check_kafka >> process_data >> generate_report
```

In a real deployment, use the environment/path available to the Airflow
task executor.

------------------------------------------------------------------------

# 59. Better architecture: Airflow should orchestrate, not become Kafka

Bad mental model:

``` text
Airflow replaces Kafka
```

Correct:

``` text
Kafka = streaming/event transport
Airflow = workflow orchestration
```

They can work together.

------------------------------------------------------------------------

# PART VI --- SPARK

# 60. What is Apache Spark?

Spark is a distributed data-processing engine.

It is commonly used for:

-   batch processing
-   large-scale transformations
-   SQL analytics
-   streaming workloads
-   ML workflows

Think:

``` text
Huge dataset
     ↓
Apache Spark
     ↓
Distributed processing
```

------------------------------------------------------------------------

# 61. Kafka vs Spark vs Airflow

Memorize this table:

  Tool                 Main purpose
  -------------------- -----------------------------
  Kafka                Event streaming / messaging
  Spark                Distributed data processing
  Airflow              Workflow orchestration
  Feast                Feature store
  Hopsworks            Feature/data platform
  TFX                  ML production pipeline
  Kubeflow Pipelines   ML workflow orchestration
  DVC                  Data/model versioning
  MLflow               Experiment/model tracking

------------------------------------------------------------------------

# PART VII --- FEATURE STORES

# 62. What is a feature?

A feature is an input used by an ML model.

Example:

``` text
temperature = 31
humidity = 72
rainfall = 12
```

Model:

``` text
temperature
humidity
rainfall
      ↓
    ML model
      ↓
prediction
```

------------------------------------------------------------------------

# 63. What is a feature store?

A feature store manages ML features consistently.

It helps with:

-   feature storage
-   feature reuse
-   feature discovery
-   training/serving consistency
-   online/offline access

Examples in your syllabus:

``` text
Feast
Hopsworks
```

------------------------------------------------------------------------

# 64. Training-serving skew

Suppose training uses:

``` text
temperature = Celsius
```

but production sends:

``` text
temperature = Fahrenheit
```

The model can behave incorrectly.

A feature store can help establish consistent feature definitions and
serving.

------------------------------------------------------------------------

# PART VIII --- TFX

# 65. TensorFlow Extended

TFX is a platform/framework for production ML pipelines using
TensorFlow.

Typical components include:

``` text
Data
 ↓
ExampleGen
 ↓
Statistics
 ↓
Schema
 ↓
Transform
 ↓
Trainer
 ↓
Evaluator
 ↓
Pusher
```

The exact pipeline depends on the application.

Conceptually:

``` text
Data
 ↓
Validate
 ↓
Transform
 ↓
Train
 ↓
Evaluate
 ↓
Deploy
```

------------------------------------------------------------------------

# PART IX --- KUBEFLOW PIPELINES

# 66. Kubeflow Pipelines

Kubeflow Pipelines allows ML workflows to be represented as
components/pipelines.

Example:

``` text
Data ingestion
      ↓
Preprocessing
      ↓
Training
      ↓
Evaluation
      ↓
Deployment
```

Compared with Airflow:

-   Airflow is general workflow orchestration.
-   Kubeflow Pipelines is strongly focused on ML workflows and
    Kubernetes environments.

They can overlap in functionality, but their ecosystems and typical use
cases differ.

------------------------------------------------------------------------

# PART X --- DVC

# 67. What is DVC?

DVC = Data Version Control.

Git tracks code.

DVC can help track large datasets/model artifacts.

Concept:

``` text
Git
 ↓
Code version

DVC
 ↓
Dataset/model version
```

Example commands:

``` bash
dvc init
dvc add data/data.csv
git add data/data.csv.dvc .gitignore
git commit -m "Track dataset"
```

For remote storage, configure the appropriate DVC remote.

------------------------------------------------------------------------

# PART XI --- MLFLOW

# 68. What is MLflow?

MLflow helps manage the ML lifecycle.

Common capabilities:

``` text
Experiment tracking
Parameter tracking
Metric tracking
Artifact storage
Model tracking/registry
```

Example:

``` python
import mlflow

with mlflow.start_run():

    learning_rate = 0.01
    accuracy = 0.91

    mlflow.log_param("learning_rate", learning_rate)
    mlflow.log_metric("accuracy", accuracy)
```

Run:

``` bash
pip install mlflow
```

Start UI/server according to the installed MLflow version and sandbox
setup.

------------------------------------------------------------------------

# PART XII --- END-TO-END UNIT 1 + 2 PROJECT

## 69. Mini project: Real-time anomaly detection

Goal:

``` text
Generate sensor data
       ↓
Kafka
       ↓
Python consumer
       ↓
Anomaly detector
       ↓
Log alert
       ↓
Airflow orchestrates periodic processing/reporting
```

------------------------------------------------------------------------

## Step 1 --- Create project

``` text
aiops_exam/
│
├── producer.py
├── consumer.py
├── logs.txt
└── dags/
    └── aiops_pipeline.py
```

------------------------------------------------------------------------

## Step 2 --- Producer

``` python
from kafka import KafkaProducer
import json
import random
import time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

for i in range(30):

    temperature = random.choice(
        [25, 26, 27, 28, 29, 30, 95]
    )

    event = {
        "sensor_id": "S1",
        "temperature": temperature,
        "timestamp": time.time()
    }

    producer.send("sensor-data", value=event)

    print("Produced:", event)

    time.sleep(1)

producer.flush()
producer.close()
```

------------------------------------------------------------------------

## Step 3 --- Consumer/anomaly detector

``` python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "sensor-data",
    bootstrap_servers="localhost:9092",
    group_id="aiops-anomaly-group",
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

THRESHOLD = 80

for message in consumer:

    event = message.value
    temperature = event["temperature"]

    if temperature > THRESHOLD:
        print(
            "ANOMALY:",
            "partition =", message.partition,
            "offset =", message.offset,
            "data =", event
        )
    else:
        print("NORMAL:", event)
```

------------------------------------------------------------------------

# 70. Step 4 --- Airflow orchestration

``` python
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="aiops_anomaly_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    check_pipeline = BashOperator(
        task_id="check_pipeline",
        bash_command="echo 'Checking AIOps pipeline'",
    )

    analyze_logs = BashOperator(
        task_id="analyze_logs",
        bash_command="python /path/to/analyze_logs.py",
    )

    report = BashOperator(
        task_id="report",
        bash_command="echo 'Anomaly report generated'",
    )

    check_pipeline >> analyze_logs >> report
```

------------------------------------------------------------------------

# PART XIII --- LOG + METRIC + ANOMALY EXAM QUESTIONS

## 71. Question: CPU spike

Given:

``` text
CPU:
40
42
43
41
45
97
```

What is the likely observation?

**Answer:** The value 97 is an anomalous/high CPU observation relative
to the preceding baseline.

------------------------------------------------------------------------

## 72. Question: Kafka lag

``` text
Current offset = 800
Log end offset = 1200
```

Calculate:

``` text
Lag = 1200 - 800 = 400
```

------------------------------------------------------------------------

## 73. Question: task failure

Airflow shows:

``` text
extract → SUCCESS
transform → FAILED
load → UPSTREAM_FAILED
```

Interpretation:

``` text
transform failed
      ↓
load depends on transform
      ↓
load cannot proceed normally
```

Inspect the **transform task logs first**.

------------------------------------------------------------------------

## 74. Question: Kafka consumer is slow

Metrics:

``` text
Producer = 10,000 msg/s
Consumer = 4,000 msg/s
```

Likely result:

``` text
Incoming rate > processing rate
```

Therefore consumer lag can grow.

------------------------------------------------------------------------

## 75. Question: log vs metric

Question:

> Which is better for finding the exact exception that caused a task
> failure?

Answer:

``` text
Logs
```

Question:

> Which is better for measuring consumer backlog?

Answer:

``` text
Metrics/offset information, especially consumer lag
```

------------------------------------------------------------------------

# PART XIV --- SANDBOX TROUBLESHOOTING CHECKLIST

## 76. If Airflow DAG is missing

Run:

``` bash
airflow dags list
```

Then:

``` bash
airflow dags list-import-errors
```

Check:

``` bash
airflow config get-value core dags_folder
```

Then verify:

``` text
DAG file is in the correct directory
Python syntax is valid
DAG object is created
dag_id is valid
imports work
```

------------------------------------------------------------------------

## 77. If Airflow task fails

Do:

``` text
1. Open DAG
2. Open failed task
3. Open logs
4. Read traceback
5. Identify exception
6. Check environment/configuration
7. Fix
8. Retry
```

Do not start by deleting the DAG.

------------------------------------------------------------------------

## 78. If Kafka command fails

First verify:

``` text
1. Kafka is running
2. Bootstrap server is correct
3. Port is correct
4. Topic exists
5. Correct Kafka script is being used
6. Environment/path is correct
```

Then:

``` bash
kafka-topics.sh --bootstrap-server localhost:9092 --list
```

------------------------------------------------------------------------

## 79. If Kafka consumer receives nothing

Check:

``` text
Topic name
Producer
Consumer group
Offsets
from-beginning behavior
Partition assignment
Broker status
```

Useful:

``` bash
kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --group sensor-group
```

------------------------------------------------------------------------

# PART XV --- MOST IMPORTANT COMMANDS TO MEMORIZE

## 80. Airflow command sheet

``` bash
airflow version

airflow dags list

airflow dags list-import-errors

airflow dags trigger <dag_id>

airflow dags list-runs -d <dag_id>

airflow tasks list <dag_id>

airflow tasks test <dag_id> <task_id> <logical_date>

airflow config list

airflow config get-value core dags_folder

airflow db migrate
```

------------------------------------------------------------------------

## 81. Kafka command sheet

Linux:

``` bash
kafka-topics.sh --bootstrap-server localhost:9092 --list

kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --topic sensor-data \
  --partitions 3 \
  --replication-factor 1

kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --topic sensor-data

kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic sensor-data

kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic sensor-data \
  --from-beginning

kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic sensor-data \
  --group sensor-group

kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --list

kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --group sensor-group
```

Windows:

``` cmd
kafka-topics.bat
kafka-console-producer.bat
kafka-console-consumer.bat
kafka-consumer-groups.bat
```

The exact Kafka script location depends on the installation.

------------------------------------------------------------------------

# PART XVI --- ONE-PAGE MEMORY MAP

## 82. Unit 1

``` text
AIOps
 │
 ├── Data
 │    ├── Logs
 │    ├── Metrics
 │    ├── Events
 │    └── Traces
 │
 ├── Analytics
 │    ├── Rules
 │    ├── Statistics
 │    └── ML
 │
 ├── Anomaly Detection
 │
 ├── Event Correlation
 │
 ├── Root Cause Analysis
 │
 ├── Predictive Maintenance
 │
 └── Automation
      ├── Restart service
      ├── Alert
      └── Remediation
```

## Unit 2

``` text
Data Pipeline
 │
 ├── Kafka
 │    ├── Producer
 │    ├── Topic
 │    ├── Partition
 │    ├── Offset
 │    ├── Consumer
 │    └── Consumer Group
 │
 ├── Airflow
 │    ├── DAG
 │    ├── Task
 │    ├── Scheduler
 │    ├── Executor
 │    ├── Worker
 │    ├── Logs
 │    └── Retry
 │
 ├── Spark
 │    └── Distributed Processing
 │
 ├── Feature Store
 │    ├── Feast
 │    └── Hopsworks
 │
 ├── TFX
 │    └── Production ML Pipeline
 │
 ├── Kubeflow
 │    └── ML Pipelines
 │
 ├── DVC
 │    └── Data/Model Versioning
 │
 └── MLflow
      └── Experiment/Model Tracking
```

------------------------------------------------------------------------

# PART XVII --- 30 RAPID-FIRE MCQs

### 1. AIOps stands for?

**Artificial Intelligence for IT Operations.**

### 2. Which data type is usually numerical?

**Metrics.**

### 3. Which data type is usually text/event records?

**Logs.**

### 4. What detects unusual behavior?

**Anomaly detection.**

### 5. What investigates why an incident happened?

**Root-cause analysis.**

### 6. What predicts possible future failures?

**Predictive analytics/maintenance.**

### 7. Kafka is primarily used for?

**Event streaming.**

### 8. Airflow is primarily used for?

**Workflow orchestration.**

### 9. Spark is primarily used for?

**Distributed data processing.**

### 10. Kafka data is organized into?

**Topics and partitions.**

### 11. Kafka position in a partition?

**Offset.**

### 12. Multiple consumers cooperating?

**Consumer group.**

### 13. What measures how far a consumer is behind?

**Consumer lag.**

### 14. Airflow workflow object?

**DAG.**

### 15. DAG stands for?

**Directed Acyclic Graph.**

### 16. Airflow unit of work?

**Task.**

### 17. Detailed reason for a failed task?

**Task logs.**

### 18. Airflow task after a temporary failure and before another attempt?

**up_for_retry.**

### 19. A task whose dependency failed can become?

**upstream_failed.**

### 20. Airflow stores workflow metadata in?

**Its metadata database.**

### 21. XCom is used for?

**Small inter-task data exchange.**

### 22. Airflow Variable?

**Configuration/value storage.**

### 23. Airflow Connection?

**External-system connection configuration/credentials.**

### 24. Feature store example?

**Feast.**

### 25. Another feature/data platform in the syllabus?

**Hopsworks.**

### 26. TFX is associated with?

**Production ML pipelines using TensorFlow.**

### 27. DVC is associated with?

**Data/model versioning.**

### 28. MLflow is associated with?

**Experiment/model tracking.**

### 29. Kubeflow Pipelines are mainly used for?

**ML workflow pipelines.**

### 30. If producer rate is greater than consumer processing rate?

**Consumer lag can increase.**

------------------------------------------------------------------------

# PART XVIII --- PRACTICAL EXAM: WHAT YOU SHOULD DO

## Scenario A --- Airflow

If the examiner says:

> Create a DAG that runs three tasks sequentially.

Write:

``` text
Task A → Task B → Task C
```

Then code:

``` python
task_a >> task_b >> task_c
```

Verify:

``` bash
airflow dags list
```

Test:

``` bash
airflow tasks list <dag_id>
```

Trigger:

``` bash
airflow dags trigger <dag_id>
```

Then inspect logs.

------------------------------------------------------------------------

## Scenario B --- Kafka

If asked:

> Create a topic and send messages.

Do:

``` bash
kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --topic test-topic \
  --partitions 3 \
  --replication-factor 1
```

Then:

``` bash
kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic test-topic
```

And consume:

``` bash
kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic test-topic \
  --from-beginning
```

------------------------------------------------------------------------

## Scenario C --- Kafka anomaly detection

Architecture:

``` text
Producer
   ↓
Kafka
   ↓
Python Consumer
   ↓
Rule/ML Detector
   ↓
Alert
```

Use:

``` python
if temperature > 80:
    print("ANOMALY")
```

Then upgrade it to Isolation Forest if the examiner asks for ML.

------------------------------------------------------------------------

## Scenario D --- Troubleshooting

If the examiner says:

> The DAG failed.

Do not guess.

``` text
DAG
 ↓
Failed Task
 ↓
Logs
 ↓
Traceback
 ↓
Root Cause
 ↓
Fix
 ↓
Retry
```

If the examiner says:

> Kafka consumer is slow.

Do:

``` text
Consumer group
      ↓
Offsets
      ↓
Lag
      ↓
Consumer logs
      ↓
CPU / memory / network
      ↓
Partitions
```

------------------------------------------------------------------------

# FINAL EXAM CHEAT SHEET

``` text
AIOps
= AI + IT Operations

AIOps lifecycle
= Ingestion → Analytics → Correlation → Automation

Log
= detailed event information

Metric
= numerical measurement

Anomaly
= unusual behavior

RCA
= determine probable cause

Predictive maintenance
= predict failures before they happen

Kafka
= event streaming

Producer
= writes

Consumer
= reads

Topic
= logical stream

Partition
= ordered Kafka log

Offset
= record position

Consumer group
= cooperating consumers

Lag
= log-end offset - consumer/current offset

Airflow
= workflow orchestration

DAG
= Directed Acyclic Graph

Task
= unit of work

Scheduler
= schedules tasks

Executor
= determines execution mechanism

Worker
= executes tasks in worker-based setups

Logs
= troubleshoot failures

Retry
= rerun failed task according to retry policy

XCom
= small task-to-task communication

Spark
= distributed data processing

Feast/Hopsworks
= feature-store/data-platform technologies

TFX
= TensorFlow production ML pipelines

Kubeflow
= ML workflows/pipelines

DVC
= data/model versioning

MLflow
= experiment/model tracking
```

## The most important practical sequence

``` text
                 AIOps EXAM
                     │
          ┌──────────┴──────────┐
          │                     │
       AIRFLOW                KAFKA
          │                     │
        DAG                  Broker
          │                     │
        Task                  Topic
          │                     │
      Dependency            Partition
          │                     │
         Run                  Offset
          │                     │
        Logs                 Consumer
          │                     │
        Retry             Consumer Group
                                │
                               Lag
                                │
                         Anomaly Detection
```

If you can create and troubleshoot this workflow from a blank sandbox:

``` text
Kafka Producer
      ↓
Kafka Topic
      ↓
Kafka Consumer
      ↓
Anomaly Detection
      ↓
Airflow DAG
      ↓
Processing
      ↓
Logs / Metrics
      ↓
Troubleshooting
```

you will have covered the core hands-on material from **Units 1 and 2**
shown in your syllabus.
