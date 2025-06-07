import pandas as pd
from io import BytesIO, StringIO

def parse_excel_attachment(file_bytes: bytes, filename: str) -> dict:
    if filename.endswith(".csv"):
        df = pd.read_csv(StringIO(file_bytes.decode("utf-8")))
        return {filename.replace(".csv", ""): df}
    else:
        xls = pd.ExcelFile(BytesIO(file_bytes))
        return {sheet: xls.parse(sheet) for sheet in xls.sheet_names}