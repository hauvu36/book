from rest_framework import status
from rest_framework.exceptions import APIException


class GenericException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    code = 1000
    summary = "Error"
    verbose = False
    error_detail = None

    def __init__(self, message=None, status_code=None, error_detail=None):
        if not message:
            message = "Oops! Something went wrong, please try again"
        if status_code:
            self.status_code = status_code
        if error_detail:
            message = error_detail
        super().__init__(message)

    def serialize(self):
        data = {
            "code": self.code,
            "summary": self.summary,
            "message": self.detail,
        }
        return data


class ObjectNotFoundException(GenericException):
    code = 1001

    def __init__(self, message=None, object_id=None):
        if not message:
            message = "Object not found: [%s] " % object_id
        super().__init__(message)


class MissingRequiredFieldException(GenericException):
    code = 1002

    def __init__(self, message=None, field_name=None):
        if not message:
            message = "Missing required field: [%s] " % field_name
        super().__init__(message)


class InvalidParameterException(GenericException):
    code = 1005

    def __init__(self, message=None):
        super().__init__(message=message)


class InvalidUploadFormException(GenericException):
    code = 1006

    def __init__(self, message=None):
        super().__init__(message=message)


class NameExistsException(GenericException):
    code = 1007
    verbose = True

    def __init__(self, message=None):
        super().__init__(message=message)


class InvalidDataException(GenericException):
    code = 1008
    verbose = True

    def __init__(self, message=None, field=None, error_detail=None, status_code=None):
        if not message:
            message = f"Input {field} error."
        super().__init__(message=message, error_detail=error_detail, status_code=status_code)


class InvalidEmail(InvalidDataException):
    code = 1009
    verbose = True

    def __init__(self, message="Your email address is invalid. Please check again"):
        super().__init__(message=message)


class ParseJsonErrorException(GenericException):
    code = 1010
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "JSON parse error."
        super().__init__(message=message)


class UnauthorizedException(GenericException):
    code = 1011
    verbose = True

    def __init__(self, message=None, status_code=status.HTTP_401_UNAUTHORIZED):
        if not message:
            message = "You need to login into the system to use this function."
        super().__init__(message=message, status_code=status_code)
