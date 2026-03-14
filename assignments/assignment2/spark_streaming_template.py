"""
WESAD Outlier Detection — PySpark Structured Streaming Template
===============================================================

Assignment 2 | Big Data Analytics

OVERVIEW
--------
This script builds a real-time stress-detection pipeline on top of the
WESAD (Wearable Stress and Affect Detection) dataset.  Because the raw
dataset is stored in files, a helper function simulates a live sensor
stream by writing chunks of a preprocessed CSV into a "stream inbox"
directory that Spark monitors.

HOW TO RUN
----------
1. Preprocess the WESAD data and save it as a single CSV whose columns
   match the schema defined in Section 1 (timestamp, datetime, eda,
   temp, hr, acc_mag, bvp_mean, condition, condition_name,
   seconds_elapsed).

2. Adjust the paths in Section 1 to point at your preprocessed CSV and
   the directories you want to use for the inbox and output.

3. Run the script from a terminal (or inside a Docker container that has
   PySpark installed):

       python spark_streaming_template.py

   The simulation thread will start feeding chunks into INBOX_DIR while
   the Spark streaming query reads and processes them.

4. Interrupt with Ctrl-C when you have seen enough output.  Spark will
   shut down cleanly.

STRUCTURE
---------
Section 1  — Configuration            (PROVIDED)
Section 2  — Stream Setup             (PROVIDED)
Section 3  — Feature Window Aggregation  (PROVIDED)
Section 4  — Outlier Scoring UDF      (TODO — students complete one function)
Section 5  — Apply UDF and Flag Outliers (PROVIDED)
Section 6  — Stream Simulation Helper (PROVIDED)
Section 7  — Output Sink              (PROVIDED - prints to console, but you can change this to write to files or a database if you like)
Section 8  — Main Execution           (PROVIDED)
"""

# ── Imports ───────────────────────────────────────────────────────────────────

import os
import time
import shutil
import threading
import pickle

# Ensure Java 17 (installed via conda or other means) takes precedence over any system Java
_jvm = os.path.join(os.path.dirname(os.path.dirname(os.__file__)), "lib", "jvm")
if os.path.isdir(_jvm):
    os.environ.setdefault("JAVA_HOME", _jvm)

import pandas as pd

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    LongType,
    IntegerType,
    FloatType,
    TimestampType,
)
from pyspark.sql.functions import (
    col,
    window,
    mean,
    stddev,
    udf,
    to_timestamp,
)


# =============================================================================
# SECTION 1 — Configuration
# =============================================================================
# PROVIDED — no changes required here, but review the paths and adjust if needed.

