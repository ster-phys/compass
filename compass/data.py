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
    "CardData",
    "HeroData",
    "StageData",
)


from collections import UserList
from glob import glob
from math import ceil, sqrt
from os.path import basename, splitext
from random import choice
from typing import Any, Literal, TypeVar, overload

from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngImageFile

from .attribute import Attribute
from .card import Card
from .hero import Hero
from .note import Note
from .path import path
from .rank import Rank
from .rarity import Rarity
from .role import Role
from .stage import Stage
from .status import Parameter
from .utils import (add_margin, merge_images, merge_images_horizon,
                    merge_images_vertical, similar)


CardList = TypeVar("CardList", bound="CardData")


class CardData(UserList[Card]):
    """Data of compass cards."""

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, data: CardList) -> None:
        ...

    def __init__(self, initlist: CardList | None = None) -> None:
        """Card data constructor."""
        super().__init__(initlist)

        if initlist is None:
            files = sorted(glob(path.card_data_dir() + "/*.json"))
            nums = list(map(lambda file: int(splitext(basename(file))[0]), files))

            for num in nums:
                self.data.append(Card.from_num(num))

    def __str__(self) -> str:
        return f"{len(self)} Cards' Data"

    @overload
    def __getitem__(self, index: int) -> Card:
        ...

    @overload
    def __getitem__(self, key: str) -> Card:
        ...

    @overload
    def __getitem__(self, *keys: str) -> Card:
        ...

    @overload
    def __getitem__(self, slice: slice) -> CardList:
        ...

    def __getitem__(self, *args) -> CardList | Card:
        if isinstance(args[0], str):
            if args[0].isdigit():
                return super().__getitem__(int(args[0]))
            else:
                return self._guess_card(args[0])
        elif isinstance(*args, tuple) and list(map(type, *args)) == [str] * len(*args):
            retval = self.__class__([])
            for arg in list(*args):
                retval.append(self._guess_card(arg))
            return retval
        else:
            return super().__getitem__(*args)

    def _guess_card(self, key: str) -> Card:
        """Guesses :class:`compass.Card` from the input.

        Parameters
        ----------
        key: :class:`str`
            String similar to card name or abbreviation.

        Returns
        -------
        :class:`compass.Card`
            ``Card`` judged to be most similar to the input string.

        """

        return similar(key, self.data, lambda el: [el.name] + el.abbreviations)

    def divide(self) -> dict[str, CardList]:
        """
        Divides into the following four types: ``offensive``, ``defensive``,
        ``supportive``, and ``recovery``.

        Returns
        -------
        Dict[:class:`str`, :class:`CardData`]
            The value returned is :class:`dict` and its keys are the following four.
            ``off`` for offensive cards, ``sup`` for support cards,
            ``def`` for defensive cards and ``rec`` for recovery cards.

        """
        type_dict = {"rec": ["癒",],
                     "sup": ["奪","止","閃","毒","害","人","除","押","黙","爆","弱","罠",],
                     "def": ["返","防","強",],
                     "off": ["近","周","遠","連",]}
        card_dict = {"off": self.__class__([]),
                     "def": self.__class__([]),
                     "sup": self.__class__([]),
                     "rec": self.__class__([]),}
        kind_list = ["rec", "sup", "def", "off"]

        def list_in_list(list1: list[Any], list2: list[Any]) -> bool:
            for el in list1:
                if el in list2:
                    return True
            return False

        for card in self:
            flag = False
            for kind in kind_list:
                if list_in_list(card.types, type_dict[kind]):
                    flag = True
                    card_dict[kind].append(card)
            if not flag:
                card_dict["sup"].append(card)

        return card_dict

    def get_card(self, *args: Attribute | Rarity,
                 season: bool = False, normal: bool = True, collabo: bool = True,
                 themes: list[str] | None = None) -> Card:
        """Returns data for card that satisfied the condition.

        Parameters
        ----------
        *args: :class:`compass.Attribute` | :class:`compass.Rarity`
            Specifies the condition for returns.
        season: :class:`bool`
            Whether or not to include season cards.
        normal: :class:`bool`
            Whether or not to include normal cards.
        collabo: :class:`bool`
            Whether or not to include collaboration cards.
        themes: List[:class:`str`] | None
            Arguments used when restricting to specific collaborations.

        Returns
        -------
        :class:`compass.Card`
            Returns a card that satisfies the conditions at random.

        """
        cards = self.get_cards(*args, season=season, normal=normal, collabo=collabo,
                               themes=themes)
        return choice(cards)

    def get_cards(self,
                  *args: Attribute | Rarity,
                  season: bool = False,
                  normal: bool = True,
                  collabo: bool = True,
                  themes: list[str] | None = None) -> CardList:
        """Returns data for cards that satisfied the condition.

        Parameters
        ----------
        *args: :class:`compass.Attribute` | :class:`compass.Rarity`
            Specifies the condition for returns.
        season: :class:`bool`
            Whether or not to include season cards.
        normal: :class:`bool`
            Whether or not to include normal cards.
        collabo: :class:`bool`
            Whether or not to include collaboration cards.
        themes: List[:class:`str`] | None
            Arguments used when restricting to specific collaborations.

        Returns
        -------
        :class:`CardData`
            Returns all cards that satisfy the condition.

        """

        attributes, rarities = [], []

        for arg in args:
            if isinstance(arg, Attribute):
                attributes.append(arg)
            elif isinstance(arg, Rarity):
                rarities.append(arg)

        if attributes == []:
            attributes = list(Attribute)
        if rarities == []:
            rarities = list(Rarity)

        retval = self.__class__([])
        if season:
            retval.extend(self.get_season_cards(attributes, rarities))
        if normal:
            retval.extend(self.get_normal_cards(attributes, rarities))
        if collabo:
            retval.extend(self.get_collabo_cards(attributes, rarities, themes))

        return retval

    def get_season_cards(self,
                         attributes: list[Attribute] = list(Attribute),
                         rarities: list[Rarity] = list(Rarity)) -> CardList:
        """Returns data for season cards.

        This function is intended for use inside the library, since it is
        possible to simulate the same behaviour with the ``get_cards``
        function. In fact, this function is called within the ``get_cards``
        function.

        Parameters
        ----------
        attributes: List[:class:`compass.Attribute`]
            Conditions relating to the attributes of cards.
        rarities: List[:class:`compass.Rarity`]
            Conditions relating to the rarities of cards.

        Returns
        -------
        :class:`CardData`
            Returns all **season** cards that satisfy the conditions given.

        """
        retval = self.__class__([])
        for card in self:
            if (card.rank == Rank.SEASON) and (card.rarity in rarities) and \
               (card.attribute in attributes):
                retval.append(card)
        return retval

    def get_normal_cards(self,
                         attributes: list[Attribute] = list(Attribute),
                         rarities: list[Rarity] = list(Rarity)) -> CardList:
        """Returns data for normal cards.

        This function is intended for use inside the library, since it is
        possible to simulate the same behaviour with the ``get_cards``
        function. In fact, this function is called within the ``get_cards``
        function.

        Parameters
        ----------
        attributes: List[:class:`compass.Attribute`]
            Conditions relating to the attributes of cards.
        rarities: List[:class:`compass.Rarity`]
            Conditions relating to the rarities of cards.

        Returns
        -------
        :class:`CardData`
            Returns all **normal** cards that satisfy the conditions given.

        """
        retval = self.__class__([])
        for card in self:
            if (card.note == Note.NORMAL) and (card.rarity in rarities) and \
               (card.attribute in attributes):
                retval.append(card)
        return retval

    def get_collabo_cards(self,
                          attributes: list[Attribute] = list(Attribute),
                          rarities: list[Rarity] = list(Rarity),
                          themes: list[str] | None = None) -> CardList:
        """Returns data for collaboration cards.

        This function is intended for use inside the library, since it is
        possible to simulate the same behaviour with the ``get_cards``
        function. In fact, this function is called within the ``get_cards``
        function.

        Parameters
        ----------
        attributes: List[:class:`compass.Attribute`]
            Conditions relating to the attributes of cards.
        rarities: List[:class:`compass.Rarity`]
            Conditions relating to the rarities of cards.
        themes: List[:class:`str`] | None
            Arguments used when restricting to specific collaborations.

        Returns
        -------
        :class:`CardData`
            Returns all **collaboration** cards that satisfy the conditions given.

        """
        retval = self.__class__([])
        for card in self:
            if (card.rank == Rank.COLLABO) and (card.rarity in rarities) and \
               (card.attribute in attributes):
                if themes is None or card.theme in themes:
                    retval.append(card)
        return retval

    def generate_image(self,
                       levels: list[int] | None = [50]*4,
                       locale: Literal["ja", "zh-TW", "en"] = "ja") -> PngImageFile:
        """Generates an image with processing applied.

        The behaviour depends on the number of cards.
        If the number of cards is one, an image with embedded card details
        is generated.
        When the number of cards is between two and four, an image of a deck
        with those cards is generated.
        If the number of cards is greater than these, an image of a list of
        cards is generated.

        Parameters
        ----------
        levels: Optional[List[int]]
            Cards' level.
        locale: Literal["ja", "zh-TW", "en"]
            If a corresponding image is available, it is used.

        Returns
        -------
        :class:`PngImageFile`
            Image object according to number of cards.

        Raises
        ------
        RuntimeError
            The number of cards must be at least one. If there are zero cards,
            this error is raised.

        """

        if len(self) == 0:
            raise RuntimeError("Invalid length of data.")
        elif len(self) == 1:
            retval = self[0].generate_image(level=levels[0], locale=locale)
        elif 2 <= len(self) <= 4:
            retval = self.generate_deck(levels=levels, locale=locale)
        else:
            retval = self.generate_large_image()
        return retval

    def generate_deck(self,
                      levels: list[int] | None = [50]*4,
                      locale: Literal["ja", "zh-TW", "en"] = "ja") -> PngImageFile:
        """Generates deck image with processing applied.

        Parameters
        ----------
        levels: Optional[List[int]]
            Cards' level.
        locale: Literal["ja", "zh-TW", "en"]
            If a corresponding image is available, it is used.

        Returns
        -------
        :class:`PngImageFile`
            Deck image object.

        Raises
        ------
        RuntimeError
            The number of cards must be between one and four.
            If they do not belong to this range, raises error.

        """

        if not (1 <= len(self) <= 4):
            raise RuntimeError("Length of data must be between 1 and 4.")

        while(len(self) > len(levels)):
            levels.extend([50])

        pilimages = [card.image for card in self]

        for _ in range(4 - len(self)):
            pilimages.append(Image.open(path.deck.blank()))

        bg_color = (0xEC, 0xED, 0xED, 0xFF) # 0xECEDED

        imgprocs = []
        imgprocs.append(add_margin(pilimages[0], top=10, right=10, bottom=10, left=80, color=bg_color))
        imgprocs.append(add_margin(pilimages[1], top=10, right=10, bottom=10, left=10, color=bg_color))
        imgprocs.append(add_margin(pilimages[2], top=10, right=10, bottom=10, left=10, color=bg_color))
        imgprocs.append(add_margin(pilimages[3], top=10, right=80, bottom=10, left=10, color=bg_color))

        img_deck = merge_images_horizon(*imgprocs, color=bg_color)
        img_deck = img_deck.resize((795, (img_deck.height *795) //img_deck.width))

        img_above = Image.open(path.deck.frame("above", locale))
        img_below = Image.open(path.deck.frame("below", locale))

        img_deck_main = Image.new("RGBA", img_deck.size, (255, 255, 255, 0))
        img_deck_alpha = Image.new("RGBA", img_deck.size, (255, 255, 255, 0))

        img_deck_main.paste(img_deck, (0, 0))
        for i in range(len(levels)):
            img_deck_alpha.paste(
                Image.open(path.deck.level(str(levels[i]))).resize(size=(40, 23)),
                (75 +170 *i, 65)
            )

        img_deck = Image.alpha_composite(img_deck_main,img_deck_alpha)

        img = merge_images_vertical(*[img_above, img_deck, img_below], color=bg_color)

        status = Parameter(0, 0, 0)
        for i in range(len(self)):
            status += self[i].status[f"lv{levels[i]:02d}"]

        atk_width = int(status.attack *(142 /480))
        def_width = int(status.defense *(56 /95))
        phs_width = int(status.physical *(77 /2331))

        atk_width = 590 if atk_width > 590 else atk_width
        def_width = 590 if def_width > 590 else def_width
        phs_width = 590 if phs_width > 590 else phs_width

        draw = ImageDraw.Draw(img)
        draw.rectangle((157, 394, 157 +atk_width, 425), fill=(196, 216, 106))
        draw.rectangle((157, 440, 157 +def_width, 471), fill=(196, 216, 106))
        draw.rectangle((157, 486, 157 +phs_width, 517), fill=(196, 216, 106))

        img_alpha = Image.new("RGBA", img.size, (255, 255, 255, 0))

        def fill_b(status: float, number: int) -> str:
            return ("b"*number + str(int(status)))[-number:]

        for i in range(5):
            img_alpha.paste(
                Image.open(path.deck.status(fill_b(status.attack, 5)[i])),
                (660 +16 *i, 400)
            )
            img_alpha.paste(
                Image.open(path.deck.status(fill_b(status.defense, 5)[i])),
                (660 +16 *i, 446)
            )
            img_alpha.paste(
                Image.open(path.deck.status(fill_b(status.physical, 5)[i])),
                (660 +16 *i, 492)
            )

        return Image.alpha_composite(img, img_alpha).convert("RGBA")

    def generate_large_image(self) -> PngImageFile:
        """Generates large image with processing applied.

        Returns
        -------
        :class:`PngImageFile`
            Image object with images of cards in a row.

        Raises
        ------
        RuntimeError
            The number of cards must be at least one. If there are zero cards,
            this error is raised.

        """

        if len(self) == 0:
            raise RuntimeError("Invalid length of data.")

        if len(self) == 1:
            return self[0].image
        else:
            imgs = [card.image for card in self]
            number = int(ceil(sqrt(len(self))))
            return merge_images(*imgs, number=number)


HeroList = TypeVar("HeroList", bound="HeroData")


class HeroData(UserList[Hero]):
    """Data of compass heroes."""

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, data: HeroList) -> None:
        ...

    def __init__(self, initlist: HeroList | None = None) -> None:
        """Hero data constructor."""
        super().__init__(initlist)

        if initlist is None:
            files = sorted(glob(path.hero_data_dir() + "/*.json"))
            nums = list(map(lambda file: int(splitext(basename(file))[0]), files))

            for num in nums:
                self.data.append(Hero.from_num(num))

    def __str__(self) -> str:
        return f"{len(self)} Heroes' Data"

    @overload
    def __getitem__(self, index: int) -> Hero:
        ...

    @overload
    def __getitem__(self, key: str) -> Hero:
        ...

    @overload
    def __getitem__(self, slice: slice) -> HeroList:
        ...

    def __getitem__(self, *args) -> HeroList | Hero:
        if isinstance(args[0], str):
            if args[0].isdigit():
                return super().__getitem__(int(args[0]))
            else:
                return self._guess_hero(args[0])
        else:
            return super().__getitem__(*args)

    def _guess_hero(self, key: str) -> Hero:
        """Guesses :class:`compass.Hero` from the input.

        Parameters
        ----------
        key: :class:`str`
            String similar to hero name.

        Returns
        -------
        :class:`compass.Hero`
            ``Hero`` judged to be most similar to the input string.

        """

        return similar(key, self.data, lambda el: [el.name])

    def get_hero(self, *roles: Role,
                 original: bool = True, collabo: bool = True) -> Hero:
        """Returns data for hero that satisfied the condition.

        Parameters
        ----------
        *roles: :class:`compass.Role`
            Specifies the condition for returns.
        original: :class:`bool`
            Whether or not to include original heroes.
        collabo: :class:`bool`
            Whether or not to include collabo heroes.

        Returns
        -------
        :class:`compass.Hero`
            Returns a hero that satisfies the conditions at random.

        """
        heroes = self.get_heroes(*roles, original=original, collabo=collabo)
        return choice(heroes)

    def get_heroes(self, *roles: Role,
                   original: bool = True, collabo: bool = True) -> HeroList:
        """Returns data for heroes that satisfied the condition.

        Parameters
        ----------
        *roles: :class:`compass.Role`
            Specifies the condition for returns.
        original: :class:`bool`
            Whether or not to include original heroes.
        collabo: :class:`bool`
            Whether or not to include collabo heroes.

        Returns
        -------
        :class:`HeroData`
            Returns all heroes that satisfy the condition.

        """

        retval = self.__class__([])
        for hero in self:
            if (hero.role in roles) and \
               ((not hero.is_collabo and original) or (hero.is_collabo and collabo)):
                retval.append(hero)

        return retval


StageList = TypeVar("StageList", bound="StageData")


class StageData(UserList[Stage]):
    """Data of compass stages."""

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, data: StageList) -> None:
        ...

    def __init__(self, initlist: StageList | None = None) -> None:
        """Stage data constructor."""
        super().__init__(initlist)

        if initlist is None:
            files = sorted(glob(path.stage_data_dir() + "/*.json"))
            ids = list(map(lambda file: int(splitext(basename(file))[0]), files))

            for id in ids:
                self.data.append(Stage.from_id(id))

    def __str__(self) -> str:
        return f"{len(self)} Stages' Data"

    @overload
    def __getitem__(self, index: int) -> Stage:
        ...

    @overload
    def __getitem__(self, key: str) -> Stage:
        ...

    @overload
    def __getitem__(self, slice: slice) -> StageList:
        ...

    def __getitem__(self, *args) -> StageList | Stage:
        if isinstance(args[0], str):
            if args[0].isdigit():
                return super().__getitem__(int(args[0]))
            else:
                return self._guess_stage(args[0])
        else:
            return super().__getitem__(*args)

    def _guess_stage(self, key: str) -> Stage:
        """Guesses :class:`compass.Stage` from the input.

        Parameters
        ----------
        key: :class:`str`
            String similar to stage name.

        Returns
        -------
        :class:`compass.Stage`
            ``Stage`` judged to be most similar to the input string.

        """

        return similar(key, self.data, lambda el: [el.name])

    def get_stage(self, number: int = 3) -> Stage:
        """Returns data for stage that satisfied the condition.

        Parameters
        ----------
        number: :class:`int`
            Number of people per team.

        Returns
        -------
        :class:`compass.Stage`
            Returns a stage that satisfies the condition at random.

        """
        stages = self.get_stages(number)
        return choice(stages)

    def get_stages(self, number: int = 3) -> StageList:
        """Returns data for stages that satisfied the condition.

        Parameters
        ----------
        number: :class:`int`
            Number of people per team.

        Returns
        -------
        :class:`StageData`
            Returns all stages that satisfies the condition.

        """
        retval = self.__class__([])
        for stage in self:
            if stage.number == number and stage.now_available:
                retval.append(stage)

        return retval
