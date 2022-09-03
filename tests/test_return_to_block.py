"""設置後復帰(→ブロック置き場)のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.game_motion import GameMotion  # noqa
from camera_system.return_to_block import ReturnToBlock  # noqa


class TestReturnToBlock(unittest.TestCase):
    """設置後復帰(→ブロック置き場)のテスト."""

    def test_return_to_block_from_block(self):
        """ブロック置き場から設置した想定のテスト."""
        angle = 0
        adjustment_flag = False
        r2b = ReturnToBlock(angle, adjustment_flag)
        r2b.current_edge = "none"  # 初期エッジをnoneにする

        # コストの期待値を求める
        expected_cost = GameMotion.ROTATION_TIME[abs(angle)//45]
        actual_cost = r2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "DS,100,-40,設置後復帰(→ブロック置き場)\n"

        actual_commands = r2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = r2b.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_return_to_block_from_middle(self):
        """中点から設置した想定のテスト(調整動作あり)."""
        angle = 45
        adjustment_flag = True
        r2b = ReturnToBlock(angle, adjustment_flag)
        r2b.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        expected_cost = GameMotion.ROTATION_TIME[abs(angle)//45]+GameMotion.VERTICAL_TIME
        actual_cost = r2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,45,100,clockwise,設置後復帰(→ブロック置き場)\n"
        expected_commands += "DS,10,-70\n"
        expected_commands += "DS,100,-40\n"

        actual_commands = r2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = r2b.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_return_to_block_from_middle_no_adjustment(self):
        """中点から設置した想定のテスト(調整動作なし)."""
        angle = -45
        adjustment_flag = False
        r2b = ReturnToBlock(angle, adjustment_flag)
        r2b.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        expected_cost = GameMotion.ROTATION_TIME[abs(angle)//45]
        actual_cost = r2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,45,100,anticlockwise,設置後復帰(→ブロック置き場)\n"
        expected_commands += "DS,100,-40\n"

        actual_commands = r2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = r2b.current_edge

        self.assertEqual(expected_edge, actual_edge)
