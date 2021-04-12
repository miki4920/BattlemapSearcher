from .utility import human_readable_size


class VerificationError(Exception):
    pass


class NameNotAlphanumerical(VerificationError):
    def __init__(self, name):
        self.message = f"00:Map Name contains non-alphanumerical characters:{name}"
        super().__init__(self.message)


class NameNotInRange(VerificationError):
    def __init__(self, name):
        self.message = f"01:Map Name has wrong length:{name}"
        super().__init__(self.message)


class ExtensionNotAccepted(VerificationError):
    def __init__(self, extension):
        self.message = f"02:Map Extension is not accepted:{extension}"
        super().__init__(self.message)


class PictureNotInRange(VerificationError):
    def __init__(self, image):
        image_size = human_readable_size(len(image))
        self.message = f"03:Map Picture has wrong size:{image_size}"
        super().__init__(self.message)


class HashNotAccepted(VerificationError):
    def __init__(self, name):
        self.message = f"04:Map Picture is blacklisted:{name}"
        super().__init__(self.message)


class HashNotUnique(VerificationError):
    def __init__(self, name):
        self.message = f"05:Map Picture is already in the database:{name}"
        super().__init__(self.message)


class DimensionsNotInRange(VerificationError):
    def __init__(self, width, height):
        self.message = f"06:Map Picture has wrong dimensions:{width},{height}"
        super().__init__(self.message)


class SquareDimensionsNotAccepted(VerificationError):
    def __init__(self, square_width, square_height):
        self.message = f"07:Map Picture is missing one of the square dimensions:{square_width},{square_height}"
        super().__init__(self.message)


class SquareDimensionsNotInRange(VerificationError):
    def __init__(self, square_width, square_height):
        self.message = f"08:One of the square dimensions is not an Integer or Null:{square_width},{square_height}"
        super().__init__(self.message)


class UploaderNotAlphanumerical(VerificationError):
    def __init__(self, uploader):
        self.message = f"09:Map Uploader contains non-alphanumerical characters:{uploader}"
        super().__init__(self.message)


class UploaderNotInRange(VerificationError):
    def __init__(self, uploader):
        self.message = f"10:Map Uploader has wrong length:{uploader}"
        super().__init__(self.message)


class TagsNotAccepted(VerificationError):
    def __init__(self, tags):
        self.message = f"11:Map Tags are in a wrong format:{tags}"
        super().__init__(self.message)
