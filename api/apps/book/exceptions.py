from apps.core.exceptions import GenericException


class PublishDateException(GenericException):
    code = 3000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "The publish_date field is invalid"
        super().__init__(message=message)


class FileEmptyException(GenericException):
    code = 3001
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "File is not valid"
        super().__init__(message=message)


class BookDoesNotExistException(GenericException):
    code = 3002
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "This book does not exist"
        super().__init__(message=message)


class FileImageException(GenericException):
    code = 3003
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "This is not image file, please upload image file"
        super().__init__(message=message)
