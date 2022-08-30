from typing import List, Tuple

class GameInfo:
    """ゲームエリア情報を保持するクラス.

    Attributes:
        block_list (List[int, int]): ブロック([ブロックID, 色ID])
        node_dict (List[int, List(int, int)]): ノード([ブロックID, 座標])
        base_color_dict (int): ベースエリアの色ID(赤、黄、緑、青)
    """
        block_list = []
        node_dict = {(0, 0): -1, (0, 1): -1, (0, 2): -1, (0, 3): -1, (0, 4): -1, (0, 5): -1, (0, 6): -1,
                     (1, 0): -1, (1, 1): 0,  (1, 2): -1, (1, 3): 1,  (1, 4): -1, (1, 5): 2,  (1, 6): -1,
                     (2, 0): -1, (2, 1): -1, (2, 2): -1, (2, 3): -1, (2, 4): -1, (2, 5): -1, (2, 6): -1,
                     (3, 0): -1, (3, 1): 3,  (3, 2): -1, (3, 3): 4,  (3, 4): -1, (3, 5): 5,  (3, 6): -1,
                     (4, 0): -1, (4, 1): -1, (4, 2): -1, (4, 3): -1, (4, 4): -1, (4, 5): -1, (4, 6): -1,
                     (5, 0): -1, (5, 1): 6,  (5, 2): -1, (5, 3): 7,  (5, 4): -1, (5, 5): 8,  (5, 6): -1,
                     (6, 0): -1, (6, 1): -1, (6, 2): -1, (6, 3): -1, (6, 4): -1, (6, 5): -1, (6, 6): -1,
                    }
        base_color_dict = {0: "東", 1: "南", 2: "西", 3: "北"}

    def get_candidate_node(self, color) -> List[Tuple[int, int]]:
        """設置先ノードの候補を取得する関数.

        Args:
            color: 運搬するブロックの色

        Returns:
            List[Tuple[int, int]]: 候補ノードの座標リスト
        """
        cand_list = []
        east_cand_list = [(6, 2), (6, 3), (6, 4)]
        south_cand_list = [(2, 6), (3, 6), (4, 6)]
        west_cand_list = [(0, 2), (0, 3), (0, 4)]
        north_cand_list = [(2, 0), (3, 0), (4, 0)]

        if base_color_dict[color] == "東":
            for cand in east_cand_list:
                if GameInfo.node_dict[cand] == -1: #ノードに設置済みのブロックがなければ候補に入れる
                    cand_list.append[cand]
                return cand_list
        elif base_color_dict[color] == "南":
            for cand in south_cand_list:
                if GameInfo.node_dict[cand] == -1:
                    cand_list.append[cand]
                return cand_list
        elif base_color_dict[color] == "西":
            for cand in west_cand_list:
                if GameInfo.node_dict[cand] == -1:
                    cand_list.append[cand]
                return cand_list
        else:
            for cand in north_cand_list:
                if GameInfo.node_dict[cand] == -1:
                    cand_list.append[cand]
                return cand_list


    def get_no_transported_block(self) -> List[Tuple[int, int]]:
        """運搬していないブロックがあるブロック置き場を取得する関数.

        Returns:
            List[Tuple[int, int]]: 運搬していないブロックがあるブロック置き場の座標リスト
        """
        no_trans_block_list = []

        for node in node_List:
            block_id = node[0]
            x = node[1][0]
            y = node[1][1]
            if block_id != -1:
                if x % 2 != 0 and y % 2 != 0:  #xとyが奇数ならば運搬していないブロックと判定
                    no_trans_block_list += [coord_x, coord_y]

        return no_trans_block_list = []


    def get_bonus_color(self) -> int:
        """ボーナスブロックの色を取得する関数.

        Returns:
            int: ボーナスブロックの色
        """
        coord = CameraCoordinateCalibrator()
        c_changer = ColorChanger()
        x = coord.end_point[0]
        y = coord.end_point[1]
        mode = c_changer.mode_color(x, y, 5, 5)

        return mode


    def get_no_entry_coordinate(self, robot) -> List[List[int, int]]:
        """走行禁止座標を取得する関数.

        Args:
            Robot: 仮想走行体

        Returns:
            List[Tuple[int, int]]: 走行禁止座標の座標リスト
        """
        x = Robot.coord[0]
        y = Robot.coord[1]
        no_entry_list = []
        
        if [x+1, y] in GameInfo.node_dict.keys() and GameInfo.node_dict[x+1, y] != -1: # 東にブロック
            no_entry_list.append([x+1, y])
            if [x+1, y-1] in GameInfo.node_dict.keys():
                no_entry_list.append([x+1, y-1])
            if [x+1, y+1] in GameInfo.node_dict.keys():
                no_entry_list.append([x+1, y+1])
        if [x, y+1] in GameInfo.node_dict.keys() and GameInfo.node_dict[x, y+1] != -1: # 南にブロック
            no_entry_list.append([x, y+1])
            if [x-1, y+1] in GameInfo.node_dict.keys():
                no_entry_list.append([x-1, y+1])
            if [x-1, y+1] in GameInfo.node_dict.keys():
                no_entry_list.append([x+1, y+1])
        if [x-1, y] in GameInfo.node_dict.keys() and GameInfo.node_dict[x-1, y] != -1: # 西にブロック
            no_entry_list.append([x-1, y])
            if [x-1, y-1] in GameInfo.node_dict.keys():
                no_entry_list.append([x-1, y-1])
            if [x-1, y+1] in GameInfo.node_dict.keys():
                no_entry_list.append([x-1, y+1])
        if [x, y-1] in GameInfo.node_dict.keys() and GameInfo.node_dict[x, y-1] != -1: # 北にブロック
            no_entry_list.append([x-1, y])
            if [x-1, y-1] in GameInfo.node_dict.keys():
                no_entry_list.append([x-1, y-1])
            if [x+1, y-1] in GameInfo.node_dict.keys():
                no_entry_list.append([x+1, y-1])
        
        return no_entry_list


    def get_no_rotate_direction(self, robot) -> List[List[int, int]]:
        """回頭禁止方向を取得する関数.
        
        Args:
            Robot: 仮想走行体

        Returns:
            List[int]: 回頭禁止方向の方位リスト
        """
        x = Robot.coord[0]
        y = Robot.coord[1]
        direct = Robot.direct
        no_rotate_list = []

        if [x+1, y] in GameInfo.node_dict.keys() and GameInfo.node_dict[x+1, y] != -1: #東にブロック
            no_rotate_list += [6]
        if [x, y+1] in GameInfo.node_dict.keys() and GameInfo.node_dict[x, y+1] != -1: #南にブロック
            no_rotate_list += [0]
        if [x-1, y] in GameInfo.node_dict.keys() and GameInfo.node_dict[x-1, y] != -1: #西にブロック
            no_rotate_list += [2]
        if [x, y-1] in GameInfo.node_dict.keys() and GameInfo.node_dict[x, y-1] != -1: #北にブロック
            no_rotate_list += [4]

        return max(no_rotate_list)

