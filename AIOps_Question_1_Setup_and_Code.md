# Question 1 --- AIOps Log Anomaly Detection

## Objective

Create a Python program that:

1.  Creates or reads a server log dataset.
2.  Contains:
    -   Timestamp
    -   CPU Usage
    -   Memory Usage
    -   Response Time
3.  Calculates basic statistics.
4.  Detects anomalies using a simple threshold.
5.  Prints anomalous records.
6.  Displays a graph containing metric values and anomalies.

Expected result:

``` text
Total records: 20
Anomalies detected: 3

Timestamp       CPU       Status
10:05           95%       ANOMALY
10:12           97%       ANOMALY
10:18           92%       ANOMALY
```

------------------------------------------------------------------------

# 1. Required Software

You need Python 3.x.

Check Python:

``` bash
python --version
```

Install the required libraries:

``` bash
python -m pip install pandas matplotlib
```

If `python` does not work on Windows, try:

``` bash
py --version
py -m pip install pandas matplotlib
```

------------------------------------------------------------------------

# 2. Create the Python File

Create a file named:

``` text
aiops_q1.py
```

Put the following code inside it.

``` python
import pandas as pd
import matplotlib.pyplot as plt
import os


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_FILE = "server_logs.csv"

# CPU greater than 90% will be treated as an anomaly
CPU_THRESHOLD = 90


# ============================================================
# 1. CREATE SAMPLE DATASET
# ============================================================

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


# ============================================================
# 2. READ DATASET
# ============================================================

def load_dataset():

    if os.path.exists(DATASET_FILE):

        print(f"Reading existing dataset: {DATASET_FILE}")

        return pd.read_csv(DATASET_FILE)

    else:

        print("Dataset not found.")
        print("Creating sample dataset...")

        return create_sample_dataset()


# ============================================================
# 3. MAIN AIOps ANALYSIS
# ============================================================

def main():

    print("\n==============================================")
    print("      AIOps Log Anomaly Detection")
    print("==============================================")

    # Load or create dataset
    df = load_dataset()

    # --------------------------------------------------------
    # Basic statistics
    # --------------------------------------------------------

    print("\n===== BASIC STATISTICS =====")

    print(
        df[
            ["CPU", "Memory", "Response_Time"]
        ].describe()
    )

    # --------------------------------------------------------
    # Threshold-based anomaly detection
    # --------------------------------------------------------

    df["Status"] = df["CPU"].apply(
        lambda cpu:
        "ANOMALY"
        if cpu > CPU_THRESHOLD
        else "NORMAL"
    )

    # Get anomalous records
    anomalies = df[
        df["Status"] == "ANOMALY"
    ]

    # --------------------------------------------------------
    # Print result
    # --------------------------------------------------------

    print("\n===== ANOMALY DETECTION =====")

    print(f"Total records: {len(df)}")

    print(
        f"Anomalies detected: "
        f"{len(anomalies)}"
    )

    print("\nTimestamp       CPU       Status")

    for _, row in anomalies.iterrows():

        print(
            f"{row['Timestamp']:<15}"
            f"{row['CPU']}%       "
            f"{row['Status']}"
        )

    # --------------------------------------------------------
    # Print complete anomalous records
    # --------------------------------------------------------

    print("\n===== ANOMALOUS RECORDS =====")

    print(
        anomalies.to_string(index=False)
    )

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    df.to_csv(
        "server_logs_with_status.csv",
        index=False
    )

    print(
        "\nResults saved as: "
        "server_logs_with_status.csv"
    )

    # --------------------------------------------------------
    # Plot graph
    # --------------------------------------------------------

    plt.figure(figsize=(12, 6))

    # CPU usage line
    plt.plot(
        df["Timestamp"],
        df["CPU"],
        marker="o",
        label="CPU Usage"
    )

    # Threshold line
    plt.axhline(
        y=CPU_THRESHOLD,
        linestyle="--",
        label="Anomaly Threshold"
    )

    # Anomaly points
    plt.scatter(
        anomalies["Timestamp"],
        anomalies["CPU"],
        s=100,
        label="Anomaly"
    )

    plt.title(
        "AIOps CPU Usage and Anomalies"
    )

    plt.xlabel("Timestamp")

    plt.ylabel(
        "CPU Usage (%)"
    )

    plt.xticks(
        rotation=45
    )

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    # Save graph
    plt.savefig(
        "aiops_anomaly_graph.png"
    )

    print(
        "Graph saved as: "
        "aiops_anomaly_graph.png"
    )

    # Display graph
    plt.show()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
```

------------------------------------------------------------------------

# 3. How to Run

Open a terminal in the folder containing `aiops_q1.py`.

Run:

``` bash
python aiops_q1.py
```

