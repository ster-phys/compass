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
    "Stage",
)


import json
from dataclasses import dataclass
from typing import Literal, TypeVar

from PIL import Image, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngImageFile

from .path import path
from .utils import get_translator


Self = TypeVar("Self", bound="Stage")


@dataclass
class Stage(object):
    """Class of a stage data."""

    _id: int
    _name: str
    _description: str
    _number: int
    _portal: int
    _official: bool
    _now: bool

    _img_path: str = ""

    def __post_init__(self) -> None:
        self._img_path = path.stage_img(self.id)

    def __str__(self) -> str:
        return f"【{self.number}on{self.number}】{self.name}"

    @property
    def id(self) -> int:
        """ID of this card."""
        return self._id

    @property
    def name(self) -> str:
        """Name of this stage."""
        return self._name

    @property
    def description(self) -> str:
        """Description of this stage."""
        return self._description

    @property
    def number(self) -> int:
        """Number of people per team on this stage."""
        return self._number

    @property
    def portal(self) -> int:
        """Number of portals on this stage."""
        return self._portal

    @property
    def is_official(self) -> bool:
        """Whether the stage is official or not."""
        return self._official

    @property
    def now_available(self) -> bool:
        """Whether the stage is available for regular matches."""
        return self._now

    @property
    def img_path(self) -> str:
        """Path to this stage's image."""
        return self._img_path

    @property
    def image(self) -> PngImageFile:
        """Obtains this stage's image as :class:`PIL.PngImagePlugin.PngImageFile`."""
        return Image.open(self.img_path).convert("RGBA")

    @classmethod
    def from_id(cls, id: int) -> Self:
        """Class method to construct :class:`compass.Stage` from stage id.

        Parameters
        ----------
        id: :class:`int`
            The ID of this stage.

        Returns
        -------
        :class:`compass.Stage`
            :class:`compass.Stage` object of this ID.

        """

        filepath = path.stage_data(id)
        with open(filepath, "r") as f:
            data = json.load(f)

        kwargs = {}
        kwargs["_id"] = data["id"]
        kwargs["_name"] = data["name"]
        kwargs["_description"] = data["description"]
        kwargs["_number"] = data["number"]
        kwargs["_portal"] = data["portal"]
        kwargs["_official"] = data["official"]
        kwargs["_now"] = data["now"]

        return cls(**kwargs)

    def generate_image(self,
                       locale: Literal["ja", "zh-TW", "en"] = "ja") -> PngImageFile:
        """Generates an image with processing applied.

        Generates an image with embedded details such as stage name
        and description.

        Parameters
        ----------
        locale: Literal["ja", "zh-TW", "en"]
            If a corresponding image is available, it is used.

        Returns
        -------
        :class:`PngImageFile`
            Generated image object.

        """

        base = Image.open(path.stage_blank).convert("RGBA")

        img = Image.new("RGBA", base.size, color=(0xFF, 0xFF, 0xFF, 0x00))
        img.paste(self.image, (46, 23))

        base = Image.alpha_composite(base, img)

        font = ImageFont.truetype(path.font(locale))

        draw = ImageDraw.Draw(base)

        _ = get_translator(locale)
        name = _(self.name)
        font = ImageFont.truetype(path.font(locale), size=31)
        draw.text((47, 165), name, (0x00, 0x00, 0x00), font=font)

        _ = get_translator(locale)
        description = _(self.description)
        font = ImageFont.truetype(path.font(locale), size=25)
        draw.text((47, 210), description, (0x64, 0x64, 0x64), font=font)

        _ = get_translator(locale)
        select = _("選択")
        font = ImageFont.truetype(path.font(locale), size=28)
        draw.text((614, 205), select, (0xFF, 0xFF, 0xFF), font=font, anchor="mm", align="center")

        return base.convert("RGBA")
