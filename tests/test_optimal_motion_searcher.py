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


class TestCompositeGameMotion(unittest.TestCase):
    """CompositeGameMotionのテスト."""

    def test_optiaml_motion_searcher(self):
        # ブロック取得ノードの座標を構成する値
        get_coord_elm = [1, 3, 5]
        # ブロック設置ノードの座標を構成する値
        set_coord_elm = [2, 3, 4]
        # 走行体の座標を構成する値
        robot_coord_elm = [2, 4]

        for robot_x in robot_coord_elm:
            for robot_y in robot_coord_elm:
                # ブロック取得
                for node_x in get_coord_elm:
                    for node_y in get_coord_elm:
                        if node_x == node_y == 3:
                            continue
                        node = GameAreaInfo.node_list[node_y * 7 + node_x]
                        robot = Robot(Coordinate(robot_x, robot_y), Direction.N)
                        with redirect_stdout(open(os.devnull, 'w')) as redirect:
                            OptimalMotionSearcher.search(robot, node)
                            redirect.close()
                # ブロック設置
                for node_x in [0, 6]:
                    for node_y in set_coord_elm:
                        node = GameAreaInfo.node_list[node_y * 7 + node_x]
                        robot = Robot(Coordinate(robot_x, robot_y), Direction.N)
                        with redirect_stdout(open(os.devnull, 'w')) as redirect:
                            OptimalMotionSearcher.search(robot, node)
                            redirect.close()
                for node_x in set_coord_elm:
                    for node_y in [0, 6]:
                        node = GameAreaInfo.node_list[node_y * 7 + node_x]
                        robot = Robot(Coordinate(robot_x, robot_y), Direction.N)
                        with redirect_stdout(open(os.devnull, 'w')) as redirect:
                            OptimalMotionSearcher.search(robot, node)
                            redirect.close()
