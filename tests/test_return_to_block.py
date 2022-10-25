"""設置後復帰(→ブロック置き場)のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from camera_system.game_motion import GameMotion
from camera_system.return_to_block import ReturnToBlock


class TestReturnToBlock(unittest.TestCase):
    """設置後復帰(→ブロック置き場)のテスト."""

    def test_return_to_block_from_block(self):
        """ブロック置き場から設置した想定のテスト."""
        angle = 0
        need_adjustment = False
        r2b = ReturnToBlock(angle, need_adjustment)
        r2b.current_edge = "none"  # 初期エッジをnoneにする

        # コストの期待値を求める
        expected_cost = GameMotion.ROTATION_BLOCK_TABLE[0]["time"]
        actual_cost = r2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "AR,50,40,アームを上げる処理(設置処理),設置後復帰(→ブロック置き場)\n"
        expected_commands += "DS,75,-70\n"
        expected_commands += "AF,50,40,アームを下げる処理\n"

        actual_commands = r2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = r2b.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_return_to_block_from_middle(self):
        """中点から設置した想定のテスト(調整動作あり)."""
        angle = 45
        need_adjustment = True
        r2b = ReturnToBlock(angle, need_adjustment)
        r2b.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        expected_cost = GameMotion.ROTATION_BLOCK_TABLE[45]["time"] + \
            GameMotion.VERTICAL_TIME + GameMotion.SLEEP_TIME * 2
        actual_cost = r2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,設置後復帰(→ブロック置き場)\n"
        expected_commands += "RT,%d,%d,clockwise\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[45]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
        expected_commands += "AR,50,40,アームを上げる処理(設置処理)\n"
        expected_commands += "DS,10,-70\n"
        expected_commands += "DS,75,-70\n"
        expected_commands += "AF,50,40,アームを下げる処理\n"

        actual_commands = r2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = r2b.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_return_to_block_from_middle_no_adjustment(self):
        """中点から設置した想定のテスト(調整動作なし)."""
        angle = -45
        need_adjustment = False
        r2b = ReturnToBlock(angle, need_adjustment)
        r2b.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        expected_cost = GameMotion.ROTATION_BLOCK_TABLE[45]["time"] + GameMotion.SLEEP_TIME * 2
        actual_cost = r2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,設置後復帰(→ブロック置き場)\n"
        expected_commands += "RT,%d,%d,anticlockwise\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[45]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
        expected_commands += "AR,50,40,アームを上げる処理(設置処理)\n"
        expected_commands += "DS,75,-70\n"
        expected_commands += "AF,50,40,アームを下げる処理\n"

        actual_commands = r2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = r2b.current_edge

        self.assertEqual(expected_edge, actual_edge)
