# compass

[![python3.10](https://img.shields.io/badge/python-3.10-3776AB.svg?logo=python)](https://docs.python.org/3.10/) [![LICENSE](https://img.shields.io/github/license/ster-phys/bot_cps)](./LICENSE) [![gitlocalized](https://gitlocalize.com/repo/8640/whole_project/badge.svg)](https://gitlocalize.com/repo/8640) [![Discord](https://img.shields.io/discord/834671256367530014.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](http://discord.gg/Pmt5BetUqb) [![Twitter Follow](https://img.shields.io/twitter/follow/bot_cps?style=social)](https://twitter.com/bot_cps)

A library for easy handling of #compass data.

The main items provided by this library are cards, heroes and stages.

## How To Install

Execute the following.

```sh
python3.10 -m pip install "compass@git+https://github.com/ster-phys/compass.git"
```

## Quick Example

The data provided by this library are available as `compass.CardData`, `compass.HeroData` and `compass.StageData`, which is a list of `compass.Card` class, a list of `compass.Hero` class and a list of `compass.Stage` class, respectively.

```python
>>> from compass import CardData
>>> cd = CardData()
>>> cd.get_card()
Card(_num=455253, _name='【BEATLESS】レイシア', _rarity=<Rarity.R: 'R'>, _types=['遠'], _cool_time=20, _activation=<Activation.SHORT: '短'>, _attribute=<Attribute.WATER: '水'>, _rank=<Rank.COLLABO: 'コラボガチャ'>, _ability='長射程のエネルギー攻撃（小ダメージ）', ...)
>>> cd["ノガド"]
Card(_num=455069, _name='究極系ノーガード戦法', _rarity=<Rarity.UR: 'UR'>, _types=['防'], _cool_time=30, _activation=<Activation.SHORT: '短'>, _attribute=<Attribute.FIRE: '火'>, _rank=<Rank.F: 'F'>, _ability='被ダメージを80%減らす（8秒間）', ...)
>>> cd["オールレンジ"].generate_image().show()
# A window opens and an image is displayed.
```

For translation, it is possible to do the following.

```python
>>> from compass import Role, get_translator
>>> _ = get_translator("zh-TW")
>>> print(_(Role.ATTACKER))
戰士
>>> _ = get_translator("en")
>>> print(_(Role.ATTACKER))
attacker
```

For other uses, check the documentation! (in preparation)

## Notes

The licence is for the source code and text.
This means that the copyright of #compass cards, hero images, etc. remains with [Game Publisher](https://app.nhn-playart.com/compass/).
