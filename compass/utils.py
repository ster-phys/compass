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
    "_install_default_translator",
    "ImageType",
    "add_margin",
    "convert_to_square",
    "get_translator",
    "merge_images",
    "merge_images_horizon",
    "merge_images_vertical",
)


import gettext
from glob import glob
from os.path import basename
from typing import Any, Callable, NewType

from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from PIL.PngImagePlugin import PngImageFile
from rapidfuzz.process import cdist

from .path import path


def get_translator(lang: str = "ja") -> Callable[[str], str]:
    """Defines ``_`` to translate.

    Parameters
    ----------
    lang: :class:`str`
        Target languages for translation.

    Returns
    -------
    Callable[[:class:`str`], :class:`str`]
        Obtains translator that translates to specific language.

    Usage
    -----

    ```python
    _ = get_translator()
    print(_("Target string to be translated."))
    ```

    """

    files = glob(path.localedir + "/*.pot")
    domains = list(map(lambda file: basename(file)[:-4], files))

    fallbacks = [
        gettext.translation(
            domain=domain,
            localedir=path.localedir,
            languages=(lang,),
            fallback=True,
        )
        for domain in domains
    ]

    translation = fallbacks[0]
    for fallback in fallbacks[1:]:
        translation.add_fallback(fallback)

    return translation.gettext


def _install_default_translator() -> None:
    """Installs ``_`` to translate."""

    files = glob(path.localedir + "/*.pot")
    domains = list(map(lambda file: basename(file)[:-4], files))

    files = glob(path.localedir + "/*/LC_MESSAGES")
    langs = tuple(map(lambda file: file.replace(f"{path.localedir}/", "")\
                                      .replace("/LC_MESSAGES", ""), files))

    fallbacks = [
        gettext.translation(
            domain=domain,
            localedir=path.localedir,
            languages=langs,
            fallback=True,
        )
        for domain in domains
    ]

    translation = fallbacks[0]
    for fallback in fallbacks[1:]:
        translation.add_fallback(fallback)

    translation.install()


ImageType = JpegImageFile | PngImageFile

# default background color
_bg_color = (0x2F, 0x31, 0x35, 0xFF) # 0x2F3135


def add_margin(pilimg: ImageType, /, *, top: int = 0, right: int = 0,
               bottom: int = 0, left: int = 0, color: int = _bg_color) -> PngImageFile:
    """Adds margin to ``PIL`` image.

    Parameters
    ----------
    pilimg: :class:`ImageType`
        Target ``PIL`` image which margin adding to.
    top: :class:`int`
        Size of the top margin to be added.
    right: :class:`int`
        Size of the right margin to be added.
    bottom: :class:`int`
        Size of the bottom margin to be added.
    left: :class:`int`
        Size of the left margin to be added.
    color: :class:`int`
        Color of the margin to be added.

    Returns
    -------
    :class:`PngImageFile`
        Image with margins added. The original image is not changed.

    """

    width = pilimg.width + right + left
    height = pilimg.height + top + bottom

    new_img = Image.new(pilimg.mode, (width, height), color)
    new_img.paste(pilimg, (left, top))

    return new_img.convert("RGBA")


def merge_images_horizon(*pilimgs: ImageType, color: int = _bg_color) -> PngImageFile:
    """Merges ``PIL`` images horizontally.

    Parameters
    ----------
    *pilimgs: :class:`ImageType`
        Images to merge. The images are merged in the order given
        in the argument.
    color: :class:`int`
        Color of the background added when the images are different
        sizes.

    Returns
    -------
    :class:`PngImageFile`
        Horizontally merged image. The original images are not changed.

    """

    def _merge_two_images(pilimg1: PngImageFile, pilimg2: PngImageFile) -> PngImageFile:
        """Merges two ``PIL`` images horizontally."""

        width = pilimg1.width + pilimg2.width
        height = max(pilimg1.height, pilimg2.height)

        new_img = Image.new(pilimg1.mode, (width, height), color=color)
        new_img.paste(pilimg1, (0, 0))
        new_img.paste(pilimg2, (pilimg1.width, 0))

        return new_img

    new_img = pilimgs[0].copy().convert("RGBA")
    for pilimg in pilimgs[1:]:
        new_img = _merge_two_images(new_img, pilimg.convert("RGBA"))

    return new_img


