"""設置後復帰(→ブロック置き場)のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.game_motion import GameMotion  # noqa
from camera_system.return_to_middle import ReturnToMiddle  # noqa


class TestReturnToMiddle(unittest.TestCase):
    """設置後復帰(→ブロック置き場)のテスト."""

    def test_return_to_middle_from_block(self):
        """ブロック置き場から設置した想定のテスト."""
        angle = 45
        r2m = ReturnToMiddle(angle)
        r2m.current_edge = "none"  # 初期エッジをnoneにする

        # コストの期待値を求める
        expected_cost = GameMotion.ROTATION_TIME[abs(angle)//45]
        actual_cost = r2m.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,45,100,clockwise,設置後復帰(→中点)\n"
        expected_commands += "EC,right\n"
        expected_commands += "DS,50,-40\n"
        expected_commands += "DL,50,0,-40,0.1,0.08,0.08\n"

        actual_commands = r2m.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

    def test_return_to_middle_from_middle(self):
        """中点から設置した想定のテスト."""
        angle = 0
        r2m = ReturnToMiddle(angle)
        r2m.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        expected_cost = GameMotion.ROTATION_TIME[abs(angle)//45]
        actual_cost = r2m.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "DS,50,-40,設置後復帰(→中点)\n"
        expected_commands += "DL,50,0,-40,0.1,0.08,0.08\n"

        actual_commands = r2m.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト