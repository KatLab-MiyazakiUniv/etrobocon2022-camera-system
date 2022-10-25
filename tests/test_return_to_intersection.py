"""設置後復帰(→交点)のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from camera_system.game_motion import GameMotion
from camera_system.return_to_intersection import ReturnToIntersection
from color_changer import Color


class TestReturnToIntersection(unittest.TestCase):
    """設置後復帰(→交点)のテスト."""

    def test_return_to_intersection_from_block(self):
        """ブロック置き場から設置した想定のテスト."""
        angle = 45
        target_color = Color.GREEN
        r2i = ReturnToIntersection(angle, target_color)
        r2i.current_edge = "none"  # 初期エッジをnoneにする

        # コストの期待値を求める
        expected_cost = GameMotion.ROTATION_BLOCK_TABLE[45]["time"] + GameMotion.SLEEP_TIME * 2
        actual_cost = r2i.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "SL,100,設置後復帰(→交点)\n"
        expected_commands += "RT,%d,%d,clockwise\n" % (
            GameMotion.ROTATION_BLOCK_TABLE[45]["angle"], GameMotion.ROTATION_BLOCK_PWM)
        expected_commands += "SL,100\n"
        expected_commands += "AR,50,40,アームを上げる処理(設置処理)\n"
        expected_commands += "EC,right\n"
        expected_commands += "DS,70,-70\n"
        expected_commands += "AF,50,40,アームを下げる処理\n"
        expected_commands += "CL,GREEN,0,-40,0.1,0.08,0.08\n"
        expected_commands += "DS,15,70\n"

        actual_commands = r2i.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

    def test_return_to_intersection_from_middle(self):
        """中点から設置した想定のテスト."""
        angle = 0
        target_color = Color.RED
        r2i = ReturnToIntersection(angle, target_color)
        r2i.current_edge = "left"  # 初期エッジを左エッジにする

        # コストの期待値を求める
        expected_cost = GameMotion.ROTATION_NO_BLOCK_TABLE[0]["time"]
        actual_cost = r2i.get_cost()  # 実際のコスト

        self.assertEqual(expected_cost, actual_cost)  # コスト計算のテスト

        # 期待するコマンドをセット
        expected_commands = "AR,50,40,アームを上げる処理(設置処理),設置後復帰(→交点)\n"
        expected_commands += "DS,70,-70\n"
        expected_commands += "AF,50,40,アームを下げる処理\n"
        expected_commands += "CL,RED,0,-40,0.1,0.08,0.08\n"
        expected_commands += "DS,15,70\n"

        actual_commands = r2i.generate_command()  # コマンドを生成する

        self.assertEqual(expected_commands, actual_commands)  # コマンド生成のテスト

    def test_return_to_intersection_unexpected_color(self):
        """交点の色以外を指定された場合のテスト"""
        with self.assertRaises(ValueError):
            angle = 0
            target_color = Color.BLACK
            r2i = ReturnToIntersection(angle, target_color)
            r2i.current_edge = "left"  # 初期エッジを左エッジにする