On Windows, you can also use:

``` bash
py aiops_q1.py
```

------------------------------------------------------------------------

# 4. If You Already Have a Dataset

You do **not** have to download a dataset for this question.

The program automatically creates:

``` text
server_logs.csv
```

if the file does not already exist.

The required CSV format is:

``` csv
Timestamp,CPU,Memory,Response_Time
10:00,45,50,120
10:01,52,52,130
10:02,48,51,115
10:03,55,55,140
10:04,61,57,150
10:05,95,70,420
```

The column names must be:

``` text
Timestamp
CPU
Memory
Response_Time
```

If you already have a dataset, put it in the same folder and name it:

``` text
server_logs.csv
```

Then simply run:

``` bash
python aiops_q1.py
```

The program will read your CSV instead of creating a new one.

------------------------------------------------------------------------

# 5. If Your Dataset Has Different Column Names

For example, your CSV might contain:

``` text
timestamp,cpu_usage,memory_usage,response_time
```

Then change the Python code accordingly.

For example:

``` python
df = df.rename(columns={
    "timestamp": "Timestamp",
    "cpu_usage": "CPU",
    "memory_usage": "Memory",
    "response_time": "Response_Time"
})
```

Place this immediately after:

``` python
df = load_dataset()
```

------------------------------------------------------------------------

# 6. Where to Get a Dataset

For this practical, a downloaded dataset is **not required**. The sample
dataset generated by the program is enough.

If your teacher specifically requires a real dataset, you can search for
server/system monitoring datasets on:

-   Kaggle
-   UCI Machine Learning Repository
-   Google Dataset Search

Look for datasets containing CPU utilization, memory utilization,
response time, server metrics, or system logs.

The dataset does not need to exactly match the question. You can map its
columns to:

``` text
Timestamp
CPU
Memory
Response_Time
```

Before using an external dataset, check:

1.  It contains enough records.
2.  CPU values are numeric percentages.
3.  Memory values are numeric percentages.
4.  Response time is numeric.
5.  A timestamp/time column is available or can be created.

------------------------------------------------------------------------

# 7. Files Generated by the Program

After running:

``` bash
python aiops_q1.py
```

you will have:

``` text
aiops_q1.py
server_logs.csv
server_logs_with_status.csv
aiops_anomaly_graph.png
```

Meaning:

  File                            Purpose
  ------------------------------- ------------------------------------
  `aiops_q1.py`                   Python program
  `server_logs.csv`               Original/sample dataset
  `server_logs_with_status.csv`   Dataset with NORMAL/ANOMALY status
  `aiops_anomaly_graph.png`       Anomaly graph

------------------------------------------------------------------------

# 8. Expected Output

You should get:

``` text
==============================================
      AIOps Log Anomaly Detection
==============================================

Reading existing dataset: server_logs.csv

===== BASIC STATISTICS =====

             CPU     Memory  Response_Time
count  20.000000  20.000000      20.000000
...

===== ANOMALY DETECTION =====

Total records: 20
Anomalies detected: 3

Timestamp       CPU       Status
10:05           95%       ANOMALY
10:12           97%       ANOMALY
10:18           92%       ANOMALY
```

A graph will also open showing:

-   CPU usage
-   The 90% threshold
-   The three anomalous points

------------------------------------------------------------------------

# 9. Important Code for the Exam

### Threshold

``` python
CPU_THRESHOLD = 90
```

### Detect anomaly

``` python
df["Status"] = df["CPU"].apply(
    lambda cpu:
    "ANOMALY" if cpu > CPU_THRESHOLD else "NORMAL"
)
```

### Get anomalies

``` python
anomalies = df[
    df["Status"] == "ANOMALY"
]
```

### Count anomalies

``` python
len(anomalies)
```

### Basic statistics

``` python
df[["CPU", "Memory", "Response_Time"]].describe()
```

### Plot

``` python
plt.plot(df["Timestamp"], df["CPU"])
plt.scatter(
    anomalies["Timestamp"],
    anomalies["CPU"]
)
```

------------------------------------------------------------------------

# 10. One-Line Exam Explanation

> The program reads or generates server log metrics, calculates
> descriptive statistics, applies a CPU threshold of 90% for anomaly
> detection, prints anomalous records, and visualizes CPU usage and
> anomalies using Matplotlib.

------------------------------------------------------------------------

# 11. Quick Run Checklist

``` text
1. Create aiops_q1.py
        ↓
2. Install libraries
        ↓
   python -m pip install pandas matplotlib
        ↓
3. Run
        ↓
   python aiops_q1.py
        ↓
4. Check:
   Total records: 20
   Anomalies detected: 3
        ↓
5. Check graph:
   aiops_anomaly_graph.png
```
