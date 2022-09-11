"""ロボットモジュール.

ロボットのクラス（構造体）を定義したモジュール
@author: kodama0720
"""

from enum import Enum
from dataclasses import dataclass
from coordinate import Coordinate


class Direction(Enum):
    """方位の列挙体.

    Attributes:
        N: 北
        NE: 北東
        E = 東
        SE = 南東
        S = 南
        SW = 南西
        W = 西
        NW = 北西
    """

    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7


@dataclass
class Robot:
    """仮想走行体のデータクラス.

    Attributes:
        coord: 座標
        direct: 方位
        edge: エッジ "left" or "right" or "none"
    """

    coord: Coordinate
    direct: Direction
    edge: str
