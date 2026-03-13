import pandas as pd

def load_csv(path):

    try:
        df = pd.read_csv(path)
        return df

    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding = "latin1")
        return df

    except Exception as e:
        print(f"Error loading the CSV file: {e}")
        return None