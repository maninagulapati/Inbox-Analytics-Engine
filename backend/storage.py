import pandas as pd
import os

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_dataframe(sheet_data: dict, base_filename: str):
    folder = os.path.join(UPLOAD_DIR, base_filename)
    os.makedirs(folder, exist_ok=True)
    for sheet_name, df in sheet_data.items():
        safe_name = sheet_name.replace(" ", "_")
        df.to_csv(os.path.join(folder, f"{safe_name}.csv"), index=False)