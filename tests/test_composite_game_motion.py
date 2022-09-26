"""中点→ブロック置き場のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from camera_system.composite_game_motion import CompositeGameMotion
from camera_system.block_to_intersection import BlockToIntersection
from camera_system.block_to_middle import BlockToMiddle
from camera_system.intersection_to_block import IntersectionToBlock
from camera_system.intersection_to_middle import IntersectionToMiddle
from camera_system.middle_to_block import MiddleToBlock
from camera_system.middle_to_intersection import MiddleToIntersection
from camera_system.middle_to_middle import MiddleToMiddle
from camera_system.return_to_intersection import ReturnToIntersection
from camera_system.return_to_middle import ReturnToMiddle
from camera_system.return_to_block import ReturnToBlock
from color_changer import Color


class TestCompositeGameMotion(unittest.TestCase):
    """CompositeGameMotionのテスト."""

    def test_composite_game_motion(self):
        game_motion_list = CompositeGameMotion()

        # 各ゲーム動作のインスタンスを生成
        b2i = BlockToIntersection(45, Color.RED, True)
        b2m = BlockToMiddle(90, True)
        i2b = IntersectionToBlock(135, True, False, True)
        i2m = IntersectionToMiddle(180, True, True)
        m2b = MiddleToBlock(-45, True, True)
        m2i = MiddleToIntersection(-90, Color.BLUE, False)
        m2m = MiddleToMiddle(-135, True, False)
        r2i = ReturnToIntersection(-45, Color.YELLOW)
        r2m = ReturnToMiddle(0)
        r2b = ReturnToBlock(45, True)

        b2i.current_edge = "left"  # current_edgeの初期値を合わせる
        # 各ゲーム動作のインスタンスから一つずつコストを計算する
        expected_cost = b2i.get_cost()
        expected_cost += b2m.get_cost()
        expected_cost += i2b.get_cost()
        expected_cost += i2m.get_cost()
        expected_cost += m2b.get_cost()
        expected_cost += m2i.get_cost()
        expected_cost += m2m.get_cost()
        expected_cost += r2i.get_cost()
        expected_cost += r2m.get_cost()
        expected_cost += r2b.get_cost()

        # 各ゲーム動作のインスタンスから一つずつコマンドを生成する
        expected_commands = b2i.generate_command()
        expected_commands += b2m.generate_command()
        expected_commands += i2b.generate_command()
        expected_commands += i2m.generate_command()
        expected_commands += m2b.generate_command()
        expected_commands += m2i.generate_command()
        expected_commands += m2m.generate_command()
        expected_commands += r2i.generate_command()
        expected_commands += r2m.generate_command()
        expected_commands += r2b.generate_command()

        # 各ゲーム動作のインスタンスをセットする
        game_motion_list.append_game_motion(b2i)
        game_motion_list.append_game_motion(b2m)
        game_motion_list.append_game_motion(i2b)
        game_motion_list.append_game_motion(i2m)
        game_motion_list.append_game_motion(m2b)
        game_motion_list.append_game_motion(m2i)
        game_motion_list.append_game_motion(m2m)
        game_motion_list.append_game_motion(r2i)
        game_motion_list.append_game_motion(r2m)
        game_motion_list.append_game_motion(r2b)

        b2i.current_edge = "left"  # current_edgeの初期値を合わせる
        actual_cost = game_motion_list.get_cost()  # CompositeGameMotionからコストを計算
        actual_commands = game_motion_list.generate_command()  # CompositeGameMotionからコマンドを生成

        self.assertEqual(expected_cost, actual_cost)  # get_cost()のテスト
        self.assertEqual(expected_commands, actual_commands)  # generate_command()のテスト
