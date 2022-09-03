"""最適動作探索モジュール.

走行体が指定されたノードに移動するための最適動作を探索する.
@author: KakinokiKanta miyashita64
"""

import numpy as np
import copy
from typing import List
from game_area_info import GameAreaInfo
from node import Node
from robot import Robot, Direction
from coordinate import Coordinate
from composite_game_motion import CompositeGameMotion
from motion_converter_mock import MotionConverterMock  # ToDo: 動作変換が実装でき次第差し替える.


class OptimalMotionSearcher:
    """最適動作探索クラス."""

    def search(self, start_robot: Robot, goal_node: Node) -> CompositeGameMotion:
        """最適動作を探索する."""
        # 探索用の仮想走行体を生成する
        robot = copy.copy(start_robot)
        # 遷移可能な状態を取得する
        robots = self.next_robots(robot)

        # コストを計算する

    def next_robots(self, current_robot: Robot) -> List[Robot]:
        """1つのゲーム動作で遷移可能な走行体の状態を返す."""
        # 8方位の角度を求める
        angs = np.array([direction.value * 45 + 90 for direction in Direction])
        # 各方位に進んだ際の移動ベクトルを求める
        dys = np.round(-np.sin(np.radians(angs)))
        dxs = np.round(-np.cos(np.radians(angs)))
        # 到達可能な座標を取得する
        coords = np.array([current_robot.coord.y, current_robot.coord.x]) + np.stack([dys, dxs], 1)

        # 回頭禁止方向を取得する
        no_rotate_directions = GameAreaInfo.get_no_rotate_direction(current_robot)
        # 走行禁止座標を取得する
        no_entry_coordinates = GameAreaInfo.get_no_entry_coordinate(current_robot)
        # 遷移可能な走行体の状態を生成する
        robots = np.array([Robot(coords[direction.value], direction.value)
                           for direction in Direction
                           if direction.value not in no_rotate_directions
                           and Coordinate(*coords[direction.value]) not in no_entry_coordinates])

        return robots
