"""運搬動作決定のテストコードを記述するモジュール.

@author: miyashita64
"""

import unittest
import os

from game_motion_decider import GameMotionDecider
from game_area_info import GameAreaInfo
from node import Node
from robot import Robot, Direction
from coordinate import Coordinate
from color_changer import Color


class TestGameMotionDecider(unittest.TestCase):
    """GameMotionDeciderのテスト."""

    def test_game_motion_decider_decide(self):
        """1つのカラーブロックについて運搬動作決定を実行する."""
        # ゲームエリア情報の初期化
        robot = Robot(Coordinate(4, 4), Direction.E, "left")
        GameAreaInfo.node_list = [
            Node(-1, Coordinate(0, 0)), Node(-1, Coordinate(1, 0)),
            Node(-1, Coordinate(2, 0)), Node(-1, Coordinate(3, 0)),
            Node(-1, Coordinate(4, 0)), Node(-1, Coordinate(5, 0)),
            Node(-1, Coordinate(6, 0)),
            Node(-1, Coordinate(0, 1)), Node(0, Coordinate(1, 1)),
            Node(-1, Coordinate(2, 1)), Node(1, Coordinate(3, 1)),
            Node(-1, Coordinate(4, 1)), Node(2, Coordinate(5, 1)),
            Node(-1, Coordinate(6, 1)),
            Node(-1, Coordinate(0, 2)), Node(-1, Coordinate(1, 2)),
            Node(-1, Coordinate(2, 2)), Node(-1, Coordinate(3, 2)),
            Node(-1, Coordinate(4, 2)), Node(-1, Coordinate(5, 2)),
            Node(-1, Coordinate(6, 2)),
            Node(-1, Coordinate(0, 3)), Node(3, Coordinate(1, 3)),
            Node(-1, Coordinate(2, 3)), Node(-1, Coordinate(3, 3)),
            Node(-1, Coordinate(4, 3)), Node(4, Coordinate(5, 3)),
            Node(-1, Coordinate(6, 3)),
            Node(-1, Coordinate(0, 4)), Node(-1, Coordinate(1, 4)),
            Node(-1, Coordinate(2, 4)), Node(-1, Coordinate(3, 4)),
            Node(-1, Coordinate(4, 4)), Node(-1, Coordinate(5, 4)),
            Node(-1, Coordinate(6, 4)),
            Node(-1, Coordinate(0, 5)), Node(5, Coordinate(1, 5)),
            Node(-1, Coordinate(2, 5)), Node(6, Coordinate(3, 5)),
            Node(-1, Coordinate(4, 5)), Node(7, Coordinate(5, 5)),
            Node(-1, Coordinate(6, 5)),
            Node(-1, Coordinate(0, 6)), Node(-1, Coordinate(1, 6)),
            Node(-1, Coordinate(2, 6)), Node(-1, Coordinate(3, 6)),
            Node(-1, Coordinate(4, 6)), Node(-1, Coordinate(5, 6)),
            Node(-1, Coordinate(6, 6)),
        ]
        GameAreaInfo.block_color_list = [
            Color.RED, Color.RED, Color.YELLOW,
            Color.YELLOW, Color.GREEN,
            Color.GREEN, Color.BLUE, Color.BLUE
        ]
        GameAreaInfo.base_color_list = [
            Color.RED, Color.YELLOW,
            Color.GREEN, Color.BLUE
        ]
        GameAreaInfo.bonus_color = Color.RED
        GameAreaInfo.intersection_list = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN]

        # 運搬動作を決定する
        game_motions = []
        for block_id in range(len(GameAreaInfo.block_color_list)):
            game_motions += GameMotionDecider.decide(robot, block_id)
        # 探索動作は、ブロックの数 * 2(取得と設置) だけあるはず
        expected_game_motions_count = len(GameAreaInfo.block_color_list) * 2
        actual_game_motions_count = len(game_motions)

        self.assertEqual(expected_game_motions_count, actual_game_motions_count)
