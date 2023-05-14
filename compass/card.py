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
    "Card",
)


import json
from dataclasses import dataclass
from typing import TypeVar

from PIL import Image, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngImageFile

from .activation import Activation
from .attribute import Attribute
from .note import Note
from .path import path
from .rank import Rank
from .rarity import Rarity
from .status import Parameter, Status
from .utils import get_translator, merge_images_vertical


Self = TypeVar("Self", bound="Card")


@dataclass
class Card(object):
    """Class of a card data."""

    _num: int
    _name: str
    _rarity: Rarity
    _types: list[str]
    _cool_time: int
    _activation: Activation
    _attribute: Attribute
    _rank: Rank
    _ability: str
    _status: Status
    _note: Note
    _theme: str

    _abbreviations: list[str]

    _img_path: str = ""

    def __post_init__(self) -> None:
        self._img_path = path.card_img(self.num)

    def __str__(self) -> str:
        return "【" + "・".join(self.types) + "】" + self.name

    @property
    def num(self) -> int:
        """Number of this card."""
        return self._num

    @property
    def name(self) -> str:
        """Name of this card."""
        return self._name

    @property
    def rarity(self) -> Rarity:
        """Rarity of this card."""
        return self._rarity

    @property
    def types(self) -> list[str]:
        """List of this card type."""
        return self._types

    @property
    def cool_time(self) -> int:
        """Cool time of this card."""
        return self._cool_time

    @property
    def activation(self) -> Activation:
        """Activation time of this card."""
        return self._activation

    @property
    def attribute(self) -> Attribute:
        """Attribute of this card."""
        return self._attribute

    @property
    def rank(self) -> Rank:
        """Available rank of this card."""
        return self._rank

    @property
    def ability(self) -> str:
        """Ability and details of this card."""
        return self._ability

    @property
    def status(self) -> Status:
        """Status of this card."""
        return self._status

    @property
    def note(self) -> Note:
        """Note for this card."""
        return self._note

    @property
    def theme(self) -> str:
        """Theme of this card."""
        return self._theme

    @property
    def abbreviations(self) -> list[str]:
        """Abbreviations of this card."""
        return self._abbreviations

    @property
    def img_path(self) -> str:
        """Path to this card image."""
        return self._img_path

    @property
    def is_collabo(self) -> bool:
        """Whether this card is a collaboration or not."""
        return self.rank.is_collabo

    @property
    def image(self) -> PngImageFile:
        """Obtains this card's image as :class:`PIL.PngImagePlugin.PngImageFile`"""
        return Image.open(self.img_path).convert("RGBA")

    @classmethod
    def from_num(cls, num: int) -> Self:
        """Class method to construct :class:`compass.Card` from card number.

        Parameters
        ----------
        num: :class:`int`
            The number of this card.

        Returns
        -------
        :class:`compass.Card`
            :class:`compass.Card` object of this number.

        """

        filepath = path.card_data(num)
        with open(filepath, "r") as f:
            data = json.load(f)

        kwargs = {}
        kwargs["_num"] = data["num"]
        kwargs["_name"] = data["name"]
        kwargs["_rarity"] = Rarity(data["rarity"])
        kwargs["_types"] = data["types"]
        kwargs["_cool_time"] = data["cool_time"]
        kwargs["_activation"] = Activation(data["activation"])
        kwargs["_attribute"] = Attribute(data["attribute"])
        kwargs["_rank"] = Rank(data["rank"])
        kwargs["_ability"] = data["ability"]
        kwargs["_status"] = Status(data["atk"], data["def"], data["phs"])
        kwargs["_note"] = Note(data["note"])
        kwargs["_theme"] = data["theme"]

        with open(path.abbs_data, "r") as f:
            abbs = json.load(f)

        kwargs["_abbreviations"] = abbs.get(str(data["num"]), [])

        return cls(**kwargs)

    def generate_image(self, level: int = 50, locale: str = "ja") -> PngImageFile:
        """Generates an image with processing applied.

        Generates an image with embedded details such as card effects
        and cool time.

        Parameters
        ----------
        level: :class:`int`
            Level of the card to be displayed.
        locale: :class:`str`
            If a corresponding image is available, it is used.

        Returns
        -------
        :class:`PngImageFile`
            Generated image object.

        """

        font = ImageFont.truetype(path.font(locale), 26)

        img_above = Image.open(path.detail.frame("above", locale))
        img_above.paste(Image.open(path.detail.rarity(self.rarity.name)), (46, 30))

        _ = get_translator(locale)
        name = _(self.name)
        draw = ImageDraw.Draw(img_above)
        draw.text((125, 24), name.replace("∗", "＊"), (255, 255, 255), font=font)
        img_above.paste(Image.open(path.detail.level(level)), (78, 35))

        img_below = Image.open(path.detail.frame("below", locale))

        status: Parameter = self.status.get(f"lv{level:02d}")

        atk_width = int(status.attack *2 /3)
        def_width = int(status.defense *17 /12)
        phs_width = int(status.physical *11 /140)

        atk_width = 336 if atk_width > 336 else atk_width
        def_width = 336 if def_width > 336 else def_width
        phs_width = 336 if phs_width > 336 else phs_width

        draw = ImageDraw.Draw(img_below)
        draw.rectangle((150,  87, 150 +atk_width, 118), fill=(196, 216, 106))
        draw.rectangle((150, 143, 150 +def_width, 174), fill=(196, 216, 106))
        draw.rectangle((150, 199, 150 +phs_width, 230), fill=(196, 216, 106))

        img_below_alpha = Image.new("RGBA", img_below.size, (255, 255, 255, 0))

        def fill_b(status: float, number: int) -> str:
            return ("b" *number +str(int(status)))[-number:]

        for i in range(4):
            img_below_alpha.paste(Image.open(path.detail.status(fill_b(status.attack, 4)[i])),(419 +16 *i, 97))
            img_below_alpha.paste(Image.open(path.detail.status(fill_b(status.defense, 4)[i])),(419 +16 *i, 153))
            img_below_alpha.paste(Image.open(path.detail.status(fill_b(status.physical, 4)[i])),(419 +16 *i, 209))

        img_below = Image.alpha_composite(img_below, img_below_alpha)
        img_below.paste(Image.open(path.detail.activation(self.activation.name.lower())), (624, 15))

        cool = f"bb{self.cool_time}"[-3:]
        for i in range(3):
            img_below.paste(Image.open(path.detail.cool_time(cool[i])), (268 +19 *i, 21))
        img_below.paste(Image.open(path.detail.cool_time("sec")), (332, 15))

        _ = get_translator(locale)
        ability = _(self.ability)
        ability = ability.translate(str.maketrans({chr(0x0021 +i): chr(0xFF01 +i) for i in range(94)}))
        ability = [ability[i *19: (i +1) *19] for i in range(len(ability) //19 +1)]
        ability = ability[:-1] if ability[-1] == "" else ability
        spacing = 5 - len(ability)

        img_middle = Image.open(path.detail.frame("middle", locale))
        pilimg_list = [img_middle for _ in range(len(ability) -1)]
        pilimg_list = [img_above] + pilimg_list + [img_below]
        ability = "\n".join(ability)
        img = merge_images_vertical(*pilimg_list, color=(0xEC, 0xED, 0xED, 0xFF)) # 0xECEDED
        draw = ImageDraw.Draw(img)
        draw.text((261, 66), ability, (160, 160, 160), font=font, spacing=spacing)

        return img.convert("RGBA")
