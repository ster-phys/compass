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
    "path",
)


from os.path import abspath, dirname
from typing import Literal


_ROOTPATH = dirname(abspath(__file__))

_COMPASS_DATA = f"{_ROOTPATH}/compass-data"

_CPS_DATA = f"{_COMPASS_DATA}/data"
_CPS_IMG = f"{_COMPASS_DATA}/img"

_DATA = f"{_ROOTPATH}/data"
_FONT = f"{_ROOTPATH}/font"
_IMG = f"{_ROOTPATH}/img"

_DECK_IMG = f"{_IMG}/deck"
_DETAIL_IMG = f"{_IMG}/detail"


class Path(object):
    """Class defining paths for the data used by this library."""

    def card_data_dir(self) -> str:
        """Path to card data directory."""
        return f"{_CPS_DATA}/card"

    def card_data(self, num: int) -> str:
        """Path to card data."""
        return f"{self.card_data_dir()}/{num}.json"

    def hero_data_dir(self) -> str:
        """Path to hero data directory."""
        return f"{_CPS_DATA}/hero"

    def hero_data(self, num: int) -> str:
        """Path to hero data."""
        return f"{self.hero_data_dir()}/{num}.json"

    def stage_data_dir(self) -> str:
        """Path to stage data directory."""
        return f"{_CPS_DATA}/stage"

    def stage_data(self, num: int) -> str:
        """Path to stage data."""
        return f"{self.stage_data_dir()}/{num}.json"


    def card_img(self, num: int) -> str:
        """Path to card image."""
        return f"{_CPS_IMG}/card/{num}.png"

    def hero_img(self, num: int) -> str:
        """Path to hero image."""
        return f"{_CPS_IMG}/hero/{num}.png"

    def icon_img(self, num: int) -> str:
        """Path to icon image."""
        return f"{_CPS_IMG}/icon/{num}.png"

    def stage_img(self, num: int) -> str:
        """Path to stage image."""
        return f"{_CPS_IMG}/stage/{num}.png"

    @property
    def abbs_data(self) -> str:
        """Path to the file where the abbreviation is stored."""
        return f"{_DATA}/abbs.json"


    def font(self, locale: Literal["ja", "zh-TW"] = "ja") -> str:
        """Path to font file."""
        sub = "TC" if locale == "zh-TW" else "JP"
        return f"{_FONT}/NotoSans{sub}-Bold.otf"


    class Deck(object):
        """Path of images for generating deck image."""

        def frame(self, position: str, locale: Literal["ja", "zh-TW"] = "ja") -> str:
            add = ".tw" if locale == "zh-TW" else ""
            return f"{_DECK_IMG}/frame/{position}{add}.png"

        def level(self, number: str | int) -> str:
            return f"{_DECK_IMG}/level/{number}.png"

        def status(self, number: str | int) -> str:
            return f"{_DECK_IMG}/status/{number}.png"

        def blank(self) -> str:
            return f"{_DECK_IMG}/blank.jpg"

    deck = Deck()
    del Deck


    class Detail(object):
        """Path of images for generating detail image."""

        def activation(self, act: Literal["long", "none", "short"]) -> str:
            return f"{_DETAIL_IMG}/activation/{act}.png"

        def cool_time(self, number: str | int) -> str:
            return f"{_DETAIL_IMG}/cool_time/{number}.png"

        def frame(self, place: str, locale: Literal["ja", "zh-TW"] = "ja") -> str:
            add = ".tw" if locale == "zh-TW" else ""
            return f"{_DETAIL_IMG}/frame/{place}{add}.png"

        def level(self, number: str | int) -> str:
            return f"{_DETAIL_IMG}/level/{number}.png"

        def rarity(self, rarity_: Literal["N", "R", "SR", "UR"]) -> str:
            return f"{_DETAIL_IMG}/rarity/{rarity_}.png"

        def status(self, number: str | int) -> str:
            return f"{_DETAIL_IMG}/status/{number}.png"

    detail = Detail()
    del Detail

    @property
    def stage_blank(self) -> str:
        """Path to a blank stage to generate embedded stage image."""
        return f"{_IMG}/stage.png"

    @property
    def localedir(self) -> str:
        """Path to locale directory."""
        return f"{_ROOTPATH}/locale"


path = Path()

del Path
