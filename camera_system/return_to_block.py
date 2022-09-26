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
        self.__angle = angle
        self.__need_adjustment = need_adjustment

    def generate_command(self) -> str:
        """設置後復帰(→ブロック置き場)のゲーム動作に必要なコマンドを生成するメソッド.

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
        if self.__need_adjustment:
            command_list += "DS,10,-70\n"

        command_list += "DS,100,-40\n"  # ブロック置き場まで後退
        self.current_edge = "none"  # 計算上のエッジをnoneにする

        # 最初の行の末尾に",設置後復帰(→ブロック置き場)"を追加する
        return command_list.replace("\n", ",設置後復帰(→ブロック置き場)\n", 1)

    def get_cost(self) -> float:
        """設置後復帰(→ブロック置き場)のゲーム動作のコストを計算するメソッド.

        Returns:
            float: コスト
        """
        # 調整動作ありの場合，縦調整の動作時間を足す（成功率に変動はなし）
        m_time = GameMotion.ROTATION_TIME[abs(self.__angle) // 45]
        if self.__need_adjustment:
            m_time += GameMotion.VERTICAL_TIME

        return m_time
