
from flask import Blueprint, request, jsonify
from functions.Image_api import resize_and_autoorient
from functions.authentication import require_api_key
import base64, io, openpyxl, os

image_resize = Blueprint('image_resize', __name__)

@image_resize.route("/api/image_resizer", methods=["POST"])
@require_api_key
def post_file():
    if False:
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
    img_file=resize_and_autoorient(resizer(request.json()))
    file_content=base64.b64encode(img_file.getvalue).decode('utf-8')
    return jsonify({
        "$content-type": "image/png",
        "$content": file_content
    })
    
@image_resize.route("/api/image_resize", methods=["POST"])
#@require_api_key
def post_file2():
    # file_content = request.json.get('File Content')["$content"]
    # width = int(request.json.get('width'))
    # height = request.json.get('height')
    # if not height: height=None
    # file_content=base64.b64decode(file_content)
    print(request.get_json().keys())
    with open(os.path.join(os.path.join(os.path.dirname(__file__),'functions'),'image.json'),'r') as f:
        json.dump(request.get_json(),indent=4, ensure_ascii=False)
    # file_content=io.BytesIO(file_content)
    img_file=resizer(request.get_json())
    file_content=base64.b64encode(img_file.getvalue()).decode('utf-8')
    return jsonify({
        "$content-type": "image/png",
        "$content": file_content
    })
    
def resizer(js):
    bb = js['File Content']
    img = resize_and_autoorient(io.BytesIO(base64.b64decode(bb["$content"])), width=js['width'] if "width" in js.keys() else None,height=js['height'] if 'height' in js.keys() else None)
    return img
if __name__=='__main__':
    import json
    with open(os.path.join(os.path.join(os.path.dirname(__file__),'functions'),'image.json'),'r') as f:
        js = json.load(f)

    img = resizer(js['body'])
    #img = resize_and_autoorient(io.BytesIO(base64.b64decode(bb["$content"])), width=200,height=None)
    from PIL import Image
    im = Image.open(img)
    im.show()