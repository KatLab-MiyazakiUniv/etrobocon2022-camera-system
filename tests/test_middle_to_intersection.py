"""中点→交点のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from camera_system.game_motion import GameMotion
from camera_system.middle_to_intersection import MiddleToIntersection


class TestMiddleToIntersection(unittest.TestCase):
    """中点→交点のテスト."""

    def test_midlle_to_intersection_at_blue(self):
        angle = 225
        target_color = "BLUE"
        m2i = MiddleToIntersection(angle, target_color)
        m2i.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 0.5560 + GameMotion.ROTATION_TIME[abs(angle)//45]
        success_rate = 0.8
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = m2i.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,225,100,clockwise,中点→交点\n"
        expected_commands += "EC,right\n"
        expected_commands += "CL,BLUE,0,60,0.1,0.08,0.08\n"
        expected_commands += "DS,20,60\n"

        actual_commands = m2i.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

    def test_midlle_to_intersection_at_green(self):
        angle = 270
        target_color = "GREEN"
        m2i = MiddleToIntersection(angle, target_color)
        m2i.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        motion_time = 0.5560 + GameMotion.ROTATION_TIME[abs(angle)//45]
        success_rate = 0.8
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = m2i.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,270,100,clockwise,中点→交点\n"
        expected_commands += "CL,GREEN,0,60,0.1,0.08,0.08\n"
        expected_commands += "DS,20,60\n"

        actual_commands = m2i.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

    def test_midlle_to_intersection_at_yellow(self):
        angle = 90
        target_color = "YELLOW"
        m2i = MiddleToIntersection(angle, target_color)
        m2i.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.5560 + GameMotion.ROTATION_TIME[abs(angle)//45]
        success_rate = 0.8
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = m2i.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,90,100,clockwise,中点→交点\n"
        expected_commands += "CL,YELLOW,0,60,0.1,0.08,0.08\n"
        expected_commands += "DS,20,60\n"

        actual_commands = m2i.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

    def test_midlle_to_intersection_at_yellow(self):
        angle = 135
        target_color = "RED"
        m2i = MiddleToIntersection(angle, target_color)
        m2i.current_edge = "right"  # 初期エッジを右エッジにする

        # コストの期待値を求める
        motion_time = 0.5560 + GameMotion.ROTATION_TIME[abs(angle)//45]
        success_rate = 0.8
        expected_cost = motion_time*success_rate+GameMotion.MAX_TIME*(1-success_rate)

        actual_cost = m2i.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "RT,135,100,clockwise,中点→交点\n"
        expected_commands += "EC,left\n"
        expected_commands += "CL,RED,0,60,0.1,0.08,0.08\n"
        expected_commands += "DS,20,60\n"

        actual_commands = m2i.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

    def test_midlle_to_intersection_unexpected_color(self):
        """交点の色以外を指定された場合のテスト"""
        with self.assertRaises(ValueError):
            angle = 90
            target_color = "WHITE"
            m2i = MiddleToIntersection(angle, target_color)
