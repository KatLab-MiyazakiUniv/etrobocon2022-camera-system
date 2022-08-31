"""ブロック置き場→中点のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.game_motion import GameMotion  # noqa
from camera_system.block_to_middle import BlockToMiddle  # noqa


class TestBlockToMiddle(unittest.TestCase):
    """ブロック置き場→中点のテスト."""

    def test_block_to_middle(self):
        angle = -45
        b2m = BlockToMiddle(angle)
        b2m.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.8094 + GameMotion.ROTATION_TIME[abs(angle)//45]
        success_rate = 0.9
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = b2m.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,45,100,anticlockwise,ブロック置き場→中点\n"
        expected_commands += "CS,BLACK,70\n"
        expected_commands += "DS,10,70\n"

        actual_commands = b2m.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = b2m.current_edge

        self.assertEqual(expected_edge, actual_edge)
