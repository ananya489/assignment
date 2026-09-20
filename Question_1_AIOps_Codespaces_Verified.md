# Question 1 — AIOps Log Anomaly Detection (GitHub Codespaces)

## Validation
The solution meets the requirements. It creates/reads 20 server-log records, calculates descriptive statistics, flags CPU values strictly greater than 90%, prints anomalous rows, and saves a graph. The intended sample produces exactly 3 anomalies: 10:05 (95%), 10:12 (97%), and 10:18 (92%).

## 1. Codespaces commands

Run from the repository root:

```bash
cd /workspaces/assignment
python --version
python -m pip install pandas matplotlib
```

Create `aiops_q1.py` in `/workspaces/assignment` and paste the code below.

Run it:

```bash
cd /workspaces/assignment
python aiops_q1.py
```

If your environment uses `python3`:

```bash
python3 --version
python3 -m pip install pandas matplotlib
python3 aiops_q1.py
```

## 2. Complete code — `aiops_q1.py`

```python
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Save graph reliably in a headless Codespaces terminal
import matplotlib.pyplot as plt

DATASET_FILE = "server_logs.csv"
CPU_THRESHOLD = 90


def create_sample_dataset():
    data = {
        "Timestamp": [
            "10:00", "10:01", "10:02", "10:03", "10:04",
            "10:05", "10:06", "10:07", "10:08", "10:09",
            "10:10", "10:11", "10:12", "10:13", "10:14",
            "10:15", "10:16", "10:17", "10:18", "10:19"
        ],
        "CPU": [
            45, 52, 48, 55, 61,
            95, 58, 63, 50, 67,
            59, 62, 97, 54, 60,
            57, 65, 69, 92, 56
        ],
        "Memory": [
            50, 52, 51, 55, 57,
            70, 54, 56, 53, 59,
            55, 58, 72, 54, 57,
            56, 60, 62, 74, 55
        ],
        "Response_Time": [
            120, 130, 115, 140, 150,
            420, 135, 145, 125, 160,
            140, 155, 450, 130, 145,
            135, 150, 165, 390, 125
        ]
    }

    df = pd.DataFrame(data)
    df.to_csv(DATASET_FILE, index=False)
    print(f"Sample dataset created: {DATASET_FILE}")
    return df


def load_dataset():
    if os.path.exists(DATASET_FILE):
        print(f"Reading existing dataset: {DATASET_FILE}")
        return pd.read_csv(DATASET_FILE)

    print("Dataset not found. Creating sample dataset...")
    return create_sample_dataset()


def main():
    print("\\n==============================================")
    print("      AIOps Log Anomaly Detection")
    print("==============================================")

    df = load_dataset()

    # Validate expected columns and numeric metric values
    required = ["Timestamp", "CPU", "Memory", "Response_Time"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    for col in ["CPU", "Memory", "Response_Time"]:
        df[col] = pd.to_numeric(df[col], errors="raise")

    print("\\n===== BASIC STATISTICS =====")
    print(df[["CPU", "Memory", "Response_Time"]].describe())

    # Threshold-based anomaly detection
    df["Status"] = df["CPU"].apply(
        lambda cpu: "ANOMALY" if cpu > CPU_THRESHOLD else "NORMAL"
    )
    anomalies = df[df["Status"] == "ANOMALY"]

    print("\\n===== ANOMALY DETECTION =====")
    print(f"Total records: {len(df)}")
    print(f"Anomalies detected: {len(anomalies)}")
    print("\\nTimestamp       CPU       Status")

    for _, row in anomalies.iterrows():
        print(f"{row['Timestamp']:<15}{row['CPU']}%       {row['Status']}")

    print("\\n===== COMPLETE ANOMALOUS RECORDS =====")
    if anomalies.empty:
        print("No anomalies found.")
    else:
        print(anomalies.to_string(index=False))

    output_csv = "server_logs_with_status.csv"
    df.to_csv(output_csv, index=False)
    print(f"\\nResults saved as: {output_csv}")

    # Plot CPU values, threshold, and anomalous points
    plt.figure(figsize=(12, 6))
    plt.plot(df["Timestamp"], df["CPU"], marker="o", label="CPU Usage")
    plt.axhline(
        y=CPU_THRESHOLD, linestyle="--", label=f"Threshold ({CPU_THRESHOLD}%)"
    )
    plt.scatter(
        anomalies["Timestamp"], anomalies["CPU"], s=100, label="Anomaly"
    )
    plt.title("AIOps CPU Usage and Anomalies")
    plt.xlabel("Timestamp")
    plt.ylabel("CPU Usage (%)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    graph_file = "aiops_anomaly_graph.png"
    plt.savefig(graph_file, dpi=150)
    plt.close()
    print(f"Graph saved as: {graph_file}")


if __name__ == "__main__":
    main()
```

## 3. Verify expected output

With the sample dataset, the anomaly summary should be:

```text
Total records: 20
Anomalies detected: 3

Timestamp       CPU       Status
10:05           95%       ANOMALY
10:12           97%       ANOMALY
10:18           92%       ANOMALY
```

The statistics table will also print. The exact formatting can vary by pandas version.

## 4. Verify generated files in Codespaces

```bash
ls -l aiops_q1.py server_logs.csv server_logs_with_status.csv aiops_anomaly_graph.png
```

Open `aiops_anomaly_graph.png` from the VS Code Explorer to view the graph. The graph includes CPU usage, the 90% threshold, and highlighted anomalies.

To verify the anomaly rows directly from the saved results:

```bash
python -c "import pandas as pd; df=pd.read_csv('server_logs_with_status.csv'); print(df[df['Status']=='ANOMALY'][['Timestamp','CPU','Status']].to_string(index=False))"
```

To verify counts:

```bash
python -c "import pandas as pd; df=pd.read_csv('server_logs_with_status.csv'); print('Total records:', len(df)); print('Anomalies detected:', (df['Status']=='ANOMALY').sum())"
```

Expected:

```text
Total records: 20
Anomalies detected: 3
```

## 5. Common issue: existing CSV

The program intentionally reads `server_logs.csv` if it already exists. If the counts do not match the expected output, remove the old sample CSV and rerun to regenerate the provided data:

```bash
cd /workspaces/assignment
rm server_logs.csv
python aiops_q1.py
```

Only remove it if you do not need the existing dataset.

## 6. Git commit and push

```bash
cd /workspaces/assignment
git status
git add aiops_q1.py server_logs.csv server_logs_with_status.csv aiops_anomaly_graph.png
git commit -m "Complete Question 1 AIOps log anomaly detection"
git push
```

If you prefer to commit only source code (and not generated outputs), use:

```bash
git add aiops_q1.py
git commit -m "Add Question 1 AIOps anomaly detection"
git push
```

## Checklist

- [ ] Python and libraries available
- [ ] `aiops_q1.py` runs without errors
- [ ] Total records = 20
- [ ] Anomalies detected = 3
- [ ] Correct timestamps/CPU values printed
- [ ] CSV with status saved
- [ ] Graph PNG saved and opened for inspection
- [ ] Changes committed and pushed
