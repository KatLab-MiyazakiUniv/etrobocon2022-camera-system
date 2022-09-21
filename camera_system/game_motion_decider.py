"""運搬動作決定モジュール.

あるブロックの運搬のためのゲーム動作を決定する
@author: miyashita64
"""

import copy
from typing import List
from game_area_info import GameAreaInfo
from node import Node, NodeType
from robot import Robot, Direction
from color_changer import Color
from coordinate import Coordinate
from optimal_motion_searcher import OptimalMotionSearcher
from composite_game_motion import CompositeGameMotion


class GameMotionDecider:
    """運搬動作決定クラス."""

    @classmethod
    def decide(cls, current_robot: Robot, target_block_id: int) -> List[CompositeGameMotion]:
        """指定されたブロックの運搬動作を決定して返す.

        Args:
            current_robot:   現在の走行体
            target_block_id: 運搬対象ブロックのID
        Returns:
            運搬動作後の走行体: Robot
        """
        # ブロックがあるノードを取得する
        on_block_node = [node for node in GameAreaInfo.node_list
                         if node.block_id == target_block_id]
        if on_block_node == []:
            print("Block %d is not exist." % (target_block_id))
            return []
        on_block_node = on_block_node[0]
        if on_block_node.node_type != NodeType.BLOCK:
            print("This block is alredy transported.")
            return []

        # ブロック取得動作の探索用ロボット
        get_robot = copy.deepcopy(current_robot)
        # ブロック取得動作を探索する
        get_block_game_motion = OptimalMotionSearcher.search(get_robot, on_block_node)

        # 設置先ノードの候補を取得する
        target_block_color = GameAreaInfo.block_color_list[target_block_id]
        candidate_nodes = GameAreaInfo.get_candidate_node(target_block_color)
        candidate_set_block_game_motions = []
        candidate_robots = []
        costs = []
        # 各設置先ノードの候補について設置動作を探索する
        for candidate_node in candidate_nodes:
            # ブロック設置動作の探索用ロボット
            candidate_set_robot = copy.deepcopy(get_robot)
            # ブロック設置動作を探索する
            candidate_set_block_game_motion = OptimalMotionSearcher.search(
                candidate_set_robot, candidate_node)
            candidate_set_block_game_motions += [candidate_set_block_game_motion]
            candidate_set_robots += [candidate_set_robot]
            # 動作が探索できなかった場合、コストを無限大にする
            cost = candidate_set_block_game_motion.get_cost()
            costs += [cost if cost > 0 else float("inf")]
        # コストが最小なブロック設置動作を採用する
        mindex = costs.index(min(costs))
        set_block_node = candidate_nodes[mindex]
        set_block_game_motion = candidate_set_block_game_motions[mindex]
        set_robot = candidate_set_robots[mindex]

        # 運搬対象のブロックを更新する
        GameAreaInfo.move_block(target_block_id, set_block_node)
        # ブロックを取得したとして、走行体の座標を更新する
        current_robot.coord = set_robot.coord
        current_robot.direct = set_robot.direct
        current_robot.edge = set_robot.edge
        # 運搬動作を返す
        return [get_block_game_motion, set_block_game_motion]


if __name__ == "__main__":
    # ゲームエリア情報の初期化
    robot = Robot(Coordinate(4, 4), Direction.E, "left")
    node_list = [
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
    GameAreaInfo.intersection_list = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN]

    # 運搬動作を決定する
    game_motions = []
    for block_id in range(len(GameAreaInfo.block_color_list)):
        game_motions += GameMotionDecider.decide(robot, block_id)