def merge_images_vertical(*pilimgs: ImageType, color: int = _bg_color) -> PngImageFile:
    """Merges ``PIL`` images vertically.

    Parameters
    ----------
    *pilimgs: :class:`ImageType`
        Images to merge. The images are merged in the order given
        in the argument.
    color: :class:`int`
        Color of the background added when the images are different
        sizes.

    Returns
    -------
    :class:`PngImageFile`
        Vertically merged image. The original images are not changed.

    """

    def _merge_two_images(pilimg1: PngImageFile, pilimg2: PngImageFile) -> PngImageFile:
        """Merges two ``PIL`` images vertically."""

        width = max(pilimg1.width, pilimg2.width)
        height = pilimg1.height + pilimg2.height

        new_img = Image.new(pilimg1.mode, (width, height), color=color)
        new_img.paste(pilimg1, (0, 0))
        new_img.paste(pilimg2, (0, pilimg1.height))

        return new_img

    new_img = pilimgs[0].copy().convert("RGBA")
    for pilimg in pilimgs[1:]:
        new_img = _merge_two_images(new_img, pilimg.convert("RGBA"))

    return new_img


def merge_images(*pilimgs: ImageType, number: int = 1, color: int = _bg_color) -> PngImageFile:
    """Merges images in a tiled format.

    Parameters
    ----------
    *pilimgs: :class:`ImageType`
        Images to merge. The images are merged in the order given
        in the argument. The horizontal direction has priority.
    number: :class:`int`
        The number of images in the horizontal direction.
    color: :class:`int`
        Color of the background added when the images are different
        sizes or the number of images is indivisible by ``number``.

    Returns
    -------
    :class:`PngImageFile`
        Vertically merged image. The original images are not changed.

    Raises
    ------
    RuntimeError
        Raised if the number of images merged horizontally is
        less than or equal to ``0``.

    """

    if number < 1:
        raise RuntimeError("The number of horizontal images must be positive.")

    horizontal_imgs: list[ImageType] = []
    for i in range(len(pilimgs)//number):
        horizontal_imgs.append(
            merge_images_horizon(*pilimgs[i*number:(i+1)*number], color=color)
        )

    if len(pilimgs)/number - len(pilimgs)//number > 0:
        horizontal_imgs.append(
            merge_images_horizon(*pilimgs[number*(len(pilimgs)//number):], color=color)
        )

    return merge_images_vertical(*horizontal_imgs, color=color)


def convert_to_square(pilimg: ImageType, color: int = _bg_color) -> PngImageFile:
    """Adds margins to make the image square.

    Parameters
    ----------
    pilimg: :class:`ImageType`
        Target ``PIL`` image which margin adding to.
    color: :class:`int`
        Color of the margin to be added.

    Returns
    -------
    :class:`PngImageFile`
        Image with margins added. The original image is not changed.

    """

    if pilimg.width == pilimg.height:
        return pilimg.copy().convert("RGBA")

    elif pilimg.width > pilimg.height:
        new_img = Image.new(pilimg.mode, (pilimg.width, pilimg.width), color)
        new_img.paste(pilimg, (0, (pilimg.width-pilimg.height)//2))
        return new_img.convert("RGBA")
    else: # pilimg.width < pilimg.height
        new_img = Image.new(pilimg.mode, (pilimg.height, pilimg.height), color)
        new_img.paste(pilimg, ((pilimg.height-pilimg.width)//2, 0))
        return new_img.convert("RGBA")


Element = NewType("Element", list[Any])

def similar(word: str,
            choices: list[Element],
            key: Callable[[Element], list[str]] = lambda el: el) -> Element:
    """Obtains an element of ``choices`` containing a string similar to ``word``.

    Parameters
    ----------
    word: :class:`str`
        Words to search for.
    choices: List[:class:`Element`]
        Sequence containing the search choices.
    key: Callable[[:class:`Element`], List[:class:`str`]]
        Function to get an object of the same type (:class:`str`) as the search
        choices from elements of ``choices``.

    Returns
    -------
    :class:`Element`
        An element of ``choices`` that contains the string the most similar to ``word``.

    """

    words: dict[str, int] = {}

    for idx, item in enumerate(choices):
        words.update({seq: idx for seq in key(item)})

    keys = list(words.keys())
    idx = cdist([word], keys).argmax()
    idx = words[keys[idx]]

    return choices[idx]
