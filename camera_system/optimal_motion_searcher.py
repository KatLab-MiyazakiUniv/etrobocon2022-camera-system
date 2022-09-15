"""最適動作探索モジュール.

走行体が指定されたノードに移動するための最適動作を探索する.
@author: KakinokiKanta miyashita64
"""

import numpy as np
import copy
import operator
from typing import List, Dict
from game_area_info import GameAreaInfo
from node import Node, NodeType
from robot import Robot, Direction
from coordinate import Coordinate
from composite_game_motion import CompositeGameMotion
from game_motion_converter import GameMotionConverter


class OptimalMotionSearcher:
    """最適動作探索クラス."""

    # 縦横移動にかかる最低限のコストの目安
    __VERTICAL_COST = 0.5480
    # 斜め移動にかかる最低限のコストの目安
    __DIAGONAL_COST = 0.7840

    @classmethod
    def search(cls, start_robot: Robot, goal_node: Node) -> CompositeGameMotion:
        """開始時の走行体から目標ノードに遷移するための最適動作を探索する.

        Args:
            start_robot: 開始時の走行体
            goal_node:   目標ノード
        Returns:
            目標ノードに遷移するためのゲーム動作群: CompositeGameMotion
        """
        # 探索する走行体のハッシュ値を保持
        open_hashs = [cls.__robot_hash(start_robot)]
        # 走行体のハッシュ値をキーに探索情報を保持
        transition_table = {
            open_hashs[0]: {"robot": copy.deepcopy(start_robot),                       # 走行体
                            "game_motions": CompositeGameMotion(),                     # 開始時からの動作群
                            "cost": cls.__predict_cost(start_robot, goal_node.coord),  # 推定コスト
                            "logs": [copy.deepcopy(start_robot)]}                      # 走行体の推移
        }

        # 探索対象がブロック設置動作か、ブロック取得動作か(True:設置, False:取得)
        is_set_motion = goal_node.node_type != NodeType.BLOCK
        # 設置動作探索時、ゴールノードにブロックがある場合
        if is_set_motion and goal_node.block_id != -1:
            print("A block already exists at the goal node.")
            # 空のCompositeGameMotionを返す
            return CompositeGameMotion()

        # 最適動作を探索する
        while transition_table[open_hashs[0]]["robot"].coord != goal_node.coord:
            # 推定コストが最小な走行体のハッシュ値(推定コスト = 初期状態からの実コスト + ゴールまでの予測コスト)
            min_cost_hash = open_hashs.pop(0)
            # 推定コストが最小な走行体についての探索情報
            min_cost_transition = transition_table[min_cost_hash]

            # 現状の走行体
            current_robot = min_cost_transition["robot"]
            # 遷移可能な走行体を取得する
            next_robots = cls.__next_robots(
                current_robot, goal_node.coord, is_set_motion)

            # 遷移可能な走行体について探索する
            for next_robot in next_robots:
                game_motion_converter = GameMotionConverter()
                # 開始時の走行体 -> 1ゲーム動作前の走行体 の動作群
                game_motions = copy.deepcopy(min_cost_transition["game_motions"])
                # 1ゲーム動作前の走行体 -> 探索対象の走行体 の動作
                game_motion = game_motion_converter.convert_game_motion(current_robot, next_robot)
                # 開始時の走行体 -> 探索対象の走行体 の動作群
                game_motions.append_game_motion(game_motion)
                # 推定コスト = 開始状態からの実コスト + ゴールまでの予測コスト
                cost = game_motions.get_cost() + cls.__predict_cost(next_robot, goal_node.coord)

                # 運搬対象の走行体に関する探索情報を生成する
                transition = {"robot": next_robot,
                              "game_motions": game_motions,
                              "cost": cost,
                              "logs": min_cost_transition["logs"] + [next_robot]}

                # 走行体のハッシュ値を求める
                next_hash = cls.__robot_hash(next_robot)

                # 探索情報がテーブルにない場合は探索情報を登録する
                if next_hash not in transition_table.keys():
                    transition_table[next_hash] = transition
                # 探索情報がテーブルにあり、より低コストで遷移できる場合は探索情報を更新する
                elif transition["cost"] < transition_table[next_hash]["cost"]:
                    transition_table[next_hash] = transition
                # それ以外の場合、探索情報を破棄する
                else:
                    continue
                # 遷移できる状態として追加する
                open_hashs.append(next_hash)

            # 遷移できる走行体がない場合
            if open_hashs == []:
                print("Impossible move (%d,%d,%s) to (%d,%d)." %
                      (start_robot.coord.x, start_robot.coord.y, start_robot.direct.name,
                       goal_node.coord.x, goal_node.coord.y))
                # 空のCompositeGameMotionを返す
                return CompositeGameMotion()

            # 最小コストのハッシュ値をリストの先頭に持ってくる
            list(set(open_hashs))
            min_hash = open_hashs[0]
            for op in open_hashs:
                if transition_table[op]["cost"] < transition_table[min_hash]["cost"]:
                    min_hash = op
            open_hashs.remove(min_hash)
            open_hashs.insert(0, min_hash)

        # 探索した最適動作を返す
        return transition_table[open_hashs[0]]["game_motions"]

    @classmethod
    def __predict_cost(cls, start_robot: Robot, goal_coord: Coordinate) -> int:
        """予測コストを算出する.

        Args:
            start_robot: 走行体
            goal_coord:  ゴール座標
        Returns:
            予測コスト: int
        """
        dy = abs(start_robot.coord.y - goal_coord.y)
        dx = abs(start_robot.coord.x - goal_coord.x)
        # できるだけ斜めに移動すると想定する
        diagonal_distance = dy if dy < dx else dx
        # 斜めに行けない分だけ縦横に移動すると想定する
        vertical_distance = abs(dy - dx)
        # ToDo: てきとーに設定した回頭角度ごとのコストを書き換える(ゲーム動作から取得する?)
        rotate_costs = {0: 0, 45: 0.5, 90: 1.0, 135: 1.5, 180: 2.0}
        # ゴールノード到達時の走行体の方位を推定する
        goal_direction = start_robot.direct
        if dy > dx:
            if start_robot.coord.y > goal_coord.y:
                goal_direction = Direction.N
            else:
                goal_direction = Direction.S
        elif dy < dx:
            if start_robot.coord.x > goal_coord.x:
                goal_direction = Direction.W
            else:
                goal_direction = Direction.E
        else:
            if start_robot.coord.y > goal_coord.y:
                if start_robot.coord.x > goal_coord.x:
                    goal_direction = Direction.NW
                else:
                    goal_direction = Direction.NE
            elif start_robot.coord.y < goal_coord.y:
                if start_robot.coord.x > goal_coord.x:
                    goal_direction = Direction.SW
                else:
                    goal_direction = Direction.SE
        # 方位の差を算出する
        dd = abs(start_robot.direct.value - goal_direction.value)
        # 逆回転を考慮する
        if dd > 4:
            dd = 8 - dd
        rotate_angle = dd * 45

        # 座標の移動に最低限かかると思われるコスト
        move_cost = vertical_distance*cls.__VERTICAL_COST + diagonal_distance*cls.__DIAGONAL_COST
        # 方向転換に最低限かかると思われるコスト
        rotate_cost = rotate_costs[rotate_angle]

        return move_cost + rotate_cost

    @classmethod
    def __next_robots(cls, current_robot: Robot, goal_coord: Coordinate, is_set_motion: bool) -> List[Robot]:  # noqa
        """1つのゲーム動作で遷移可能な走行体を返す.

        Args:
            current_robot: 現在の走行体
            goal_coord: 目標座標
            is_set_motion: 設置動作か取得動作か(True:設置, False:取得)
        Returns:
            遷移可能な走行体: List[Robot]
        """
        # 8方位の角度を求める
        angs = np.array([direction.value * 45 + 90 for direction in Direction])
        # 各方位に進んだ際の移動ベクトルを求める
        dxs = np.round(-np.cos(np.radians(angs)))
        dys = np.round(-np.sin(np.radians(angs)))
        # 各方位に進んだ際に到達可能なxとyのリストを取得する
        xys = np.array([current_robot.coord.x, current_robot.coord.y]) \
            + np.stack([dxs, dys], 1).astype(int)
        # 1つのゲーム動作で遷移可能な走行体を生成する
        robots = [Robot(Coordinate(*xys[direction.value]), direction, "none")
                  for direction in Direction]

        # 回頭禁止方向を取得する
        no_rotate_directions = GameAreaInfo.get_no_rotate_direction(current_robot)
        # 走行禁止座標を取得する
        no_entry_coordinates = GameAreaInfo.get_no_entry_coordinate(current_robot)
        # ブロックがあるノードを取得する
        on_block_coordinates = GameAreaInfo.get_on_block_coordinate()
        # 設置動作の探索の場合
        goal_line_coordinates = []
        if is_set_motion:
            # 設置先ノードがブロックエリア外周の上下(y座標が0か6)/左右どちらにあるか(True:上下, False:左右)
            is_border_y = goal_coord.y % 6 == 0
            # 設置先ノードがある外辺の座標を走行禁止座標とする
            if is_border_y:
                goal_line_coordinates += [Coordinate(x, goal_coord.y) for x in range(7)
                                          if x != goal_coord.x]
            else:
                goal_line_coordinates += [Coordinate(goal_coord.x, y) for y in range(7)
                                          if y != goal_coord.y]

        # 行動制限を考慮する
        robots = [robot for robot in robots if 0 <= robot.coord.y <= 6 and 0 <= robot.coord.x <= 6
                  # 回頭禁止方向を持つ走行体を除外する
                  and robot.direct not in no_rotate_directions
                  # 走行禁止座標を持つ走行体を除外する
                  and robot.coord not in no_entry_coordinates
                  # 設置時、ゴール座標以外でゴール座標がある外周上の座標を持つ走行体を除外する
                  and ((is_set_motion and robot.coord == goal_coord)
                       or (robot.coord not in goal_line_coordinates))
                  # 取得時、ゴール座標以外でブロックがある座標を持つ走行体を除外する
                  and (((not is_set_motion) and robot.coord == goal_coord)
                       or (robot.coord not in on_block_coordinates))]

        return robots

    @classmethod
    def __robot_hash(cls, robot: Robot) -> int:
        """走行体の状態ごとのハッシュ値を計算する.

        Args:
            robot: 走行体
        Returns:
            ハッシュ値: int
        """
        return int(100 * robot.coord.x + 10 * robot.coord.y + robot.direct.value)
