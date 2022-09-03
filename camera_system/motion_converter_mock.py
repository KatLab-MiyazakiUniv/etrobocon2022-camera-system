"""動作変換ができるまでの代替モジュール.

2つの仮想走行体からゲーム動作を求める.
@author miyashita64
"""

from robot import Robot
from node import Node, NodeType
from game_area_info import GameAreaInfo
from game_motion import GameMotion
from intersection_to_middle import IntersectionToMiddle
from intersection_to_block import IntersectionToBlock
from middle_to_intersection import MiddleToIntersection
from middle_to_middle import MiddleToMiddle
from middle_to_block import MiddleToBlock
from block_to_middle import BlockToMiddle
from block_to_intersection import BlockToIntersection


class MotionConverterMock():
    """動作変換を代替するクラス."""

    @classmethod
    def coord_to_node(cls, coord) -> Node:
        """指定した座標を持つノードを返す."""
        return [node for node in GameAreaInfo.node_list if node.coord == coord][0]

    @classmethod
    def convert(cls, before: Robot, after: Robot) -> GameMotion:
        """走行体状態が遷移するために必要なゲーム動作を返す.

        Args:
            before: 遷移前状態
            after:  遷移後状態

        Returns:
            GameMotion: 遷移に必要なゲーム動作
        """
        before_type = cls.coord_to_node(before.coord).nodeType
        after_type = cls.coord_to_node(after.coord).nodeType
        if before_type == NodeType.CROSS:
            if after_type == NodeType.MIDDLE:
                return IntersectionToMiddle(0, False)
            elif after_type == NodeType.BLOCK:
                return IntersectionToBlock(0, False)
        elif before_type == NodeType.MIDDLE:
            if after_type == NodeType.CROSS:
                return MiddleToIntersection(0, "RED")
            elif after_type == NodeType.MIDDLE:
                MiddleToMiddle(0, False)
            elif after_type == NodeType.BLOCK:
                return MiddleToBlock(0, False)
        elif before_type == NodeType.BLOCK:
            if after_type == NodeType.CROSS:
                return BlockToIntersection(0, "RED")
            elif after_type == NodeType.MIDDLE:
                return BlockToMiddle(0)
