"""最適動作探索のテストコードを記述するモジュール.

@author: miyashita64
"""

import unittest
import os
from contextlib import redirect_stdout

from optimal_motion_searcher import OptimalMotionSearcher
from game_area_info import GameAreaInfo
from node import Node
from robot import Robot, Direction
from coordinate import Coordinate
from color_changer import Color
from composite_game_motion import CompositeGameMotion
from color_changer import Color


class TestOptimalMotionSearcher(unittest.TestCase):
    """OptimalMotionSearcherのテスト."""

    def test_optiaml_motion_search_get_block(self):
        """全ブロック置き場への取得動作を探索する."""
<<<<<<< HEAD
        # ゲームエリア情報の初期化
        robot = Robot(Coordinate(4, 4), Direction.E, "left")
        GameAreaInfo.node_list = [
            Node(-1, Coordinate(0, 0)), Node(-1, Coordinate(1, 0)),
            Node(-1, Coordinate(2, 0)), Node(-1, Coordinate(3, 0)),
            Node(-1, Coordinate(4, 0)), Node(-1, Coordinate(5, 0)),
            Node(-1, Coordinate(6, 0)),
            Node(-1, Coordinate(0, 1)), Node(0, Coordinate(1, 1)),
            Node(-1, Coordinate(2, 1)), Node(1, Coordinate(3, 1)),
            Node(-1, Coordinate(4, 1)), Node(2, Coordinate(5, 1)),
            Node(-1, Coordinate(6, 1)),
            Node(-1, Coordinate(0, 2)), Node(-1, Coordinate(1, 2)),
            Node(-1, Coordinate(2, 2)), Node(-1, Coordinate(3, 2)),
            Node(-1, Coordinate(4, 2)), Node(-1, Coordinate(5, 2)),
            Node(-1, Coordinate(6, 2)),
            Node(-1, Coordinate(0, 3)), Node(3, Coordinate(1, 3)),
            Node(-1, Coordinate(2, 3)), Node(-1, Coordinate(3, 3)),
            Node(-1, Coordinate(4, 3)), Node(4, Coordinate(5, 3)),
            Node(-1, Coordinate(6, 3)),
            Node(-1, Coordinate(0, 4)), Node(-1, Coordinate(1, 4)),
            Node(-1, Coordinate(2, 4)), Node(-1, Coordinate(3, 4)),
            Node(-1, Coordinate(4, 4)), Node(-1, Coordinate(5, 4)),
            Node(-1, Coordinate(6, 4)),
            Node(-1, Coordinate(0, 5)), Node(5, Coordinate(1, 5)),
            Node(-1, Coordinate(2, 5)), Node(6, Coordinate(3, 5)),
            Node(-1, Coordinate(4, 5)), Node(7, Coordinate(5, 5)),
            Node(-1, Coordinate(6, 5)),
            Node(-1, Coordinate(0, 6)), Node(-1, Coordinate(1, 6)),
            Node(-1, Coordinate(2, 6)), Node(-1, Coordinate(3, 6)),
            Node(-1, Coordinate(4, 6)), Node(-1, Coordinate(5, 6)),
            Node(-1, Coordinate(6, 6)),
        ]
        GameAreaInfo.block_color_list = [
            Color.RED, Color.RED, Color.YELLOW,
            Color.YELLOW, Color.GREEN,
            Color.GREEN, Color.BLUE, Color.BLUE
        ]
        GameAreaInfo.base_color_list = [
            Color.RED, Color.YELLOW,
            Color.GREEN, Color.BLUE
        ]
        GameAreaInfo.bonus_color = Color.RED
=======
        # Lコースの交点の色をセットする
>>>>>>> 08d31dcd566f81cc9706ae0f5b473cdd5de726df
        GameAreaInfo.intersection_list = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN]

        # ブロック取得開始時の走行体の座標
        robot_coords = [Coordinate(2, 2), Coordinate(2, 4), Coordinate(4, 2), Coordinate(4, 4)]
        # ブロック取得の座標
        get_coords = [Coordinate(1, 1), Coordinate(1, 3), Coordinate(1, 5),
                      Coordinate(3, 1), Coordinate(3, 5),
                      Coordinate(5, 1), Coordinate(5, 3), Coordinate(5, 5)]

        for robot_coord in robot_coords:
            # ブロック取得について探索する
            for get_coord in get_coords:
                start_robot = Robot(robot_coord, Direction.N, "left")
                goal_node = GameAreaInfo.node_list[get_coord.y * 7 + get_coord.x]
                # 探索する
                get_game_motions = OptimalMotionSearcher.search(start_robot, goal_node)

                actual_cost = get_game_motions.get_cost()   # 探索した動作のコスト
                unexpected_cost = 0     # 期待しないコスト(探索失敗)

                # 取得動作は可能なため、探索した動作のコストが0は異常
                self.assertNotEqual(unexpected_cost, actual_cost)

    def test_optiaml_motion_search_set_block(self):
        """全ブロック置き場から全ブロック設置先への設置動作を探索する."""
