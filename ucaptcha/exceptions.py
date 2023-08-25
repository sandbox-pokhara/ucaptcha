class CaptchaException(Exception):
    pass


class WrongUserKeyException(CaptchaException):
    pass


class ZeroBalanceException(CaptchaException):
    pass


class KeyDoesNotExistException(CaptchaException):
    pass
