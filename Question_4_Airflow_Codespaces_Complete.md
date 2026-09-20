# Question 4 — Apache Airflow AIOps Workflow
## GitHub Codespaces Practical

This practical creates an Airflow DAG to automate an AIOps workflow with four sequential tasks:

1. Collect system metrics
2. Process metrics
3. Detect anomalies
4. Generate a report

The DAG uses `PythonOperator` and XCom to pass data between tasks. With the sample CPU usage of 87%, the workflow should detect an anomaly.

---

## 1. Create the DAG directory

Run from the repository root:

```bash
cd /workspaces/assignment
mkdir -p DAG
```

## 2. Create the DAG file

Create `DAG/aiops_workflow.py` and add:

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def collect_metrics(**context):
    metrics = {
        "cpu": 87,
        "memory": 65,
        "response_time": 420
    }
    context["ti"].xcom_push(key="metrics", value=metrics)
    print("Collected metrics:", metrics)


def process_metrics(**context):
    metrics = context["ti"].xcom_pull(
        task_ids="collect_metrics",
        key="metrics"
    )
    processed = {key: value for key, value in metrics.items()}
    context["ti"].xcom_push(key="processed_metrics", value=processed)
    print("Processed metrics:", processed)


def detect_anomaly(**context):
    metrics = context["ti"].xcom_pull(
        task_ids="process_metrics",
        key="processed_metrics"
    )

    anomaly = metrics["cpu"] > 80
    context["ti"].xcom_push(key="anomaly", value=anomaly)
    print("Anomaly detected:", anomaly)


def generate_report(**context):
    metrics = context["ti"].xcom_pull(
        task_ids="process_metrics",
        key="processed_metrics"
    )
    anomaly = context["ti"].xcom_pull(
        task_ids="detect_anomaly",
        key="anomaly"
    )

    report = {
        "metrics": metrics,
        "anomaly_detected": anomaly,
        "status": "ALERT" if anomaly else "NORMAL"
    }

    print("Final AIOps Report:", report)


with DAG(
    dag_id="aiops_workflow",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["AIOps", "monitoring"]
) as dag:

    task_collect = PythonOperator(
        task_id="collect_metrics",
        python_callable=collect_metrics
    )

    task_process = PythonOperator(
        task_id="process_metrics",
        python_callable=process_metrics
    )

    task_detect = PythonOperator(
        task_id="detect_anomaly",
        python_callable=detect_anomaly
    )

    task_report = PythonOperator(
        task_id="generate_report",
        python_callable=generate_report
    )

    task_collect >> task_process >> task_detect >> task_report
```

## 3. Create the Airflow Docker Compose file

Create `docker-compose-airflow.yml` in `/workspaces/assignment`:

```yaml
services:
  airflow:
    image: apache/airflow:2.10.5-python3.11
    container_name: airflow
    command: standalone
    ports:
      - "8080:8080"
    environment:
      AIRFLOW__CORE__EXECUTOR: SequentialExecutor
      AIRFLOW__CORE__LOAD_EXAMPLES: "False"
    volumes:
      - ./DAG:/opt/airflow/dags
```

## 4. Start Airflow

```bash
cd /workspaces/assignment
docker compose -f docker-compose-airflow.yml up -d
```

Check container status:

```bash
docker compose -f docker-compose-airflow.yml ps
```

View logs and locate the standalone login credentials:

```bash
docker compose -f docker-compose-airflow.yml logs -f airflow
```

## 5. Open the Airflow UI in Codespaces

1. Open the **Ports** tab in Codespaces.
2. Open forwarded port `8080` (make it public only if your environment requires it; otherwise keep it private).
3. Sign in using the credentials shown in the Airflow logs.
4. Find the DAG `aiops_workflow`.
5. Unpause it if needed, then trigger it manually.

## 6. Verify execution

Confirm these tasks all succeed, in order:

```text
collect_metrics >> process_metrics >> detect_anomaly >> generate_report
```

Open the task logs and verify the metrics and final report.

Expected result with the sample values:

```text
Anomaly detected: True
Final AIOps Report: {
    'metrics': {'cpu': 87, 'memory': 65, 'response_time': 420},
    'anomaly_detected': True,
    'status': 'ALERT'
}
```

## 7. Stop Airflow

```bash
cd /workspaces/assignment
docker compose -f docker-compose-airflow.yml down
```

## 8. Commit and push to GitHub

Commit the DAG:

```bash
cd /workspaces/assignment
git add DAG/aiops_workflow.py
git commit -m "Add Question 4 AIOps Airflow DAG"
git push
```

Commit the Docker Compose file:

```bash
git add docker-compose-airflow.yml
git commit -m "Add Docker Compose setup for Airflow"
git push
```

## Final checklist

- [ ] `DAG/aiops_workflow.py` created
- [ ] Airflow container is running
- [ ] Airflow UI opened on port `8080`
- [ ] All four DAG tasks succeeded
- [ ] Anomaly result is `True` for CPU usage of 87%
- [ ] DAG and Compose file committed and pushed
