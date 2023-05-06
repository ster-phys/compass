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
    "Attribute",
)


from enum import Enum
from typing import TypeVar


Self = TypeVar("Self", bound="Attribute")


class Attribute(str, Enum):
    """Attribute of the card."""

    WATER = _("水") # type: ignore
    FIRE = _("火") # type: ignore
    WOOD = _("木") # type: ignore

    def __str__(self) -> str:
        return self.value

    def __lt__(self, obj: str | Self) -> bool:
        obj = self.__class__(obj)
        return (self, obj) in [(self.WATER, self.WOOD), (self.WOOD, self.FIRE),
                               (self.FIRE, self.WATER),]

    def __le__(self, obj: str | Self) -> bool:
        return self.__lt__(obj) or self.__eq__(obj)

    def __gt__(self, obj: str | Self) -> bool:
        return not self.__le__(obj)

    def __ge__(self, obj: str | Self) -> bool:
        return not self.__lt__(obj)

    @property
    def color(self) -> int:
        """Obtains this attribute color."""
        d = {
            self.WATER: 0x0D1BCE,
            self.FIRE: 0xE7382A,
            self.WOOD: 0x59B93A
        }
        return d[self]
