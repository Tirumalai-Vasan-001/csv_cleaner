import pandas as pd
def inspect_csv(df):
    report = {}

    report["rows"] = df.shape[0]
    report["columns"] = df.shape[1]
    report["column_Names"] = list(df.columns)
    report["data_types"] = df.dtypes.astype(str).to_dict()
    report["missing_values"] = df.isnull().sum().to_dict()
    report["duplicate_values"] = int(df.duplicated().sum())

    return report

