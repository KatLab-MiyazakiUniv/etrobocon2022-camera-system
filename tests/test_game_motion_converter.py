"""GameMotionConverterクラスのテストコードを記述するモジュール.

@author: mutotaka0426
"""
import unittest

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.game_motion_converter import GameMotionConverter  # noqa
from color_changer import Color  # noqa
from robot import Robot, Direction  # noqa
from coordinate import Coordinate  # noqa
from game_area_info import GameAreaInfo  # noqa
from block_to_intersection import BlockToIntersection  # noqa
from block_to_middle import BlockToMiddle  # noqa
from intersection_to_block import IntersectionToBlock   # noqa
from intersection_to_middle import IntersectionToMiddle  # noqa
from middle_to_block import MiddleToBlock  # noqa
from middle_to_intersection import MiddleToIntersection  # noqa
from middle_to_middle import MiddleToMiddle  # noqa


class TestGameMotionConverter(unittest.TestCase):
    def test_return_block_to_intersection(self):
        """BlockToIntersection（ブロック置き場→交点）を返すテスト."""
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(5, 5), Direction.E, "none")  # 現在の走行体
        next_robot = Robot(Coordinate(6, 4), Direction.NE, "none")  # 次の走行体

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = BlockToIntersection(-45, Color.GREEN)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "none"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_block_to_middle(self):
        """BlockToMiddle（ブロック置き場→中点）を返すテスト."""
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(3, 5), Direction.SE, "none")  # 現在の走行体
        next_robot = Robot(Coordinate(4, 5), Direction.E, "none")  # 次の走行体

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = BlockToMiddle(-45)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "none"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_intersection_to_block(self):
        """IntersectionToBlock（交点→ブロック置き場）を返すテスト(調整動作なし)."""
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(2, 4), Direction.S, "left")  # 現在の走行体
        next_robot = Robot(Coordinate(3, 3), Direction.NE, "none")  # 次の走行体

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = IntersectionToBlock(-135, False, False)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "none"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_intersection_to_block_vertical(self):
        """IntersectionToBlock（交点→ブロック置き場）を返すテスト(縦調整あり).
        `(current_robot.edge == "right") and (clockwise_angle == 45)` のパターン
        """
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(2, 4), Direction.S, "right")  # 現在の走行体
        next_robot = Robot(Coordinate(1, 5), Direction.SW, "none")  # 次の走行体

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = IntersectionToBlock(45, True, False)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "none"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_intersection_to_block_diagonal1(self):
        """IntersectionToBlock（交点→ブロック置き場）を返すテスト(斜め調整あり).
        `(current_robot.edge == "right") and (clockwise_angle == 315)` のパターン
        """
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(2, 4), Direction.S, "right")  # 現在の走行体
        next_robot = Robot(Coordinate(3, 5), Direction.SE, "none")  # 次の走行体

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = IntersectionToBlock(-45, False, True)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "none"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_intersection_to_block_diagonal2(self):
        """IntersectionToBlock（交点→ブロック置き場）を返すテスト(斜め調整あり).
        `clockwise_angle == 0` のパターン
        """
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(2, 4), Direction.SE, "none")  # 現在の走行体
        next_robot = Robot(Coordinate(3, 5), Direction.SE, "none")  # 次の走行体

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = IntersectionToBlock(0, False, True)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "none"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_intersection_to_middle(self):
        """IntersectionToMiddle（交点→中点）を返すテスト(調整動作なし)."""
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(4, 2), Direction.E, "right")  # 現在の走行体
        next_robot = Robot(Coordinate(3, 2), Direction.W, "none")  # 次の走行体

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = IntersectionToMiddle(180, False)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "left"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_intersection_to_middle_adjust1(self):
        """IntersectionToMiddle（交点→中点）を返すテスト(調整動作あり).
        `current_robot.edge == "right") and (clockwise_angle == 270)` のパターン
        """
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(4, 2), Direction.E, "right")  # 現在の走行体
        next_robot = Robot(Coordinate(4, 1), Direction.N, "none")  # 次の走行体

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = IntersectionToMiddle(-90, True)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "left"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_intersection_to_middle_adjust2(self):
        """IntersectionToMiddle（交点→中点）を返すテスト(調整動作あり).
        `clockwise_angle == 45` のパターン
        """
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(4, 2), Direction.NE, "none")  # 現在の走行体
        next_robot = Robot(Coordinate(5, 2), Direction.E, "none")  # 次の走行体

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = IntersectionToMiddle(45, True)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "right"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_middle_to_block(self):
        """MiddleToBlock（中点→ブロック置き場）を返すテスト(調整動作なし)."""
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(3, 4), Direction.NE, "right")  # 現在の走行体
        next_robot = Robot(Coordinate(3, 5), Direction.S, "none")  # 次の走行体

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = MiddleToBlock(135, False)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "none"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_middle_to_block_adjustment_none(self):
        """MiddleToBlock（中点→ブロック置き場）を返すテスト(調整動作あり).
        `(current_robot.edge == "none") and (clockwise_angle == 0)` のパターン
        """

        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(3, 4), Direction.S, "none")  # 現在の走行体
        next_robot = Robot(Coordinate(3, 5), Direction.S, "none")  # 次の走行体

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = MiddleToBlock(0, True)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "none"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_middle_to_block_adjustment_left(self):
        """MiddleToBlock（中点→ブロック置き場）を返すテスト(調整動作あり).
        `(current_robot.edge == "left") and (45 <= clockwise_angle <= 135)` のパターン
        """
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(3, 4), Direction.SW, "left")  # 現在の走行体
        next_robot = Robot(Coordinate(3, 3), Direction.N, "none")  # 次の走行体

        # 反時計回りで45度回頭できる状況にする
        GameAreaInfo.node_list[3+5*7].block_id = -1  # x+y*7

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = MiddleToBlock(135, True)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "none"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_middle_to_block_adjustment_right(self):
        """MiddleToBlock（中点→ブロック置き場）を返すテスト(調整動作あり).
        `(current_robot.edge == "right") and (225 <= clockwise_angle <= 315)` のパターン
        """
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(3, 4), Direction.NE, "right")  # 現在の走行体
        next_robot = Robot(Coordinate(3, 3), Direction.N, "none")  # 次の走行体

        # 反時計回りで45度回頭できる状況にする
        GameAreaInfo.node_list[3+5*7].block_id = -1  # x+y*7

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = MiddleToBlock(-45, True)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "none"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_middle_to_intersection(self):
        """MiddleToIntersection（中点→交点）を返すテスト."""
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(3, 2), Direction.N, "none")  # 現在の走行体
        next_robot = Robot(Coordinate(2, 2), Direction.W, "none")  # 次の走行体

        # 反時計回りで90度回頭できる状況にする
        GameAreaInfo.node_list[3+3*7].block_id = -1  # x+y*7

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = MiddleToIntersection(-90, Color.RED)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "left"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_middle_to_middle(self):
        """MiddleToMiddle（中点→中点）を返すテスト(調整動作なし)."""
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(1, 2), Direction.W, "left")  # 現在の走行体
        next_robot = Robot(Coordinate(2, 3), Direction.SE, "none")  # 次の走行体

        # 反時計回りで135度回頭できる状況にする
        GameAreaInfo.node_list[1+1*7].block_id = -1  # x+y*7
        GameAreaInfo.node_list[1+3*7].block_id = -1  # x+y*7

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = MiddleToMiddle(-135, False)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "right"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_middle_to_middle_adjustment1(self):
        """MiddleToMiddle（中点→中点）を返すテスト(調整動作あり).
        `current_robot.edge == "none"` のパターン
        """
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(2, 3), Direction.E, "none")  # 現在の走行体
        next_robot = Robot(Coordinate(3, 2), Direction.NE, "none")  # 次の走行体

        # 反時計回りで45度回頭しないといけない状況にする
        GameAreaInfo.node_list[1+3*7].block_id = -1  # x+y*7

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = MiddleToMiddle(-45, True)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "left"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_middle_to_middle_adjustment2(self):
        """MiddleToMiddle（中点→中点）を返すテスト(調整動作あり).
        `current_robot.coord.y % 2 == 0` のパターン
        """
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(1, 2), Direction.W, "right")  # 現在の走行体
        next_robot = Robot(Coordinate(2, 3), Direction.SE, "none")  # 次の走行体

        # 時計回りで225度回頭しないといけない状況にする
        GameAreaInfo.node_list[1+3*7].block_id = -1  # x+y*7

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = MiddleToMiddle(225, True)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "left"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_return_middle_to_middle_adjustment3(self):
        """MiddleToMiddle（中点→中点）を返すテスト(調整動作あり).
        `current_robot.coord.y % 2 == 1` のパターン
        """
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(2, 3), Direction.NE, "left")  # 現在の走行体
        next_robot = Robot(Coordinate(3, 4), Direction.SE, "none")  # 次の走行体

        # 時計回りで225度回頭しないといけない状況にする
        GameAreaInfo.node_list[1+3*7].block_id = -1  # x+y*7

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot)
        expected = MiddleToMiddle(90, True)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "right"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def __init_game_area_info(self):
        """テスト用にゲームエリア情報を初期化する."""
        # ノードリストを初期化
        block_count = 0
        for index in range(49):
            x = index % 7
            y = index // 7
            if x == y == 3:  # (3, 3)は-1
                GameAreaInfo.node_list[index].block_id = -1
            elif (x % 2) == (y % 2) == 1:  # ブロック置き場の場合
                GameAreaInfo.node_list[index].block_id = block_count
                block_count += 1
            else:
                GameAreaInfo.node_list[index].block_id = -1

        # Lコースの交点の色をセットする
        GameAreaInfo.intersection_list = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN]
