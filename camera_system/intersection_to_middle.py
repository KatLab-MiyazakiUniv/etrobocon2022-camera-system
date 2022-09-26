"""交点→中点のゲーム動作モジュール.

交点→中点のゲーム動作のコマンド生成やコスト計算をする
パラメータは https://github.com/KatLab-MiyazakiUniv/etrobocon2022/pull/89 を参照
@author mutotaka0426
"""

from game_motion import GameMotion


class IntersectionToMiddle(GameMotion):
    """交点→中点のゲーム動作クラス."""

    def __init__(self, angle: int, need_adjustment: bool) -> None:
        """IntersectionToMiddleのコンストラクタ.

        Args:
            angle: 方向転換の角度
            need_adjustment: 調整動作の有無

        """
        self.__angle = angle
        self.__need_adjustment = need_adjustment
        self.__motion_time = 0.5480
        self.__success_rate = 0.8

    def generate_command(self) -> str:
        """交点→中点のゲーム動作に必要なコマンドを生成するメソッド.

        Returns:
            str: コマンド
        """
        command_list = ""  # コマンドのリストを格納する文字列

        if self.__angle != 0:  # 回頭角度が0の場合はコマンドは生成しない
            # 回頭角度が正の数の場合時計回り，負の数の場合反時計回りで回頭をセットする
            clockwise = "clockwise" if self.__angle > 0 else "anticlockwise"
            command_list += "RT,%d,%d,%s\n" % (abs(self.__angle),
                                               GameMotion.ROTATION_PWM, clockwise)

        # 回頭後にエッジが切り替わる場合，エッジ切り替えをセットする
        if (next_edge := self.get_next_edge(self.__angle)) != self.current_edge:
            command_list += "EC,%s\n" % next_edge
            self.current_edge = next_edge  # 現在のエッジを更新する

        # 調整動作ありの場合，縦調整をセットする
        if self.__need_adjustment:
            command_list += "DS,10,70\n"

        command_list += "DL,80,0,60,0.1,0.08,0.08\n"  # 中点までライントレース

        return command_list.replace("\n", ",交点→中点\n", 1)  # 最初の行の末尾に",交点→中点"を追加する

    def get_cost(self) -> float:
        """交点→中点のゲーム動作のコストを計算するメソッド.

        Returns:
            float: コスト
        """
        m_time = self.__motion_time  # m_time: 回頭や調整動作込みの動作時間

        # 動作時間に回頭時間を足す（成功率に変動はなし）
        m_time += GameMotion.ROTATION_TIME[abs(self.__angle) // 45]
        # 調整動作ありの場合，縦調整の動作時間を足す（成功率に変動はなし）
        if self.__need_adjustment:
            m_time += GameMotion.VERTICAL_TIME

        # 動作時間 * 成功率 + 最大計測時間 * 失敗率
        cost = m_time*self.__success_rate+GameMotion.MAX_TIME*(1-self.__success_rate)

        return cost
