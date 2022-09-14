"""中点→ブロック置き場のゲーム動作モジュール.

中点→ブロック置き場のゲーム動作のコマンド生成やコスト計算をする
パラメータは https://github.com/KatLab-MiyazakiUniv/etrobocon2022/pull/89 を参照
@author mutotaka0426
"""

from game_motion import GameMotion


class MiddleToBlock(GameMotion):
    """中点→ブロック置き場のゲーム動作クラス."""

    def __init__(self, angle: int, adjustment_flag: bool) -> None:
        """MiddleToBlockのコンストラクタ.

        Args:
            angle: 方向転換の角度
            adjustment_flag: 調整動作の有無

        """
        self.__angle = angle
        self.__adjustment_flag = adjustment_flag
        self.__motion_time = 0.6970
        self.__success_rate = 1.0

    def generate_command(self) -> str:
        """中点→ブロック置き場のゲーム動作に必要なコマンドを生成するメソッド.

        Returns:
            str: コマンド
        """
        command_list = ""  # コマンドのリストを格納する文字列

        if self.__angle != 0:  # 回頭角度が0の場合はコマンドは生成しない
            # 回頭角度が正の数の場合時計回り，負の数の場合反時計回りで回頭をセットする
            clockwise = "clockwise" if self.__angle > 0 else "anticlockwise"
            command_list += "RT,%d,%d,%s\n" % (abs(self.__angle),
                                               GameMotion.ROTATION_PWM, clockwise)

        # 調整動作ありの場合，縦調整をセットする
        if self.__adjustment_flag:
            command_list += "DS,10,70\n"

        command_list += "DS,90,70\n"  # ブロック置き場まで直進

        # エッジ切り替えのコマンドは生成しないが，計算上はエッジをnoneにする
        self.current_edge = "none"

        return command_list.replace("\n", ",中点→ブロック置き場\n", 1)  # 最初の行の末尾に",中点→ブロック置き場"を追加する

    def get_cost(self) -> float:
        """中点→ブロック置き場のゲーム動作のコストを計算するメソッド.

        Returns:
            float: コスト
        """
        m_time = self.__motion_time  # m_time: 回頭や調整動作込みの動作時間

        # 動作時間に回頭時間を足す（成功率に変動はなし）
        m_time += GameMotion.ROTATION_TIME[abs(self.__angle) // 45]
        # 調整動作ありの場合，縦調整の動作時間を足す（成功率に変動はなし）
        if self.__adjustment_flag:
            m_time += GameMotion.VERTICAL_TIME

        # 動作時間 * 成功率 + 最大計測時間 * 失敗率
        cost = m_time*self.__success_rate+GameMotion.MAX_TIME*(1-self.__success_rate)

        return cost
