"""ゲームエリア攻略を計画するモジュール.

ゲームエリア攻略を計画する
@author: miyashita64
"""

from game_area_info import GameAreaInfo
from robot import Robot, Direction
from coordinate import Coordinate
from color_changer import Color
from block_selector import BlockSelector
from game_motion_decider import GameMotionDecider


class GamePlanner:
    """ゲーム攻略を計画するクラス."""

    @classmethod
    def plan(cls) -> str:
        """ゲーム攻略を計画する.

        Returns:
            動作コマンド: str
        """
        # 運搬動作を実現するゲーム動作群のリスト
        game_motions_list = []
        # ボーナスブロック設置後の走行体を求める
        # ToDo: ボーナスブロック運搬の調整によって走行体を書き換える必要がある
        setted_bonus_robots = {
            GameAreaInfo.base_color_list[0].value: Robot(Coordinate(4, 4), Direction.E, "left"),
            GameAreaInfo.base_color_list[1].value: Robot(Coordinate(4, 4), Direction.S, "left"),
            GameAreaInfo.base_color_list[2].value: Robot(Coordinate(2, 4), Direction.W, "left"),
            GameAreaInfo.base_color_list[3].value: Robot(Coordinate(4, 2), Direction.N, "left")}
        robot = setted_bonus_robots[GameAreaInfo.bonus_color.value]

        block_selector = BlockSelector()
        # 全てのカラーブロックについて、運搬動作を決定する
        while GameAreaInfo.get_no_transported_block() != []:
            on_block_node = block_selector.select_block(robot)
            game_motions_list += GameMotionDecider.decide(robot, on_block_node.block_id)
        # ゲーム動作群のリストからコマンドを生成する
        motion_commands = ""
        for game_motions in game_motions_list:
            motion_commands += game_motions.generate_command()

        # 動作コマンドの文字列を返す
        return motion_commands


if __name__ == "__main__":
    # ゲームエリア情報の初期化
    robot = Robot(Coordinate(2, 2), Direction.S, "left")
    GameAreaInfo.block_color_list = [
        Color.RED, Color.RED, Color.YELLOW,
        Color.YELLOW, Color.GREEN, Color.GREEN,
        Color.BLUE, Color.BLUE
    ]
    GameAreaInfo.base_color_list = [
        Color.RED, Color.YELLOW,
        Color.GREEN, Color.BLUE
    ]
    GameAreaInfo.bonus_color = Color.RED
    GameAreaInfo.intersection_list = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN]
    motions = []
    print("block colors", [color.value for color in GameAreaInfo.block_color_list])
    # 運搬動作を決定する
    motion_commands = GamePlanner.plan()
    print(motion_commands)
