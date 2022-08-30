import cv2
from typing import List, Tuple

class GameInfo:
    """ゲームエリア情報を保持するクラス.

    Attributes:
        block_list (List[int, str): ブロック([ブロックID, 色])
        node_list (List[int, List(int, int)]): ノード([ブロックID, 座標])
        color_list (str): ベースエリアの色(赤、黄、緑、青)
        robot (List[int, List(int, int)]): 仮想走行体([座標, 方位])
    """
        block_list = []
        node_list = [[-1, [0, 0]], [-1, [0, 1]], [-1, [0, 2]], [-1, [0, 3]], [-1, [0, 4]], [-1, [0, 5]], [-1, [0, 6]],
                     [-1, [1, 0]], [0, [1, 1]],  [-1, [1, 2]], [1, [1, 3]],  [-1, [1, 4]], [2, [1, 5]], [-1, [1, 6]],
                     [-1, [2, 0]], [-1, [2, 1]], [-1, [2, 2]], [-1, [2, 3]], [-1, [2, 4]], [-1, [2, 5]], [-1, [2, 6]],
                     [-1, [3, 0]], [3, [3, 1]],  [-1, [3, 2]], [4, [3, 3]],  [-1, [3, 4]], [-5, [3, 5]], [-1, [3, 6]],
                     [-1, [4, 0]], [-1, [4, 1]], [-1, [4, 2]], [-1, [4, 3]], [-1, [4, 4]], [-1, [4, 5]], [-1, [4, 6]],
                     [-1, [5, 0]], [6, [5, 1]],  [-1, [5, 2]], [7, [5, 3]],  [-1, [5, 4]], [-8, [5, 5]], [-1, [5, 6]],
                     [-1, [6, 0]], [-1, [6, 1]], [-1, [6, 2]], [-1, [6, 3]], [-1, [6, 4]], [-1, [6, 5]], [-1, [6, 6]]
                    ]
        base_color_list = [0, 1, 2, 3]

    def get_candidate_node(self, color) -> List[Tuple[int, int]]:
    """設置先ノードの候補を取得する関数.

    Args:
        color: 運搬するブロックの色

    Returns:
        List[Tuple[int, int]]: 候補ノードの座標リスト ([x座標, y座標]の形で格納)
    """

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


    def get_bonus_color(self) -> str:
    """ボーナスブロックの色を取得する関数.

    Returns:
        str: ボーナスブロックの色
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
        List[Tuple[int, int]]: 走行禁止座標の座標リスト ([x座標, y座標]の形で格納)
    """



    def get_no_rotate_direction(self, robot) -> List[List[int, int]]:
    """回頭禁止方向を取得する関数.
    
    Args:
        Robot: 仮想走行体

    Returns:
        List[int]: 回頭禁止方向の座標リスト
    """
    for robot[]

