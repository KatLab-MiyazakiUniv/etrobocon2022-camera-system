"""ノードモジュール.

ノードを保持するクラスを定義している
@author: kodama0720
"""

from enum import Enum
from coordinate import Coordinate


class NodeType(Enum):
    """ノードタイプの列挙体.

    Attributes:
        INTERSECTION: 交点
        MIDDLE: 中点
        BLOCK: ブロック置き場
    """

    INTERSECTION = 0
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
        self.__block_id = block_id
        self.__coord = coord
        if coord.x % 2 != 0 and coord.y % 2 != 0:
            self.__node_type = NodeType.BLOCK
        elif coord.x % 2 == 0 and coord.y % 2 == 0:
            self.__node_type = NodeType.INTERSECTION
        else:
            self.__node_type = NodeType.MIDDLE

    @property
    def block_id(self) -> int:
        """Getter.

        Returns:
            int: ブロックID
        """
        return self.__block_id

    @property
    def coord(self) -> Coordinate:
        """Getter.

        Returns:
            Coordinate: 座標
        """
        return self.__coord

    @property
    def node_type(self) -> NodeType:
        """Getter.

        Returns:
            NodeType: ノードの型
        """
        return self.__node_type
