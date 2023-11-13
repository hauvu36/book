from apps.core.exceptions import GenericException


class MissedUsernameOrEmailException(GenericException):
    code = 2000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Username or email is required."
        super().__init__(message=message)


class EmailToResetNotExistException(GenericException):
    code = 2001
    verbose = True

    def __init__(self, field="e-mail address", message=None):
        if not message:
            message = f"This {field} does not exist."
        super().__init__(message=message)


class EmailRegisteredNotVerifiedException(GenericException):
    code = 2002
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "This e-mail address is not verified. Please check your mailbox."
        super().__init__(message=message)


class PasswordsNotMatchException(GenericException):
    code = 2003
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "The two password fields didn't match."
        super().__init__(message=message)


class UsernameRegisteredWithThisEmailException(GenericException):
    code = 2004
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "A user is already registered with this e-mail address."
        super().__init__(message=message)


class UsernameAlreadyExistException(GenericException):
    code = 2005
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Username is already existed."
        super().__init__(message=message)


class PasswordValidateError(GenericException):
    code = 2006
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Password is not valid. Please try again."
        super().__init__(message=message)


class EmailValidateError(GenericException):
    code = 2007
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Email is not valid. Please try again."
        super().__init__(message=message)


class UserAccountDisabledException(GenericException):
    code = 2008
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "User account is disabled."
        super().__init__(message=message)


class LogInException(GenericException):
    code = 2009
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Unable to log in with provided credentials."
        super().__init__(message=message)


class PasswordException(GenericException):
    code = 2010
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Please enter the current password correctly"
        super().__init__(message=message)


class UserNotExistsException(GenericException):
    code = 2011
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "User does not exist"
        super().__init__(message=message)


class EmailNotExistException(GenericException):
    code = 2011
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "There is not user exist with this email."
        super().__init__(message=message)
