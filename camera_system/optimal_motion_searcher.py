"""最適動作探索モジュール.

走行体が指定されたノードに移動するための最適動作を探索する.
@author: KakinokiKanta miyashita64
"""

import numpy as np
import copy
from typing import List, Dict
from game_area_info import GameAreaInfo
from node import Node
from robot import Robot, Direction
from coordinate import Coordinate
from composite_game_motion import CompositeGameMotion
from motion_converter_mock import MotionConverterMock  # ToDo: 動作変換が実装でき次第差し替える.


class OptimalMotionSearcher:
    """最適動作探索クラス."""
    @classmethod
    def search(cls, start_robot: Robot, goal_node: Node) -> CompositeGameMotion:
        """最適動作を探索する."""
        # 探索する状態のハッシュ値を保持
        open = [cls.robot_hash(start_robot)]
        # 各状態について、状態、遷移するための動作群、予測コストを保持
        state_table = {
            open[0]: { "robot": copy.copy(start_robot),
                       "motions": CompositeGameMotion(),
                       "cost": cls.pre_cost() }
        }

        while state_table[open[0]]["robot"].coord != goal_node.coord:
            # コストが最小な状態を取り出す
            min_robot_state = state_table[open.pop(0)]
            # 遷移可能な状態を取得する
            robots = cls.next_robots(min_robot_state["robot"])
            for robot in robots:
                hash = cls.robot_hash(robot)
                motions = copy.copy(min_robot_state["motions"])
                motion = MotionConverterMock.convert(min_robot_state["robot"], robot)
                state = { "robot": robot,
                          "motions": motions.append_game_motion(motion),
                          "cost": motions.get_cost() + cls.pre_cost(robot) }
                if hash not in state_table.keys():
                    state_table[hash] = state
                elif state["cost"] < state_table[hash]["cost"]:
                    state_table[hash] = state
                else:
                    continue
                # ToDo: openがコストの昇順になるようにhashを挿入する
        return state_table[open[0]]["motions"]

    @classmethod
    def pre_cost(cls, start_coord: Coordinate, end_coord: Coordinate) -> int:
        """予測コストを算出する.

        Args:
            start_coord:
            end_coord:
        
        Returns:
            予測コスト: int
        """
        return np.abs(start_coord.y - end_coord.y) + np.abs(start_coord.x - end_coord.x)

    @classmethod
    def next_robots(cls, current_robot: Robot) -> List[Robot]:
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

    @classmethod
    def robot_hash(cls, robot: Robot) -> int:
        """走行体の状態ごとのハッシュ値を計算する.

        Args:
            robot:
        
        Returns:
            ハッシュ値: int
        """
        
        return 100 * robot.coord.y + 10 * robot.coord.x + robot.direct.value