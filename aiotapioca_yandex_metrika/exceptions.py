from aiotapioca import ResponseProcessException, TapiocaException

__all__ = (
    "BackwardCompatibilityError",
    "YandexMetrikaApiError",
    "YandexMetrikaClientError",
    "YandexMetrikaDownloadLogError",
    "YandexMetrikaLimitError",
    "YandexMetrikaServerError",
    "YandexMetrikaTokenError",
)


class YandexMetrikaApiError(ResponseProcessException):
    def __str__(self):
        return f"{self.response.status} {self.response.reason} {self.message}\nHEADERS = {self.response.headers}\nURL = {self.response.url}"


class YandexMetrikaClientError(YandexMetrikaApiError):
    def __init__(self, code=None, errors=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = code
        self.errors = errors

    def __str__(self):
        return f"code={self.code}, message={self.message}, errors={self.errors}"


class YandexMetrikaServerError(YandexMetrikaClientError):

    pass


class YandexMetrikaTokenError(YandexMetrikaClientError):

    pass


class YandexMetrikaLimitError(YandexMetrikaClientError):

    pass


class YandexMetrikaDownloadLogError(YandexMetrikaClientError):
    def __str__(self):
        return self.message


class BackwardCompatibilityError(TapiocaException):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return (
            f"This {self.name} is deprecated and not supported. "
            "Install a later version "
            "'pip install --upgrade async-tapi-yandex-metrika'. "
            "Info https://github.com/ilindrey/async-tapi-yandex-metrika"
        )
