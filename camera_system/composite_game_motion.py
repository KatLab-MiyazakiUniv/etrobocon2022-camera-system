"""ゲーム動作のリスト管理モジュール.

ゲーム動作のリストからコマンド生成やコスト計算をする
@author mutotaka0426
"""

from game_motion import GameMotion


class CompositeGameMotion:
    """ゲーム動作のリストを管理するクラス."""

    def __init__(self) -> None:
        """CompositeGameMotionのコンストラクタ."""
        self.__game_motion_list = []

    def append_game_motion(self, game_motion: GameMotion) -> None:
        """リストにゲーム動作を追加する.

        Args:
            game_motion: ゲーム動作インスタンス
        """
        self.__game_motion_list.append(game_motion)

    def generate_command(self) -> str:
        """ゲーム動作のリストからコマンドを生成する.

        Returns:
            str: コマンド
        """
        commands = ""
        for game_motion in self.__game_motion_list:
            commands += game_motion.generate_command()
        return commands

    def get_cost(self) -> float:
        """ゲーム動作のリストからコストを計算する.

        Returns:
            float: 総コスト
        """
        total_cost = 0
        for game_motion in self.__game_motion_list:
            total_cost += game_motion.get_cost()
        return total_cost
