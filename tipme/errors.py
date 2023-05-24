# tipme Copyright (c) 2023 STACiA (staciax)
# Licensed under the MIT license. Refer to the LICENSE file in the project root for more information.

__all__ = (
    'TipmeError',
    'HTTPException',
    'NotFound',
    'InternalServerError',
)


class TipmeError(Exception):
    pass


class HTTPException(TipmeError):
    pass


class NotFound(HTTPException):
    pass


class InternalServerError(TipmeError):
    pass
