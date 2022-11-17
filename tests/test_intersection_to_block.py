"""交点→ブロック置き場のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426 miyashita64
"""

import unittest

from camera_system.game_motion import GameMotion
from camera_system.intersection_to_block import IntersectionToBlock


class TestIntersectionToBlock(unittest.TestCase):
    """交点→ブロック置き場のテスト."""

    def test_intersection_to_block_vertical(self):
        """縦調整あり斜め調整なしのテスト."""
        first_angle = -45  # 1回目の回頭角度
        second_angle = -45  # 2回目の回頭角度
        angle = first_angle+second_angle
        vertical_flag = True
        diagonal_flag = False
        have_block = True  # ブロックを保持している
        can_first_correction = False
        can_second_correction = False
        i2b = IntersectionToBlock(angle, vertical_flag, diagonal_flag,
                                  have_block, can_first_correction, can_second_correction)
        i2b.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.8615
        # 2回分の回頭のスリープ時間を足す
        motion_time += GameMotion.ROTATION_BLOCK_TABLE[45]["time"] + GameMotion.SLEEP_TIME * 2
        motion_time += GameMotion.ROTATION_BLOCK_TABLE[45]["time"] + GameMotion.SLEEP_TIME * 2
        motion_time += GameMotion.VERTICAL_TIME
        success_rate = 0.9
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = i2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,交点→ブロック置き場\n"
        expected_commands += "RT,%d,%d,anticlockwise\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[45]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
        expected_commands += "DS,12,70,20mm直進(縦調整)\n"
        expected_commands += "SL,100\n"
        expected_commands += "RT,%d,%d,anticlockwise\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[45]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
        expected_commands += "DS,132,70\n"
        expected_commands += "DS,20,70\n"

        actual_commands = i2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = i2b.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_intersection_to_block_diagonal(self):
        """縦調整なし斜め調整ありのテスト."""
        first_angle = 0  # 1回目の回頭角度
        second_angle = 45  # 2回目の回頭角度
        angle = first_angle+second_angle
        vertical_flag = False
        diagonal_flag = True
        have_block = True  # ブロックを保持している
        can_first_correction = False
        can_second_correction = False
        i2b = IntersectionToBlock(angle, vertical_flag, diagonal_flag,
                                  have_block, can_first_correction, can_second_correction)
        i2b.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.8615
        motion_time += GameMotion.ROTATION_BLOCK_TABLE[45]["time"] + GameMotion.SLEEP_TIME * 2
        motion_time += GameMotion.DIAGONAL_TIME
        success_rate = 0.9
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = i2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,交点→ブロック置き場\n"
        expected_commands += "RT,%d,%d,clockwise\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[45]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
        expected_commands += "DS,17,70,30mm直進(斜め調整)\n"
        expected_commands += "DS,132,70\n"
        expected_commands += "DS,20,70\n"

        actual_commands = i2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = i2b.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_intersection_to_block_no_adjustment(self):
        """調整動作なしのテスト."""
        first_angle = 180  # 1回目の回頭角度
        second_angle = 45  # 2回目の回頭角度
        angle = first_angle+second_angle
        vertical_flag = False
        diagonal_flag = False
        have_block = False  # ブロックを保持していない
        can_first_correction = False
        can_second_correction = False
        i2b = IntersectionToBlock(angle, vertical_flag, diagonal_flag,
                                  have_block, can_first_correction, can_second_correction)
        i2b.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 0.8615
        motion_time += GameMotion.ROTATION_NO_BLOCK_TABLE[180]["time"] + GameMotion.SLEEP_TIME * 2
        motion_time += GameMotion.ROTATION_NO_BLOCK_TABLE[45]["time"] + GameMotion.SLEEP_TIME * 2
        success_rate = 0.9
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = i2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,交点→ブロック置き場\n"
        expected_commands += "RT,%d,%d,clockwise\n" % (
            GameMotion.ROTATION_NO_BLOCK_TABLE[180]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
        expected_commands += "RT,%d,%d,clockwise\n" % (
            GameMotion.ROTATION_NO_BLOCK_TABLE[45]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
        expected_commands += "DS,132,70\n"
        expected_commands += "DS,20,70\n"

        actual_commands = i2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = i2b.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_intersection_to_block_unexpected_motion(self):
        """縦調整と斜め調整をどちらも指定された場合のテスト"""
        with self.assertRaises(ValueError):
            first_angle = 180  # 1回目の回頭角度
            second_angle = 45  # 2回目の回頭角度
            angle = first_angle+second_angle
            vertical_flag = True
            diagonal_flag = True
            have_block = False  # ブロックを保持していない
            can_first_correction = False
            can_second_correction = False
            i2b = IntersectionToBlock(angle, vertical_flag, diagonal_flag,
                                      have_block, can_first_correction, can_second_correction)

    def test_intersection_to_block_no_rotation(self):
        """回頭しない場合のテスト."""
        angle = 0
        vertical_flag = False
        diagonal_flag = True
        have_block = False  # ブロックを保持していない
        can_first_correction = False
        can_second_correction = False
        i2b = IntersectionToBlock(angle, vertical_flag, diagonal_flag,
                                  have_block, can_first_correction, can_second_correction)
        i2b.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 0.8615 + GameMotion.DIAGONAL_TIME
        success_rate = 0.9
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = i2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "DS,17,70,30mm直進(斜め調整),交点→ブロック置き場\n"
        expected_commands += "DS,132,70\n"
        expected_commands += "DS,20,70\n"

        actual_commands = i2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = i2b.current_edge

        self.assertEqual(expected_edge, actual_edge)

    def test_intersection_to_block_with_correction(self):
        """角度補正を2回行う場合のテスト."""
        first_angle = 180  # 1回目の回頭角度
        second_angle = 45  # 2回目の回頭角度
        angle = first_angle+second_angle
        vertical_flag = False
        diagonal_flag = False
        have_block = False  # ブロックを保持していない
        can_first_correction = True
        can_second_correction = True
        i2b = IntersectionToBlock(angle, vertical_flag, diagonal_flag,
                                  have_block, can_first_correction, can_second_correction)
        i2b.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        # SLEEP_TIME * 3を使うとテスト時にアンダーフロー分の誤差が出る場合ある
        motion_time = 0.8615
        motion_time += GameMotion.ROTATION_NO_BLOCK_TABLE[180]["time"] + GameMotion.SLEEP_TIME * 2
        motion_time += GameMotion.SLEEP_TIME
        motion_time += GameMotion.ROTATION_NO_BLOCK_TABLE[45]["time"] + GameMotion.SLEEP_TIME * 2
        motion_time += GameMotion.SLEEP_TIME
        success_rate = 0.9
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = i2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,交点→ブロック置き場\n"
        expected_commands += "RT,%d,%d,clockwise\n" % (
            GameMotion.ROTATION_NO_BLOCK_TABLE[180]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
        expected_commands += "XR,0,47\n"
        expected_commands += "SL,100\n"
        expected_commands += "RT,%d,%d,clockwise\n" % (
            GameMotion.ROTATION_NO_BLOCK_TABLE[45]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
        expected_commands += "XR,45,47\n"
        expected_commands += "SL,100\n"
        expected_commands += "DS,132,70\n"
        expected_commands += "DS,20,70\n"

        actual_commands = i2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = i2b.current_edge

        self.assertEqual(expected_edge, actual_edge)


def test_intersection_to_block_only_first_correction(self):
    """1回目のみ角度補正を行う場合のテスト."""
    first_angle = 180  # 1回目の回頭角度
    second_angle = 45  # 2回目の回頭角度
    angle = first_angle+second_angle
    vertical_flag = False
    diagonal_flag = False
    have_block = False  # ブロックを保持していない
    can_first_correction = True
    can_second_correction = False
    i2b = IntersectionToBlock(angle, vertical_flag, diagonal_flag,
                              have_block, can_first_correction, can_second_correction)
    i2b.current_edge = "left"  # 初期エッジを左エッジにする

    # コストの期待値を求める
    motion_time = 0.8615
    motion_time += GameMotion.ROTATION_NO_BLOCK_TABLE[180]["time"] + GameMotion.SLEEP_TIME * 2
    motion_time += GameMotion.ROTATION_NO_BLOCK_TABLE[45]["time"] + GameMotion.SLEEP_TIME * 2
    success_rate = 0.9
    expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

    actual_cost = i2b.get_cost()  # 実際のコスト

    self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

    # 期待するコマンドをセット
    expected_commands = "SL,100,交点→ブロック置き場\n"
    expected_commands += "RT,%d,%d,clockwise\n" % (
        GameMotion.ROTATION_NO_BLOCK_TABLE[180]["angle"], GameMotion.ROTATION_BLOCK_PWM)
    expected_commands += "SL,100\n"
    expected_commands += "XR,0,47\n"
    expected_commands += "SL,100\n"
    expected_commands += "RT,%d,%d,clockwise\n" % (
        GameMotion.ROTATION_NO_BLOCK_TABLE[45]["angle"], GameMotion.ROTATION_BLOCK_PWM)
    expected_commands += "SL,100\n"
    expected_commands += "DS,132,70\n"

    actual_commands = i2b.generate_command()  # コマンドを生成する

    self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

    expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
    actual_edge = i2b.current_edge

    self.assertEqual(expected_edge, actual_edge)


def test_intersection_to_block_only_second_correction(self):
    """2回目のみ角度補正を行う場合のテスト."""
    first_angle = 180  # 1回目の回頭角度
    second_angle = 45  # 2回目の回頭角度
    angle = first_angle+second_angle
    vertical_flag = False
    diagonal_flag = False
    have_block = False  # ブロックを保持していない
    can_first_correction = False
    can_second_correction = True
    i2b = IntersectionToBlock(angle, vertical_flag, diagonal_flag,
                              have_block, can_first_correction, can_second_correction)
    i2b.current_edge = "left"  # 初期エッジを左エッジにする

    # コストの期待値を求める
    motion_time = 0.8615
    motion_time += GameMotion.ROTATION_NO_BLOCK_TABLE[180]["time"] + GameMotion.SLEEP_TIME * 2
    motion_time += GameMotion.ROTATION_NO_BLOCK_TABLE[45]["time"] + GameMotion.SLEEP_TIME * 2
    success_rate = 0.9
    expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

    actual_cost = i2b.get_cost()  # 実際のコスト

    self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

    # 期待するコマンドをセット
    expected_commands = "SL,100,交点→ブロック置き場\n"
    expected_commands += "RT,%d,%d,clockwise\n" % (
        GameMotion.ROTATION_NO_BLOCK_TABLE[180]["angle"], GameMotion.ROTATION_BLOCK_PWM)
    expected_commands += "SL,100\n"
    expected_commands += "RT,%d,%d,clockwise\n" % (
        GameMotion.ROTATION_NO_BLOCK_TABLE[45]["angle"], GameMotion.ROTATION_BLOCK_PWM)
    expected_commands += "SL,100\n"
    expected_commands += "XR,45,47\n"
    expected_commands += "SL,100\n"
    expected_commands += "DS,132,70\n"

    actual_commands = i2b.generate_command()  # コマンドを生成する

    self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

    expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
    actual_edge = i2b.current_edge

    self.assertEqual(expected_edge, actual_edge)
