"""
preprocess_wesad.py
-------------------
Preprocesses WESAD E4 wristband data for a single subject into a 1 Hz
merged feature DataFrame with condition labels.

E4 CSV format:
  Row 0: unix start timestamp (UTC)
  Row 1: sample rate (Hz)
  Rows 2+: sample data

Usage:
  python preprocess_wesad.py [subject_dir]

  subject_dir defaults to ../../data/WESAD/S2 (relative to this script).
  Output CSV is written to the same directory as this script.
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats as sp_stats


# ---------------------------------------------------------------------------
# Helper: parse a single-column (or multi-column) E4 CSV
# ---------------------------------------------------------------------------

def parse_e4_csv(filepath: str, col_names: list) -> pd.DataFrame:
    """
    Read an Empatica E4 CSV file and return a DataFrame indexed by
    a DatetimeIndex reconstructed from the start timestamp and sample rate.

    Parameters
    ----------
    filepath : str
        Absolute path to the CSV file.
    col_names : list of str
        Names to assign to the data columns (excluding the timestamp index).

    Returns
    -------
    pd.DataFrame
        DataFrame with a DatetimeIndex (UTC) and one column per signal.
    """
    # The first two rows carry metadata, not data.
    with open(filepath, "r") as f:
        start_ts = float(f.readline().strip().split(",")[0])
        sample_rate = float(f.readline().strip().split(",")[0])

    # Read the actual data rows (skip the two header rows).
    df = pd.read_csv(filepath, skiprows=2, header=None, names=col_names)

    # Build timestamps: t_i = start + i / sample_rate
    n_samples = len(df)
    offsets_sec = np.arange(n_samples) / sample_rate
    timestamps = pd.to_datetime(start_ts + offsets_sec, unit="s", utc=True)

    df.index = timestamps
    df.index.name = "timestamp"
    return df


# ---------------------------------------------------------------------------
# Helper: parse tags.csv
# ---------------------------------------------------------------------------

def parse_tags(filepath: str) -> list:
    """
    Read tags.csv and return a sorted list of tag unix timestamps (float).

    Tags may be stored one per line OR as a single line of space/comma-
    separated values, so we handle both formats.
    """
    tags = []
    with open(filepath, "r") as f:
        content = f.read().strip()

    if not content:
        return tags

    # Try splitting by newline first; fall back to splitting by whitespace/comma.
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if len(lines) == 1:
        # Might be space-separated or comma-separated on a single line
        tokens = lines[0].replace(",", " ").split()
    else:
        tokens = lines

    for token in tokens:
        try:
            tags.append(float(token))
        except ValueError:
            pass  # skip anything that isn't a number

    return sorted(tags)


# ---------------------------------------------------------------------------
# Helper: assign condition labels from the .pkl file
# ---------------------------------------------------------------------------

# WESAD condition label mapping (from the dataset paper):
#   0 = not defined / transition
#   1 = baseline
#   2 = stress (TSST)
#   3 = amusement
#   4 = meditation
#   5, 6, 7 = other protocol events (map to 0)
# For this assignment we keep only 0 (transition), 1 (baseline), 2 (stress), 3 (amusement).

_CONDITION_NAMES = {
    0: "unknown/transition",
    1: "baseline",
    2: "stress",
    3: "amusement",
}

# Chest sensor (label) sample rate in the WESAD pkl
_CHEST_HZ = 700


def assign_conditions_from_pkl(df: pd.DataFrame, pkl_path: str) -> pd.DataFrame:
    """
    Add 'condition' and 'condition_name' columns by loading ground-truth
    labels from the WESAD subject .pkl file.

    The pkl label array is recorded at 700 Hz (chest sensor rate).
    We downsample to 1 Hz by taking the mode within each second, then
    align by index position with the merged 1 Hz DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        1 Hz merged DataFrame (DatetimeIndex, UTC).
    pkl_path : str
        Path to the subject .pkl file (e.g. S2/S2.pkl).

    Returns
    -------
    pd.DataFrame
        df with 'condition' (int) and 'condition_name' (str) columns added.
    """
    import pickle

    with open(pkl_path, "rb") as f:
        raw = pickle.load(f, encoding="latin1")

    label_700hz = raw["label"]  # shape: (N,) at 700 Hz

    # Downsample 700 Hz labels to 1 Hz: reshape and take per-second mode.
    n_seconds = len(label_700hz) // _CHEST_HZ
    label_700hz_trimmed = label_700hz[: n_seconds * _CHEST_HZ]
    label_matrix = label_700hz_trimmed.reshape(n_seconds, _CHEST_HZ)
    label_1hz = sp_stats.mode(label_matrix, axis=1, keepdims=False).mode  # (n_seconds,)

    # Map labels: keep 1, 2, 3; collapse everything else to 0.
    label_1hz = np.where(np.isin(label_1hz, [1, 2, 3]), label_1hz, 0).astype(int)

    # Align by index position (both start at second 0 of the session).
    n_rows = min(len(df), len(label_1hz))
    condition = np.zeros(len(df), dtype=int)
    condition[:n_rows] = label_1hz[:n_rows]

    df = df.copy()
    df["condition"] = condition
    df["condition_name"] = pd.Series(condition).map(
        lambda x: _CONDITION_NAMES.get(x, "unknown/transition")
    ).values
    return df


# ---------------------------------------------------------------------------
# Main preprocessing pipeline
# ---------------------------------------------------------------------------

def preprocess(subject_dir: str, output_path: str) -> None:
    """
    Full preprocessing pipeline for one WESAD subject's E4 data.

    Parameters
    ----------
    subject_dir : str
        Path to the subject directory (e.g. .../WESAD/S2).
        The E4 data are expected in <subject_dir>/S<N>_E4_Data/.
    output_path : str
        Full path for the output CSV file.
    """
    # Locate the E4 data subdirectory (handles subjects named S2, S3, etc.)
    subject_name = os.path.basename(os.path.normpath(subject_dir))
    e4_dir = os.path.join(subject_dir, f"{subject_name}_E4_Data")
    if not os.path.isdir(e4_dir):
        # Fall back: if the provided directory itself contains the CSVs
        e4_dir = subject_dir

    print(f"Reading E4 data from: {e4_dir}")

    # ------------------------------------------------------------------
    # 1. Parse each signal file
    # ------------------------------------------------------------------

    eda = parse_e4_csv(os.path.join(e4_dir, "EDA.csv"), ["eda"])
    bvp = parse_e4_csv(os.path.join(e4_dir, "BVP.csv"), ["bvp_mean"])
    hr  = parse_e4_csv(os.path.join(e4_dir, "HR.csv"),  ["hr"])
    tmp = parse_e4_csv(os.path.join(e4_dir, "TEMP.csv"), ["temp"])
    acc = parse_e4_csv(os.path.join(e4_dir, "ACC.csv"),  ["acc_x", "acc_y", "acc_z"])

    # ------------------------------------------------------------------
    # 2. ACC: convert from 1/64g units to g, then compute magnitude
    # ------------------------------------------------------------------
    acc_g = acc[["acc_x", "acc_y", "acc_z"]] / 64.0
    acc["acc_mag"] = np.sqrt(
        acc_g["acc_x"] ** 2 + acc_g["acc_y"] ** 2 + acc_g["acc_z"] ** 2
    )

    # ------------------------------------------------------------------
    # 3. Resample all signals to 1 Hz
    # ------------------------------------------------------------------
    # Use closed='left', label='left' for consistent bin labelling.
    resample_kwargs = dict(rule="1s", closed="left", label="left")

    eda_1hz  = eda[["eda"]].resample(**resample_kwargs).mean()
    bvp_1hz  = bvp[["bvp_mean"]].resample(**resample_kwargs).mean()
    tmp_1hz  = tmp[["temp"]].resample(**resample_kwargs).mean()
    hr_1hz   = hr[["hr"]].resample(**resample_kwargs).ffill()      # already 1 Hz
    acc_1hz  = acc[["acc_mag"]].resample(**resample_kwargs).mean()

    # ------------------------------------------------------------------
    # 4. Merge all signals (inner join on common time range)
    # ------------------------------------------------------------------
    signals = [eda_1hz, bvp_1hz, tmp_1hz, hr_1hz, acc_1hz]
    merged = signals[0]
    for sig in signals[1:]:
        merged = merged.join(sig, how="inner")

    print(f"Merged shape before NaN drop: {merged.shape}")

    # ------------------------------------------------------------------
    # 5. Assign condition labels from the .pkl ground-truth file
    # ------------------------------------------------------------------
    pkl_path = os.path.join(subject_dir, f"{subject_name}.pkl")
    if os.path.isfile(pkl_path):
        print(f"Loading ground-truth labels from: {pkl_path}")
        merged = assign_conditions_from_pkl(merged, pkl_path)
    else:
        print(f"WARNING: .pkl not found at {pkl_path}. All labels will be 0.")
        merged["condition"] = 0
        merged["condition_name"] = "unknown/transition"

    # ------------------------------------------------------------------
    # 6. Add seconds_elapsed column
    # ------------------------------------------------------------------
    session_start_ns = merged.index[0].value  # nanoseconds
    merged["seconds_elapsed"] = (
        (merged.index.astype(np.int64) - session_start_ns) / 1e9
    ).astype(int)

    # ------------------------------------------------------------------
    # 7. Drop rows with any NaN values
    # ------------------------------------------------------------------
    n_before = len(merged)
    merged.dropna(inplace=True)
    n_after = len(merged)
    if n_before != n_after:
        print(f"Dropped {n_before - n_after} rows containing NaN values.")

    # ------------------------------------------------------------------
    # 8. Reset index, add datetime column, reorder columns, save
    # ------------------------------------------------------------------
    merged = merged.reset_index()  # makes DatetimeIndex into 'timestamp' column
    merged.rename(columns={"timestamp": "datetime"}, inplace=True)
    merged.insert(0, "timestamp", merged["datetime"].astype(np.int64) / 1e9)
    # Reorder to match expected schema
    col_order = ["timestamp", "datetime", "eda", "temp", "hr", "acc_mag",
                 "bvp_mean", "condition", "condition_name", "seconds_elapsed"]
    merged = merged[[c for c in col_order if c in merged.columns]]

    merged.to_csv(output_path, index=False)
    print(f"\nSaved to: {output_path}")

    # ------------------------------------------------------------------
    # 9. Print summary
    # ------------------------------------------------------------------
    print("\n--- Summary ---")
    print(f"Shape: {merged.shape}")
    print(f"Columns: {list(merged.columns)}")
    print(f"\nDate range:")
    print(f"  Start : {merged['datetime'].iloc[0]}")
    print(f"  End   : {merged['datetime'].iloc[-1]}")
    print(f"  Duration: {merged['seconds_elapsed'].max()} seconds "
          f"({merged['seconds_elapsed'].max() / 60:.1f} minutes)")

    print("\nCondition distribution:")
    cond_counts = merged.groupby(["condition", "condition_name"]).size().reset_index(name="samples")
    for _, row in cond_counts.iterrows():
        pct = 100.0 * row["samples"] / len(merged)
        print(f"  [{int(row['condition'])}] {row['condition_name']:<22} "
              f"{int(row['samples']):>6} samples  ({pct:.1f}%)")

    print("\nSignal statistics:")
    print(merged[["eda", "bvp_mean", "temp", "hr", "acc_mag"]].describe().round(4).to_string())


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Preprocess WESAD E4 data for a single subject to 1 Hz CSV."
    )
    parser.add_argument(
        "subject_dir",
        nargs="?",
        default=None,
        help="Path to subject directory (default: ../../data/WESAD/S2 relative to this script).",
    )
    args = parser.parse_args()

    # Resolve subject directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if args.subject_dir is None:
        subject_dir = os.path.normpath(os.path.join(script_dir, "../../data/WESAD/S2"))
    else:
        subject_dir = os.path.abspath(args.subject_dir)

    if not os.path.isdir(subject_dir):
        print(f"Error: subject directory not found: {subject_dir}", file=sys.stderr)
        sys.exit(1)

    # Derive subject name from directory for the output filename
    subject_name = os.path.basename(os.path.normpath(subject_dir))
    output_filename = f"wesad_{subject_name}_1hz.csv"
    output_path = os.path.join(script_dir, output_filename)

    preprocess(subject_dir, output_path)


if __name__ == "__main__":
    main()
