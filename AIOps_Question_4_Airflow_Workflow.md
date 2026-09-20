# Question 4 --- Build an AIOps Workflow Using Airflow

## Objective

Create an Apache Airflow DAG representing a basic AIOps workflow.

The workflow must contain:

``` text
Collect Metrics
      ↓
Process Metrics
      ↓
Detect Anomaly
      ↓
Generate Report
```

The DAG must:

-   Use `PythonOperator`.
-   Define all four tasks.
-   Define the correct dependencies.
-   Run tasks in this exact order:

``` text
collect_metrics >> process_metrics >> detect_anomaly >> generate_report
```

------------------------------------------------------------------------

# 1. Prerequisites

You need:

-   Python
-   Apache Airflow
-   A working Airflow environment

Check Python:

``` bash
python --version
```

Check Airflow:

``` bash
airflow version
```

For the environment used in this practical, Airflow should be available.

You do **not** need any additional Python package for `PythonOperator`
if Airflow is already installed.

------------------------------------------------------------------------

# 2. Airflow DAG Folder

If you are using your existing Airflow setup, first check the DAG
folder:

``` bash
echo $AIRFLOW__CORE__DAGS_FOLDER
```

If you previously configured:

``` text
/home/piyush_kumar/airflow-practice-Piyush/dags
```

then the DAG file should be placed there.

You can also check the configured DAG folder with:

``` bash
airflow config get-value core dags_folder
```

------------------------------------------------------------------------

# 3. Create the DAG File

Create:

``` text
aiops_airflow_dag.py
```

Put the following complete code inside it:

``` python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


# ============================================================
# CONFIGURATION
# ============================================================

CPU_THRESHOLD = 80


# ============================================================
# TASK 1 — COLLECT METRICS
# ============================================================

def collect_metrics(**context):

    # Sample server metrics
    cpu = 87
    memory = 65
    response_time = 420

    print("===== Collect Metrics =====")

    print(f"CPU = {cpu}%")
    print(f"Memory = {memory}%")
    print(f"Response Time = {response_time} ms")

    print("Metrics collected successfully")

    # Store metrics in XCom so the next task can use them
    metrics = {
        "cpu": cpu,
        "memory": memory,
        "response_time": response_time
    }

    context["ti"].xcom_push(
        key="server_metrics",
        value=metrics
    )


# ============================================================
# TASK 2 — PROCESS METRICS
# ============================================================

def process_metrics(**context):

    # Get metrics from the previous task
    metrics = context["ti"].xcom_pull(
        task_ids="collect_metrics",
        key="server_metrics"
    )

    print("===== Process Metrics =====")

    print("Processing collected server metrics...")

    print(f"CPU = {metrics['cpu']}%")
    print(f"Memory = {metrics['memory']}%")
    print(
        f"Response Time = "
        f"{metrics['response_time']} ms"
    )

    print("Metrics processed successfully")


# ============================================================
# TASK 3 — DETECT ANOMALY
# ============================================================

def detect_anomaly(**context):

    # Get metrics from collect_metrics
    metrics = context["ti"].xcom_pull(
        task_ids="collect_metrics",
        key="server_metrics"
    )

    cpu = metrics["cpu"]

    print("===== Detect Anomaly =====")

    print(f"CPU = {cpu}%")
    print(f"Threshold = {CPU_THRESHOLD}%")

    if cpu > CPU_THRESHOLD:

        print(
            "Anomaly detected: High CPU usage"
        )

    else:

        print(
            "No anomaly detected"
        )


# ============================================================
# TASK 4 — GENERATE REPORT
# ============================================================

def generate_report():

    print("\n")
    print("===== AIOps Report =====")

    print("Metrics collected successfully")
    print("Metrics processed successfully")
    print("Anomaly detection completed")

    print("========================")


# ============================================================
# DEFAULT ARGUMENTS
# ============================================================

default_args = {
    "owner": "aiops",

    "retries": 1,

    "retry_delay": timedelta(minutes=1)
}


# ============================================================
# CREATE DAG
# ============================================================

with DAG(

    dag_id="aiops_workflow",

    default_args=default_args,

    description="Basic AIOps workflow using Airflow",

    start_date=datetime(2026, 1, 1),

    schedule=None,

    catchup=False,

    tags=["aiops", "monitoring"]
) as dag:


    # ========================================================
    # TASK DEFINITIONS
    # ========================================================

    collect_task = PythonOperator(

        task_id="collect_metrics",

        python_callable=collect_metrics
    )


    process_task = PythonOperator(

        task_id="process_metrics",

        python_callable=process_metrics
    )


    anomaly_task = PythonOperator(

        task_id="detect_anomaly",

        python_callable=detect_anomaly
    )


    report_task = PythonOperator(

        task_id="generate_report",

        python_callable=generate_report
    )


    # ========================================================
    # TASK DEPENDENCIES
    # ========================================================

    collect_task >> process_task >> anomaly_task >> report_task
```

------------------------------------------------------------------------

# 4. Understand the DAG

The four Python functions are:

