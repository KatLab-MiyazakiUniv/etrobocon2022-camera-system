"""GameMotionConverterクラスのテストコードを記述するモジュール.

@author: mutotaka0426
"""
import unittest

from camera_system.game_motion_converter import GameMotionConverter
from color_changer import Color
from robot import Robot, Direction
from coordinate import Coordinate
from game_area_info import GameAreaInfo
from block_to_intersection import BlockToIntersection
from block_to_middle import BlockToMiddle
from intersection_to_block import IntersectionToBlock
from intersection_to_middle import IntersectionToMiddle
from middle_to_block import MiddleToBlock
from middle_to_intersection import MiddleToIntersection
from middle_to_middle import MiddleToMiddle


class TestGameMotionConverter(unittest.TestCase):
    def test_return_block_to_intersection(self):
        """BlockToIntersection（ブロック置き場→交点）を返すテスト."""
        self.__init_game_area_info()  # ゲームエリア情報の初期化
        game_motion_converter = GameMotionConverter()  # インスタンス化
        current_robot = Robot(Coordinate(5, 5), Direction.E, "none")  # 現在の走行体
        next_robot = Robot(Coordinate(6, 4), Direction.NE, "none")  # 次の走行体
        is_set_motion = True  # 設置動作(ブロックを持っている状態）

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = BlockToIntersection(-45, Color.GREEN, True)

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
        is_set_motion = True  # 設置動作(ブロックを持っている状態）

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = BlockToMiddle(-45, True)

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
        is_set_motion = True  # 設置動作(ブロックを持っている状態）

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = IntersectionToBlock(-135, False, False, True)

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
        is_set_motion = True  # 設置動作(ブロックを持っている状態）

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = IntersectionToBlock(45, True, False, True)

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
        is_set_motion = True  # 設置動作(ブロックを持っている状態）

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = IntersectionToBlock(-45, False, True, True)

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
        is_set_motion = True  # 設置動作(ブロックを持っている状態）

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = IntersectionToBlock(0, False, True, True)

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
        is_set_motion = True  # 設置動作(ブロックを持っている状態）

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = IntersectionToMiddle(180, False, True)

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
        is_set_motion = True  # 設置動作(ブロックを持っている状態）

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = IntersectionToMiddle(-90, True, True)

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
        is_set_motion = True  # 設置動作(ブロックを持っている状態）

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = IntersectionToMiddle(45, True, True)

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
        is_set_motion = True  # 設置動作(ブロックを持っている状態）

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = MiddleToBlock(135, False, True)

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
        is_set_motion = True  # 設置動作(ブロックを持っている状態）

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = MiddleToBlock(0, True, True)

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
        is_set_motion = False  # 取得動作(ブロックを持っていない状態）

        # 反時計回りで45度回頭できる状況にする
        GameAreaInfo.node_list[3+5*7].block_id = -1  # x+y*7

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = MiddleToBlock(135, True, False)

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
        is_set_motion = False  # 取得動作(ブロックを持っていない状態）

        # 反時計回りで45度回頭できる状況にする
        GameAreaInfo.node_list[3+5*7].block_id = -1  # x+y*7

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = MiddleToBlock(-45, True, False)

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
        is_set_motion = False  # 取得動作(ブロックを持っていない状態）

        # 反時計回りで90度回頭できる状況にする
        GameAreaInfo.node_list[3+3*7].block_id = -1  # x+y*7

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = MiddleToIntersection(-90, Color.RED, False)

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
        is_set_motion = False  # 取得動作(ブロックを持っていない状態）

        # 反時計回りで135度回頭できる状況にする
        GameAreaInfo.node_list[1+1*7].block_id = -1  # x+y*7
        GameAreaInfo.node_list[1+3*7].block_id = -1  # x+y*7

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = MiddleToMiddle(-135, False, False)

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
        is_set_motion = False  # 取得動作(ブロックを持っていない状態）

        # 反時計回りで45度回頭しないといけない状況にする
        GameAreaInfo.node_list[1+3*7].block_id = -1  # x+y*7

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = MiddleToMiddle(-45, True, False)

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
        is_set_motion = False  # 取得動作(ブロックを持っていない状態）

        # 時計回りで225度回頭しないといけない状況にする
        GameAreaInfo.node_list[1+3*7].block_id = -1  # x+y*7

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = MiddleToMiddle(225, True, False)

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
        is_set_motion = False  # 取得動作(ブロックを持っていない状態）

        # 時計回りで225度回頭しないといけない状況にする
        GameAreaInfo.node_list[1+3*7].block_id = -1  # x+y*7

        actual = game_motion_converter.convert_game_motion(current_robot, next_robot, is_set_motion)
        expected = MiddleToMiddle(90, True, False)

        self.assertEqual(expected, actual)  # 期待したゲーム動作を取得しているかテスト

        expected_edge = "right"
        actual_edge = next_robot.edge
        self.assertEqual(expected_edge, actual_edge)  # 次の走行体のエッジを正しくセットできているかテスト

    def test_convert_game_motion_failure(self):
        """遷移できない場合のテスト."""
        with self.assertRaises(ValueError):
            self.__init_game_area_info()  # ゲームエリア情報の初期化
            game_motion_converter = GameMotionConverter()  # インスタンス化
            current_robot = Robot(Coordinate(2, 1), Direction.N, "left")  # 現在の走行体
            next_robot = Robot(Coordinate(2, 2), Direction.S, "none")  # 次の走行体
            is_set_motion = False  # 取得動作(ブロックを持っていない状態）

            # 両隣にブロックがあるため回頭できず，エラーを返す
            actual = game_motion_converter.convert_game_motion(
                current_robot, next_robot, is_set_motion)

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
