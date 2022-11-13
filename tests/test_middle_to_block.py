"""中点→ブロック置き場のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426 miyashita64
"""

import unittest

from camera_system.game_motion import GameMotion
from camera_system.middle_to_block import MiddleToBlock


class TestMiddleToBlock(unittest.TestCase):
    """中点→ブロック置き場のテスト."""

    def test_midlle_to_block(self):
        """調整動作ありのテスト."""
        angle = 270
        need_adjustment = True
        have_block = True  # ブロックを保持している
        can_correction = False
        m2b = MiddleToBlock(angle, need_adjustment, have_block, can_correction)
        m2b.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.697 + GameMotion.ROTATION_BLOCK_TABLE[270]["time"] \
            + GameMotion.VERTICAL_TIME + GameMotion.SLEEP_TIME * 2
        success_rate = 0.78
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = m2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,中点→ブロック置き場\n"
        expected_commands += "RT,%d,%d,clockwise\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[270]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
        expected_commands += "DS,12,70,20mm直進(縦調整)\n"
        expected_commands += "DS,71,70\n"

        actual_commands = m2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = m2b.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_midlle_to_block_no_adjustment(self):
        """調整動作なしのテスト."""
        angle = 315
        need_adjustment = False
        have_block = False  # ブロックを保持していない
        can_correction = False
        m2b = MiddleToBlock(angle, need_adjustment, have_block, can_correction)
        m2b.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.697 + \
            GameMotion.ROTATION_NO_BLOCK_TABLE[315]["time"] + GameMotion.SLEEP_TIME * 2
        success_rate = 0.78
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = m2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,中点→ブロック置き場\n"
        expected_commands += "RT,%d,%d,clockwise\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[315]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
        expected_commands += "DS,71,70\n"

        actual_commands = m2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = m2b.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_midlle_to_block_with_correction(self):
        """方向転換後に角度補正を行う場合のテスト."""
        angle = 315
        need_adjustment = False
        have_block = False  # ブロックを保持していない
        can_correction = True
        m2b = MiddleToBlock(angle, need_adjustment, have_block, can_correction)
        m2b.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.697 + \
            GameMotion.ROTATION_NO_BLOCK_TABLE[315]["time"] + GameMotion.SLEEP_TIME * 3
        success_rate = 0.78
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = m2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,中点→ブロック置き場\n"
        expected_commands += "RT,%d,%d,clockwise\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[315]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
        expected_commands += "XR,0,47\n"
        expected_commands += "SL,100\n"
        expected_commands += "DS,71,70\n"

        actual_commands = m2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = m2b.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_midlle_to_block_zero_anglewith_correction(self):
        """方向転換後に角度補正を行う場合のテスト."""
        angle = 0
        need_adjustment = False
        have_block = False  # ブロックを保持していない
        can_correction = True
        m2b = MiddleToBlock(angle, need_adjustment, have_block, can_correction)
        m2b.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.697 + \
            GameMotion.ROTATION_NO_BLOCK_TABLE[0]["time"] + GameMotion.SLEEP_TIME * 2
        success_rate = 0.78
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = m2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,中点→ブロック置き場\n"
        expected_commands += "XR,0,47\n"
        expected_commands += "SL,100\n"
        expected_commands += "DS,71,70\n"

        actual_commands = m2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = m2b.current_edge

        self.assertEqual(expected_edge, actual_edge)
