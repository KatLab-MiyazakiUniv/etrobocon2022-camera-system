"""運搬ブロック決定モジュール.

次に運搬するブロックを決定する
@author mutotaka0426
"""

from game_area_info import GameAreaInfo
from robot import Robot
from coordinate import Coordinate
from node import Node


class BlockSelector:
    """運搬ブロック決定クラス."""

    def select_block(self, robot: Robot) -> Node:
        """ゲームエリア情報を基に次に運搬するブロックを返す.

        Args:
            robot: 現在の走行体の状態

        Returns:
            Node: 次に運搬するブロックを持つノード
        """
        cand_nodes = GameAreaInfo.get_no_transported_block()  # ブロックID順に候補ブロックを持つノードを格納

        # 優先順位1: 走行体からのマンハッタン距離が小さいブロック
        if len(cand_nodes) > 1:  # 候補が複数ある場合
            # 走行体からのマンハッタン距離が最も小さいブロックを求める
            min_distance = min([self.__calculate_distance(robot.coord, node.coord)
                               for node in cand_nodes])
            # 走行体からのマンハッタン距離が最も小さいブロックを持つノードに絞り込む
            cand_nodes = [node for node in cand_nodes if min_distance ==
                          self.__calculate_distance(robot.coord, node.coord)]

        # 優先順位2: ダブルアップボーナスとなるブロック
        if len(cand_nodes) > 1:  # 候補が複数ある場合
            # ボーナスブロックと同じ色のブロックを持つノードに絞り込む
            double_up_nodes = [
                node for node in cand_nodes
                if GameAreaInfo.block_color_list[node.block_id] == GameAreaInfo.bonus_color]
            # ボーナスブロックと同じ色のブロックがない場合はcand_nodesはそのまま
            if double_up_nodes != []:
                cand_nodes = double_up_nodes

        # 優先順位3: 設置先までのマンハッタン距離が小さいブロック
        if len(cand_nodes) > 1:  # 候補が複数ある場合
            # 設置先までのマンハッタン距離が最も小さいブロックを求める
            min_distance = min([self.__calculate_distance(node.coord, destination.coord)
                                for node in cand_nodes
                                for destination in GameAreaInfo.get_candidate_node(
                                    GameAreaInfo.block_color_list[node.block_id])])
            # 設置先までのマンハッタン距離が最も小さいブロックを持つノードに絞り込む
            cand_nodes = [node for node in cand_nodes
                          for destination
                          in GameAreaInfo.get_candidate_node(
                              GameAreaInfo.block_color_list[node.block_id])
                          if min_distance == self.__calculate_distance(
                              node.coord, destination.coord)]

        # 優先順位4：ブロックIDの数字が小さいブロック
        return cand_nodes[0]

    def __calculate_distance(self, coord1: Coordinate, coord2: Coordinate) -> int:
        """2点座標のマンハッタン距離を求める.

        Args:
            coord1: 座標1
            coord2: 座標2

        Returns:
            int: 座標1と座標2のマンハッタン距離
        """
        return abs(coord1.x-coord2.x) + abs(coord1.y-coord2.y)
