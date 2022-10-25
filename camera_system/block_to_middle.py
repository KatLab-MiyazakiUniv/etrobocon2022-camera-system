"""ブロック置き場→中点のゲーム動作モジュール.

ブロック置き場→中点のゲーム動作のコマンド生成やコスト計算をする
パラメータは https://github.com/KatLab-MiyazakiUniv/etrobocon2022/pull/89 を参照
@author mutotaka0426
"""

from game_motion import GameMotion


class BlockToMiddle(GameMotion):
    """ブロック置き場→中点のゲーム動作クラス."""

    CORRECTION_TARGET_ANGLE = 90

    def __init__(self, angle: int, with_block: bool) -> None:
        """BlockToMiddleのコンストラクタ.

        Args:
            angle: 方向転換の角度
            with_block: ブロックを保持している場合True

        """
        if with_block:  # ブロックを保持している場合
            self.__rotation_angle = GameMotion.ROTATION_BLOCK_TABLE[abs(angle)]["angle"]
            self.__rotation_pwm = GameMotion.ROTATION_BLOCK_PWM
            self.__rotation_time = GameMotion.ROTATION_BLOCK_TABLE[abs(angle)]["time"]
            self.__correction_pwm = GameMotion.CORRECTION_BLOCK_PWM
        else:  # ブロックを保持していない場合
            self.__rotation_angle = GameMotion.ROTATION_NO_BLOCK_TABLE[abs(angle)]["angle"]
            self.__rotation_pwm = GameMotion.ROTATION_NO_BLOCK_PWM
            self.__rotation_time = GameMotion.ROTATION_NO_BLOCK_TABLE[abs(angle)]["time"]
            self.__correction_pwm = GameMotion.CORRECTION_NO_BLOCK_PWM
        self.__direct_rotation = "clockwise" if angle > 0 else "anticlockwise"
        self.__motion_time = 0.8094
        self.__success_rate = 0.9

    def generate_command(self) -> str:
        """ブロック置き場→中点のゲーム動作に必要なコマンドを生成するメソッド.

        Returns:
            str: コマンド
        """
        command_list = ""  # コマンドのリストを格納する文字列

        command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)
        if self.__rotation_angle != 0:  # 回頭角度が0の場合は回頭のコマンドを生成しない
            # 回頭を安定させるために、回頭の前後にスリープを入れる
            command_list += "RT,%d,%d,%s\n" % (self.__rotation_angle,
                                               self.__rotation_pwm, self.__direct_rotation)
            command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)
        # 角度を補正する
        command_list += "XR,%d,%d\n" % (self.CORRECTION_TARGET_ANGLE, self.__correction_pwm)
        command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)

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
        m_time += self.__rotation_time
        # 回頭している場合，回頭前後のスリープ時間を足す
        if self.__rotation_angle != 0:
            m_time += GameMotion.SLEEP_TIME * 2

        # 動作時間 * 成功率 + 最大計測時間 * 失敗率
        cost = m_time*self.__success_rate+GameMotion.MAX_TIME*(1-self.__success_rate)

        return cost
