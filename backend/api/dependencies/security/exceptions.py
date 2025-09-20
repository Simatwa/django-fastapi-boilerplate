class BaseSecurityException(Exception):
    pass


class InvalidSecretError(BaseException):
    def __init__(self, api_response: object, *args, **kwargs):
        self.api_response = api_response
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"<{self.__class__.__name__} api_response={self.api_response}>"
