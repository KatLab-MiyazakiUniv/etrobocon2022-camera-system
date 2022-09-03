"""最適動作探索モジュール.

走行体が指定されたノードに移動するための最適動作を探索する.
@author: KakinokiKanta miyashita64
"""

from typing import List
import copy
import numpy as np
from types import DynamicClassAttribute
from camera_system.coordinate import Coordinate
from game_area_info import GameAreaInfo
from robot import Robot, Direction
from motion_converter_mock import MotionConverterMock  # ToDo: 動作変換が実装でき次第差し替える.
from composite_game_motion import CompositeGameMotion


class OptimalMotionSearcher:
    """最適動作探索クラス."""

    def search(self, start_robot: Robot, goal_node: Node) -> CompositeGameMotion:
        """最適動作を探索する."""
        # 遷移可能な状態を出す
        # 8通りのロボット状態を作成
        robot = copy.copy(start_robot)
        robots = self.next_robots(robot)
        
        
        #コストを計算する
     
            
    def next_robots(self, current_robot: Robot) -> List[Robot]:
        """1つのゲーム動作で遷移可能な走行体の状態を返す"""
        angs = np.array([direction.value * 45 + 90 for direction in Direction])

        dys = np.round(-np.sin(np.radians(angs)))
        dxs = np.round(-np.cos(np.radians(angs)))

        coords = np.array([robot.coord.y, robot.coord.x]) + np.stack([dys, dxs], 1)
        
        no_rotate_directions = GameAreaInfo.get_no_rotate_direction(current_robot)
        no_entry_coordinates = GameAreaInfo.get_no_entry_coordinate(current_robot)
        robots = np.array([Robot(coords[direction.value], direction.value) for direction in Direction 
                           if not direction.value in no_rotate_directions
                           and not Coordinate(*coords[direction.value]) in no_entry_coordinates])
        
        return robots