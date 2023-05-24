from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypedDict

# tipme Copyright (c) 2023 STACiA (staciax)
# Licensed under the MIT license. Refer to the LICENSE file in the project root for more information.


if TYPE_CHECKING:
    from typing_extensions import NotRequired

# fmt: off
__all__ = (
    'Donate',
    'DonateType'
)
# fmt: on


class DonateType(TypedDict):
    datetime: str
    author: str
    amount: float
    channel: str
    reference_number: str
    message: NotRequired[str]


class Donate:
    def __init__(self, data: DonateType) -> None:
        self.author: str = data['author']
        self.amount: float = float(data['amount'])
        self.channel: str = data['channel']
        self.reference_number: str = data['reference_number']
        self.datetime: str = data['datetime']
        self.message: Optional[str] = data.get('message')

    def __repr__(self) -> str:
        return f'<Donate author={self.author!r} amount={self.amount!r} channel={self.channel!r} reference_number={self.reference_number!r} datetime={self.datetime!r} message={self.message!r}>'

    def __float__(self) -> float:
        return self.amount

    # == operator
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Donate) and self.reference_number == other.reference_number

    # != operator
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.reference_number)

    # > operator
    def __gt__(self, other: object) -> bool:
        return isinstance(other, Donate) and self.amount > other.amount

    # >= operator
    def __ge__(self, other: object) -> bool:
        return isinstance(other, Donate) and self.amount >= other.amount

    # < operator
    def __lt__(self, other: object) -> bool:
        return isinstance(other, Donate) and self.amount < other.amount

    # <= operator
    def __le__(self, other: object) -> bool:
        return isinstance(other, Donate) and self.amount <= other.amount

    # + operator
    def __add__(self, other: object) -> float:
        if not isinstance(other, Donate):
            raise TypeError(f'unsupported operand type(s) for +: \'Donate\' and \'{type(other).__name__}\'')
        return self.amount + other.amount

    # - operator
    def __sub__(self, other: object) -> float:
        if not isinstance(other, Donate):
            raise TypeError(f'unsupported operand type(s) for -: \'Donate\' and \'{type(other).__name__}\'')
        return self.amount - other.amount
