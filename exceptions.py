# Simply exceptions to handle errors with external API


class ExternalApiError(Exception):
    """
    Basic class to handle general errors with external api
    """
    pass


class ExternalApiConnectionError(ExternalApiError):
    """
    Exception to handle connection errors to external api
    """
    pass


class ExternalApiFetchError(ExternalApiError):
    """
    Exception to handle errors with fetching data from external api
    """
    pass


class ExternalApiParseError(ExternalApiError):
    """
    Exception to handle errors with parsing data returned by external api
    """
    pass