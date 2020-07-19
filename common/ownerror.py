# -*- coding: utf-8 -*-
"""
@Time ： 2019/12/26 11:51
@Auth ： zhulk

"""
class UnSupportBrowserTypeError(Exception):
    pass


class UnSupportDriverModeError(Exception):
    pass


class SendKeysNoneError(Exception):
    pass


class ClickElementTooMuchError(Exception):
    pass


class UrlError(Exception):
    pass

class RouterNameRepeatError(Exception):
    pass