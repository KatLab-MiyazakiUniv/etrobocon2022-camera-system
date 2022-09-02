"""交点→ブロック置き場のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.game_motion import GameMotion  # noqa
from camera_system.intersection_to_block import IntersectionToBlock  # noqa


class TestIntersectionToBlock(unittest.TestCase):
    """交点→ブロック置き場のテスト."""

    def test_intersection_to_block_vertical(self):
        """縦調整あり斜め調整なしのテスト."""
        first_angle = -45  # 1回目の回頭角度
        second_angle = -45  # 2回目の回頭角度
        angle = first_angle+second_angle
        vertical_flag = True
        diagonal_flag = False
        i2b = IntersectionToBlock(angle, vertical_flag, diagonal_flag)
        i2b.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.7840
        motion_time += GameMotion.ROTATION_TIME[abs(first_angle)//45]
        motion_time += GameMotion.ROTATION_TIME[abs(second_angle)//45]
        motion_time += GameMotion.VERTICAL_TIME
        success_rate = 1.0
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = i2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,45,100,anticlockwise,交点→ブロック置き場\n"
        expected_commands += "DS,10,70\n"
        expected_commands += "RT,45,100,anticlockwise\n"
        expected_commands += "DS,150,70\n"

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
        i2b = IntersectionToBlock(angle, vertical_flag, diagonal_flag)
        i2b.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.7840
        motion_time += GameMotion.ROTATION_TIME[abs(first_angle)//45]
        motion_time += GameMotion.ROTATION_TIME[abs(second_angle)//45]
        motion_time += GameMotion.DIAGONAL_TIME
        success_rate = 1.0
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = i2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,45,100,clockwise,交点→ブロック置き場\n"
        expected_commands += "DS,20,70\n"
        expected_commands += "DS,150,70\n"

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
        i2b = IntersectionToBlock(angle, vertical_flag, diagonal_flag)
        i2b.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 0.7840 + \
            GameMotion.ROTATION_TIME[abs(first_angle)//45] + \
            GameMotion.ROTATION_TIME[abs(second_angle)//45]
        success_rate = 1.0
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = i2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,180,100,clockwise,交点→ブロック置き場\n"
        expected_commands += "RT,45,100,clockwise\n"
        expected_commands += "DS,150,70\n"

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
            i2b = IntersectionToBlock(angle, vertical_flag, diagonal_flag)

    def test_intersection_to_block_no_rotation(self):
        """回頭しない場合のテスト."""
        angle = 0
        vertical_flag = False
        diagonal_flag = True
        i2b = IntersectionToBlock(angle, vertical_flag, diagonal_flag)
        i2b.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 0.7840 + GameMotion.DIAGONAL_TIME
        success_rate = 1.0
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = i2b.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "DS,20,70,交点→ブロック置き場\n"
        expected_commands += "DS,150,70\n"

        actual_commands = i2b.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

        expected_edge = "none"  # generate_command()後のcurrent_edgeは"none"になる
        actual_edge = i2b.current_edge

        self.assertEqual(expected_edge, actual_edge)
