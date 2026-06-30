import pandas as pd

def load_recruiter_csv(path: str):
    df = pd.read_csv(path)
    return df.to_dict(orient="records")