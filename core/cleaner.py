import numpy as np
import pandas as pd

# ----- MISSING VALUE HANDLING -----
def handle_missing_values(df, missing_map):

    df = df.copy()

    df.replace(
        ["", "N/A", "NA", "null", "?", "-", "NULL", "na", "n/a"],
        np.nan,
        inplace=True
    )

    filled_info = {}

    for col, method in missing_map.items():

        missing_before = df[col].isnull().sum()

        if missing_before == 0 or method == "None":
            continue

        if method == "Drop":
            df = df[df[col].notna()]
            filled_info[col] = (missing_before, "Dropped Rows")

        elif method == "Mean":
            df[col] = df[col].fillna(df[col].mean())
            filled_info[col] = (missing_before, "Mean")

        elif method == "Median":
            df[col] = df[col].fillna(df[col].median())
            filled_info[col] = (missing_before, "Median")

        elif method == "Mode":
            df[col] = df[col].fillna(df[col].mode()[0])
            filled_info[col] = (missing_before, "Mode")

        elif method == "FFill":
            df[col] = df[col].ffill()
            filled_info[col] = (missing_before, "Forward Fill")

        elif method == "BFill":
            df[col] = df[col].bfill()
            filled_info[col] = (missing_before, "Backward Fill")

    return df, filled_info

# ---------- DATA TYPE VALIDATION --------
def validate_column_types(df, dtype_map):

    df = df.copy()

    conversion_report = {}  # invalid values -> nan
    dtype_changes = {}      # conversion summary

    for col, dtype in dtype_map.items():

        prev_dtype = str(df[col].dtype)

        if dtype == "string":
            df[col] = df[col].astype(str)
            dtype_changes[col] = f"{prev_dtype} -> String"
            continue

        elif dtype == "int":
            cleaned = (df[col].astype(str)
                       .str.strip()
                       .str.replace(",", "", regex=False)
                       .str.replace("$", "", regex=False)
                       .str.replace("₹", "", regex=False)
                       .str.replace("-", "", regex=False)
                       .str.replace("/", "", regex=False)
                       )
            converted = pd.to_numeric(cleaned, errors="coerce").astype("Int64")
            new_dtype = "Int"

        elif dtype == "float":
            cleaned = (df[col].astype(str)
                       .str.strip()
                       .str.replace(",", "", regex=False)
                       .str.replace("$", "", regex=False)
                       .str.replace("₹", "", regex=False)
                       .str.replace("-", "", regex=False)
                       .str.replace("/", "", regex=False)
                       )
            converted = pd.to_numeric(cleaned, errors="coerce")
            new_dtype = "Float"

        else:
            continue

        failed = converted.isna() & df[col].notna()
        failed_count = int(failed.sum())

        if failed_count > 0:
            conversion_report[col] = failed_count

        df[col] = converted

        dtype_changes[col] = f"{prev_dtype} -> {new_dtype}"

    return df, conversion_report, dtype_changes

# -------- DUPLICATES REMOVAL --------
def remove_duplicates(df):
    duplicates = df[df.duplicated()]
    df_clean = df.drop_duplicates()
    return df_clean, duplicates


def save_cleaned_csv(df, path):
    df.to_csv(path, index = False)

#creating report
def save_report(report, path):
    with open(path,'w') as f:
        f.write(report)