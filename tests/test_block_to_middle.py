"""ブロック置き場→中点のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426 miyashita64
"""

import unittest

from camera_system.game_motion import GameMotion
from camera_system.block_to_middle import BlockToMiddle


class TestBlockToMiddle(unittest.TestCase):
    """ブロック置き場→中点のテスト."""

    def test_block_to_middle(self):
        angle = -45
        have_block = True  # ブロックを保持している
        can_correction = False
        b2m = BlockToMiddle(angle, have_block, can_correction)
        b2m.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.8094 + \
            GameMotion.ROTATION_BLOCK_TABLE[45]["time"] + GameMotion.SLEEP_TIME * 2
        success_rate = 0.9
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = b2m.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,ブロック置き場→中点\n"
        expected_commands += "RT,%d,%d,anticlockwise\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[45]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
        expected_commands += "CS,BLACK,70\n"
        expected_commands += "DS,10,70\n"

        actual_commands = b2m.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = b2m.current_edge

        self.assertEqual(expected_edge, actual_edge)