``` text
collect_metrics()
process_metrics()
detect_anomaly()
generate_report()
```

They become Airflow tasks using:

``` python
PythonOperator
```

The final dependency is:

``` python
collect_task >> process_task >> anomaly_task >> report_task
```

Therefore Airflow executes:

``` text
collect_metrics
       ↓
process_metrics
       ↓
detect_anomaly
       ↓
generate_report
```

------------------------------------------------------------------------

# 5. Task 1 --- collect_metrics

The task generates:

``` text
CPU = 87
Memory = 65
Response Time = 420 ms
```

The code is:

``` python
def collect_metrics(**context):

    cpu = 87
    memory = 65
    response_time = 420
```

It then stores the metrics using Airflow XCom:

``` python
context["ti"].xcom_push(
    key="server_metrics",
    value=metrics
)
```

This allows the following tasks to access the collected data.

------------------------------------------------------------------------

# 6. Task 2 --- process_metrics

The task retrieves the metrics:

``` python
metrics = context["ti"].xcom_pull(
    task_ids="collect_metrics",
    key="server_metrics"
)
```

Then prints:

``` text
===== Process Metrics =====

Processing collected server metrics...

CPU = 87%
Memory = 65%
Response Time = 420 ms

Metrics processed successfully
```

------------------------------------------------------------------------

# 7. Task 3 --- detect_anomaly

The CPU threshold is:

``` python
CPU_THRESHOLD = 80
```

The task checks:

``` python
if cpu > CPU_THRESHOLD:
```

Since:

``` text
87 > 80
```

the output is:

``` text
Anomaly detected: High CPU usage
```

If CPU were 70:

``` text
70 > 80
```

would be false, so it would print:

``` text
No anomaly detected
```

------------------------------------------------------------------------

# 8. Task 4 --- generate_report

The final task prints:

``` text
===== AIOps Report =====
Metrics collected successfully
Metrics processed successfully
Anomaly detection completed
========================
```

This represents the final AIOps workflow report.

------------------------------------------------------------------------

# 9. Put the DAG in Airflow

Copy:

``` text
aiops_airflow_dag.py
```

to your Airflow DAG directory.

For your existing setup:

``` bash
cp aiops_airflow_dag.py ~/airflow-practice-Piyush/dags/
```

Verify:

``` bash
ls ~/airflow-practice-Piyush/dags/
```

You should see:

``` text
aiops_airflow_dag.py
```

------------------------------------------------------------------------

# 10. Verify Airflow Detects the DAG

Run:

``` bash
airflow dags list
```

Look for:

``` text
aiops_workflow
```

You can also filter:

``` bash
airflow dags list | grep aiops
```

Expected:

``` text
aiops_workflow
```

------------------------------------------------------------------------

# 11. Check the DAG Structure

Run:

``` bash
airflow tasks list aiops_workflow
```

You should see:

``` text
collect_metrics
process_metrics
detect_anomaly
generate_report
```

To see the dependency graph:

``` bash
airflow dags show aiops_workflow
```

The dependency should be:

``` text
collect_metrics
       ↓
process_metrics
       ↓
detect_anomaly
       ↓
generate_report
```

------------------------------------------------------------------------

# 12. Test the DAG

The easiest way to test it from the terminal is:

``` bash
airflow dags test aiops_workflow 2026-09-20
```

Airflow should execute the four tasks in order.

Expected output from the task logs will contain:

``` text
===== Collect Metrics =====
CPU = 87%
Memory = 65%
Response Time = 420 ms
Metrics collected successfully
```

Then:

``` text
===== Process Metrics =====
Processing collected server metrics...
CPU = 87%
Memory = 65%
Response Time = 420 ms
Metrics processed successfully
```

Then:

``` text
===== Detect Anomaly =====
CPU = 87%
Threshold = 80%
Anomaly detected: High CPU usage
```

Finally:

``` text
===== AIOps Report =====
Metrics collected successfully
Metrics processed successfully
Anomaly detection completed
========================
```

------------------------------------------------------------------------

# 13. Start the Airflow UI

If your Airflow environment is already initialized, you can start the
API server:

``` bash
airflow api-server --port 8080
```

Then open:

``` text
http://localhost:8080
```

If your existing Airflow setup uses the standalone command, you can also
use:

``` bash
airflow standalone
```

The exact startup command depends on how your Airflow environment was
configured.

------------------------------------------------------------------------

# 14. Airflow UI Workflow

In the Airflow UI:

1.  Find:

``` text
aiops_workflow
```

2.  Open the DAG.
3.  Trigger it.
4.  Open the task graph.
5.  You should see:

``` text
collect_metrics
       ↓
process_metrics
       ↓
detect_anomaly
       ↓
generate_report
```

6.  Open each task to view its logs.

------------------------------------------------------------------------

# 15. Complete Command Sequence

Assuming your Airflow environment is already installed:

### Check Airflow

``` bash
airflow version
```

### Find DAG directory

``` bash
airflow config get-value core dags_folder
```

### Copy DAG

