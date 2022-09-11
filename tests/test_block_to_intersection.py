"""ブロック置き場→交点のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from color_changer import Color  # noqa
from camera_system.game_motion import GameMotion  # noqa
from camera_system.block_to_intersection import BlockToIntersection  # noqa


class TestBlockToIntersection(unittest.TestCase):
    """ブロック置き場→交点のテスト."""

    def test_block_to_intersection_at_blue(self):
        angle = -180
        target_color = Color.BLUE
        b2i = BlockToIntersection(angle, target_color)
        b2i.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 1.0700 + GameMotion.ROTATION_TIME[abs(angle)//45]
        success_rate = 1.0
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = b2i.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,180,100,anticlockwise,ブロック置き場→交点\n"
        expected_commands += "CS,BLUE,70\n"
        expected_commands += "DS,42,60\n"

        actual_commands = b2i.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = b2i.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_block_to_intersection_at_green(self):
        angle = -215
        target_color = Color.GREEN
        b2i = BlockToIntersection(angle, target_color)
        b2i.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 1.0700 + GameMotion.ROTATION_TIME[abs(angle)//45]
        success_rate = 1.0
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = b2i.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,215,100,anticlockwise,ブロック置き場→交点\n"
        expected_commands += "CS,GREEN,70\n"
        expected_commands += "DS,42,60\n"

        actual_commands = b2i.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = b2i.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_block_to_intersection_at_yellow(self):
        angle = -270
        target_color = Color.YELLOW
        b2i = BlockToIntersection(angle, target_color)
        b2i.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 1.0700 + GameMotion.ROTATION_TIME[abs(angle)//45]
        success_rate = 1.0
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = b2i.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,270,100,anticlockwise,ブロック置き場→交点\n"
        expected_commands += "CS,YELLOW,70\n"
        expected_commands += "DS,42,60\n"

        actual_commands = b2i.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = b2i.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_block_to_intersection_at_red(self):
        angle = -315
        target_color = Color.RED
        b2i = BlockToIntersection(angle, target_color)
        b2i.current_edge = "none"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 1.0700 + GameMotion.ROTATION_TIME[abs(angle)//45]
        success_rate = 1.0
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = b2i.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,315,100,anticlockwise,ブロック置き場→交点\n"
        expected_commands += "CS,RED,70\n"
        expected_commands += "DS,42,60\n"

        actual_commands = b2i.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = b2i.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_block_to_intersection_unexpected_color(self):
        """交点の色以外を指定された場合のテスト"""
        with self.assertRaises(ValueError):
            angle = 90
            target_color = Color.BLACK
            b2i = BlockToIntersection(angle, target_color)