<<<<<<< HEAD
        # ゲームエリア情報の初期化
        robot = Robot(Coordinate(4, 4), Direction.E, "left")
        GameAreaInfo.node_list = [
            Node(-1, Coordinate(0, 0)), Node(-1, Coordinate(1, 0)),
            Node(-1, Coordinate(2, 0)), Node(-1, Coordinate(3, 0)),
            Node(-1, Coordinate(4, 0)), Node(-1, Coordinate(5, 0)),
            Node(-1, Coordinate(6, 0)),
            Node(-1, Coordinate(0, 1)), Node(0, Coordinate(1, 1)),
            Node(-1, Coordinate(2, 1)), Node(1, Coordinate(3, 1)),
            Node(-1, Coordinate(4, 1)), Node(2, Coordinate(5, 1)),
            Node(-1, Coordinate(6, 1)),
            Node(-1, Coordinate(0, 2)), Node(-1, Coordinate(1, 2)),
            Node(-1, Coordinate(2, 2)), Node(-1, Coordinate(3, 2)),
            Node(-1, Coordinate(4, 2)), Node(-1, Coordinate(5, 2)),
            Node(-1, Coordinate(6, 2)),
            Node(-1, Coordinate(0, 3)), Node(3, Coordinate(1, 3)),
            Node(-1, Coordinate(2, 3)), Node(-1, Coordinate(3, 3)),
            Node(-1, Coordinate(4, 3)), Node(4, Coordinate(5, 3)),
            Node(-1, Coordinate(6, 3)),
            Node(-1, Coordinate(0, 4)), Node(-1, Coordinate(1, 4)),
            Node(-1, Coordinate(2, 4)), Node(-1, Coordinate(3, 4)),
            Node(-1, Coordinate(4, 4)), Node(-1, Coordinate(5, 4)),
            Node(-1, Coordinate(6, 4)),
            Node(-1, Coordinate(0, 5)), Node(5, Coordinate(1, 5)),
            Node(-1, Coordinate(2, 5)), Node(6, Coordinate(3, 5)),
            Node(-1, Coordinate(4, 5)), Node(7, Coordinate(5, 5)),
            Node(-1, Coordinate(6, 5)),
            Node(-1, Coordinate(0, 6)), Node(-1, Coordinate(1, 6)),
            Node(-1, Coordinate(2, 6)), Node(-1, Coordinate(3, 6)),
            Node(-1, Coordinate(4, 6)), Node(-1, Coordinate(5, 6)),
            Node(-1, Coordinate(6, 6)),
        ]
        GameAreaInfo.block_color_list = [
            Color.RED, Color.RED, Color.YELLOW,
            Color.YELLOW, Color.GREEN,
            Color.GREEN, Color.BLUE, Color.BLUE
        ]
        GameAreaInfo.base_color_list = [
            Color.RED, Color.YELLOW,
            Color.GREEN, Color.BLUE
        ]
        GameAreaInfo.bonus_color = Color.RED
=======
        # Lコースの交点の色をセットする
>>>>>>> 08d31dcd566f81cc9706ae0f5b473cdd5de726df
        GameAreaInfo.intersection_list = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN]

        # ブロック取得の座標
        get_coords = [Coordinate(1, 1), Coordinate(1, 3), Coordinate(1, 5),
                      Coordinate(3, 1), Coordinate(3, 5),
                      Coordinate(5, 1), Coordinate(5, 3), Coordinate(5, 5)]
        # ブロック設置の座標
        set_coords = [Coordinate(0, 2), Coordinate(0, 3), Coordinate(0, 4),
                      Coordinate(2, 0), Coordinate(3, 0), Coordinate(4, 0),
                      Coordinate(2, 6), Coordinate(3, 6), Coordinate(4, 6),
                      Coordinate(6, 2), Coordinate(6, 3), Coordinate(6, 4)]

        # 各ブロック置き場について
        for get_coord in get_coords:
            getted_robot = Robot(get_coord, Direction.N, "left")
            actual_success_count = 0        # 探索成功数
            unexpected_success_count = 0    # 期待しない探索成功数
            # ブロック設置について探索する
            for set_coord in set_coords:
                goal_node = GameAreaInfo.node_list[set_coord.y * 7 + set_coord.x]
                # 探索失敗のメッセージを無視するため標準出力を非表示にする
                with redirect_stdout(open(os.devnull, 'w')) as redirect:
                    # 探索する
                    set_game_motions = OptimalMotionSearcher.search(getted_robot, goal_node)
                    cost = set_game_motions.get_cost()
                    # コストが0より大きければ、運搬動作を探索できている
                    if cost > 0:
                        actual_success_count += 1
                    redirect.close()
            # 少なくとも1つの経路はあるはずなので、探索成功数0回は異常
            self.assertNotEqual(unexpected_success_count, actual_success_count)
