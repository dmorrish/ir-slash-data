class IracingError(Exception):
    """Raised when there is some other error when communicating with the server."""

    def __init__(self, message, response=None):
        self.response = response
        super(IracingError, self).__init__(message)


class AuthenticationError(IracingError):
    """Raised when our attempt to authenticate fails"""

    def __init__(self, message, response=None):
        super(AuthenticationError, self).__init__(message, response=response)


class ServerDownError(IracingError):
    """Raised when the iRacing /data server is down for maintenance."""

    def __init__(self, message, response=None):
        super(ServerDownError, self).__init__(message, response=response)


class ForbiddenError(IracingError):
    """Raised when a user is forbidden from accessing the requested data."""

    def __init__(self, message, response=None):
        super(ForbiddenError, self).__init__(message, response=response)


class NotFoundError(IracingError):
    """Raised when the requested data is not found."""

    def __init__(self, message, response=None):
        super(NotFoundError, self).__init__(message, response=response)


class BadRequestError(IracingError):
    """Raised when there is an error during a build request."""

    def __init__(self, message, request, response=None):
        self.request = request
        super(BadRequestError, self).__init__(message, response=response)
