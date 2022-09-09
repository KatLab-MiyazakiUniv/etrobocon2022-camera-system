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
from motion_converter_mock import MotionConverterMock  # ToDo: 動作変換が実装でき次第差し替える.
# 動作確認用
import time
from color_changer import Color


class OptimalMotionSearcher:
    """最適動作探索クラス."""

    # 縦横移動にかかるコストの目安
    __VERTICAL_COST = 0.5480
    # 斜め移動にかかるコストの目安
    __DIAGONAL_COST = 0.7840

    @classmethod
    def search(cls, start_robot: Robot, goal_node: Node) -> CompositeGameMotion:
        """開始状態から目標ノードに遷移するための最適動作を探索する.

        Args:
            start_robot: 開始状態
            goal_node:   目標ノード
        Returns:
            目標ノードに遷移するためのゲーム動作群: CompositeGameMotion
        """
        # 探索する状態のハッシュ値を保持
        open = [cls.robot_hash(start_robot)]
        # 走行体について、状態のハッシュ値をキーに状態、遷移するための動作群、予測コスト、ロボットの遷移を保持
        # ToDo: エッジを保持する
        state_table = {
            open[0]: {"robot": copy.deepcopy(start_robot),
                      "motions": CompositeGameMotion(),
                      "cost": cls.pre_cost(start_robot, goal_node.coord),
                      "logs": [copy.deepcopy(start_robot)]}
        }

        # 探索対象がブロック設置動作か、ブロック取得動作か(True:設置, False:取得)
        is_set_motion = goal_node.node_type != NodeType.BLOCK.value
        # ブロック置き場でないゴールノード(=設置動作時)にブロックがある場合
        if is_set_motion and goal_node.block_id != -1:
            print("A block already exists at the goal node.")
            # 空のCompositeGameMotionを返す
            return CompositeGameMotion()

        # 最適動作を探索する
        while state_table[open[0]]["robot"].coord != goal_node.coord:
            # コストが最小な状態を取り出す
            min_cost_state = state_table[open.pop(0)]
            # 遷移可能な状態を取得する
            options = cls.next_robots(min_cost_state["robot"], is_set_motion, goal_node.coord)
            # 遷移可能な各状態について探索する
            for option in options:
                # 状態のハッシュ値を求める
                hash = cls.robot_hash(option)
                # 開始状態からその状態までの動作を保持する
                motions = copy.deepcopy(min_cost_state["motions"])
                motion = MotionConverterMock.convert(min_cost_state["robot"], option)
                motions.append_game_motion(motion)

                # 走行体の状態に関する情報を生成する
                state = {"robot": option,
                         "motions": motions,
                         "cost": motions.get_cost() + cls.pre_cost(option, goal_node.coord),
                         "logs": min_cost_state["logs"] + [option]}
                # テーブルにない状態については情報を登録する
                if hash not in state_table.keys():
                    state_table[hash] = state
                # テーブルにある状態をより低コストで実現できる場合は情報更新する
                elif state["cost"] < state_table[hash]["cost"]:
                    state_table[hash] = state
                # それ以外の場合、状態を破棄する
                else:
                    continue
                open.append(hash)

            # 遷移できる状態がない場合
            if open == []:
                print("ERROR: Impossible move (%d,%d,%s) to (%d,%d)." %
                      (start_robot.coord.x, start_robot.coord.y, start_robot.direct.name,
                       goal_node.coord.x, goal_node.coord.y))
                # 空のCompositeGameMotionを返す
                return CompositeGameMotion()

            # 最小コストのハッシュ値をリストの先頭に持ってくる
            list(set(open))
            min_hash = open[0]
            for op in open:
                if state_table[op]["cost"] < state_table[min_hash]["cost"]:
                    min_hash = op
            open.remove(min_hash)
            open.insert(0, min_hash)

        # 探索した移動経路を表示する
        print(state_table[open[0]]["logs"])
        # 探索した最適動作を返す
        return state_table[open[0]]["motions"]

    @classmethod
    def pre_cost(cls, start_robot: Robot, goal_coord: Coordinate) -> int:
        """予測コストを算出する.

        Args:
            start_robot: 走行体
            goal_coord:  ゴール座標
        Returns:
            予測コスト: int
        """
        dy = abs(start_robot.coord.y - goal_coord.y)
        dx = abs(start_robot.coord.x - goal_coord.x)
        # 斜めに移動できるだけ斜めに移動すると想定する
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

        # 座標の移動にかかるコスト
        move_cost = vertical_distance*cls.__VERTICAL_COST + diagonal_distance*cls.__DIAGONAL_COST
        # 方向転換にかかるコスト
        rotate_cost = rotate_costs[rotate_angle]

        return move_cost + rotate_cost

    @classmethod
    def next_robots(cls, current_robot: Robot, is_set_motion: bool, goal_coord: Coordinate) -> List[Robot]:  # noqa
        """1つのゲーム動作で遷移可能な走行体の状態を返す.

        Args:
            current_robot: 現在の走行体
            is_set_motion: 設置動作か取得動作か(True:設置, False:取得)
            goal_coord: 目標座標
        Returns:
            遷移可能な走行体の状態: List[Robot]
        """
        # 8方位の角度を求める
        angs = np.array([direction.value * 45 + 90 for direction in Direction])
        # 各方位に進んだ際の移動ベクトルを求める
        dxs = np.round(-np.cos(np.radians(angs)))
        dys = np.round(-np.sin(np.radians(angs)))
        # 各方位に進んだ際に到達可能なxとyのリストを取得する
        xys = np.array([current_robot.coord.x, current_robot.coord.y]) + \
            np.stack([dxs, dys], 1).astype(int)
        # 遷移可能な走行体を生成する
        robots = [Robot(Coordinate(*xys[direction.value]), direction) for direction in Direction]

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
                  # 回頭禁止方向を持つ走行体を除外
                  and robot.direct not in no_rotate_directions
                  # 走行禁止座標を持つ走行体を除外
                  and robot.coord not in no_entry_coordinates
                  # 設置時、ゴール座標以外でゴール座標がある外周上の座標を持つ走行体を除外
                  and (
                      (is_set_motion and robot.coord == goal_coord)
                      or robot.coord not in goal_line_coordinates)
                  # 取得時、ゴール座標以外でブロックがある座標を持つ走行体を除外
                  and (
                      ((not is_set_motion) and robot.coord == goal_coord)
                      or robot.coord not in on_block_coordinates)]

        return robots

    @classmethod
    def robot_hash(cls, robot: Robot) -> int:
        """走行体の状態ごとのハッシュ値を計算する.

        Args:
            robot: 走行体の状態
        Returns:
            ハッシュ値: int
        """
        return int(100 * robot.coord.x + 10 * robot.coord.y + robot.direct.value)


