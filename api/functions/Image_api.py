from PIL import Image
import io, os
import configparser
from flask import request
config = configparser.ConfigParser()
config.read(os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)),'config'),"config.ini"))
if __name__ == '__main__':
    from tools_get_files import save_file_on_error
else:
    from tools_get_files import save_file_on_error


def autoorient(image):
    """Accepts a PIL image item as input, returns a PIL image item as output."""
    # get exif data from image
    try:
        exif = image._getexif()
    except AttributeError:
        exif = None

    # if image has no exif data, return it unmodified
    if exif is None:
        return image

    # define exif orientation values and corresponding transformations
    ORIENTATIONS = {
        3: (Image.ROTATE_180,),
        6: (Image.ROTATE_270,),
        8: (Image.ROTATE_90,),
        2: (Image.FLIP_LEFT_RIGHT,),
        4: (Image.FLIP_TOP_BOTTOM, Image.ROTATE_180),
        5: (Image.FLIP_LEFT_RIGHT, Image.ROTATE_270),
        7: (Image.FLIP_LEFT_RIGHT, Image.ROTATE_90),
    }
    
    orientation = exif.get(274)
    if orientation not in ORIENTATIONS:
        return image

    for transform in ORIENTATIONS[orientation]:
        image = image.transpose(transform)
        
    return image

def autoorient2(image):
    """Accepts a PIL image item as input, returns a PIL image item as output."""
    # get exif data from image
    image = Image.open(image)
    try:
        exif = image._getexif()
    except AttributeError:
        exif = None

    # if image has no exif data, return it unmodified
    if exif is None:
        return image
    
    # define exif orientation values and corresponding transformations
    ORIENTATIONS = {
        3: (Image.ROTATE_180,),
        6: (Image.ROTATE_270,),
        8: (Image.ROTATE_90,),
        2: (Image.FLIP_LEFT_RIGHT,),
        4: (Image.FLIP_TOP_BOTTOM, Image.ROTATE_180),
        5: (Image.FLIP_LEFT_RIGHT, Image.ROTATE_270),
        7: (Image.FLIP_LEFT_RIGHT, Image.ROTATE_90),
    }
    
    orientation = exif.get(274)
    if orientation not in ORIENTATIONS:
        return image

    for transform in ORIENTATIONS[orientation]:
        image = image.transpose(transform)
    img_file = io.BytesIO()
    image.save(img_file, format='PNG')
    img_file.seek(0)
    file = io.BytesIO(img_file.getvalue())
    file.seek(0)
    print(type(img_file))
    print("_-------------------------------------------------------------------------")
    return file

def autoorient4(image):
    """Accepts a PIL image item as input, returns a PIL image item as output."""
    # get exif data from image
    image = Image.open(image)
    try:
        exif = image._getexif()
    except AttributeError:
        exif = None

    # if image has no exif data, return it unmodified
    if exif is None:
        return image
    
    # define exif orientation values and corresponding transformations
    ORIENTATIONS = {
        3: (Image.ROTATE_180,),
        6: (Image.ROTATE_270,),
        8: (Image.ROTATE_90,),
        2: (Image.FLIP_LEFT_RIGHT,),
        4: (Image.FLIP_TOP_BOTTOM, Image.ROTATE_180),
        5: (Image.FLIP_LEFT_RIGHT, Image.ROTATE_270),
        7: (Image.FLIP_LEFT_RIGHT, Image.ROTATE_90),
    }
    
    orientation = exif.get(274)
    if orientation not in ORIENTATIONS:
        return image

    for transform in ORIENTATIONS[orientation]:
        image = image.transpose(transform)
    img_file = io.BytesIO()
    image.save(img_file, format='PNG')
    img_file.seek(0)
    file = io.BytesIO(img_file.getvalue())
    file.seek(0)
    print(type(img_file))
    print("_-------------------------------------------------------------------------")
    return file
# @save_file_on_error
# def resize_and_autoorient(file,width,height=None):
#     """Accepts a file bytes object and returns a file bytes object
#     Resizes an image based on specifications in the config."""
#     f = Image.open(file)
#     f = autoorient(f)
#     f=f.resize((int(height),int(width)))
#     # Create a bytes object to send in response
#     img_file = io.BytesIO()
#     f.save(img_file, format='PNG')
#     img_file.seek(0)
#     return img_file
def autoorient_2(file):
    image = Image.open(file)
    f = autoorient(image)
    img_file = io.BytesIO()
    f.save(img_file,format='PNG')
    img_file.seek(0)
    return img_file
def resize_and_autoorient(file, width,height=None):
    """Accepts a file bytes object and returns a file bytes object
    Resizes an image based on specifications in the config."""
    f = Image.open(file)
    f = autoorient(f)
    if not height:
        height,w = f.size
        height = width/(w/height)
    f=f.resize((int(height),int(width)), resample=Image.LANCZOS)
    # Create a bytes object to send in response
    img_file = io.BytesIO()
    f.save(img_file, format='PNG')
    img_file.seek(0)
    return img_file