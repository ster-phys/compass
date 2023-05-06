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
    "Parameter",
    "Status",
)


from collections import UserDict
from copy import copy
from dataclasses import dataclass
from typing import TypeVar


Self = TypeVar("Self", bound="Parameter")


@dataclass
class Parameter(object):
    """Parameter of the compass data."""

    attack: float
    defense: float
    physical: float

    def __iadd__(self, obj: Self) -> Self:
        self.attack += obj.attack
        self.defense += obj.defense
        self.physical += obj.physical
        return self

    def __add__(self, obj: Self) -> Self:
        tmp = copy(self)
        tmp.__iadd__(obj)
        return tmp

    def __isub__(self, obj: Self) -> Self:
        self.attack -= obj.attack
        self.defense -= obj.defense
        self.physical -= obj.physical
        return self

    def __sub__(self, obj: Self) -> Self:
        tmp = copy(self)
        tmp.__isub__(obj)
        return tmp

    def __imul__(self, obj: Self) -> Self:
        self.attack *= obj.attack
        self.defense *= obj.defense
        self.physical *= obj.physical
        return self

    def __mul__(self, obj: Self) -> Self:
        tmp = copy(self)
        tmp.__imul__(obj)
        return tmp

    def __itruediv__(self, obj: Self) -> Self:
        self.attack /= obj.attack
        self.defense /= obj.defense
        self.physical /= obj.physical
        return self

    def __truediv__(self, obj: Self) -> Self:
        tmp = copy(self)
        tmp.__itruediv__(obj)
        return tmp


class Status(UserDict):
    """Status of the card."""

    def __init__(self,
                 atk: dict[str, int | float],
                 def_: dict[str, int | float],
                 phs: dict[str, int | float]) -> None:
        """Status of the card.

        Parameters
        ----------
        atk: Dict[:class:`str`, :class:`int` | :class:`float`]
            Card attack parameter.
        def_: Dict[:class:`str`, :class:`int` | :class:`float`]
            Card defense parameter.
        phs: Dict[:class:`str`, :class:`int` | :class:`float`]
            Card physical parameter.

        """

        super().__init__()
        for lv in [1, 20, 30, 40, 50, 60]:
            param = Parameter(atk[f"lv{lv:02d}"], def_[f"lv{lv:02d}"], phs[f"lv{lv:02d}"])
            self.update({f"lv{lv:02d}": param})
