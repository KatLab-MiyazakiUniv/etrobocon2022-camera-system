"""ノードモジュール.

ノードを保持するクラスを定義している
@author: kodama0720
"""

from enum import Enum
from dataclasses import dataclass
from coordinate import Coordinate


class NodeType(Enum):
    """ノードタイプの列挙体.

    Attributes:
        CROSS: 交点
        MIDDLE: 中点
        BLOCK: ブロック置き場
    """

    CROSS = 0
    MIDDLE = 1
    BLOCK = 2


@dataclass
class Node:
    """ノードのデータクラス.

    Attributes:
        block_id: ブロックID
        coord: 座標
        node_type: ノードの型 (0:交点 1:中点 2:ブロック置き場)
    """

    block_id: int
    coord: Coordinate
    node_type: NodeType
