"""ゲームエリア情報モジュール.

ゲームエリア情報を保持するクラスを定義している
@author: kodama0720
"""

from typing import List, Tuple, Dict
from .robot import Robot, Direction
from .color_changer import Color


class GameInfo:
    """ゲームエリア情報を保持するクラス.

    Attributes:
        block_id_list (int): ブロック(色ID)
        base_id_list (int): ベースブロック(色ID)
        end_id (int): ボーナスブロック(色ID)
        node_dict (Dict[Tuple(int, int), int]): ノード([座標,ブロックID])
        base_color_dict (Dict{int, str}): ベースエリアの色ID(赤、黄、緑、青)
        __east_cand_list = (List[Tuple(int, int)]): 東の候補ノードになりうる座標リスト
        __south_cand_list = (List[Tuple(int, int)]): 南の候補ノードになりうる座標リスト
        __west_cand_list = (List[Tuple(int, int)]): 西の候補ノードになりうる座標リスト
        __north_cand_list = (List[Tuple(int, int)]): 北の候補ノードになりうる座標リスト
    """

    block_id_list = []
    base_id_list = []
    end_id = []
    node_dict = {
        (0, 0): -1, (0, 1): -1, (0, 2): -1, (0, 3): -1, (0, 4): -1, (0, 5): -1, (0, 6): -1,
        (1, 0): -1, (1, 1): 0,  (1, 2): -1, (1, 3): 1,  (1, 4): -1, (1, 5): 2,  (1, 6): -1,
        (2, 0): -1, (2, 1): -1, (2, 2): -1, (2, 3): -1, (2, 4): -1, (2, 5): -1, (2, 6): -1,
        (3, 0): -1, (3, 1): 3,  (3, 2): -1, (3, 3): -1, (3, 4): -1, (3, 5): 4,  (3, 6): -1,
        (4, 0): -1, (4, 1): -1, (4, 2): -1, (4, 3): -1, (4, 4): -1, (4, 5): -1, (4, 6): -1,
        (5, 0): -1, (5, 1): 5,  (5, 2): -1, (5, 3): 6,  (5, 4): -1, (5, 5): 7,  (5, 6): -1,
        (6, 0): -1, (6, 1): -1, (6, 2): -1, (6, 3): -1, (6, 4): -1, (6, 5): -1, (6, 6): -1,
    }
    base_color_dict = {Color.RED.value: "東", Color.YELLOW.value: "南",
                       Color.GREEN.value: "西", Color.BLUE.value: "北"}
    __east_cand_list = [(6, 2), (6, 3), (6, 4)]  # 東の候補ノードになりうる座標リスト
    __south_cand_list = [(2, 6), (3, 6), (4, 6)]  # 南の候補ノードになりうる座標リスト
    __west_cand_list = [(0, 2), (0, 3), (0, 4)]  # 西の候補ノードになりうる座標リスト
    __north_cand_list = [(2, 0), (3, 0), (4, 0)]  # 北の候補ノードになりうる座標リスト

    def get_candidate_node(self, color: int) -> List[Tuple[int, int]]:
        """設置先ノードの候補を取得する関数.

        Args:
            color: 運搬するブロックの色

        Returns:
            List[Tuple(int, int)]: 候補ノードの座標リスト
        """
        cand_list = []

        if GameInfo.base_color_dict[color] == "東":
            for cand in GameInfo.__east_cand_list:
                if GameInfo.node_dict[cand] == -1:  # 対象のノードに既に設置済みのブロックがなければ候補に入れる
                    cand_list.append(cand)
        elif GameInfo.base_color_dict[color] == "南":
            for cand in GameInfo.__south_cand_list:
                if GameInfo.node_dict[cand] == -1:
                    cand_list.append(cand)
        elif GameInfo.base_color_dict[color] == "西":
            for cand in GameInfo.__west_cand_list:
                if GameInfo.node_dict[cand] == -1:
                    cand_list.append(cand)
        else:
            for cand in GameInfo.__north_cand_list:
                if GameInfo.node_dict[cand] == -1:
                    cand_list.append(cand)

        return cand_list

    def get_no_transported_block(self) -> List[Tuple[int, int]]:
        """運搬していないブロックがあるブロック置き場を取得する関数.

        Returns:
            List[Tuple(int, int)]: 運搬していないブロックがあるブロック置き場の座標リスト
        """
        no_trans_block_list = []  # 候補ノードの座標リストを格納する

        for key, value in GameInfo.node_dict.items():
            x = key[0]
            y = key[1]
            block_id = value

            if block_id != -1:  # ブロックがない座標を省く
                if x % 2 != 0 and y % 2 != 0:  # xとyが奇数ならば運搬していないブロックと判定
                    no_trans_block_list.append((x, y))

        return no_trans_block_list

    def get_no_entry_coordinate(self, robot) -> List[Tuple[int, int]]:
        """走行禁止座標を取得する関数.

        Args:
            robot: 仮想走行体

        Returns:
            List[Tuple(int, int)]: 走行禁止座標の座標リスト
        """
        x = robot.coord[0]
        y = robot.coord[1]
        no_entry_list = []

        if (x+1, y) in GameInfo.node_dict.keys() and GameInfo.node_dict[x+1, y] != -1:  # 東にブロック
            no_entry_list.append((x+1, y))  # ブロックのある座標
            if (x+1, y-1) in GameInfo.node_dict.keys():
                no_entry_list.append((x+1, y-1))  # ブロックのある座標の北の座標
            if (x+1, y+1) in GameInfo.node_dict.keys():
                no_entry_list.append((x+1, y+1))  # ブロックのある座標の南の座標
        if (x, y+1) in GameInfo.node_dict.keys() and GameInfo.node_dict[x, y+1] != -1:  # 南にブロック
            no_entry_list.append((x, y+1))  # ブロックのある座標
            if (x-1, y+1) in GameInfo.node_dict.keys():
                no_entry_list.append((x-1, y+1))  # ブロックのある座標の西の座標
            if (x-1, y+1) in GameInfo.node_dict.keys():
                no_entry_list.append((x+1, y+1))  # ブロックのある座標の東の座標
        if (x-1, y) in GameInfo.node_dict.keys() and GameInfo.node_dict[x-1, y] != -1:  # 西にブロック
            no_entry_list.append((x-1, y))  # ブロックのある座標
            if (x-1, y-1) in GameInfo.node_dict.keys():
                no_entry_list.append((x-1, y-1))  # ブロックのある座標の北の座標
            if (x-1, y+1) in GameInfo.node_dict.keys():
                no_entry_list.append((x-1, y+1))  # ブロックのある座標の南の座標
        if (x, y-1) in GameInfo.node_dict.keys() and GameInfo.node_dict[x, y-1] != -1:  # 北にブロック
            no_entry_list.append((x, y-1))  # ブロックのある座標
            if (x-1, y-1) in GameInfo.node_dict.keys():
                no_entry_list.append((x-1, y-1))  # ブロックのある座標の西の座標
            if (x+1, y-1) in GameInfo.node_dict.keys():
                no_entry_list.append((x+1, y-1))  # ブロックのある座標の東の座標

        return no_entry_list

    def get_no_rotate_direction(self, robot) -> List[int]:
        """回頭禁止方向を取得する関数.

        Args:
            robot: 仮想走行体

        Returns:
            List[int]: 回頭禁止方向の方位リスト
        """
        x = robot.coord[0]
        y = robot.coord[1]
        direct = robot.direct
        no_rotate_list = []

        # 東にブロック
        if (x+1, y) in GameInfo.node_dict.keys() and GameInfo.node_dict[x+1, y] != -1:
            no_rotate_list.append(6)  # 西を回頭禁止方向に追加
        # 南にブロック
        if (x, y+1) in GameInfo.node_dict.keys() and GameInfo.node_dict[x, y+1] != -1:
            no_rotate_list.append(0)  # 北を回頭禁止方向に追加
        # 西にブロック
        if (x-1, y) in GameInfo.node_dict.keys() and GameInfo.node_dict[x-1, y] != -1:
            no_rotate_list.append(2)  # 東を回頭禁止方向に追加
        # 北にブロック
        if (x, y-1) in GameInfo.node_dict.keys() and GameInfo.node_dict[x, y-1] != -1:
            no_rotate_list.append(4)  # 南を回頭禁止方向に追加

        # 回頭禁止方向が2つ以上ある場合、それらの間にある方向も回頭禁止方向
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
    # インスタンス化
    info = GameInfo()
    robo = Robot()

    robo.coord = [2, 1]
    robo.direct = Direction.N.value
    color = Color.RED.value

    info.block_id_list = [Color.RED.value, Color.RED.value, Color.YELLOW.value, Color.YELLOW.value,
                          Color.GREEN.value, Color.GREEN.value, Color.BLUE.value, Color.BLUE.value]
    info.base_id_list = [Color.RED.value, Color.YELLOW.value, Color.GREEN.value, Color.BLUE.value]
    info.end_id = Color.RED.value
    print(info.block_id_list)
    print(info.base_id_list)
    print(info.end_id)

    print("候補ノード")
    print(info.get_candidate_node(color))
    print("未運搬のブロックがあるブロック置き場")
    print(info.get_no_transported_block())
    print("走行禁止座標")
    print(info.get_no_entry_coordinate(robo))
    print("回頭禁止方向")
    print(info.get_no_rotate_direction(robo))
