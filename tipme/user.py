# tipme Copyright (c) 2023 STACiA (staciax)
# Licensed under the MIT license. Refer to the LICENSE file in the project root for more information.

from typing import TypedDict

# fmt: off
__all__ = (
    'User',
    'UserType'
)
# fmt: on


class UserType(TypedDict):
    username: str
    email: str


class User:
    def __init__(self, data: UserType) -> None:
        self.username: str = data['username']
        self.email: str = data['email']

    def __repr__(self) -> str:
        return f'<User username={self.username} email={self.email}>'
