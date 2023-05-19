from flask import request
import base64
import io


def get_file_base64():
    file_content = request.json.get('content')
    file_content=base64.b64decode(file_content)
    file_content=io.BytesIO(file_content)
    return file_content