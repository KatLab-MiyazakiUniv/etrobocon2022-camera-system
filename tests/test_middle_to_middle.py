"""中点→中点のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from camera_system.game_motion import GameMotion
from camera_system.middle_to_middle import MiddleToMiddle


class TestMiddleToMiddle(unittest.TestCase):
    """中点→中点のテスト."""

    def test_middle_to_middle(self):
        """調整動作ありのテスト."""
        angle = 45
        need_adjustment = True
        have_block = True  # ブロックを保持している
        m2m = MiddleToMiddle(angle, need_adjustment, have_block)
        m2m.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 1.149 + \
            GameMotion.ROTATION_BLOCK_TABLE[45]["time"]+GameMotion.DIAGONAL_TIME
        success_rate = 0.5
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = m2m.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,%d,%d,clockwise,中点→中点\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[45]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "DS,30,70\n"
        expected_commands += "CS,BLACK,70\n"
        expected_commands += "DS,25,70\n"
        expected_commands += "DS,20,70\n"

        actual_commands = m2m.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

    def test_middle_to_middle_no_adjustment(self):
        """調整動作なしのテスト."""
        angle = 90
        need_adjustment = False
        have_block = False  # ブロックを保持していない
        m2m = MiddleToMiddle(angle, need_adjustment, have_block)
        m2m.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 1.149 + GameMotion.ROTATION_NO_BLOCK_TABLE[90]["time"]
        success_rate = 0.5
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = m2m.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,%d,%d,clockwise,中点→中点\n" % (
            GameMotion.ROTATION_NO_BLOCK_TABLE[90]["angle"], GameMotion.ROTATION_NO_BLOCK_PWM)
        expected_commands += "EC,right\n"
        expected_commands += "DS,30,70\n"
        expected_commands += "CS,BLACK,70\n"
        expected_commands += "DS,25,70\n"

        actual_commands = m2m.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト
