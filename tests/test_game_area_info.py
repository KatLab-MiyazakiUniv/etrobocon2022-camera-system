"""GameAreaInfoクラスのテストコードを記述するモジュール.

@author: kodama0720
"""


import unittest

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.game_area_info import GameAreaInfo  # noqa
from camera_system.color_changer import Color  # noqa
from camera_system.robot import Direction, Robot  # noqa
from camera_system.node import NodeType, Node  # noqa
from coordinate import Coordinate  # noqa


class TestGameAreaInfo(unittest.TestCase):
    def test_get_candidate_node(self):
        """候補ノードを取得するテスト."""
        GameAreaInfo.base_color_list = [
            Color.RED, Color.YELLOW,
            Color.GREEN, Color.BLUE
        ]
        color = Color.BLUE  # 北
        expected = [Coordinate(2, 0), Coordinate(3, 0), Coordinate(4, 0)]
        node_list = GameAreaInfo.get_candidate_node(color)
        actual = [node.coord for node in node_list]

        self.assertEqual(expected, actual)

    def test_get_no_transported_block(self):
        """未運搬のブロック置き場があるブロック置き場を取得するテスト."""
        expected = [
            Node(0, Coordinate(1, 1)), Node(1, Coordinate(3, 1)),
            Node(2, Coordinate(5, 1)), Node(3, Coordinate(1, 3)),
            Node(4, Coordinate(5, 3)), Node(5, Coordinate(1, 5)),
            Node(6, Coordinate(3, 5)), Node(7, Coordinate(5, 5))
        ]
        actual = GameAreaInfo.get_no_transported_block()
        for i in range(len(actual)):
            self.assertEqual(expected[i].block_id, actual[i].block_id)
            self.assertEqual(expected[i].coord, actual[i].coord)
            self.assertEqual(expected[i].node_type.value, actual[i].node_type.value)

    def test_get_no_entry_coordinate(self):
        """走行禁止座標を取得するテスト."""
        robo = Robot(Coordinate(1, 2), Direction.NE.value)
        expected = [
            Coordinate(1, 3), Coordinate(0, 3), Coordinate(2, 3),
            Coordinate(1, 1), Coordinate(0, 1), Coordinate(2, 1)
        ]
        actual = GameAreaInfo.get_no_entry_coordinate(robo)

        self.assertEqual(expected, actual)

    def test_get_no_rotate_direction(self):
        """回頭禁止方向を取得するテスト."""
        robo = Robot(Coordinate(1, 4), Direction.E.value)
        expected = [0, 4, 5, 6, 7]
        actual = GameAreaInfo.get_no_rotate_direction(robo)

        self.assertEqual(expected, actual)
