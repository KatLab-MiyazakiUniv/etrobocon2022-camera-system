"""中点→ブロック置き場のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.game_motion import Edge, GameMotion  # noqa
from camera_system.middle_to_block import MiddleToBlock  # noqa


class TestMiddleToBlock(unittest.TestCase):
    """中点→ブロック置き場のテスト."""

    def test_midlle_to_block(self):
        """調整動作ありのテスト."""
        angle = 270
        adjustment_flag = True
        m2b = MiddleToBlock(angle, adjustment_flag)
        m2b.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.6970 + GameMotion.ROTATION_TIME[abs(angle)//45]+GameMotion.VERTICAL_TIME
        success_rate = 1.0
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = m2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,270,100,clockwise,中点→ブロック置き場\n"
        expected_commands += "DS,10,70\n"
        expected_commands += "DS,90,70\n"

        actual_commands = m2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = m2b.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_midlle_to_block_no_adjustment(self):
        """調整動作なしのテスト."""
        angle = 315
        adjustment_flag = False
        m2b = MiddleToBlock(angle, adjustment_flag)
        m2b.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.6970 + GameMotion.ROTATION_TIME[abs(angle)//45]
        success_rate = 1.0
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = m2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,315,100,clockwise,中点→ブロック置き場\n"
        expected_commands += "DS,90,70\n"

        actual_commands = m2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = m2b.current_edge

        self.assertEqual(expected_edge, actual_edge)
