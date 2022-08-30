from typing import List, Tuple, Dict


class GameInfo:
    """ゲームエリア情報を保持するクラス.

    Attributes:
        block_list (List[int, int]): ブロック([ブロックID, 色ID])
        node_dict (Dict[Tuple(int, int), int]): ノード([座標,ブロックID])
        base_color_dict (Dict(int)): ベースエリアの色ID(赤、黄、緑、青)
    """

    __block_id_list = []
    __base_id_list = []
    __end_id = []
    __node_dict = {
        (0, 0): -1, (0, 1): -1, (0, 2): -1, (0, 3): -1, (0, 4): -1, (0, 5): -1, (0, 6): -1,
        (1, 0): -1, (1, 1): 0,  (1, 2): -1, (1, 3): 1,  (1, 4): -1, (1, 5): 2,  (1, 6): -1,
        (2, 0): -1, (2, 1): -1, (2, 2): -1, (2, 3): -1, (2, 4): -1, (2, 5): -1, (2, 6): -1,
        (3, 0): -1, (3, 1): 3,  (3, 2): -1, (3, 3): -1,  (3, 4): -1, (3, 5): 4, (3, 6): -1,
        (4, 0): -1, (4, 1): -1, (4, 2): -1, (4, 3): -1, (4, 4): -1, (4, 5): -1, (4, 6): -1,
        (5, 0): -1, (5, 1): 5,  (5, 2): -1, (5, 3): 6,  (5, 4): -1, (5, 5): 7,  (5, 6): -1,
        (6, 0): -1, (6, 1): -1, (6, 2): -1, (6, 3): -1, (6, 4): -1, (6, 5): -1, (6, 6): -1,
    }
    __base_color_dict = {0: "東", 1: "南", 2: "西", 3: "北"}

    def color_block_setter(block_id_list: List[int]) -> None:
        """ block_id_listのsetter.

        Args:
            block_id_list: カラーブロックの色idの配列

        """
        GameInfo.__block_id_list = block_id_list

    def base_color_block_setter(base_id_list: List[int]) -> None:
        """ block_id_listのsetter.

        Args:
            block_id_list: ベースサークルブロックの色idの配列
        """
        GameInfo.__base_id_list = base_id_list

    def bonus_block_setter(end_id: int) -> None:
        """ block_id_listのsetter.

        Args:
            block_id_list: ボーナスブロックの色id
        """
        GameInfo.__end_id = end_id

    def get_candidate_node(self, color: int) -> List[Tuple[int, int]]:
        """設置先ノードの候補を取得する関数.

        Args:
            color: 運搬するブロックの色

        Returns:
            List[Tuple[int, int]]: 候補ノードの座標リスト
        """
        cand_list = []
        east_cand_list = [(6, 2), (6, 3), (6, 4)]  # 東の候補ノードになりうる座標リスト
        south_cand_list = [(2, 6), (3, 6), (4, 6)]  # 南の候補ノードになりうる座標リスト
        west_cand_list = [(0, 2), (0, 3), (0, 4)]  # 西の候補ノードになりうる座標リスト
        north_cand_list = [(2, 0), (3, 0), (4, 0)]  # 北の候補ノードになりうる座標リスト

        if base_color_dict[color] == "東":
            for cand in east_cand_list:
                if GameInfo.__node_dict[cand] == -1:  # 対象のノードに既に設置済みのブロックがなければ候補に入れる
                    cand_list.append[cand]
        elif base_color_dict[color] == "南":
            for cand in south_cand_list:
                if GameInfo.__node_dict[cand] == -1:
                    cand_list.append[cand]
        elif base_color_dict[color] == "西":
            for cand in west_cand_list:
                if GameInfo.__node_dict[cand] == -1:
                    cand_list.append[cand]
        else:
            for cand in north_cand_list:
                if GameInfo.__node_dict[cand] == -1:
                    cand_list.append[cand]

        return cand_list

    def get_no_transported_block(self) -> List[List(int, int)]:
        """運搬していないブロックがあるブロック置き場を取得する関数.

        Returns:
            List[List(int, int)]: 運搬していないブロックがあるブロック置き場の座標リスト
        """
        no_trans_block_list = []  # 候補ノードの座標リストを格納する

        for node in node_dict:
            x = node[0][0]
            y = node[0][1]
            block_id = node[1]

            if block_id != -1:  # ブロックがない座標を省く
                if x % 2 != 0 and y % 2 != 0:  # xとyが奇数ならば運搬していないブロックと判定
                    no_trans_block_list += [coord_x, coord_y]

        return no_trans_block_list

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
            robot: 仮想走行体

        Returns:
            List[Tuple[int, int]]: 走行禁止座標の座標リスト
        """
        x = robot.coord[0]
        y = robot.coord[1]
        no_entry_list = []

        if [x+1, y] in GameInfo.node_dict.keys() and GameInfo.node_dict[x+1, y] != -1:  # 東にブロック
            no_entry_list.append([x+1, y])  # ブロックのある座標
            if [x+1, y-1] in GameInfo.node_dict.keys():
                no_entry_list.append([x+1, y-1])  # ブロックのある座標の北の座標
            if [x+1, y+1] in GameInfo.node_dict.keys():
                no_entry_list.append([x+1, y+1])  # ブロックのある座標の南の座標
        if [x, y+1] in GameInfo.node_dict.keys() and GameInfo.node_dict[x, y+1] != -1:  # 南にブロック
            no_entry_list.append([x, y+1])
            if [x-1, y+1] in GameInfo.node_dict.keys():
                no_entry_list.append([x-1, y+1])
            if [x-1, y+1] in GameInfo.node_dict.keys():
                no_entry_list.append([x+1, y+1])
        if [x-1, y] in GameInfo.node_dict.keys() and GameInfo.node_dict[x-1, y] != -1:  # 西にブロック
            no_entry_list.append([x-1, y])
            if [x-1, y-1] in GameInfo.node_dict.keys():
                no_entry_list.append([x-1, y-1])
            if [x-1, y+1] in GameInfo.node_dict.keys():
                no_entry_list.append([x-1, y+1])
        if [x, y-1] in GameInfo.node_dict.keys() and GameInfo.node_dict[x, y-1] != -1:  # 北にブロック
            no_entry_list.append([x-1, y])
            if [x-1, y-1] in GameInfo.node_dict.keys():
                no_entry_list.append([x-1, y-1])
            if [x+1, y-1] in GameInfo.node_dict.keys():
                no_entry_list.append([x+1, y-1])

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

        if [x+1, y] in GameInfo.node_dict.keys() and GameInfo.node_dict[x+1, y] != -1:  # 東にブロック
            no_rotate_list += [6]  # 西を回頭禁止方向に追加
        if [x, y+1] in GameInfo.node_dict.keys() and GameInfo.node_dict[x, y+1] != -1:  # 南にブロック
            no_rotate_list += [0]  # 北を回頭禁止方向に追加
        if [x-1, y] in GameInfo.node_dict.keys() and GameInfo.node_dict[x-1, y] != -1:  # 西にブロック
            no_rotate_list += [2]  # 東を回頭禁止方向に追加
        if [x, y-1] in GameInfo.node_dict.keys() and GameInfo.node_dict[x, y-1] != -1:  # 北にブロック
            no_rotate_list += [4]  # 南を回頭禁止方向に追加

        # 回頭禁止方向が2つ以上ある場合、それらの間にある方向も回頭禁止
        if min(no_rotate_list) < direct and direct < max(no_rotate_list):
            for i in range(min(no_rotate_list)):
                no_rotate_list += [i]
            for i in range(direct+1, max(no_rotate_list)):
                no_rotate_list += [i]
        else:
            for i in range(min(no_rotate_list)+1, max(no_rotate_list)):
                no_rotate_list += [i]

        return no_rotate_list

    if __name__ == "__main__":
        # インスタンス化
        info = GameInfo()