``` bash
cp aiops_airflow_dag.py ~/airflow-practice-Piyush/dags/
```

### Check DAG

``` bash
airflow dags list | grep aiops
```

### Check tasks

``` bash
airflow tasks list aiops_workflow
```

### Show dependency graph

``` bash
airflow dags show aiops_workflow
```

### Test

``` bash
airflow dags test aiops_workflow 2026-09-20
```

### Start UI/API server

``` bash
airflow api-server --port 8080
```

Then visit:

``` text
http://localhost:8080
```

------------------------------------------------------------------------

# 16. If the DAG Does Not Appear

Check the DAG folder:

``` bash
airflow config get-value core dags_folder
```

Then check that the file exists there.

For example:

``` bash
ls ~/airflow-practice-Piyush/dags/
```

You should see:

``` text
aiops_airflow_dag.py
```

Then check for DAG import errors:

``` bash
airflow dags list-import-errors
```

Also check that Airflow can import the file:

``` bash
python ~/airflow-practice-Piyush/dags/aiops_airflow_dag.py
```

If this produces no Python error, the DAG file itself is syntactically
valid.

------------------------------------------------------------------------

# 17. Important Airflow Concepts

## DAG

DAG means:

``` text
Directed Acyclic Graph
```

It defines the workflow and task dependencies.

------------------------------------------------------------------------

## PythonOperator

`PythonOperator` executes a Python function as an Airflow task.

Example:

``` python
PythonOperator(
    task_id="collect_metrics",
    python_callable=collect_metrics
)
```

------------------------------------------------------------------------

## Task ID

Every task has a unique ID:

``` python
task_id="collect_metrics"
```

The four task IDs are:

``` text
collect_metrics
process_metrics
detect_anomaly
generate_report
```

------------------------------------------------------------------------

## Dependency

This:

``` python
collect_task >> process_task
```

means:

``` text
collect_metrics
      ↓
process_metrics
```

The complete dependency is:

``` python
collect_task >> process_task >> anomaly_task >> report_task
```

------------------------------------------------------------------------

# 18. XCom in This Practical

The `collect_metrics` task produces data.

It stores the data:

``` python
context["ti"].xcom_push(
    key="server_metrics",
    value=metrics
)
```

Another task retrieves it:

``` python
context["ti"].xcom_pull(
    task_ids="collect_metrics",
    key="server_metrics"
)
```

The flow is:

``` text
collect_metrics
      |
      | XCom
      ↓
process_metrics
      |
      ↓
detect_anomaly
```

This demonstrates how data can move between Airflow tasks.

------------------------------------------------------------------------

# 19. AIOps Workflow

The practical represents this AIOps lifecycle:

``` text
             SERVER
                |
                ↓
        Collect Metrics
                |
                ↓
        Process Metrics
                |
                ↓
       Detect Anomaly
                |
                ↓
        Generate Report
```

The anomaly rule is:

``` text
CPU > 80%
```

Example:

``` text
CPU = 87%
```

Therefore:

``` text
87 > 80
```

Result:

``` text
Anomaly detected: High CPU usage
```

------------------------------------------------------------------------

# 20. Exam Explanation

> This Airflow DAG implements a basic AIOps monitoring workflow. The
> `collect_metrics` task generates server metrics using a
> `PythonOperator`. The metrics are passed to the processing task using
> XCom. The `detect_anomaly` task checks whether CPU usage is greater
> than 80%. Finally, `generate_report` prints the AIOps report. The
> tasks are executed sequentially using the dependency
> `collect_metrics >> process_metrics >> detect_anomaly >> generate_report`.

------------------------------------------------------------------------

# 21. Quick Revision

### DAG

``` python
with DAG(
    dag_id="aiops_workflow",
    ...
)
```

### PythonOperator

``` python
PythonOperator(
    task_id="collect_metrics",
    python_callable=collect_metrics
)
```

### CPU threshold

``` python
CPU_THRESHOLD = 80
```

### Detection

``` python
if cpu > CPU_THRESHOLD:
    print("Anomaly detected: High CPU usage")
else:
    print("No anomaly detected")
```

### Dependency

``` python
collect_task >> process_task >> anomaly_task >> report_task
```

### Test

``` bash
airflow dags test aiops_workflow 2026-09-20
```

### List DAGs

``` bash
airflow dags list
```

### List tasks

``` bash
airflow tasks list aiops_workflow
```

### Check import errors

``` bash
airflow dags list-import-errors
```

------------------------------------------------------------------------

# 22. Final Expected Workflow

``` text
┌─────────────────────┐
│  collect_metrics    │
│                     │
│ CPU = 87            │
│ Memory = 65         │
│ Response = 420 ms   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  process_metrics    │
│                     │
│ Process metrics     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  detect_anomaly     │
│                     │
│ CPU > 80 ?          │
│ YES → ANOMALY       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  generate_report    │
│                     │
│ ===== AIOps Report  │
│ Metrics collected   │
│ Metrics processed   │
│ Anomaly completed   │
└─────────────────────┘
```
