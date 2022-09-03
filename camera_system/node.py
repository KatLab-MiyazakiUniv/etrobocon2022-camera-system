"""ノードモジュール.

ノードを保持するクラスを定義している
@author: kodama0720
"""

from enum import Enum
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


class Node:
    """ノードを保持するクラス."""

    def __init__(self, block_id: int, coord: Coordinate) -> None:
        """Nodeのコンストラクタ.

        Args:
            block_id(int): ブロックID
            coord(Coordinate): 座標
            node_type(NodeType): ノードの型
        """
        self.block_id = block_id
        self.coord = coord
        if coord.x % 2 != 0 and coord.y % 2 != 0:
            self.node_type = NodeType.BLOCK.value
        elif coord.x % 2 == 0 and coord.y % 2 == 0:
            self.node_type = NodeType.CROSS.value
        else:
            self.node_type = NodeType.MIDDLE.value
