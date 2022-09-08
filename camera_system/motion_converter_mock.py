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
        before_type = cls.coord_to_node(before.coord).node_type
        after_type = cls.coord_to_node(after.coord).node_type
        if before_type == NodeType.CROSS.value:
            if after_type == NodeType.MIDDLE.value:
                return IntersectionToMiddle(0, False)
            elif after_type == NodeType.BLOCK.value:
                return IntersectionToBlock(0, False, False)
        elif before_type == NodeType.MIDDLE.value:
            if after_type == NodeType.CROSS.value:
                return MiddleToIntersection(0, "RED")
            elif after_type == NodeType.MIDDLE.value:
                return MiddleToMiddle(0, False)
            elif after_type == NodeType.BLOCK.value:
                return MiddleToBlock(0, False)
        elif before_type == NodeType.BLOCK.value:
            if after_type == NodeType.CROSS.value:
                return BlockToIntersection(0, "RED")
            elif after_type == NodeType.MIDDLE.value:
                return BlockToMiddle(0)
        else:
            print("異常")
