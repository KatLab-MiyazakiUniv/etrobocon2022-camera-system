"""設置後復帰のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.game_motion import GameMotion  # noqa
from camera_system.return_after_setup import ReturnAfterSetup  # noqa


class TestReturnAfterSetup(unittest.TestCase):
    """設置後復帰のテスト."""

    def test_return_after_setup(self):
        """調整動作ありのテスト."""
        angle = 45
        target_node = "intersection"
        target_color = "GREEN"
        ras = ReturnAfterSetup(angle, target_node, target_color)
        ras.current_edge = "none"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        expected_cost = GameMotion.ROTATION_TIME[abs(angle)//45]
        actual_cost = ras.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,45,100,clockwise,設置後復帰\n"
        expected_commands += "EC,right\n"
        expected_commands += "DS,70,-40\n"
        expected_commands += "CL,GREEN,0,-40,0.1,0.08,0.08\n"
        expected_commands += "DS,15,60\n"

        actual_commands = ras.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト
