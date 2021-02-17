class VerificationError(Exception):
    pass


class NameNotAlphanumerical(VerificationError):
    def __init__(self, message="00:Map Name contains non-alphanumerical characters"):
        self.message = message
        super().__init__(self.message)


class NameNotInRange(VerificationError):
    def __init__(self, message="01:Map Name has wrong length"):
        self.message = message
        super().__init__(self.message)


class ExtensionNotAccepted(VerificationError):
    def __init__(self, message="02:Map Extension is not accepted"):
        self.message = message
        super().__init__(self.message)


class ImageNotInRange(VerificationError):
    def __init__(self, message="03:Map Image has wrong size"):
        self.message = message
        super().__init__(self.message)


class UploaderNotAlphanumerical(VerificationError):
    def __init__(self, message="04:Map Uploader contains non-alphanumerical characters"):
        self.message = message
        super().__init__(self.message)


class UploaderNotInRange(VerificationError):
    def __init__(self, message="05:Map Uploader has wrong length"):
        self.message = message
        super().__init__(self.message)
