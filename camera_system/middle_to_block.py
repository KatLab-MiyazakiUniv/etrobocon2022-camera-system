"""中点→ブロック置き場のゲーム動作モジュール.

中点→ブロック置き場のゲーム動作のコマンド生成やコスト計算をする
パラメータは https://github.com/KatLab-MiyazakiUniv/etrobocon2022/pull/89 を参照
@author mutotaka0426 miyashita64
"""

from game_motion import GameMotion


class MiddleToBlock(GameMotion):
    """中点→ブロック置き場のゲーム動作クラス."""

    def __init__(self, angle: int, need_adjustment: bool,
                 with_block: bool, can_correction: bool) -> None:
        """MiddleToBlockのコンストラクタ.

        Args:
            angle: 方向転換の角度
            need_adjustment: 調整動作の有無
            with_block: ブロックを保持している場合True
            can_correction: 角度補正可能な場合True
        """
        # rotation_angleは指定角度に対して実際に回頭する角度
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
        self.__need_adjustment = need_adjustment
        self.__can_correction = can_correction
        self.__correction_target_angle = 0
        self.__motion_time = 0.697
        self.__success_rate = 0.78

    def generate_command(self) -> str:
        """中点→ブロック置き場のゲーム動作に必要なコマンドを生成するメソッド.

        Returns:
            str: コマンド
        """
        command_list = ""  # コマンドのリストを格納する文字列

        # 回頭を安定させるために、回頭前にスリープを入れる
        if self.__rotation_angle != 0 or self.__can_correction:
            command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)
        if self.__rotation_angle != 0:  # 回頭角度が0の場合は回頭のコマンドを生成しない
            # 回頭角度が正の数の場合時計回り，負の数の場合反時計回りで回頭をセットする
            # 回頭を安定させるために、回頭の前後にスリープを入れる
            command_list += "RT,%d,%d,%s\n" % (self.__rotation_angle,
                                               self.__rotation_pwm, self.__direct_rotation)
            command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)
        if self.__can_correction:   # 直線を認識できる座標と方向であれば角度を補正する
            command_list += "XR,%d,%d\n" % (self.__correction_target_angle, self.__correction_pwm)
            command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)

        # 調整動作ありの場合，縦調整をセットする
        if self.__need_adjustment:
            command_list += "DS,13,70,20mm直進(縦調整)\n"

        command_list += "DS,71,70\n"  # ブロック置き場まで直進

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
        m_time += self.__rotation_time
        # 回頭前後のスリープ時間を足す
        if self.__rotation_angle != 0 or self.__can_correction:
            m_time += GameMotion.SLEEP_TIME * 2
        # 方向転換する、かつ、角度補正する場合、スリープが1回増える
        if self.__rotation_angle != 0 and self.__can_correction:
            m_time += GameMotion.SLEEP_TIME
        # 調整動作ありの場合，縦調整の動作時間を足す（成功率に変動はなし）
        if self.__need_adjustment:
            m_time += GameMotion.VERTICAL_TIME

        # 動作時間 * 成功率 + 最大計測時間 * 失敗率
        cost = m_time*self.__success_rate+GameMotion.MAX_TIME*(1-self.__success_rate)

        return cost
