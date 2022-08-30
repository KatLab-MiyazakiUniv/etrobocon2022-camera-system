"""ロボットモジュール.

ロボットのクラス（構造体）を定義したモジュール
@author: kodama0720
"""

from enum import Enum


class Direction(Enum):
    """方位の列挙体."""

    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7


class Robot:
    """仮想走行体クラス."""

    coord = [0, 0]
    direct = Direction.N.value
