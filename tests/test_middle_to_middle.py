"""中点→中点のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.game_motion import GameMotion  # noqa
from camera_system.middle_to_middle import MiddleToMiddle  # noqa


class TestMiddleToMiddle(unittest.TestCase):
    """中点→中点のテスト."""

    def test_middle_to_middle(self):
        """調整動作ありのテスト."""
        angle = 45
        adjustment_flag = True
        m2m = MiddleToMiddle(angle, adjustment_flag)
        m2m.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 1.149 + \
            GameMotion.ROTATION_TIME[abs(angle)//45]+GameMotion.DIAGONAL_TIME
        success_rate = 0.5
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = m2m.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,45,100,clockwise,中点→中点\n"
        expected_commands += "DS,30,70\n"
        expected_commands += "CS,BLACK,70\n"
        expected_commands += "DS,25,70\n"
        expected_commands += "DS,20,70\n"

        actual_commands = m2m.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

    def test_middle_to_middle_no_adjustment(self):
        """調整動作なしのテスト."""
        angle = 90
        adjustment_flag = False
        m2m = MiddleToMiddle(angle, adjustment_flag)
        m2m.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 1.149 + GameMotion.ROTATION_TIME[abs(angle)//45]
        success_rate = 0.5
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = m2m.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,90,100,clockwise,中点→中点\n"
        expected_commands += "EC,right\n"
        expected_commands += "DS,30,70\n"
        expected_commands += "CS,BLACK,70\n"
        expected_commands += "DS,25,70\n"

        actual_commands = m2m.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト