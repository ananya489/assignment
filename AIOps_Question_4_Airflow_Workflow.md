Question 4 — Build an AIOps Workflow using Airflow

We will do this using your GitHub Codespace + Python Airflow DAG file.

The workflow will be:

collect_metrics
       ↓
process_metrics
       ↓
detect_anomaly
       ↓
generate_report
1. Project Structure

Inside your Codespace, use:

aiops-airflow/
└── dags/
    └── aiops_workflow.py

Create the folders:

mkdir -p aiops-airflow/dags
cd aiops-airflow
2. Airflow Installation

If Airflow is already installed in your Codespace, skip this step.

Check:

airflow version

You should get an Airflow version such as:

3.1.0

If Airflow is not installed, install it according to the Python version and Airflow constraints used by your Codespace environment.

3. Create the DAG File

Create:

dags/aiops_workflow.py

Use this complete code:

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


CPU_THRESHOLD = 80


# Task 1
def collect_metrics(**context):

    cpu = 87
    memory = 65
    response_time = 420

    print("===== Collect Metrics =====")
    print(f"CPU = {cpu}%")
    print(f"Memory = {memory}%")
    print(f"Response Time = {response_time} ms")

    metrics = {
        "cpu": cpu,
        "memory": memory,
        "response_time": response_time
    }

    context["ti"].xcom_push(
        key="server_metrics",
        value=metrics
    )

    print("Metrics collected successfully")


# Task 2
def process_metrics(**context):

    metrics = context["ti"].xcom_pull(
        task_ids="collect_metrics",
        key="server_metrics"
    )

    print("===== Process Metrics =====")
    print(f"CPU = {metrics['cpu']}%")
    print(f"Memory = {metrics['memory']}%")
    print(f"Response Time = {metrics['response_time']} ms")

    print("Metrics processed successfully")


# Task 3
def detect_anomaly(**context):

    metrics = context["ti"].xcom_pull(
        task_ids="collect_metrics",
        key="server_metrics"
    )

    cpu = metrics["cpu"]

    print("===== Detect Anomaly =====")
    print(f"CPU = {cpu}%")
    print(f"Threshold = {CPU_THRESHOLD}%")

    if cpu > CPU_THRESHOLD:
        print("Anomaly detected: High CPU usage")
    else:
        print("No anomaly detected")


# Task 4
def generate_report():

    print()
    print("===== AIOps Report =====")
    print("Metrics collected successfully")
    print("Metrics processed successfully")
    print("Anomaly detection completed")
    print("========================")


default_args = {
    "owner": "aiops",
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}


with DAG(
    dag_id="aiops_workflow",
    default_args=default_args,
    description="Basic AIOps workflow using Airflow",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["aiops", "monitoring"]
) as dag:

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

    collect_task >> process_task >> anomaly_task >> report_task
4. Important Part — Task Dependencies

This line is the most important part of the question:

collect_task >> process_task >> anomaly_task >> report_task

It creates:

collect_metrics
       ↓
process_metrics
       ↓
detect_anomaly
       ↓
generate_report

Therefore Airflow will execute the tasks in exactly this order.

5. Put the DAG in Airflow's DAG Folder

Check your Airflow DAG folder:

airflow config get-value core dags_folder

It will return something similar to:

/home/codespace/airflow/dags

or:

/home/<user>/airflow/dags

Copy your DAG there if necessary.

For example:

cp aiops-airflow/dags/aiops_workflow.py ~/airflow/dags/

Then verify:

airflow dags list

Look for:

aiops_workflow
6. Check for DAG Import Errors

Run:

airflow dags list-import-errors

If there are no errors, your DAG has loaded correctly.

You can also check the tasks:

airflow tasks list aiops_workflow

Expected tasks:

collect_metrics
process_metrics
detect_anomaly
generate_report
7. Check the DAG Structure

Run:

airflow dags show aiops_workflow

The dependency should represent:

collect_metrics
        ↓
process_metrics
        ↓
detect_anomaly
        ↓
generate_report
8. Test the DAG

For your practical, the easiest way to test the complete workflow is:

airflow dags test aiops_workflow 2026-09-20

Airflow will execute the tasks.

9. Expected Output
Task 1 — Collect Metrics
===== Collect Metrics =====
CPU = 87%
Memory = 65%
Response Time = 420 ms
Metrics collected successfully
Task 2 — Process Metrics
===== Process Metrics =====
CPU = 87%
Memory = 65%
Response Time = 420 ms
Metrics processed successfully
Task 3 — Detect Anomaly

Because:

CPU = 87
CPU threshold = 80

and:

87 > 80

the output is:

===== Detect Anomaly =====
CPU = 87%
Threshold = 80%
Anomaly detected: High CPU usage
Task 4 — Generate Report
===== AIOps Report =====
Metrics collected successfully
Metrics processed successfully
Anomaly detection completed
========================
10. How XCom Is Used

This part:

context["ti"].xcom_push(
    key="server_metrics",
    value=metrics
)

stores the collected metrics in Airflow's XCom.

The next task retrieves them:

metrics = context["ti"].xcom_pull(
    task_ids="collect_metrics",
    key="server_metrics"
)

So the data flow is:

collect_metrics
      │
      │ XCom
      ▼
process_metrics
      │
      │ XCom
      ▼
detect_anomaly

For this basic practical, XCom is a simple way to pass the generated metrics between tasks.

11. Important Airflow Concepts
DAG

DAG means:

Directed Acyclic Graph

It defines the workflow and task dependencies.

Our DAG ID is:

aiops_workflow
PythonOperator

We use:

PythonOperator

to execute Python functions as Airflow tasks.

For example:

collect_task = PythonOperator(
    task_id="collect_metrics",
    python_callable=collect_metrics
)
task_id

Each task needs a unique ID.

We have:

collect_metrics
process_metrics
detect_anomaly
generate_report
Dependency Operator

This:

>>

means runs after.

For example:

collect_task >> process_task

means:

collect_task
     ↓
process_task
12. Complete Execution Flow
                    AIRFLOW
                       │
                       ▼
              ┌─────────────────┐
              │ Collect Metrics  │
              │ CPU = 87%        │
              │ Memory = 65%     │
              │ Response = 420ms │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Process Metrics  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Detect Anomaly   │
              │ CPU > 80 ?       │
              └────────┬────────┘
                       │
                  YES  │
                       ▼
          Anomaly detected:
          High CPU usage
                       │
                       ▼
              ┌─────────────────┐
              │ Generate Report  │
              └─────────────────┘
13. Exact Commands to Remember

For the exam:

Check Airflow
airflow version
Check DAG folder
airflow config get-value core dags_folder
List DAGs
airflow dags list
Check tasks
airflow tasks list aiops_workflow
Check import errors
airflow dags list-import-errors
Show DAG structure
airflow dags show aiops_workflow
Test DAG
airflow dags test aiops_workflow 2026-09-20
14. Final Exam Answer

If the examiner asks:

Create an Apache Airflow DAG representing a basic AIOps workflow.

Remember these four tasks:

collect_metrics
        ↓
process_metrics
        ↓
detect_anomaly
        ↓
generate_report

And the most important dependency line is:

collect_task >> process_task >> anomaly_task >> report_task

The DAG uses:

from airflow import DAG
from airflow.operators.python import PythonOperator

The anomaly condition is:

if cpu > 80:
    print("Anomaly detected: High CPU usage")
else:
    print("No anomaly detected")

And the final report is:

===== AIOps Report =====
Metrics collected successfully
Metrics processed successfully
Anomaly detection completed
========================

Q4 is complete when aiops_workflow loads successfully in Airflow and the four tasks execute in the required order.
