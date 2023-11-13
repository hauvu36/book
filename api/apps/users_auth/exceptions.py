from apps.core.exceptions import GenericException


class TokenExpiredException(GenericException):
    code = 8000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Token is invalid or expired."
        super().__init__(message=message)
