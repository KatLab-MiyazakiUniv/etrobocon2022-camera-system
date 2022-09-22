"""ブロック置き場→交点のゲーム動作モジュール.

ブロック置き場→交点のゲーム動作のコマンド生成やコスト計算をする
パラメータは https://github.com/KatLab-MiyazakiUniv/etrobocon2022/pull/89 を参照
@author mutotaka0426
"""

from game_motion import GameMotion
from color_changer import Color


class BlockToIntersection(GameMotion):
    """ブロック置き場→交点のゲーム動作クラス."""

    def __init__(self, angle: int, target_color: Color, with_block: bool) -> None:
        """BlockToIntersectionのコンストラクタ.

        Args:
            angle: 方向転換の角度
            target_color: 目標となる交点の色
            with_block: ブロックを保持している場合True
        """
        if with_block:  # ブロックを保持している場合
            self.__rotation_angle = GameMotion.ROTATION_BLOCK_TABLE[abs(angle)]["angle"]
            self.__rotation_pwm = GameMotion.ROTATION_BLOCK_PWM
            self.__rotation_time = GameMotion.ROTATION_BLOCK_TABLE[abs(angle)]["time"]
        else:  # ブロックを保持していない場合
            self.__rotation_angle = GameMotion.ROTATION_NO_BLOCK_TABLE[abs(angle)]["angle"]
            self.__rotation_pwm = GameMotion.ROTATION_NO_BLOCK_PWM
            self.__rotation_time = GameMotion.ROTATION_NO_BLOCK_TABLE[abs(angle)]["time"]
        self.__direct_rotation = "clockwise" if angle > 0 else "anticlockwise"
        self.__target_color = target_color
        self.__motion_time = 1.0700
        self.__success_rate = 1.0

        expected_color = [Color.BLUE, Color.GREEN, Color.YELLOW, Color.RED]
        # 交点の色以外を指定された場合エラーを出す
        if self.__target_color not in expected_color:
            raise ValueError('"%s" is an Unexpected Color' % self.__target_color.name)

    def generate_command(self) -> str:
        """ブロック置き場→交点のゲーム動作に必要なコマンドを生成するメソッド.

        Returns:
            str: コマンド
        """
        command_list = ""  # コマンドのリストを格納する文字列

        if self.__rotation_angle != 0:  # 回頭角度が0の場合は回頭のコマンドを生成しない
            # 回頭角度が正の数の場合時計回り，負の数の場合反時計回りで回頭をセットする
            command_list += "RT,%d,%d,%s\n" % (self.__rotation_angle,
                                               self.__rotation_pwm, self.__direct_rotation)

        command_list += "CS,%s,70\n" % self.__target_color.name  # エッジを認識するまで直進
        command_list += "DS,42,60\n"  # 走行体がエッジに乗るまで直進

        # エッジ切り替えのコマンドは生成しないが，計算上はエッジをnoneにする
        self.current_edge = "none"

        return command_list.replace("\n", ",ブロック置き場→交点\n", 1)  # 最初の行の末尾に",ブロック置き場→交点"を追加する

    def get_cost(self) -> float:
        """ブロック置き場→交点のゲーム動作のコストを計算するメソッド.

        Returns:
            float: コスト
        """
        m_time = self.__motion_time  # m_time: 回頭や調整動作込みの動作時間

        # 動作時間に回頭時間を足す（成功率に変動はなし）
        m_time += self.__rotation_time

        # 動作時間 * 成功率 + 最大計測時間 * 失敗率
        cost = m_time*self.__success_rate+GameMotion.MAX_TIME*(1-self.__success_rate)

        return cost
