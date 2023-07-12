
from flask import Blueprint, request, jsonify
from functions.Image_api import resize_and_autoorient
from functions.authentication import require_api_key
import base64, io, openpyxl, os

image_resize = Blueprint('image_resize', __name__)

@image_resize.route("/api/image_resizer", methods=["POST"])
@require_api_key
def post_file():
    file_content = request.json.get('File Content')["$content"]
    width = int(request.json.get('width'))
    height = request.json.get('height')
    if not height: height=None
    file_content=base64.b64decode(file_content)
    file_content=io.BytesIO(file_content)
    img_file=resize_and_autoorient(file_content,width=width,height=height)
    file_content=base64.b64encode(img_file.getvalue).decode('utf-8')
    return jsonify({
        "$content-type": "image/png",
        "$content": file_content
    })
    
@image_resize.route("/api/image_resize", methods=["POST"])
@require_api_key
def post_file2():
    file_content = request.json.get('File Content')["$content"]
    width = int(request.json.get('width'))
    height = request.json.get('height')
    if not height: height=None
    file_content=base64.b64decode(file_content)
    file_content=io.BytesIO(file_content)
    img_file=resize_and_autoorient(file_content,width=width,height=height)
    file_content=base64.b64encode(img_file.getvalue).decode('utf-8')
    return jsonify({
        "$content-type": "image/png",
        "$content": file_content
    })
    
if __name__=='__main__':
    import json
    with open(os.path.join(os.path.join(os.path.dirname(__file__),'functions'),'image.json'),'r') as f:
        js = json.load(f)
    bb = js['body']['File Content']
    print(bb.keys())
    img = resize_and_autoorient(io.BytesIO(base64.b64decode(bb["$content"])), width=200,height=None)
    print(type(img))
    from PIL import Image
    im = Image.open(img)
    im.show()