"""ブロック置き場→中点のゲーム動作モジュール.

ブロック置き場→中点のゲーム動作のコマンド生成やコスト計算をする
パラメータは https://github.com/KatLab-MiyazakiUniv/etrobocon2022/pull/89 を参照
@author mutotaka0426
"""

from game_motion import GameMotion


class BlockToMiddle(GameMotion):
    """ブロック置き場→中点のゲーム動作クラス."""

    def __init__(self, angle: int) -> None:
        """BlockToMiddleのコンストラクタ.

        Args:
            angle: 方向転換の角度

        """
        self.__angle = angle
        self.__motion_time = 0.8094
        self.__success_rate = 0.9

    def generate_command(self) -> str:
        """ブロック置き場→中点のゲーム動作に必要なコマンドを生成するメソッド.

        Returns:
            str: コマンド
        """
        command_list = ""  # コマンドのリストを格納する文字列

        if self.__angle != 0:  # 回頭角度が0の場合はコマンドは生成しない
            # 回頭角度が正の数の場合時計回り，負の数の場合反時計回りで回頭をセットする
            clockwise = "clockwise" if self.__angle > 0 else "anticlockwise"
            command_list += "RT,%d,%d,%s\n" % (abs(self.__angle),
                                               GameMotion.ROTATION_PWM, clockwise)

        command_list += "CS,BLACK,70\n"  # エッジを認識するまで直進
        command_list += "DS,10,70\n"  # 走行体がエッジに乗るまで直進

        # エッジ切り替えのコマンドは生成しないが，計算上はエッジをnoneにする
        self.current_edge = "none"

        return command_list.replace("\n", ",ブロック置き場→中点\n", 1)  # 最初の行の末尾に",ブロック置き場→中点"を追加する

    def get_cost(self) -> float:
        """ブロック置き場→中点のゲーム動作のコストを計算するメソッド.

        Returns:
            float: コスト
        """
        m_time = self.__motion_time  # m_time: 回頭や調整動作込みの動作時間

        # 動作時間に回頭時間を足す（成功率に変動はなし）
        m_time += GameMotion.ROTATION_TIME[abs(self.__angle) // 45]

        # 動作時間 * 成功率 + 最大計測時間 * 失敗率
        cost = m_time*self.__success_rate+GameMotion.MAX_TIME*(1-self.__success_rate)

        return cost
