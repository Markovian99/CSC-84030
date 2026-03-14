# Assignment 2 — Streaming Outlier Detection with Physiological Sensor Data

**CSC 84030 — Big Data Analytics**

---

## Overview

Wearable sensors continuously stream physiological signals—EDA (electrodermal activity), heart rate, skin temperature, and accelerometer data. Detecting anomalies in these streams in real time is a core big data problem that requires algorithms that work on data *as it arrives*, without access to the full dataset.

In this assignment you will build a **streaming outlier detection pipeline** on simulated physiological data from the [WESAD dataset](https://archive.ics.uci.edu/dataset/465/wesad). You will implement and compare **two specific techniques**:

1. **Reservoir Sampling** — a streaming algorithm that maintains a statistically representative sample of data seen so far, used here to estimate a running baseline for z-score outlier detection.
2. **Isolation Forest** — a batch-trained anomaly detection model applied to features extracted from streaming windows.

Both methods are applied inside a **Spark Structured Streaming** pipeline.

---

## Learning Objectives

By completing this assignment you will:

- Implement Reservoir Sampling from scratch and understand why it produces a uniform random sample
- Train an Isolation Forest model offline and apply it to streaming feature windows
- Build a working Spark Structured Streaming pipeline with windowed aggregation and UDF inference
- Critically compare a stateless streaming algorithm against a batch-trained model

---

## Provided Files

| File | Description |
|---|---|
| `assignment2_starter.ipynb` | Starter notebook — complete the TODO cells |
| `spark_streaming_template.py` | Spark Structured Streaming skeleton |
| `preprocess_wesad.py` | Script that converts raw WESAD E4 CSVs → `wesad_S2_1hz.csv` |
| `wesad_S2_1hz.csv` | **Pre-built** — preprocessed 1 Hz dataset for Subject S2, ready to use |

> **You do not need to download the raw WESAD dataset.** `wesad_S2_1hz.csv` is provided and is all you need for the core assignment. `preprocess_wesad.py` is provided for transparency.

---

## Dataset Description

`wesad_S2_1hz.csv` contains 1 Hz physiological signals from Subject S2, with columns:

| Column | Description | Unit |
|---|---|---|
| `timestamp` | Unix timestamp | s |
| `datetime` | Human-readable time | — |
| `eda` | Electrodermal activity | μS |
| `temp` | Skin temperature | °C |
| `hr` | Heart rate | bpm |
| `acc_mag` | Accelerometer magnitude | g |
| `bvp_mean` | Blood volume pulse (downsampled mean) | — |
| `condition` | Ground-truth label: 1=baseline, 2=stress, 3=amusement, 0=transition | — |
| `condition_name` | Human-readable condition | — |
| `seconds_elapsed` | Seconds from session start | s |

---

## Part 1 — Data Exploration (15 points)

In `assignment2_starter.ipynb`, complete the cells in **Section 1**:

1. Load `wesad_S2_1hz.csv` into a pandas DataFrame.
2. Plot each signal (`eda`, `hr`, `temp`, `acc_mag`) as a time series, coloring the background by `condition` (baseline=green, stress=red, amusement=blue). Use `seconds_elapsed` as the x-axis.
3. Compute and display a table of per-condition statistics: mean and standard deviation of each signal.
4. **Answer in a markdown cell:** Which signal shows the most visible difference between baseline and stress? Justify your answer in 2–3 sentences.

---

## Part 2 — Reservoir Sampling (25 points)

Reservoir Sampling (Algorithm R) maintains a fixed-size random sample of a data stream such that at any point, every element seen so far has an equal probability of being in the reservoir.

### 2a — Implement `ReservoirSampler` (15 pts)

In `assignment2_starter.ipynb`, Section 2, implement the `ReservoirSampler` class:

```python
class ReservoirSampler:
    def __init__(self, capacity: int):
        ...

    def update(self, value: float) -> None:
        """Add one value from the stream using Algorithm R."""
        ...

    def sample_mean(self) -> float:
        ...

    def sample_std(self) -> float:
        ...
```

**Requirements:**
- `capacity` is the fixed reservoir size (use 500 for this assignment)
- `update()` must implement Algorithm R exactly — do **not** simply append to a list
- `sample_mean()` and `sample_std()` return statistics over the current reservoir contents

### 2b — Streaming Z-Score Outlier Detection (10 pts)

Using your `ReservoirSampler`, implement a streaming pass over the EDA signal:

```
For each row in the dataset (in time order):
    1. Update the reservoir with the current EDA value
    2. Compute z-score: z = (eda - reservoir.sample_mean()) / reservoir.sample_std()
    3. Flag as outlier if |z| > 2.5
```

Store results in a column `reservoir_outlier` (True/False). Plot the EDA signal with outlier points highlighted in red, and the reservoir mean ± 2.5σ as a shaded band.

**Answer in a markdown cell:**
- How many outliers were detected in the stress condition vs. baseline?
- What is the effect of reservoir `capacity` on detection quality? Try at least two different values (e.g., 100 and 1000).

---

## Part 3 — Isolation Forest (25 points)

### 3a — Feature Extraction (10 pts)

Divide the dataset into **30-second non-overlapping windows** (use `seconds_elapsed // 30` as the window key). For each window compute:

| Feature | Description |
|---|---|
| `mean_eda` | Mean EDA |
| `std_eda` | Standard deviation of EDA |
| `mean_hr` | Mean heart rate |
| `mean_temp` | Mean skin temperature |
| `mean_acc_mag` | Mean accelerometer magnitude |

The result should be a DataFrame with one row per window.

### 3b — Train Isolation Forest (5 pts)

Train an `sklearn` `IsolationForest` using **only windows labeled as baseline (`condition == 1`)**.

```python
from sklearn.ensemble import IsolationForest
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
# Train on baseline windows only
model.fit(baseline_features)
```

### 3c — Apply to All Windows (10 pts)

Apply the trained model to all windows. The model returns `-1` (outlier) or `1` (inlier). Also extract the raw anomaly score with `decision_function()` — lower is more anomalous.

Store results in `iso_outlier` and `iso_score` columns. Plot `iso_score` over time and mark detected outliers.

**Answer in a markdown cell:**
- What fraction of stress windows are detected as outliers? What fraction of baseline windows?
- Does training only on baseline data matter? What would happen if you trained on all data?
- The model may flag more outliers than you expect. Examine the per-feature statistics for baseline vs. stress windows — which feature(s) do you think are most responsible for the detections, and why?

---

## Part 4 — Spark Structured Streaming (15 points)

Open `spark_streaming_template.py`. The windowed aggregation (Section 3) is already provided — it mirrors what you did in Part 3a. Your only task is **Section 4**.

**Section 4 — Outlier Scoring UDF (15 pts):** Fill in the body of `score_window_udf`. Load the `isolation_forest.pkl` you saved in Part 3b and call `model.decision_function()` on the five window features. The docstring in the template walks you through the three lines of code needed.

Run the script and paste the first batch of console output into a markdown cell at the end of your notebook.

---

## Part 5 — Comparison & Analysis (20 pts)

In a markdown cell at the end of your notebook, compare the two approaches across these dimensions:

| Dimension | Reservoir Sampling | Isolation Forest |
|---|---|---|
| Requires training data? | | |
| Updates with new data? | | |
| Inference latency per window | | |
| Precision on stress windows | | |
| False positive rate on baseline | | |

**Answer these questions (2–4 sentences each):**

1. Which method had higher precision for detecting stress windows? Support your answer with specific numbers from Parts 2 and 3.
2. What is the key algorithmic reason Reservoir Sampling works without storing all past data?
3. Reservoir Sampling continuously updates its sample as new data arrives. What happens to your Isolation Forest when the physiological baseline shifts over a long session? What does this reveal about the fundamental trade-off between the two approaches, and how would you fix the Isolation Forest?
4. **Algorithm R probability check (show your calculation):** The full S2 recording has 7,864 rows, of which 611 are labeled `stress`. Your reservoir capacity is 500. After processing all rows, what is the expected number of stress-condition samples in the reservoir? What is the probability that any single stress row ends up in the reservoir?
5. In Part 4, the Isolation Forest model is loaded from disk and called inside a Spark UDF for every window. What is the practical problem with this design in a high-throughput stream, and how would you mitigate it?

---

## Deliverables

Submit a **single ZIP file** containing:

```
lastname_assignment2/
├── assignment2_starter.ipynb    # completed notebook (run all cells before submitting)
└── spark_streaming_template.py  # completed Spark pipeline
```

All written analysis, plots, and answers belong in markdown cells inside the notebook — no separate report is required.

---

## Grading

| Component | Points |
|---|---|
| Part 1 — Data Exploration | 15 |
| Part 2 — Reservoir Sampling | 25 |
| Part 3 — Isolation Forest | 25 |
| Part 4 — Spark Streaming | 15 |
| Part 5 — Comparison & Analysis | 20 |
| **Total** | **100** |

---

## Practical Notes

- The entire assignment can run on your laptop — no cluster required. Spark runs in local mode.
- Required packages: `pandas`, `numpy`, `matplotlib`, `scikit-learn`, `pyspark`
- Spark requires **Java 17 or later**. If you see a Java version error, install it and ensure `JAVA_HOME` points to it.
- Run all notebook cells top-to-bottom before submitting — the grader will not re-run partial notebooks.
- `wesad_S2_1hz.csv` has 7,864 rows (~131 minutes of data at 1 Hz).
