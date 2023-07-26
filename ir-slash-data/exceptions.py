class IracingError(Exception):
    """Raised when there is some other error when communicating with the server."""

    def __init__(self, message, response):
        self.response = response
        super(IracingError, self).__init__(message)


class AuthenticationError(IracingError):
    """Raised when our attempt to authenticate fails"""

    def __init__(self, message, response):
        super(AuthenticationError, self).__init__(message, response)


class ServerDownError(IracingError):
    """Raised when the iRacing /data server is down for maintenance."""

    def __init__(self, message, response):
        super(ServerDownError, self).__init__(message, response)


class ForbiddenError(IracingError):
    """Raised when a user is forbidden from accessing the requested data."""

    def __init__(self, message, response):
        super(ForbiddenError, self).__init__(message, response)


class NotFoundError(IracingError):
    """Raised when the requested data is not found."""

    def __init__(self, message, response):
        super(NotFoundError, self).__init__(message, response)


class BadRequestError(IracingError):
    """Raised when there is an error during a build request."""

    def __init__(self, message, response, request):
        self.request = request
        super(BadRequestError, self).__init__(message, response)
