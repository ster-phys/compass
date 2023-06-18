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

__title__ = "compass"
__author__ = "ster"
__license__ = "GPL-3.0"
__copyright__ = "Copyright 2021-present ster"
__version__ = "1.2.2"


from .utils import _install_default_translator

_install_default_translator()


from .activation import Activation
from .attribute import Attribute
from .card import Card
from .data import CardData, HeroData, StageData
from .hero import Hero
from .note import Note
from .rank import Rank
from .rarity import Rarity
from .role import Role
from .stage import Stage
from .status import Parameter, Status
from .utils import get_translator


del _install_default_translator
