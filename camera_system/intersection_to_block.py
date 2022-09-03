"""交点→ブロック置き場のゲーム動作モジュール.

交点→ブロック置き場のゲーム動作のコマンド生成やコスト計算をする
パラメータは https://github.com/KatLab-MiyazakiUniv/etrobocon2022/pull/89 を参照
@author mutotaka0426
"""

from game_motion import GameMotion


class IntersectionToBlock(GameMotion):
    """交点→ブロック置き場のゲーム動作クラス."""

    def __init__(self, angle: int, vertical_flag: bool, diagonal_flag: bool) -> None:
        """IntersectionToBlockのコンストラクタ.

        Args:
            angle: 方向転換の角度
            vertical_flag: 縦調整動作の有無
            diagonal_flag: 斜め調整動作の有無

        """
        # 最後の45度は2回目の回頭で実行するため，angleを2つに分ける
        if angle == 0:
            self.__first_angle = 0
            self.__second_angle = 0
        else:
            self.__first_angle = angle - 45 if angle > 0 else angle + 45
            self.__second_angle = 45 if angle > 0 else -45

        self.__vertical_flag = vertical_flag
        self.__diagonal_flag = diagonal_flag
        self.__motion_time = 0.7840
        self.__success_rate = 1.0

        # 縦調整と斜め調整を両方実行することはない
        if self.__vertical_flag and self.__diagonal_flag:
            raise ValueError('Combining Vertical and Diagonal Adjustments is an Unexpected Motion')

    def generate_command(self) -> str:
        """交点→ブロック置き場のゲーム動作に必要なコマンドを生成するメソッド.

        Returns:
            str: コマンド
        """
        command_list = ""  # コマンドのリストを格納する文字列

        if self.__first_angle != 0:  # 回頭角度が0の場合はコマンドは生成しない
            # 回頭角度が正の数の場合時計回り，負の数の場合反時計回りで回頭をセットする
            clockwise = "clockwise" if self.__first_angle > 0 else "anticlockwise"
            command_list += "RT,%d,%d,%s\n" % (abs(self.__first_angle),
                                               GameMotion.ROTATION_PWM, clockwise)

        # 縦調整動作ありの場合，縦調整をセットする
        if self.__vertical_flag:
            command_list += "DS,10,70\n"

        if self.__second_angle != 0:  # 回頭角度が0の場合はコマンドは生成しない
            # 回頭角度が正の数の場合時計回り，負の数の場合反時計回りで回頭をセットする
            clockwise = "clockwise" if self.__second_angle > 0 else "anticlockwise"
            command_list += "RT,%d,%d,%s\n" % (abs(self.__second_angle),
                                               GameMotion.ROTATION_PWM, clockwise)

        # 斜め調整動作ありの場合，斜め調整をセットする
        if self.__diagonal_flag:
            command_list += "DS,20,70\n"

        command_list += "DS,150,70\n"

        # エッジ切り替えのコマンドは生成しないが，計算上はエッジをnoneにする
        self.current_edge = "none"

        return command_list.replace("\n", ",交点→ブロック置き場\n", 1)  # 最初の行の末尾に",交点→ブロック置き場"を追加する

    def get_cost(self) -> float:
        """交点→ブロック置き場のゲーム動作のコストを計算するメソッド.

        Returns:
            float: コスト
        """
        m_time = self.__motion_time  # m_time: 回頭や調整動作込みの動作時間

        # 動作時間に回頭時間を足す（成功率に変動はなし）
        m_time += GameMotion.ROTATION_TIME[abs(self.__first_angle) // 45]
        m_time += GameMotion.ROTATION_TIME[abs(self.__second_angle) // 45]
        # 調整動作ありの場合，調整の動作時間を足す（成功率に変動はなし）
        if self.__vertical_flag:  # 縦調整ありの場合
            m_time += GameMotion.VERTICAL_TIME

        if self.__diagonal_flag:  # 横調整ありの場合
            m_time += GameMotion.DIAGONAL_TIME

        # 動作時間 * 成功率 + 最大計測時間 * 失敗率
        cost = m_time*self.__success_rate+GameMotion.MAX_TIME*(1-self.__success_rate)

        return cost
