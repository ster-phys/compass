"""
A library that provides Compass Data Structures

The GNU General Public License v3.0 (GPL-3.0)

Copyright (C) 2021-present ster <ster.physics@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

"""

__all__ = (
    "Rank",
)


from enum import Enum
from typing import TypeVar


Self = TypeVar("Self", bound="Rank")

_rank_order = ("F", "E", "D", "C", "B", "A", "S1",)


class Rank(str, Enum):
    """Available rank of the card."""
    # normal
    S1 = "S1"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"

    # others
    EVENT = _("イベント") # type: ignore
    COLLABO = _("コラボガチャ") # type: ignore
    SEASON = _("シーズン報酬") # type: ignore

    def __str__(self) -> str:
        return self.value

    @property
    def is_collabo(self) -> bool:
        return self.value not in _rank_order

    def __lt__(self, obj: str | Self) -> bool:
        obj = self.__class__(obj)
        if self.is_collabo or obj.is_collabo:
            return False
        return _rank_order.index(self.value) < _rank_order.index(obj.value)

    def __le__(self, obj: str | Self) -> bool:
        obj = self.__class__(obj)
        if self.is_collabo or obj.is_collabo:
            return False
        return _rank_order.index(self.value) <= _rank_order.index(obj.value)

    def __gt__(self, obj: str | Self) -> bool:
        obj = self.__class__(obj)
        if self.is_collabo or obj.is_collabo:
            return False
        return _rank_order.index(self.value) > _rank_order.index(obj.value)

    def __ge__(self, obj: str | Self) -> bool:
        obj = self.__class__(obj)
        if self.is_collabo or obj.is_collabo:
            return False
        return _rank_order.index(self.value) >= _rank_order.index(obj.value)
