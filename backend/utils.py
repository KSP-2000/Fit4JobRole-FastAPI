import pandas as pd
import io
import json
import os

# Excel download (must use BytesIO)
def export_to_excel(data: list[dict]):
    if not data:
        return None
    
    df = pd.DataFrame(data)
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl') # must have "openpyxl" installed

    return excel_buffer.getvalue()


# JSON file related utils
def open_json_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
    return data

def append_to_json_file(data, filename):
    if os.path.exists(filename):
        with open(filename, "r+", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
            if not isinstance(existing_data, list):
                existing_data = []
            existing_data.extend(data)
            f.seek(0)
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
    else:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)