"""動作変換モジュール.

現在の走行体と次の走行体からゲーム動作を生成する
@author mutotaka0426 miyashita64
@note 調整動作の有無の判定については https://qr.paps.jp/RFEkV を参照
"""

from robot import Robot, Direction
from coordinate import Coordinate
from game_area_info import GameAreaInfo
from node import Node, NodeType
from color_changer import Color
from game_motion import GameMotion
from block_to_intersection import BlockToIntersection
from block_to_middle import BlockToMiddle
from intersection_to_block import IntersectionToBlock
from intersection_to_middle import IntersectionToMiddle
from middle_to_block import MiddleToBlock
from middle_to_intersection import MiddleToIntersection
from middle_to_middle import MiddleToMiddle
from return_to_block import ReturnToBlock
from return_to_intersection import ReturnToIntersection
from return_to_middle import ReturnToMiddle


class GameMotionConverter:
    """動作変換クラス."""

    def convert_game_motion(self, current_robot: Robot, next_robot: Robot,
                            is_set_motion: bool) -> GameMotion:
        """現在の走行体から次の走行体に至るのに必要なゲーム動作を生成する.

        Args:
            current_robot: 現在の走行体
            next_robot: 次の走行体
            is_set_motion: 設置動作か取得動作か(True:設置, False:取得)

        Returns:
            GameMotion: ゲーム動作
        """
        game_motion = None  # 戻り値となるゲーム動作
        with_block = is_set_motion  # ブロックを保持しているか(設置動作であるか)

        # 現在の走行体と次の走行体のノードタイプを求める
        current_node_type = self.__convert_to_node_type(current_robot.coord)
        next_node_type = self.__convert_to_node_type(next_robot.coord)

        # 回頭角度を求める
        angle = self.__get_rotation_angle(current_robot, next_robot)

        # 次の走行体のエッジをセットする
        if current_node_type == NodeType.BLOCK or next_node_type == NodeType.BLOCK:
            next_robot.edge = "none"  # →ブロック置き場 or ブロック置き場→ の場合はエッジは"none"になる
        else:
            next_robot.edge = self.__get_next_edge(angle, current_robot.edge)

        # 方向転換後に角度補正が可能かを判定する
        can_correction = self.__check_can_correction(current_robot.coord, next_robot.direct)

        # ゲーム動作を生成する
        if current_node_type == NodeType.BLOCK:  # 現在の地点がブロック置き場の場合
            if next_node_type == NodeType.INTERSECTION:  # 次の地点が交点の場合
                # 交点座標をintersection_listの座標(2*2)に直す
                conv_x = (next_robot.coord.x // 2) // 2
                conv_y = (next_robot.coord.y // 2) // 2
                target_color = GameAreaInfo.intersection_list[conv_x+conv_y*2]  # 交点の色をセットする

                game_motion = BlockToIntersection(angle, target_color, with_block, can_correction)

            elif next_node_type == NodeType.MIDDLE:  # 次の地点が中点の場合
                game_motion = BlockToMiddle(angle, with_block, can_correction)

        elif current_node_type == NodeType.INTERSECTION:  # 現在の地点が交点の場合
            if next_node_type == NodeType.BLOCK:  # 次の地点がブロック置き場の場合
                clockwise_angle = angle % 360  # 時計回りの場合の角度に直す

                # 縦調整動作の有無を判定
                vertical_conditions = []  # 縦調整の有無を判定する条件のリスト
                vertical_conditions.append(clockwise_angle == 90)
                vertical_conditions.append(clockwise_angle == 270)
                vertical_conditions.append((current_robot.edge == "left")
                                           and (clockwise_angle == 135))
                vertical_conditions.append((current_robot.edge == "left")
                                           and (clockwise_angle == 315))
                vertical_conditions.append((current_robot.edge == "right")
                                           and (clockwise_angle == 45))
                vertical_conditions.append((current_robot.edge == "right")
                                           and (clockwise_angle == 225))
                vertical_flag = True if any(vertical_conditions) else False  # いずれかの条件を満たしたとき縦調整有

                # 縦調整前に角度補正が可能かを判定する
                in_adjustment_direct = current_robot.direct  # エッジの交差点に乗るための方向転換時の走行体の向き
                if angle != 0:
                    # 縦調整前の回頭角度から方位の差分を求める
                    before_adjustment_angle = angle - 45 if angle > 0 else angle + 45
                    sub_direct_val = before_adjustment_angle // 45
                    # 現在の方位に差分を足し、方位の範囲に正規化する
                    current_direct_val = current_robot.direct.value
                    in_adjustment_direct_val = (
                        current_direct_val + sub_direct_val) % len(Direction)
                    in_adjustment_direct = Direction(in_adjustment_direct_val)

                can_adjust_correction = self.__check_can_correction(
                    current_robot.coord, in_adjustment_direct)

                # 斜め調整動作の有無を判定
                diagonal_conditions = []  # 斜め調整の有無を判定する条件のリスト
                diagonal_conditions.append(clockwise_angle == 0)
                diagonal_conditions.append((current_robot.edge == "left")
                                           and (clockwise_angle == 45))
                diagonal_conditions.append((current_robot.edge == "right")
                                           and (clockwise_angle == 315))
                diagonal_flag = True if any(diagonal_conditions) else False  # いずれかの条件を満たしたとき斜め調整有

                game_motion = IntersectionToBlock(angle, vertical_flag, diagonal_flag, with_block,
                                                  can_adjust_correction, can_correction)

            elif next_node_type == NodeType.MIDDLE:  # 次の地点が中点の場合
                clockwise_angle = angle % 360  # 時計回りの場合の角度に直す
                adjust_conditions = []  # 調整動作の有無を判定する条件のリスト
                adjust_conditions.append(clockwise_angle == 0)
                adjust_conditions.append(clockwise_angle == 45)
                adjust_conditions.append(clockwise_angle == 315)
                adjust_conditions.append((current_robot.edge == "left")
                                         and (clockwise_angle == 90))
                adjust_conditions.append((current_robot.edge == "right")
                                         and (clockwise_angle == 270))
                need_adjustment = True if any(adjust_conditions) else False  # いずれかの条件を満たしたとき調整有

                game_motion = IntersectionToMiddle(
                    angle, need_adjustment, with_block, can_correction)

        elif current_node_type == NodeType.MIDDLE:  # 現在の地点が中点の場合
            if next_node_type == NodeType.BLOCK:  # 次の地点がブラック置き場の場合
                clockwise_angle = angle % 360  # 時計回りの場合の角度に直す
                adjust_conditions = []  # 調整動作の有無を判定する条件のリスト
                adjust_conditions.append((current_robot.edge == "none")
                                         and (clockwise_angle == 0))
                adjust_conditions.append((current_robot.edge == "left")
                                         and (45 <= clockwise_angle <= 135))
                adjust_conditions.append((current_robot.edge == "right")
                                         and (225 <= clockwise_angle <= 315))
                need_adjustment = True if any(adjust_conditions) else False  # いずれかの条件を満たしたとき調整有

                game_motion = MiddleToBlock(angle, need_adjustment, with_block, can_correction)

            elif next_node_type == NodeType.INTERSECTION:  # 次の地点が交点の場合
                # 交点座標をintersection_listの座標(2*2)に直す
                conv_x = (next_robot.coord.x // 2) // 2
                conv_y = (next_robot.coord.y // 2) // 2
                target_color = GameAreaInfo.intersection_list[conv_x+conv_y*2]  # 交点の色をセットする

                game_motion = MiddleToIntersection(angle, target_color, with_block, can_correction)

            elif next_node_type == NodeType.MIDDLE:  # 次の地点が中点の場合
                # 調整動作の有無を調べる
                adjust_conditions = []  # 調整動作の有無を判定する条件のリスト
                if current_robot.edge == "none":
                    adjust_conditions.append(abs(angle) == 45)
                elif current_robot.coord.y % 2 == 0:
                    adjust_conditions.append(next_robot.edge == "left"
                                             and next_robot.direct in [Direction.NW, Direction.SE])
                    adjust_conditions.append(next_robot.edge == "right"
                                             and next_robot.direct in [Direction.NE, Direction.SW])
                else:
                    adjust_conditions.append(next_robot.edge == "left"
                                             and next_robot.direct in [Direction.NE, Direction.SW])
                    adjust_conditions.append(next_robot.edge == "right"
                                             and next_robot.direct in [Direction.NW, Direction.SE])
                need_adjustment = True if any(adjust_conditions) else False  # いずれかの条件を満たしたとき調整有

                game_motion = MiddleToMiddle(angle, need_adjustment, with_block, can_correction)

        return game_motion  # ゲーム動作を返す

    def convert_return_motion(self, current_robot: Robot, next_robot: Robot) -> GameMotion:
        """現在の走行体から次の走行体に至るのに必要な復帰動作を生成する.

        Args:
            current_robot: 現在の走行体
            next_robot: 次の走行体

        Returns:
            GameAreaInfo: ゲーム動作
        """
        game_motion = None  # 戻り値となるゲーム動作

        # 次の走行体のノードタイプを求める
        next_node_type = self.__convert_to_node_type(next_robot.coord)

        # 回頭角度を求める
        angle = self.__get_rotation_angle(current_robot, next_robot)

        # 次の走行体のエッジをセットする
        if next_node_type == NodeType.BLOCK:
            next_robot.edge = "none"  # →ブロック置き場 の場合はエッジは"none"になる
        else:
            next_robot.edge = self.__get_next_edge(angle, current_robot.edge)

        # ゲーム動作を生成する
        if next_node_type == NodeType.BLOCK:  # 次の地点がブロック置き場の場合
            clockwise_angle = angle % 360  # 時計回りの場合の角度に直す
            adjust_conditions = []  # 調整動作の有無を判定する条件のリスト
            adjust_conditions.append((current_robot.edge == "left")
                                     and (clockwise_angle == 315))
            adjust_conditions.append((current_robot.edge == "right")
                                     and (clockwise_angle == 45))
            need_adjustment = True if any(adjust_conditions) else False  # いずれかの条件を満たしたとき調整有

            game_motion = ReturnToBlock(angle, need_adjustment)

        elif next_node_type == NodeType.INTERSECTION:  # 次の地点が交点の場合
            # 交点座標をintersection_listの座標(2*2)に直す
            conv_x = (next_robot.coord.x // 2) // 2
            conv_y = (next_robot.coord.y // 2) // 2
            target_color = GameAreaInfo.intersection_list[conv_x+conv_y*2]  # 交点の色をセットする

            game_motion = ReturnToIntersection(angle, target_color)

        elif next_node_type == NodeType.MIDDLE:  # 次の地点が中点の場合
            game_motion = ReturnToMiddle(angle)

        return game_motion  # ゲーム動作を返す

    def __convert_to_node_type(self, coord: Coordinate) -> NodeType:
        """指定した座標からノードタイプを返す.

        Args:
            coord: 座標

        Returns:
            NodeType: 指定した座標のノードタイプ
        """
        # 2次元座標を1次配列の形に直してゲームエリア情報のノードリストから取得する
        node = GameAreaInfo.node_list[coord.x+coord.y*7]
        return node.node_type

    def __get_rotation_angle(self, current_robot: Robot, next_robot: Robot) -> int:
        """二つの走行体の方位から回頭角度を求める.

        Args:
            current_robot: 現在の走行体
            next_robot: 次の走行体

        Returns:
            int: 回頭角度
        """
        # 計算のために方位のvalueをセットする
        current_value = current_robot.direct.value
        next_value = next_robot.direct.value

        # 回頭禁止方向のリストを取得
        no_rotate_list = GameAreaInfo.get_no_rotate_direction(current_robot)

        # 時計回りの場合を考える
        clockwise_angle = 360
        direct_diff = ((next_value+8)-current_value) % 8  # 時計回りの場合の方位差
        # next_directまで時計回りした場合に向く方位のリストをセットする
        direct_list = [Direction((current_value+diff) % 8) for diff in range(1, direct_diff+1)]
        if set(direct_list) & set(no_rotate_list) == set():  # 時計回りする時に回頭禁止方向に当たらない場合(同じ方位がない場合)
            clockwise_angle = direct_diff * 45

        # 反時計回りの場合を考える
        anticlockwise_angle = -360
        direct_diff = ((current_value+8)-next_value) % 8  # 反時計回りの場合の方位差
        # next_directまで反時計回りした場合に向く方位のリストをセットする
        direct_list = [Direction((current_value-diff) % 8) for diff in range(1, direct_diff+1)]
        if set(direct_list) & set(no_rotate_list) == set():  # 反時計回りする時に回頭禁止方向に当たらない場合(同じ方位がない場合)
            anticlockwise_angle = direct_diff * -45

        # 時計回りも反時計回りも角度が360の場合，目的の方位まで回頭できないためエラーを出す
        if abs(clockwise_angle) == abs(anticlockwise_angle) == 360:
            raise ValueError('Cannot transition from "%s, %s" to "%s, %s"' % (
                current_robot.coord, current_robot.direct, next_robot.coord, next_robot.direct))

        # 時計回りと反時計回りで回頭角度が小さいほうを採用する
        if abs(clockwise_angle) <= abs(anticlockwise_angle):
            return clockwise_angle
        else:
            return anticlockwise_angle

    def __get_next_edge(self, angle: int, current_edge: str) -> str:
        """現在のエッジと回頭角度から次のエッジを求める(GameMotion.get_next_edgeと同じアルゴリズム).

        Args:
            angle: 方向転換の角度
            current_edge: 現在のエッジ

        Returns:
            str: 次のエッジ "left" or "right" or "none"
        """
        conv_angle = angle % 360  # 時計回りの場合の角度に直す（0~360）
        next_edge = current_edge
        if current_edge == "left":
            if conv_angle >= 90 and conv_angle <= 225:  # 後方に回頭する場合エッジを反転する
                next_edge = "right"
        elif current_edge == "right":
            if conv_angle >= 135 and conv_angle <= 270:  # 後方に回頭する場合エッジを反転する
                next_edge = "left"
        else:  # current_edge == "none"
            if conv_angle >= 45 and conv_angle <= 135:  # 右側に回頭する場合エッジを右にする
                next_edge = "right"
            elif conv_angle >= 225 and conv_angle <= 315:
                next_edge = "left"  # 左側に回頭する場合エッジを左にする

        return next_edge

    def __check_can_correction(self, coord: Coordinate, direct: Direction) -> bool:
        """指定座標で指定方向を向く走行体が角度補正が可能か判定する.

        リアカメラが余裕を持って写す範囲(260mm~880mm)
        - 縦を向いている場合    3座標以上(125mm*3 = 375mm)
        - 斜めを向いている場合  2座標以上(125mm*1.414213...*2 = 353.5...mm)
        に座標があれば、角度補正が可能とする.

        Args:
            coord: 走行体の座標
            direct: 走行体の向き

        Returns:
            bool: 走行体が角度補正可能かどうか(True: 可能/False: 不可能)
        """
        NORTH_DIRECTS = [Direction.N, Direction.NE, Direction.NW]
        EAST_DIRECTS = [Direction.E, Direction.NE, Direction.SE]
        SOUTH_DIRECTS = [Direction.S, Direction.SE, Direction.SW]
        WEST_DIRECTS = [Direction.W, Direction.NW, Direction.SW]

        LOWER_DISTANCE = 240  # カメラが写す最小距離[mm]
        UPPER_DISTANCE = 900  # カメラが写す最大距離[mm]
        MARGIN = 20           # 余白距離[mm](黒線幅)
        COORD_LENGTH = 125    # 隣接座標(縦横)との距離[mm]

        # リアカメラが写す座標の方向を求める
        dx = 0
        dy = 0
        if direct in NORTH_DIRECTS:
            dy = 1
        elif direct in SOUTH_DIRECTS:
            dy = -1
        if direct in EAST_DIRECTS:
            dx = -1
        elif direct in WEST_DIRECTS:
            dx = 1

        for i in range(1, 6):  # リアカメラ方向の座標について
            # 対象座標
            x = coord.x + dx * i
            y = coord.y + dy * i
            if x < 0 or 6 < x or y < 0 or 6 < y:  # 対象座標がコースに存在しない場合
                break
            # 座標とのユークリッド距離を実数値で求める
            distance = ((dx*i)**2 + (dy*i)**2) ** (0.5) * COORD_LENGTH
            # 座標がカメラが写す範囲にあれば、線を抽出可能と判定する
            if LOWER_DISTANCE+MARGIN < distance < UPPER_DISTANCE-MARGIN:
                return True
        return False
