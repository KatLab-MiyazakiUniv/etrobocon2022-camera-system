"""中点→中点のゲーム動作モジュール.

中点→中点のゲーム動作のコマンド生成やコスト計算をする
パラメータは https://github.com/KatLab-MiyazakiUniv/etrobocon2022/pull/89 を参照
@author mutotaka0426
"""

from game_motion import GameMotion


class MiddleToMiddle(GameMotion):
    """中点→中点のゲーム動作クラス."""

    def __init__(self, angle: int, need_adjustment: bool, with_block: bool) -> None:
        """MiddleToMiddleのコンストラクタ.

        Args:
            angle: 方向転換の角度
            need_adjustment: 調整動作の有無
            with_block: ブロックを保持している場合True

        """
        self.__angle = angle
        # rotation_angleは指定角度に対して実際に回頭する角度
        if with_block:  # ブロックを保持している場合
            self.__rotation_angle = GameMotion.ROTATION_BLOCK_TABLE[abs(angle)]["angle"]
            self.__rotation_pwm = GameMotion.ROTATION_BLOCK_PWM
            self.__rotation_time = GameMotion.ROTATION_BLOCK_TABLE[abs(angle)]["time"]
        else:  # ブロックを保持していない場合
            self.__rotation_angle = GameMotion.ROTATION_NO_BLOCK_TABLE[abs(angle)]["angle"]
            self.__rotation_pwm = GameMotion.ROTATION_NO_BLOCK_PWM
            self.__rotation_time = GameMotion.ROTATION_NO_BLOCK_TABLE[abs(angle)]["time"]
        self.__direct_rotation = "clockwise" if angle > 0 else "anticlockwise"
        self.__need_adjustment = need_adjustment
        self.__motion_time = 1.1490
        self.__success_rate = 0.5

    def generate_command(self) -> str:
        """中点→中点のゲーム動作に必要なコマンドを生成するメソッド.

        Returns:
            str: コマンド
        """
        command_list = ""  # コマンドのリストを格納する文字列

        if self.__angle != 0:  # 回頭角度が0の場合は回頭のコマンドを生成しない
            # 回頭角度が正の数の場合時計回り，負の数の場合反時計回りで回頭をセットする
            # 回頭を安定させるために、回頭の前後にスリープを入れる
            command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)
            command_list += "RT,%d,%d,%s\n" % (self.__rotation_angle,
                                               self.__rotation_pwm, self.__direct_rotation)
            command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)

        # 回頭後にエッジが切り替わる場合，エッジ切り替えをセットする
        if (next_edge := self.get_next_edge(self.__angle)) != self.current_edge:
            command_list += "EC,%s\n" % next_edge
            self.current_edge = next_edge  # 現在のエッジを更新する

        command_list += "DS,30,70\n"  # 連続で使用する場合を考え黒線を認識しないように直進
        command_list += "CS,BLACK,70\n"  # エッジを認識するまで直進
        command_list += "DS,25,70\n"  # 走行体がエッジに乗るまで直進

        # 調整動作ありの場合，斜め調整をセットする
        if self.__need_adjustment:
            command_list += "DS,20,70\n"

        return command_list.replace("\n", ",中点→中点\n", 1)  # 最初の行の末尾に",中点→中点"を追加する

    def get_cost(self) -> float:
        """中点→中点のゲーム動作のコストを計算するメソッド.

        Returns:
            float: コスト
        """
        m_time = self.__motion_time  # m_time: 回頭や調整動作込みの動作時間

        # 動作時間に回頭時間を足す（成功率に変動はなし）
        m_time += self.__rotation_time
        # 回頭している場合，回頭前後のスリープ時間を足す
        if self.__rotation_angle != 0:
            m_time += + GameMotion.SLEEP_TIME * 2
        # 調整動作ありの場合，斜め調整の動作時間を足す（成功率に変動はなし）
        if self.__need_adjustment:
            m_time += GameMotion.DIAGONAL_TIME

        # 動作時間 * 成功率 + 最大計測時間 * 失敗率
        cost = m_time*self.__success_rate+GameMotion.MAX_TIME*(1-self.__success_rate)

        return cost
