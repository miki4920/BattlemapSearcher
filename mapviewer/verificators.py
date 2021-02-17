import re
from .config import CONFIG
from .errors import *
from PIL import Image


def verify_name(name):
    alphanumerical = re.match("^\w*$", name)
    length = CONFIG.MINIMUM_NAME_LENGTH <= len(name) <= CONFIG.NAME_LENGTH
    if not alphanumerical:
        raise NameNotAlphanumerical
    if not length:
        raise NameNotInRange


def verify_extension(extension):
    valid_extension = extension in CONFIG.IMAGE_EXTENSIONS
    if not valid_extension:
        raise ExtensionNotAccepted


def verify_picture(picture):
    valid_size = CONFIG.MINIMUM_NAME_LENGTH < len(picture) < CONFIG.MAXIMUM_IMAGE_SIZE
    if not valid_size:
        raise ImageNotInRange


def verify_uploader(uploader):
    alphanumerical = re.match("^\w*$", uploader)
    length = CONFIG.MINIMUM_NAME_LENGTH <= len(uploader) <= CONFIG.NAME_LENGTH
    if not alphanumerical:
        raise UploaderNotAlphanumerical
    if not length:
        raise UploaderNotInRange


def get_map_dictionary(data):
    name = data["name"]
    verify_name(name)
    extension = data["extension"]
    verify_extension(extension)
    picture = data["picture"]
    verify_picture(picture)
    uploader = data["uploader"]
    verify_uploader(uploader)

    image_data = Image.open(picture)
    width, height = image_data.size
    square_width, square_height = data["square_width"], data["square_height"]
    tags = data.get("tags")
    if not tags:
        tags = []
    else:
        tags = tags.split(",")
    map_dictionary = {"name": name,
                      "extension": extension,
                      "picture": picture,
                      "uploader": uploader,
                      "width": width,
                      "height": height,
                      "square_width": square_width,
                      "square_height": square_height,
                      "tags": tags
    }

    return map_dictionary