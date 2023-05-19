import io
import zipfile
import zlib
from PIL import Image


def add_icon_to_word_file(word_file, icon_file, imagepath):
    """Adds an icon to a word file by first unzipping it, replacing an icon png file with a bytes object. returns a compressed BytesIO. No further processing is necessary to use as a document.

    Args:
        word_file (Bytes): Word file as a Bytes - object.
        icon_file (Bytes): Image object to be passed to the placeholder.

    Returns:
        BytesIO: BytesIO object to be opened or saved for word-document processing.
    """
    with zipfile.ZipFile(io.BytesIO(word_file), mode='r') as zf:

        files = {x: zf.read(x) for x in zf.namelist()}
        files[imagepath] = icon_file

    new_word_file = io.BytesIO()
    with zipfile.ZipFile(new_word_file, mode='w', compression=zipfile.ZIP_DEFLATED) as zkf:
        for name, file in files.items():
            zkf.writestr(name, file)

    new_word_file.seek(0)
    return new_word_file


def autoorient(image):
    """Autoorients an image pre-loaded with PIL

    Args:
        image (Image): Pillow Image object

    Returns:
        Image: Pillow Image-object
    """
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