if __name__ == "__main__":
    start_time = time.time()

    # コースを初期化する
    robo = Robot(Coordinate(4, 2), Direction.N)
    GameAreaInfo.block_id_list = [
        Color.RED.value, Color.YELLOW.value,
        Color.GREEN.value, Color.BLUE.value,
        Color.RED.value, Color.YELLOW.value,
        Color.GREEN.value, Color.BLUE.value
    ]
    GameAreaInfo.base_id_list = [
        Color.RED.value, Color.YELLOW.value,
        Color.GREEN.value, Color.BLUE.value
    ]
    GameAreaInfo.end_id = Color.RED.value

    # 全ブロックをブロックID順に運搬する
    for block_id, block_color_id in enumerate(GameAreaInfo.block_id_list):
        node = [node for node in GameAreaInfo.node_list if node.block_id == block_id][0]
        # 取得動作を探索する
        OptimalMotionSearcher.search(robo, node)
        # 設置先候補ノードを取得する
        candidate_coords = GameAreaInfo.get_candidate_node(block_color_id)
        costs = []
        # 各設置先候補ノードについて設置動作を探索する
        for candidate_coord in candidate_coords:
            candidate_node = GameAreaInfo.node_list[candidate_coord.y*7+candidate_coord.x]
            motions = OptimalMotionSearcher.search(robo, candidate_node)
            # 遷移不可能な動作のコストを大きく設定する
            cost = motions.get_cost()
            costs += [cost if cost > 0 else 100000000000]
        # マップを更新する
        mindex = costs.index(min(costs))
        set_node = GameAreaInfo.node_list[candidate_coords[mindex].y *
                                          7+candidate_coords[mindex].x]
        GameAreaInfo.move_block(block_id, set_node)

    print(time.time() - start_time)
