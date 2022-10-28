"""ブロック置き場→交点のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from camera_system.game_motion import GameMotion
from camera_system.block_to_intersection import BlockToIntersection
from color_changer import Color


class TestBlockToIntersection(unittest.TestCase):
    """ブロック置き場→交点のテスト."""

    def test_block_to_intersection_at_blue(self):
        angle = -180
        target_color = Color.BLUE
        have_block = True  # ブロックを保持している
        b2i = BlockToIntersection(angle, target_color, have_block)
        b2i.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 1.086 + \
            GameMotion.ROTATION_BLOCK_TABLE[180]["time"] + GameMotion.SLEEP_TIME * 2
        success_rate = 0.78
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = b2i.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,ブロック置き場→交点\n"
        expected_commands += "RT,%d,%d,anticlockwise\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[180]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
        expected_commands += "CS,BLUE,70\n"
        expected_commands += "DS,42,60\n"

        actual_commands = b2i.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = b2i.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_block_to_intersection_at_green(self):
        angle = -225
        target_color = Color.GREEN
        have_block = True  # ブロックを保持している
        b2i = BlockToIntersection(angle, target_color, have_block)
        b2i.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 1.086 + \
            GameMotion.ROTATION_BLOCK_TABLE[225]["time"] + GameMotion.SLEEP_TIME * 2
        success_rate = 0.78
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = b2i.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,ブロック置き場→交点\n"
        expected_commands += "RT,%d,%d,anticlockwise\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[225]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
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
        have_block = False  # ブロックを保持していない
        b2i = BlockToIntersection(angle, target_color, have_block)
        b2i.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 1.086 + \
            GameMotion.ROTATION_NO_BLOCK_TABLE[270]["time"] + GameMotion.SLEEP_TIME * 2
        success_rate = 0.78
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = b2i.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,ブロック置き場→交点\n"
        expected_commands += "RT,%d,%d,anticlockwise\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[270]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
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
        have_block = False  # ブロックを保持していない
        b2i = BlockToIntersection(angle, target_color, have_block)
        b2i.current_edge = "none"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 1.086 + \
            GameMotion.ROTATION_NO_BLOCK_TABLE[315]["time"] + GameMotion.SLEEP_TIME * 2
        success_rate = 0.78
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = b2i.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,ブロック置き場→交点\n"
        expected_commands += "RT,%d,%d,anticlockwise\n" % (
            GameMotion.ROTATION_NO_BLOCK_TABLE[315]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
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
            have_block = True  # ブロックを保持している
            b2i = BlockToIntersection(angle, target_color, have_block)
