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
    "Role",
)


from enum import Enum


class Role(str, Enum):
    """Role of the hero."""

    ATTACKER = _("アタッカー") # type: ignore
    SPRINTER = _("スプリンター") # type: ignore
    GUNNER = _("ガンナー") # type: ignore
    TANK = _("タンク") # type: ignore

    def __str__(self) -> str:
        return self.value
