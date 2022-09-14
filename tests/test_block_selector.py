"""BlockSelectorクラスのテストコードを記述するモジュール.

@author: mutotaka0426
"""


import unittest

from pathlib import Path
import sys
from camera_system.block_selector import BlockSelector
from game_area_info import GameAreaInfo
from robot import Robot, Direction
from coordinate import Coordinate
from color_changer import Color
from node import Node


class TestBlockSelector(unittest.TestCase):
    def test_select_block_priority1(self):
        """優先順位1で決定するパターン."""
        robot = Robot(Coordinate(6, 6), Direction.N.value)
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

        block_selector = BlockSelector()
        actual = block_selector.select_block(robot)
        actual_color = GameAreaInfo.block_color_list[actual.block_id]
        expected = Node(7, Coordinate(5, 5))  # 右下のブロック置き場
        expected_color = Color.BLUE

        self.assertEqual(expected.block_id, actual.block_id)  # ブロックIDのテスト
        self.assertEqual(expected.coord, actual.coord)  # 座標のテスト
        self.assertEqual(expected.node_type, actual.node_type)  # ノードの型のテスト
        self.assertEqual(expected_color, actual_color)  # ブロックの色のテスト

    def test_select_block_priority2(self):
        """優先順位2で決定するパターン."""
        robot = Robot(Coordinate(2, 2), Direction.N.value)
        GameAreaInfo.block_color_list = [
            Color.RED, Color.GREEN, Color.YELLOW,
            Color.YELLOW, Color.RED,
            Color.GREEN, Color.BLUE, Color.BLUE
        ]
        GameAreaInfo.base_color_list = [
            Color.RED, Color.YELLOW,
            Color.GREEN, Color.BLUE
        ]
        GameAreaInfo.bonus_color = Color.GREEN

        block_selector = BlockSelector()
        actual = block_selector.select_block(robot)
        actual_color = GameAreaInfo.block_color_list[actual.block_id]
        expected = Node(1, Coordinate(3, 1))  # 真ん中上のブロック置き場
        expected_color = Color.GREEN

        self.assertEqual(expected.block_id, actual.block_id)  # ブロックIDのテスト
        self.assertEqual(expected.coord, actual.coord)  # 座標のテスト
        self.assertEqual(expected.node_type, actual.node_type)  # ノードの型のテスト
        self.assertEqual(expected_color, actual_color)  # ブロックの色のテスト

    def test_select_block_priority3(self):
        """優先順位3で決定するパターン."""
        robot = Robot(Coordinate(4, 4), Direction.N.value)
        GameAreaInfo.block_color_list = [
            Color.RED, Color.GREEN, Color.YELLOW,
            Color.YELLOW, Color.BLUE,
            Color.GREEN, Color.BLUE, Color.RED
        ]
        GameAreaInfo.base_color_list = [
            Color.RED, Color.YELLOW,
            Color.GREEN, Color.BLUE
        ]
        GameAreaInfo.bonus_color = Color.GREEN

        block_selector = BlockSelector()
        actual = block_selector.select_block(robot)
        actual_color = GameAreaInfo.block_color_list[actual.block_id]
        expected = Node(7, Coordinate(5, 5))  # 右下のブロック置き場
        expected_color = Color.RED

        self.assertEqual(expected.block_id, actual.block_id)  # ブロックIDのテスト
        self.assertEqual(expected.coord, actual.coord)  # 座標のテスト
        self.assertEqual(expected.node_type, actual.node_type)  # ノードの型のテスト
        self.assertEqual(expected_color, actual_color)  # ブロックの色のテスト

    def test_select_block_priority4(self):
        """優先順位4で決定するパターン."""
        robot = Robot(Coordinate(4, 4), Direction.N.value)
        GameAreaInfo.block_color_list = [
            Color.RED, Color.GREEN, Color.YELLOW,
            Color.RED, Color.BLUE,
            Color.GREEN, Color.YELLOW, Color.BLUE
        ]
        GameAreaInfo.base_color_list = [
            Color.RED, Color.GREEN,
            Color.YELLOW, Color.BLUE
        ]
        GameAreaInfo.bonus_color = Color.GREEN

        block_selector = BlockSelector()
        actual = block_selector.select_block(robot)
        actual_color = GameAreaInfo.block_color_list[actual.block_id]
        expected = Node(4, Coordinate(5, 3))  # 右真ん中のブロック置き場
        expected_color = Color.BLUE

        self.assertEqual(expected.block_id, actual.block_id)  # ブロックIDのテスト
        self.assertEqual(expected.coord, actual.coord)  # 座標のテスト
        self.assertEqual(expected.node_type, actual.node_type)  # ノードの型のテスト
        self.assertEqual(expected_color, actual_color)  # ブロックの色のテスト
