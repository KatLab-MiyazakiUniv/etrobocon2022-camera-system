"""ゲームエリア情報モジュール.

ゲームエリア情報を保持するクラスを定義している
@author: kodama0720
"""

from typing import List
from robot import Robot, Direction
from color_changer import Color
from node import Node, NodeType
from coordinate import Coordinate


class GameAreaInfo:
    """ゲームエリア情報を保持するクラス.

    Attributes:
        block_color_list (List[Color]): ブロックの色のリスト
        base_color_list (List[Color]): ベースブロックの色のリスト
        bonus_color (List[Color]): ボーナスブロックの色
        intersection_list (List[Color]): 交点の色のリスト
        node_list (List[Node]): ノードリスト(ノード)
        __east_cand_list = (List[Node]): 東の候補ノードになりうる座標リスト
        __south_cand_list = (List[Node]): 南の候補ノードになりうる座標リスト
        __west_cand_list = (List[Node]): 西の候補ノードになりうる座標リスト
        __north_cand_list = (List[Node]): 北の候補ノードになりうる座標リスト
    """

    block_color_list = []
    base_color_list = []
    bonus_color = []
    intersection_list = []
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
    __east_cand_list = [
        Node(-1, Coordinate(6, 2)), Node(-1, Coordinate(6, 3)), Node(-1, Coordinate(6, 4))
    ]
    __south_cand_list = [
        Node(-1, Coordinate(2, 6)), Node(-1, Coordinate(3, 6)), Node(-1, Coordinate(4, 6))
    ]
    __west_cand_list = [
        Node(-1, Coordinate(0, 2)), Node(-1, Coordinate(0, 3)), Node(-1, Coordinate(0, 4))
    ]
    __north_cand_list = [
        Node(-1, Coordinate(2, 0)), Node(-1, Coordinate(3, 0)), Node(-1, Coordinate(4, 0))
    ]

    @staticmethod
    def get_candidate_node(color: Color) -> List[Node]:
        """設置先ノードの候補を取得する関数.

        Args:
            color: 運搬するブロックの色

        Returns:
            List[Node]: 候補ノード
        """
        # ベースエリアの色と東西南北の対応表
        base_color_dict = {GameAreaInfo.base_color_list[0].value: "東",
                           GameAreaInfo.base_color_list[1].value: "南",
                           GameAreaInfo.base_color_list[2].value: "西",
                           GameAreaInfo.base_color_list[3].value: "北"}

        color_id = color.value  # colorをidに直す
        # 一致する要素(候補ノードになりうるノードの中で設置済みのブロックが無いノード)を返す
        if base_color_dict[color_id] == "東":
            cand = [east_cand for node in GameAreaInfo.node_list
                    for east_cand in GameAreaInfo.__east_cand_list
                    if node.coord == east_cand.coord and node.block_id == -1]
        elif base_color_dict[color_id] == "南":
            cand = [south_cand for node in GameAreaInfo.node_list
                    for southt_cand in GameAreaInfo.__south_cand_list
                    if node.coord == south_cand.coord and node.block_id == -1]
        elif base_color_dict[color_id] == "西":
            cand = [west_cand for node in GameAreaInfo.node_list
                    for west_cand in GameAreaInfo.__west_cand_list
                    if node.coord == west_cand.coord and node.block_id == -1]
        else:
            cand = [north_cand for node in GameAreaInfo.node_list
                    for north_cand in GameAreaInfo.__north_cand_list
                    if node.coord == north_cand.coord and node.block_id == -1]

        return cand

    @staticmethod
    def get_no_transported_block() -> List[Node]:
        """運搬していないブロックがあるブロック置き場を取得する関数.

        Returns:
            List[Node]: 運搬していないブロックがあるブロック置き場のノード
        """
        no_trans_block_color_list = []

        # ブロックがブロック置き場にあるノードをリストに格納する
        for node in GameAreaInfo.node_list:
            if node.block_id != -1:  # ブロックがあるノード
                if node.node_type == NodeType.BLOCK:  # ブロック置き場のノード
                    no_trans_block_color_list.append(node)

        return no_trans_block_color_list

    @staticmethod
    def get_no_entry_coordinate(robot) -> List[Coordinate]:
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
    def get_no_rotate_direction(robot) -> List[Direction]:
        """回頭禁止方向を取得する関数.

        Args:
            robot: 仮想走行体

        Returns:
            List[Direction]: 回頭禁止方向の方位リスト
        """
        # 回頭禁止方向の方位リスト
        no_rotate_directions = []

        # 走行体の東のノード
        east_coord = Coordinate(robot.coord.x+1, robot.coord.y)
        node_id = int(east_coord.y * 7 + east_coord.x)
        if 0 <= node_id < 49:
            east_node = GameAreaInfo.node_list[node_id]
            # ノードにブロックが存在する場合、西を回頭禁止方向に追加
            if east_node.block_id != -1:
                no_rotate_directions += [Direction.W]

        # 走行体の南のノード
        south_coord = Coordinate(robot.coord.x, robot.coord.y+1)
        node_id = int(south_coord.y * 7 + south_coord.x)
        if 0 <= node_id < 49:
            south_node = GameAreaInfo.node_list[node_id]
            # ノードにブロックが存在する場合、北を回頭禁止方向に追加
            if south_node.block_id != -1:
                no_rotate_directions += [Direction.N]

        # 走行体の西のノード
        west_coord = Coordinate(robot.coord.x-1, robot.coord.y)
        node_id = int(west_coord.y * 7 + west_coord.x)
        if 0 <= node_id < 49:
            west_node = GameAreaInfo.node_list[node_id]
            # ノードにブロックが存在する場合、東を回頭禁止方向に追加
            if west_node.block_id != -1:
                no_rotate_directions += [Direction.E]

        # 走行体の北のノード
        north_coord = Coordinate(robot.coord.x, robot.coord.y-1)
        node_id = int(north_coord.y * 7 + north_coord.x)
        if 0 <= node_id < 49:
            north_node = GameAreaInfo.node_list[node_id]
            # ノードにブロックが存在する場合、南を回頭禁止方向に追加
            if north_node.block_id != -1:
                no_rotate_directions += [Direction.S]

        # 回頭禁止方向が2つ以上ある場合、それらの間にある方位も回頭禁止方向
        if len(no_rotate_directions) >= 2:
            min_direction_value = min([direction.value for direction in no_rotate_directions])
            max_direction_value = max([direction.value for direction in no_rotate_directions])
            if min_direction_value < robot.direct.value < max_direction_value:
                for direction_value in range(min_direction_value):
                    no_rotate_directions += [Direction(direction_value)]
                for direction_value in range(max_direction_value+1, 8):
                    no_rotate_directions += [Direction(direction_value)]
            else:
                for direction_value in range(min_direction_value+1, max_direction_value):
                    no_rotate_directions += [Direction(direction_value)]

        return no_rotate_directions


if __name__ == "__main__":
    robo = Robot(Coordinate(1, 2), Direction.N)

    color = Color.RED

    GameAreaInfo.block_color_list = [
        Color.RED, Color.RED, Color.YELLOW,
        Color.YELLOW, Color.GREEN, Color.GREEN,
        Color.BLUE, Color.BLUE
    ]
    GameAreaInfo.base_color_list = [
        Color.RED, Color.YELLOW,
        Color.GREEN, Color.BLUE
    ]
    GameAreaInfo.bonus_color = Color.RED
    print(GameAreaInfo.block_color_list)
    print(GameAreaInfo.base_color_list)
    print(GameAreaInfo.bonus_color)

    print("候補ノード")
    print(GameAreaInfo.get_candidate_node(color))
    print("未運搬のブロックがあるブロック置き場")
    for block in GameAreaInfo.get_no_transported_block():
        print(block.block_id, block.coord)
    print("走行禁止座標")
    print(GameAreaInfo.get_no_entry_coordinate(robo))
    print("回頭禁止方向")
    print(GameAreaInfo.get_no_rotate_direction(robo))
