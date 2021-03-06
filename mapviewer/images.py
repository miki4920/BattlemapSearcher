import io
from PIL import Image

from mapviewer.config import CONFIG


def create_thumbnail(picture):
    im = Image.open(picture)
    im.thumbnail((CONFIG.THUMBNAIL_SIZE, CONFIG.THUMBNAIL_SIZE), Image.ANTIALIAS)
    img_byte_arr = io.BytesIO()
    im.save(img_byte_arr, format=CONFIG.THUMBNAI_FORMAT)
    img_byte_arr.seek(0)
    return img_byte_arr.read()
