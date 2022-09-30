"""設置後復帰(→ブロック置き場)のゲーム動作モジュール.

設置後復帰(→ブロック置き場)のゲーム動作のコマンド生成やコスト計算をする
パラメータは https://github.com/KatLab-MiyazakiUniv/etrobocon2022/pull/89 を参照
@author mutotaka0426
"""

from game_motion import GameMotion


class ReturnToBlock(GameMotion):
    """設置後復帰(→ブロック置き場)のゲーム動作クラス."""

    def __init__(self, angle: int, need_adjustment: bool) -> None:
        """ReturnToBlockのコンストラクタ.

        Args:
            angle: 方向転換の角度
            need_adjustment: 調整動作の有無
        """
        self.__rotation_angle = GameMotion.ROTATION_BLOCK_TABLE[abs(angle)]["angle"]
        self.__rotation_pwm = GameMotion.ROTATION_BLOCK_PWM
        self.__rotation_time = GameMotion.ROTATION_BLOCK_TABLE[abs(angle)]["time"]
        self.__direct_rotation = "clockwise" if angle > 0 else "anticlockwise"
        self.__need_adjustment = need_adjustment

    def generate_command(self) -> str:
        """設置後復帰(→ブロック置き場)のゲーム動作に必要なコマンドを生成するメソッド.

        Returns:
            str: コマンド
        """
        command_list = ""  # コマンドのリストを格納する文字列

        if self.__rotation_angle != 0:  # 回頭角度が0の場合は回頭のコマンドを生成しない
            # 回頭角度が正の数の場合時計回り，負の数の場合反時計回りで回頭をセットする
            # 回頭を安定させるために、回頭の前後にスリープを入れる
            command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)
            command_list += "RT,%d,%d,%s\n" % (self.__rotation_angle,
                                               self.__rotation_pwm, self.__direct_rotation)
            command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)
        command_list += "AR,50,40,アームを上げる処理(設置処理)\n"

        # 調整動作ありの場合，縦調整をセットする
        if self.__need_adjustment:
            command_list += "DS,10,-70\n"

        command_list += "DS,100,-40\n"  # ブロック置き場まで後退
        command_list += "AF,50,40,アームを下げる処理\n"
        self.current_edge = "none"  # 計算上のエッジをnoneにする

        # 最初の行の末尾に",設置後復帰(→ブロック置き場)"を追加する
        return command_list.replace("\n", ",設置後復帰(→ブロック置き場)\n", 1)

    def get_cost(self) -> float:
        """設置後復帰(→ブロック置き場)のゲーム動作のコストを計算するメソッド.

        Returns:
            float: コスト
        """
        # 調整動作ありの場合，縦調整の動作時間を足す（成功率に変動はなし）
        m_time = self.__rotation_time
        if self.__need_adjustment:
            m_time += GameMotion.VERTICAL_TIME
        # 回頭している場合，回頭前後のスリープ時間を足す
        if self.__rotation_angle != 0:
            m_time += GameMotion.SLEEP_TIME * 2

        return m_time