# PROVIDED: create (or retrieve) the SparkSession
spark = (
    SparkSession.builder
    .appName("WESAD_Outlier_Detection")
    # Allow Spark to process late data for up to 30 seconds
    .config("spark.sql.streaming.schemaInference", "false")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

# PROVIDED: schema for the preprocessed WESAD CSV
WESAD_SCHEMA = StructType([
    StructField("timestamp",        DoubleType(),  True),  # Unix timestamp (float)
    StructField("datetime",         StringType(),  True),  # ISO-8601 string
    StructField("eda",              DoubleType(),  True),  # Electrodermal activity (µS)
    StructField("temp",             DoubleType(),  True),  # Skin temperature (°C)
    StructField("hr",               DoubleType(),  True),  # Heart rate (bpm)
    StructField("acc_mag",          DoubleType(),  True),  # Accelerometer magnitude
    StructField("bvp_mean",         DoubleType(),  True),  # Blood volume pulse mean
    StructField("condition",        IntegerType(), True),  # Numeric condition label
    StructField("condition_name",   StringType(),  True),  # "baseline" / "stress" / "amusement"
    StructField("seconds_elapsed",  DoubleType(),  True),  # Seconds from start of recording
])

# PROVIDED: directory paths — update these to match your local setup
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
INBOX_DIR   = os.path.join(BASE_DIR, "stream_inbox")    # Spark reads from here
OUTPUT_DIR  = os.path.join(BASE_DIR, "stream_output")   # Spark writes results here
CHECKPOINT  = os.path.join(BASE_DIR, "stream_checkpoint")

# PROVIDED: path to the preprocessed CSV (single file or directory of part files)
PREPROCESSED_CSV = os.path.join(BASE_DIR, "wesad_S2_1hz.csv")

# PROVIDED: outlier threshold — windows with score above this are flagged
OUTLIER_THRESHOLD = 0.0   # IsolationForest decision boundary: scores above 0 are outliers

# PROVIDED: path to an optional pre-trained IsolationForest model (pickle)
MODEL_PATH = os.path.join(BASE_DIR, "isolation_forest.pkl")

# PROVIDED: ensure directories exist and inbox is empty before starting
for d in [INBOX_DIR, OUTPUT_DIR, CHECKPOINT]:
    os.makedirs(d, exist_ok=True)

# Clear the inbox so previous runs do not interfere
for f in os.listdir(INBOX_DIR):
    fp = os.path.join(INBOX_DIR, f)
    if os.path.isfile(fp):
        os.remove(fp)


# =============================================================================
# SECTION 2 — Stream Setup
# =============================================================================
# PROVIDED — reads a streaming CSV source from INBOX_DIR.

# PROVIDED: create a streaming DataFrame that watches INBOX_DIR for new CSV files
raw_stream = (
    spark.readStream
    .format("csv")
    .option("header", "true")
    .option("maxFilesPerTrigger", 1)   # process one chunk at a time
    .schema(WESAD_SCHEMA)
    .load(INBOX_DIR)
)

# PROVIDED: parse the Unix timestamp float into a proper Spark TimestampType
#   multiplied by 1e3 to convert seconds → milliseconds for from_unixtime
stream_df = raw_stream.withColumn(
    "event_time",
    (col("timestamp")).cast(TimestampType()),
)


# =============================================================================
# SECTION 3 — Feature Window Aggregation
# =============================================================================
# PROVIDED — computes the same five features you built in Part 3a of the
# notebook, but over a live stream of 30-second tumbling windows.

windowed_features = (
    stream_df
    .withWatermark("event_time", "10 seconds")   # allow up to 10 s late arrivals
    .groupBy(
        window("event_time", "30 seconds")        # 30-second tumbling window
    )
    .agg(
        F.mean("eda").alias("mean_eda"),
        F.stddev("eda").alias("std_eda"),
        F.mean("hr").alias("mean_hr"),
        F.mean("temp").alias("mean_temp"),
        F.mean("acc_mag").alias("mean_acc_mag"),
    )
)


# =============================================================================
# SECTION 4 — Outlier Scoring UDF
# =============================================================================
# TODO (students): implement the body of score_window_udf below.
#
# The function receives five window-level statistics (the same features you
# computed in Part 3a of the notebook) and must return a float outlier score.
# Higher score = more anomalous.
#
# Steps:
#   1. Load your saved IsolationForest model:
#          with open(MODEL_PATH, "rb") as f:
#              model = pickle.load(f)
#
#   2. Call decision_function() on the five inputs:
#          raw = model.decision_function([[mean_eda, std_eda, mean_hr,
#                                          mean_temp, mean_acc_mag]])[0]
#
#   3. Return float(-raw)
#      (sklearn returns LOWER values for outliers; flipping the sign means
#       higher score = more anomalous, consistent with OUTLIER_THRESHOLD above)
#
# The null-guard and UDF registration below are already provided — do not
# change them.


def score_window_udf(mean_eda, std_eda, mean_hr, mean_temp, mean_acc_mag):
    """Return an outlier score for a 30-second window (higher = more anomalous)."""
    # PROVIDED: return 0.0 when a window has too few rows to produce statistics
    if any(v is None for v in [mean_eda, std_eda, mean_hr, mean_temp, mean_acc_mag]):
        return 0.0

    # TODO (students): load your model and return the outlier score.
    # Replace the line below with your implementation.
    raise NotImplementedError("Complete score_window_udf in Section 4")


# PROVIDED: register the function as a Spark UDF returning FloatType
score_udf = udf(score_window_udf, FloatType())


# =============================================================================
# SECTION 5 — Apply UDF and Flag Outliers
# =============================================================================
# PROVIDED — applies the UDF to the windowed features and adds is_outlier.

scored_df = windowed_features.withColumn(
    "outlier_score",
    score_udf(
        col("mean_eda"),
        col("std_eda"),
        col("mean_hr"),
        col("mean_temp"),
        col("mean_acc_mag"),
    ),
)

result_df = scored_df.withColumn(
    "is_outlier",
    col("outlier_score") > OUTLIER_THRESHOLD,
)


# =============================================================================
# SECTION 6 — Stream Simulation Helper
# =============================================================================
# PROVIDED — reads the preprocessed CSV in chunks and drops them into INBOX_DIR
# to simulate a real-time sensor stream.

def simulate_stream(
    csv_path: str,
    inbox_dir: str,
    chunk_size: int = 30,
    delay: float = 2.0,
) -> None:
    """
    Simulate a real-time data stream by writing chunks of a CSV to inbox_dir.

    Parameters
    ----------
    csv_path : str
        Path to the fully preprocessed WESAD CSV file.
    inbox_dir : str
        Directory that the Spark streaming source is watching.
    chunk_size : int
        Number of rows to write per chunk (each chunk = one micro-batch file).
        Default: 30 rows (~30 seconds of data at 1 Hz).
    delay : float
        Seconds to wait between writing consecutive chunks.
        Default: 2 seconds (faster than real time to speed up demos).
    """
    print(f"[Simulation] Reading data from: {csv_path}")
    df = pd.read_csv(csv_path)
    total_rows = len(df)
    n_chunks = (total_rows + chunk_size - 1) // chunk_size

    print(f"[Simulation] {total_rows:,} rows → {n_chunks} chunks of {chunk_size} rows each")
    print(f"[Simulation] Writing to inbox: {inbox_dir}")
    print(f"[Simulation] Delay between chunks: {delay}s\n")

    for i in range(n_chunks):
        chunk = df.iloc[i * chunk_size : (i + 1) * chunk_size]
        out_path = os.path.join(inbox_dir, f"chunk_{i:05d}.csv")
        # Write with header so Spark can parse column names (schema is enforced anyway)
        chunk.to_csv(out_path, index=False)
        print(f"[Simulation] Wrote chunk {i + 1}/{n_chunks}  ({len(chunk)} rows)  → {out_path}")
        time.sleep(delay)

    print("[Simulation] All chunks written.  Stream simulation complete.")


# =============================================================================
# SECTION 7 — Output Sink
# =============================================================================
# PROVIDED — prints each micro-batch to the console.
# Copy the first batch of output and paste it into a markdown cell in your notebook.

streaming_query = (
    result_df.writeStream
    .format("console")
    .outputMode("update")          # emit only rows that changed this micro-batch
    .option("truncate", "false")   # show full column values
    .option("numRows", 20)         # maximum rows to display per trigger
    .option("checkpointLocation", CHECKPOINT)
    .trigger(processingTime="5 seconds")
)


# =============================================================================
# SECTION 8 — Main Execution
# =============================================================================
# PROVIDED — starts the simulation thread and the streaming query, then waits.

if __name__ == "__main__":
    # PROVIDED: verify that the preprocessed CSV exists before starting
    if not os.path.isfile(PREPROCESSED_CSV):
        raise FileNotFoundError(
            f"Preprocessed CSV not found: {PREPROCESSED_CSV}\n"
            "Please preprocess the WESAD data and save it at that path, "
            "or update PREPROCESSED_CSV in Section 1."
        )

    # PROVIDED: start the stream simulation in a background thread so it runs
    # concurrently with the Spark streaming query
    sim_thread = threading.Thread(
        target=simulate_stream,
        kwargs={
            "csv_path":   PREPROCESSED_CSV,
            "inbox_dir":  INBOX_DIR,
            "chunk_size": 30,    # rows per chunk (~30 seconds at 1 Hz)
            "delay":      2.0,   # seconds between chunks
        },
        daemon=True,   # thread exits automatically when the main process exits
    )

    print("=" * 60)
    print("  WESAD Outlier Detection — Structured Streaming")
    print("=" * 60)
    print(f"  Inbox  : {INBOX_DIR}")
    print(f"  Output : {OUTPUT_DIR}")
    print(f"  Threshold: outlier_score > {OUTLIER_THRESHOLD}")
    print("=" * 60)
    print()

    # PROVIDED: start the simulation thread
    sim_thread.start()

    # PROVIDED: start the streaming query and block until interrupted
    query = streaming_query.start()

    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        print("\n[Main] Interrupt received — stopping streaming query.")
        query.stop()
        print("[Main] Streaming query stopped.  Exiting.")
