"""座標モジュール.

座標を保持するクラスを定義している
@author: kodama0720
"""

from dataclasses import dataclass


@dataclass
class Coordinate:
    """座標のデータクラス.

    Attributes:
        x: x座標
        y: y座標
    """

    x: int
    y: int
