"""GameInfoクラスのテストコードを記述するモジュール.

@author: kodama0720
"""


import unittest

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.game_info import GameInfo  # noqa
from camera_system.color_changer import Color  # noqa
from camera_system.robot import Robot, Direction  # noqa


class TestGameInfo(unittest.TestCase):
    # 候補ノードを取得するテスト
    def test_get_candidate_node(self):
        info = GameInfo()
        color = Color.BLUE.value  # 北
        expected = [(2, 0), (3, 0), (4, 0)]
        actual = info.get_candidate_node(color)

        self.assertEqual(expected, actual)

    # 未運搬のブロック置き場があるブロック置き場を取得するテスト
    def test_get_no_transported_block(self):
        info = GameInfo()
        color = Color.BLUE.value
        expected = [(1, 1), (1, 3), (1, 5), (3, 1), (3, 5), (5, 1), (5, 3), (5, 5)]
        actual = info.get_no_transported_block()

        self.assertEqual(expected, actual)

    # 走行禁止座標を取得するテスト
    def test_get_no_entry_coordinate(self):
        info = GameInfo()
        robo = Robot()
        robo.coord = [1, 2]
        robo.direct = Direction.NE.value  # 北東
        expected = [(1, 3), (0, 3), (2, 3), (1, 1), (0, 1), (2, 1)]
        actual = info.get_no_entry_coordinate(robo)

        self.assertEqual(expected, actual)

    # 回頭禁止方向を取得するテスト
    def test_get_no_rotate_direction(self):
        info = GameInfo()
        robo = Robot()
        robo.coord = [1, 4]
        robo.direct = Direction.E.value  # 北東
        expected = [0, 4, 5, 6, 7]
        actual = info.get_no_rotate_direction(robo)

        self.assertEqual(expected, actual)
