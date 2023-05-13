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
    "Hero",
)


import json
from dataclasses import dataclass
from random import choice
from typing import TypeVar

from PIL import Image
from PIL.PngImagePlugin import PngImageFile

from .path import path
from .role import Role
from .status import Parameter


Self = TypeVar("Self", bound="Hero")


@dataclass
class Hero(object):
    """Class of a hero data."""

    _num: int
    _id: int
    _name: str
    _role: Role
    _parameter: Parameter
    _setname: str
    _speed: float
    _ultname: str
    _ultinvincible: str
    _ult: str
    _haname: str
    _ha: str
    _abilityname: str
    _ability: str
    _collabo: bool

    _img_path: str = ""
    _iconpath: str = ""

    def __post_init__(self) -> None:
        self._img_path = path.hero_img(self.num)
        self._iconpath = path.icon_img(self.num)

    def __str__(self) -> str:
        return f"{self.id:03}_{self.setname}"

    @property
    def num(self) -> int:
        """Number of this hero."""
        return self._num

    @property
    def id(self) -> int:
        """ID of this hero."""
        return self._id

    @property
    def name(self) -> str:
        """Name of this hero."""
        return self._name

    @property
    def role(self) -> Role:
        """Role of this hero."""
        return self._role

    @property
    def parameter(self) -> Parameter:
        """Parameter of this hero."""
        return self._parameter

    @property
    def setname(self) -> str:
        """The shortened name of this hero."""
        return self._setname

    @property
    def speed(self) -> float:
        """Movement speed of this hero."""
        return self._speed

    @property
    def ultname(self) -> str:
        """Name of this hero's ultimate skill."""
        return self._ultname

    @property
    def ultinvincible(self) -> str:
        """Invincibility time of this hero's ultimate skill."""
        return self._ultinvincible

    @property
    def ult(self) -> str:
        """Ultimate skill of this hero."""
        return self._ult

    @property
    def haname(self) -> str:
        """Name of this hero's hero action."""
        return self._haname

    @property
    def ha(self) -> str:
        """Hero action of this hero."""
        return self._ha

    @property
    def abilityname(self) -> str:
        """Name of this hero's hero ability."""
        return self._abilityname

    @property
    def ability(self) -> str:
        """Hero ability of this hero."""
        return self._ability

    @property
    def is_collabo(self) -> bool:
        """Whether this hero is a collaborative hero or not."""
        return self._collabo

    @property
    def img_path(self) -> str:
        """Path to this hero image."""
        return self._img_path

    @property
    def iconpath(self) -> str:
        """Path to this hero's icon."""
        return self._iconpath

    @property
    def image(self) -> PngImageFile:
        """Obtains this hero's image as :class:`PIL.PngImagePlugin.PngImageFile`."""
        return Image.open(self.img_path).convert("RGBA")

    @property
    def icon(self) -> PngImageFile:
        """Obtains this hero's icon as :class:`PIL.PngImagePlugin.PngImageFile`."""
        return Image.open(self.iconpath).convert("RGBA")

    @property
    def color(self) -> int:
        """Obtains main color of this hero."""
        img = self.icon
        x, y = choice(range(img.size[0])), choice(range(img.size[1]))
        r, g, b, a = img.getpixel((x, y))
        return (((r << 8) + g) << 8) + b

    @classmethod
    def from_num(cls, num: int) -> Self:
        """Class method to construct :class:`compass.Hero` from hero number.

        Parameters
        ----------
        num: :class:`int`
            The number of this hero.

        Returns
        -------
        :class:`compass.Hero`
            :class:`compass.Hero` object of this number.

        """

        filepath = path.hero_data(num)
        with open(filepath, "r") as f:
            data = json.load(f)

        kwargs = {}
        kwargs["_num"] = data["num"]
        kwargs["_id"] = data["id"]
        kwargs["_name"] = data["name"]
        kwargs["_role"] = Role(data["role"])
        kwargs["_parameter"] = Parameter(data["atk"], data["def"], data["phs"])
        kwargs["_setname"] = data["setname"]
        kwargs["_speed"] = data["speed"]
        kwargs["_ultname"] = data["ultname"]
        kwargs["_ultinvincible"] = data["ultinvincible"]
        kwargs["_ult"] = data["ult"]
        kwargs["_haname"] = data["haname"]
        kwargs["_ha"] = data["ha"]
        kwargs["_abilityname"] = data["abilityname"]
        kwargs["_ability"] = data["ability"]
        kwargs["_collabo"] = data["collabo"]

        return cls(**kwargs)
