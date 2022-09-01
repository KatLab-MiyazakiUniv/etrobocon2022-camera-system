"""ゲームエリア情報モジュール.

ゲームエリア情報を保持するクラスを定義している
@author: kodama0720
"""

from typing import List, Tuple, Dict
from robot import Robot, Direction
from color_changer import Color
from node import Node, NodeType
from coordinate import Coordinate


class GameAreaInfo:
    """ゲームエリア情報を保持するクラス.

    Attributes:
        __cross ノードが交点
        __middle ノードが中点
        __block_storage ノードがブロック置き場
        block_id_list (List[int]): ブロック(色ID)
        base_id_list (List[int]): ベースブロック(色ID)
        end_id (List[int]): ボーナスブロック(色ID)
        node_list (List[Node]): ノードリスト(ノード)
        base_color_dict (Dict{int, str}): ベースエリアの色ID(赤、黄、緑、青)
        __east_cand_list = (List[Node]): 東の候補ノードになりうる座標リスト
        __south_cand_list = (List[Node]): 南の候補ノードになりうる座標リスト
        __west_cand_list = (List[Node]): 西の候補ノードになりうる座標リスト
        __north_cand_list = (List[Node]): 北の候補ノードになりうる座標リスト
    """

    __cross = NodeType.CROSS.value
    __middle = NodeType.MIDDLE.value
    __block_storage = NodeType.BLOCK.value
    block_id_list = []
    base_id_list = []
    end_id = []
    node_list = [
        Node(-1, Coordinate(0, 0), __cross), Node(-1, Coordinate(1, 0), __middle),
        Node(-1, Coordinate(2, 0), __cross), Node(-1, Coordinate(3, 0), __middle),
        Node(-1, Coordinate(4, 0), __cross), Node(-1, Coordinate(5, 0), __middle),
        Node(-1, Coordinate(6, 0), __cross),
        Node(-1, Coordinate(0, 1), __cross), Node(0, Coordinate(1, 1), __block_storage),
        Node(-1, Coordinate(2, 1), __cross), Node(1, Coordinate(3, 1), __block_storage),
        Node(-1, Coordinate(4, 1), __cross), Node(2, Coordinate(5, 1), __block_storage),
        Node(-1, Coordinate(6, 1), __cross),
        Node(-1, Coordinate(0, 2), __cross), Node(-1, Coordinate(1, 2), __middle),
        Node(-1, Coordinate(2, 2), __cross), Node(-1, Coordinate(3, 2), __middle),
        Node(-1, Coordinate(4, 2), __cross), Node(-1, Coordinate(5, 2), __middle),
        Node(-1, Coordinate(6, 2), __cross),
        Node(-1, Coordinate(0, 3), __cross), Node(3, Coordinate(1, 3), __block_storage),
        Node(-1, Coordinate(2, 3), __cross), Node(-1, Coordinate(3, 3), __middle),
        Node(-1, Coordinate(4, 3), __cross), Node(4, Coordinate(5, 3), __block_storage),
        Node(-1, Coordinate(6, 3), __cross),
        Node(-1, Coordinate(0, 4), __cross), Node(-1, Coordinate(1, 4), __middle),
        Node(-1, Coordinate(2, 4), __cross), Node(-1, Coordinate(3, 4), __middle),
        Node(-1, Coordinate(4, 4), __cross), Node(-1, Coordinate(5, 4), __middle),
        Node(-1, Coordinate(6, 4), __cross),
        Node(-1, Coordinate(0, 5), __cross), Node(5, Coordinate(1, 5), __block_storage),
        Node(-1, Coordinate(2, 5), __cross), Node(6, Coordinate(3, 5), __block_storage),
        Node(-1, Coordinate(4, 5), __cross), Node(7, Coordinate(5, 5), __block_storage),
        Node(-1, Coordinate(6, 5), __cross),
        Node(-1, Coordinate(0, 6), __cross), Node(-1, Coordinate(1, 6), __middle),
        Node(-1, Coordinate(2, 6), __cross), Node(-1, Coordinate(3, 6), __middle),
        Node(-1, Coordinate(4, 6), __cross), Node(-1, Coordinate(5, 6), __middle),
        Node(-1, Coordinate(6, 6), __cross),
    ]
    base_color_dict = {Color.RED.value: "東", Color.YELLOW.value: "南",
                       Color.GREEN.value: "西", Color.BLUE.value: "北"}
    __east_cand_list = [
        Node(-1, Coordinate(6, 2), __cross), Node(-1, Coordinate(6, 3),
                                                  __middle), Node(-1, Coordinate(6, 4), __cross)
    ]
    __south_cand_list = [
        Node(-1, Coordinate(2, 6), __cross), Node(-1, Coordinate(3, 6),
                                                  __middle), Node(-1, Coordinate(4, 6), __cross)
    ]
    __west_cand_list = [
        Node(-1, Coordinate(0, 2), __cross), Node(-1, Coordinate(0, 3),
                                                  __middle), Node(-1, Coordinate(0, 4), __cross)
    ]
    __north_cand_list = [
        Node(-1, Coordinate(2, 0), __cross), Node(-1, Coordinate(3, 0),
                                                  __middle), Node(-1, Coordinate(4, 0), __cross)
    ]

    @staticmethod
    def get_candidate_node(color: int) -> List[Node]:
        """設置先ノードの候補を取得する関数.

        Args:
            color: 運搬するブロックの色

        Returns:
            List[Node]: 候補ノード
        """
        # 一致する要素(候補ノードになりうるノードの中で設置済みのブロックが無いノード)を返す
        if GameAreaInfo.base_color_dict[color] == "東":
            cand = [east_cand.coord for node in GameAreaInfo.node_list
                    for east_cand in GameAreaInfo.__east_cand_list
                    if node.coord == east_cand.coord and node.block_id == -1]
        elif GameAreaInfo.base_color_dict[color] == "南":
            cand = [south_cand.coord for node in GameAreaInfo.node_list
                    for southt_cand in GameAreaInfo.__south_cand_list
                    if node.coord == south_cand.coord and node.block_id == -1]
            return list(set(GameAreaInfo.node_list) & set(GameAreaInfo.__south_cand_list))
        elif GameAreaInfo.base_color_dict[color] == "西":
            cand = [west_cand.coord for node in GameAreaInfo.node_list
                    for west_cand in GameAreaInfo.__west_cand_list
                    if node.coord == west_cand.coord and node.block_id == -1]
        else:
            cand = [north_cand.coord for node in GameAreaInfo.node_list
                    for north_cand in GameAreaInfo.__north_cand_list
                    if node.coord == north_cand.coord and node.block_id == -1]

        return cand

    @staticmethod
    def get_no_transported_block() -> List[Node]:
        """運搬していないブロックがあるブロック置き場を取得する関数.

        Returns:
            List[Node]: 運搬していないブロックがあるブロック置き場のノード
        """
        no_trans_block_list = []

        # ブロックがブロック置き場にあるノードをリストに格納する
        for node in GameAreaInfo.node_list:
            if node.block_id != -1:  # ブロックがあるノード
                if node.node_type == GameAreaInfo.__block_storage:  # ブロック置き場のノード
                    no_trans_block_list.append(node)

        return no_trans_block_list

    @staticmethod
    def get_no_entry_coordinate(robot) -> List[Node]:
        """走行禁止座標を取得する関数.

        Args:
            robot: 仮想走行体

        Returns:
            List[Coordinate]: 走行禁止座標の座標リスト
        """
        coord = robot.coord
        no_entry_list = []

        # 東にブロック
        if robot.coord.x < 6:
            # 東の座標
            block_coord = Coordinate(robot.coord.x+1, robot.coord.y)
            # 東の座標にブロックが存在する場合、東を走行禁止座標に追加
            east_coord = [
                node.coord for node in GameAreaInfo.node_list
                if node.block_id != -1 and node.coord == block_coord
            ]
            no_entry_list += east_coord
            if east_coord:
                if block_coord.y > 0:
                    # 北東を走行禁止座標に追加
                    no_entry_list.append(Coordinate(block_coord.x, block_coord.y-1))
                if block_coord.y < 6:
                    # 南東を走行禁止座標に追加
                    no_entry_list.append(Coordinate(block_coord.x, block_coord.y+1))

        # 南にブロック
        if robot.coord.y < 6:
            # 南の座標
            block_coord = Coordinate(robot.coord.x, robot.coord.y+1)
            # 南の座標にブロックが存在する場合、南を走行禁止座標に追加
            south_coord = [
                node.coord for node in GameAreaInfo.node_list
                if node.block_id != -1 and node.coord == block_coord
            ]
            no_entry_list += south_coord
            if south_coord:
                if block_coord.x > 0:
                    # 南西を走行禁止座標に追加
                    no_entry_list.append(Coordinate(block_coord.x-1, block_coord.y))
                if block_coord.x < 6:
                    # 南東を走行禁止座標に追加
                    no_entry_list.append(Coordinate(block_coord.x+1, block_coord.y))

        # 西にブロック
        if robot.coord.x > 0:
            # 西の座標
            block_coord = Coordinate(robot.coord.x-1, robot.coord.y)
            # 西の座標にブロックが存在する場合、西を走行禁止座標に追加
            west_coord = [
                node.coord for node in GameAreaInfo.node_list
                if node.block_id != -1 and node.coord == block_coord
            ]
            no_entry_list += west_coord
            if west_coord:
                if block_coord.x > 0:
                    # 北西を走行禁止座標に追加
                    no_entry_list.append(Coordinate(block_coord.x, block_coord.y-1))
                if block_coord.x < 6:
                    # 南西を走行禁止座標に追加
                    no_entry_list.append(Coordinate(block_coord.x, block_coord.y+1))

        # 北にブロック
        if robot.coord.y > 0:
            # 北の座標
            block_coord = Coordinate(robot.coord.x, robot.coord.y-1)
            # 北の座標にブロックが存在する場合、北を走行禁止座標に追加
            north_coord = [
                node.coord for node in GameAreaInfo.node_list
                if node.block_id != -1 and node.coord == block_coord
            ]
            no_entry_list += north_coord
            if north_coord:
                if block_coord.x > 0:
                    # 北西を走行禁止座標に追加
                    no_entry_list.append(Coordinate(block_coord.x-1, block_coord.y))
                if block_coord.x < 6:
                    # 北東を走行禁止座標に追加
                    no_entry_list.append(Coordinate(block_coord.x+1, block_coord.y))

        return no_entry_list

    @staticmethod
    def get_no_rotate_direction(robot) -> List[int]:
        """回頭禁止方向を取得する関数.

        Args:
            robot: 仮想走行体

        Returns:
            List[int]: 回頭禁止方向の方位リスト
        """
        coord = robot.coord
        direct = robot.direct
        no_rotate_list = []

        # 東の座標
        block_coord = Coordinate(robot.coord.x+1, robot.coord.y)
        # 東の座標にブロックが存在する場合、西を回頭禁止方向に追加
        no_rotate_list += [
            Direction.W.value for node in GameAreaInfo.node_list
            if node.block_id != -1 and node.coord == block_coord
        ]
        # 南の座標
        block_coord = Coordinate(robot.coord.x, robot.coord.y+1)
        # 南の座標にブロックが存在する場合、北を回頭禁止方向に追加
        no_rotate_list += [
            Direction.N.value for node in GameAreaInfo.node_list
            if node.block_id != -1 and node.coord == block_coord]
        # 西の座標
        block_coord = Coordinate(robot.coord.x-1, robot.coord.y)
        # 西の座標にブロックが存在する場合、東を回頭禁止方向に追加
        no_rotate_list += [
            Direction.E.value for node in GameAreaInfo.node_list
            if node.block_id != -1 and node.coord == block_coord]
        # 北の座標
        block_coord = Coordinate(robot.coord.x, robot.coord.y-1)
        # 北の座標にブロックが存在する場合、南を回頭禁止方向に追加
        no_rotate_list += [
            Direction.S.value for node in GameAreaInfo.node_list
            if node.block_id != -1 and node.coord == block_coord]

        # 回頭禁止方向が2つ以上ある場合、それらの間にある方位も回頭禁止方向
        if len(no_rotate_list) >= 2:
            if min(no_rotate_list) < direct and direct < max(no_rotate_list):
                for i in range(min(no_rotate_list)):
                    no_rotate_list.append(i)
                for i in range(max(no_rotate_list)+1, 8):
                    no_rotate_list.append(i)
            else:
                for i in range(min(no_rotate_list)+1, max(no_rotate_list)):
                    no_rotate_list.append(i)

        return no_rotate_list


if __name__ == "__main__":
    robo = Robot(Coordinate(1, 2), Direction.N.value)

    color = Color.RED.value

    GameAreaInfo.block_id_list = [
        Color.RED.value, Color.RED.value, Color.YELLOW.value,
        Color.YELLOW.value, Color.GREEN.value, Color.GREEN.value,
        Color.BLUE.value, Color.BLUE.value
    ]
    GameAreaInfo.base_id_list = [
        Color.RED.value, Color.YELLOW.value,
        Color.GREEN.value, Color.BLUE.value
    ]
    GameAreaInfo.end_id = Color.RED.value
    print(GameAreaInfo.block_id_list)
    print(GameAreaInfo.base_id_list)
    print(GameAreaInfo.end_id)

    print("候補ノード")
    print(GameAreaInfo.get_candidate_node(color))
    print("未運搬のブロックがあるブロック置き場")
    print(GameAreaInfo.get_no_transported_block())
    print("走行禁止座標")
    print(GameAreaInfo.get_no_entry_coordinate(robo))
    print("回頭禁止方向")
    print(GameAreaInfo.get_no_rotate_direction(robo))
