"""交点→ブロック置き場のゲーム動作モジュール.

交点→ブロック置き場のゲーム動作のコマンド生成やコスト計算をする
パラメータは https://github.com/KatLab-MiyazakiUniv/etrobocon2022/pull/89 を参照
@author mutotaka0426
"""

from game_motion import GameMotion


class IntersectionToBlock(GameMotion):
    """交点→ブロック置き場のゲーム動作クラス."""

    CORRECTION_TARGET_ANGLE = 45

    def __init__(self, angle: int, vertical_flag: bool, diagonal_flag: bool,
                 with_block: bool) -> None:
        """IntersectionToBlockのコンストラクタ.

        Args:
            angle: 方向転換の角度
            vertical_flag: 縦調整動作の有無
            diagonal_flag: 斜め調整動作の有無
            with_block: ブロックを保持している場合True

        """
        # 縦調整と斜め調整を両方実行することはない
        if vertical_flag and diagonal_flag:
            raise ValueError('Combining Vertical and Diagonal Adjustments is an Unexpected Motion')

        # 最後の45度は2回目の回頭で実行するため，angleを2つに分ける
        if angle == 0:
            first_angle = 0
            second_angle = 0
        else:
            first_angle = angle - 45 if angle > 0 else angle + 45
            second_angle = 45 if angle > 0 else -45

        if with_block:  # ブロックを保持している場合
            self.__first_angle = GameMotion.ROTATION_BLOCK_TABLE[abs(first_angle)]["angle"]
            self.__second_angle = GameMotion.ROTATION_BLOCK_TABLE[abs(second_angle)]["angle"]
            self.__rotation_pwm = GameMotion.ROTATION_BLOCK_PWM
            self.__first_rotation_time = GameMotion.ROTATION_BLOCK_TABLE[abs(
                first_angle)]["time"]
            self.__second_rotation_time = GameMotion.ROTATION_BLOCK_TABLE[abs(
                second_angle)]["time"]
            self.__correction_pwm = GameMotion.CORRECTION_BLOCK_PWM
        else:  # ブロックを保持していない場合
            self.__first_angle = GameMotion.ROTATION_NO_BLOCK_TABLE[abs(first_angle)]["angle"]
            self.__second_angle = GameMotion.ROTATION_NO_BLOCK_TABLE[abs(second_angle)]["angle"]
            self.__rotation_pwm = GameMotion.ROTATION_NO_BLOCK_PWM
            self.__first_rotation_time = GameMotion.ROTATION_NO_BLOCK_TABLE[abs(
                first_angle)]["time"]
            self.__second_rotation_time = GameMotion.ROTATION_NO_BLOCK_TABLE[abs(
                second_angle)]["time"]
            self.__correction_pwm = GameMotion.CORRECTION_NO_BLOCK_PWM
        self.__direct_rotation = "clockwise" if angle > 0 else "anticlockwise"
        self.__vertical_flag = vertical_flag
        self.__diagonal_flag = diagonal_flag
        self.__motion_time = 0.7840
        self.__success_rate = 1.0

    def generate_command(self) -> str:
        """交点→ブロック置き場のゲーム動作に必要なコマンドを生成するメソッド.

        Returns:
            str: コマンド
        """
        command_list = ""  # コマンドのリストを格納する文字列

        command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)
        if self.__first_angle != 0:  # 回頭角度が0の場合は回頭のコマンドを生成しない
            # 回頭角度が正の数の場合時計回り，負の数の場合反時計回りで回頭をセットする
            # 回頭を安定させるために、回頭の前後にスリープを入れる
            command_list += "RT,%d,%d,%s\n" % (self.__first_angle,
                                               self.__rotation_pwm, self.__direct_rotation)
            command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)
            # 角度を補正する
            command_list += "XR,%d,%d\n" % (self.CORRECTION_TARGET_ANGLE, self.__correction_pwm)
            command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)

        # 縦調整動作ありの場合，縦調整をセットする
        if self.__vertical_flag:
            command_list += "DS,10,70\n"

        if self.__second_angle != 0:  # 回頭角度が0の場合は回頭のコマンドを生成しない
            # 回頭角度が正の数の場合時計回り，負の数の場合反時計回りで回頭をセットする
            # 回頭を安定させるために、回頭の前後にスリープを入れる
            command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)
            command_list += "RT,%d,%d,%s\n" % (self.__second_angle,
                                               self.__rotation_pwm, self.__direct_rotation)
            command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)
        # 角度を補正する
        command_list += "XR,%d,%d\n" % (self.CORRECTION_TARGET_ANGLE, self.__correction_pwm)
        command_list += "SL,%d\n" % (GameMotion.SLEEP_TIME * 1000)

        # 斜め調整動作ありの場合，斜め調整をセットする
        if self.__diagonal_flag:
            command_list += "DS,20,70\n"

        command_list += "DS,132,70\n"

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
        m_time += self.__first_rotation_time
        m_time += self.__second_rotation_time
        # 回頭している場合，回頭前後のスリープ時間を足す
        if self.__first_angle != 0:
            m_time += GameMotion.SLEEP_TIME * 2
        if self.__second_angle != 0:
            m_time += GameMotion.SLEEP_TIME * 2
        # 調整動作ありの場合，調整の動作時間を足す（成功率に変動はなし）
        if self.__vertical_flag:  # 縦調整ありの場合
            m_time += GameMotion.VERTICAL_TIME

        if self.__diagonal_flag:  # 横調整ありの場合
            m_time += GameMotion.DIAGONAL_TIME

        # 動作時間 * 成功率 + 最大計測時間 * 失敗率
        cost = m_time*self.__success_rate+GameMotion.MAX_TIME*(1-self.__success_rate)

        return cost
