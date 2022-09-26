"""交点→中点のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from camera_system.game_motion import GameMotion
from camera_system.intersection_to_middle import IntersectionToMiddle


class TestIntersectionToMiddle(unittest.TestCase):
    """交点→中点のテスト."""

    def test_intersection_to_middle(self):
        """調整動作ありのテスト."""
        angle = 270
        need_adjustment = True
        have_block = True  # ブロックを保持している
        i2m = IntersectionToMiddle(angle, need_adjustment, have_block)
        i2m.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.5480 + \
            GameMotion.ROTATION_BLOCK_TABLE[270]["time"]+GameMotion.VERTICAL_TIME
        success_rate = 0.8
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = i2m.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,%d,%d,clockwise,交点→中点\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[270]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "EC,left\n"
        expected_commands += "DS,10,70\n"
        expected_commands += "DL,80,0,60,0.1,0.08,0.08\n"

        actual_commands = i2m.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

    def test_intersection_to_middle_no_adjustment(self):
        """調整動作なしのテスト."""
        angle = 315
        need_adjustment = False
        have_block = True  # ブロックを保持している
        i2m = IntersectionToMiddle(angle, need_adjustment, have_block)
        i2m.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.5480 + GameMotion.ROTATION_BLOCK_TABLE[315]["time"]
        success_rate = 0.8
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = i2m.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,%d,%d,clockwise,交点→中点\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[315]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "DL,80,0,60,0.1,0.08,0.08\n"

        actual_commands = i2m.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

    def test_intersection_to_middle_none_to_left(self):
        """エッジがnoneからleftとなるテスト."""
        angle = -45
        need_adjustment = False
        have_block = True  # ブロックを保持している
        i2m = IntersectionToMiddle(angle, need_adjustment, have_block)
        i2m.current_edge = "none"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.5480 + GameMotion.ROTATION_BLOCK_TABLE[45]["time"]
        success_rate = 0.8
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = i2m.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,%d,%d,anticlockwise,交点→中点\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[45]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "EC,left\n"
        expected_commands += "DL,80,0,60,0.1,0.08,0.08\n"

        actual_commands = i2m.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

    def test_intersection_to_middle_none_to_right(self):
        """エッジがnoneからrightとなるテスト."""
        angle = 45
        need_adjustment = False
        have_block = False  # ブロックを保持していない
        i2m = IntersectionToMiddle(angle, need_adjustment, have_block)
        i2m.current_edge = "none"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.5480 + GameMotion.ROTATION_NO_BLOCK_TABLE[45]["time"]
        success_rate = 0.8
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = i2m.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,%d,%d,clockwise,交点→中点\n" % (
            GameMotion.ROTATION_NO_BLOCK_TABLE[45]["angle"], GameMotion.ROTATION_NO_BLOCK_PWM)
        expected_commands += "EC,right\n"
        expected_commands += "DL,80,0,60,0.1,0.08,0.08\n"

        actual_commands = i2m.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

    def test_intersection_to_middle_none_to_none(self):
        """エッジがnoneから変わらないテスト."""
        angle = 180
        need_adjustment = False
        have_block = False  # ブロックを保持していない
        i2m = IntersectionToMiddle(angle, need_adjustment, have_block)
        i2m.current_edge = "none"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.5480 + GameMotion.ROTATION_NO_BLOCK_TABLE[180]["time"]
        success_rate = 0.8
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = i2m.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,%d,%d,clockwise,交点→中点\n" % (
            GameMotion.ROTATION_NO_BLOCK_TABLE[180]["angle"], GameMotion.ROTATION_NO_BLOCK_PWM)
        expected_commands += "DL,80,0,60,0.1,0.08,0.08\n"

        actual_commands = i2m.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト
