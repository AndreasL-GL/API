import json
import pandas as pd
import io
import base64

def detect_and_create_file(file, content_type = None):
    if type(file)==dict:
        return {
            "$content-type":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if content_type == '.xlsx' else "Application/json",
            "$content":base64.b64encode(io.BytesIO(pd.DataFrame(file).to_excel()).getvalue()).decode('utf-8') if content_type =='.xlsx' else file
        }
    elif type(file)==pd.DataFrame:
        if content_type == '.xlsx':
            f = io.BytesIO()
            file.to_excel(f,index=False)
            f.seek(0)
            f = base64.b64encode(f.getvalue()).decode()
    elif type(file)==io.BytesIO:
        f = base64.b64encode(file.getvalue()).decode()
    elif type(file) == bytes:
        f = base64.b64encode(file).decode()
    elif type(file) == str:
        try:
            base64.b64decode(file)
        except:
            return {"text":file}
        f=file
    else: return None
    return {
        "$content-type":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if content_type == '.xlsx' else "Application/json",
        "$content":f
    }