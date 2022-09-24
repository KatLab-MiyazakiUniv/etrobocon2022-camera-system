"""カメラシステムモジュール.

カメラシステムにおいて、一番最初に呼ばれるクラスを定義している
@author: Takahiro55555 miyashita64 kawanoichi
"""
import os
import shutil

from camera_calibrator import CameraCalibrator
from game_area_info import GameAreaInfo
from client import Client
from game_planner import GamePlanner
# 検証後に消す
from game_area_info import GameAreaInfo
from robot import Robot, Direction
from node import Node
from coordinate import Coordinate
from color_changer import Color

class CameraSystem:
    """カメラシステムクラス."""

    __SUBMIT_DIRECTORY_PATH = "camera_system/datafiles/"

    def __init__(self, is_left_course: bool, robot_ip: str) -> None:
        """カメラシステムのコンストラクタ.

        Args:
            is_left_course (bool, optional): 左コースの場合 True. Defaults to True.
            robot_ip: 走行体のIPアドレス
        """
        self.__set_is_left_course(is_left_course)
        self.__robot_ip = robot_ip

    def start(self, camera_id=1) -> None:
        """ゲーム攻略を計画する."""
        # # カメラキャリブレーションを開始する
        # camera_calibrator = CameraCalibrator(camera_id)
        # # GUIから座標を取得する
        # camera_calibrator.start_camera_calibration()

        # 通信を開始する
        client = Client(self.robot_ip, 8080)
        # 開始合図を受け取るまで待機する
        client.wait_for_start_signal()

        # ゲームエリア情報の初期化
        robot = Robot(Coordinate(4, 4), Direction.E, "left")
        GameAreaInfo.node_list = [
            Node(-1, Coordinate(0, 0)), Node(-1, Coordinate(1, 0)),
            Node(-1, Coordinate(2, 0)), Node(-1, Coordinate(3, 0)),
            Node(-1, Coordinate(4, 0)), Node(-1, Coordinate(5, 0)),
            Node(-1, Coordinate(6, 0)),
            Node(-1, Coordinate(0, 1)), Node(0, Coordinate(1, 1)),
            Node(-1, Coordinate(2, 1)), Node(1, Coordinate(3, 1)),
            Node(-1, Coordinate(4, 1)), Node(2, Coordinate(5, 1)),
            Node(-1, Coordinate(6, 1)),
            Node(-1, Coordinate(0, 2)), Node(-1, Coordinate(1, 2)),
            Node(-1, Coordinate(2, 2)), Node(-1, Coordinate(3, 2)),
            Node(-1, Coordinate(4, 2)), Node(-1, Coordinate(5, 2)),
            Node(-1, Coordinate(6, 2)),
            Node(-1, Coordinate(0, 3)), Node(3, Coordinate(1, 3)),
            Node(-1, Coordinate(2, 3)), Node(-1, Coordinate(3, 3)),
            Node(-1, Coordinate(4, 3)), Node(4, Coordinate(5, 3)),
            Node(-1, Coordinate(6, 3)),
            Node(-1, Coordinate(0, 4)), Node(-1, Coordinate(1, 4)),
            Node(-1, Coordinate(2, 4)), Node(-1, Coordinate(3, 4)),
            Node(-1, Coordinate(4, 4)), Node(-1, Coordinate(5, 4)),
            Node(-1, Coordinate(6, 4)),
            Node(-1, Coordinate(0, 5)), Node(5, Coordinate(1, 5)),
            Node(-1, Coordinate(2, 5)), Node(6, Coordinate(3, 5)),
            Node(-1, Coordinate(4, 5)), Node(7, Coordinate(5, 5)),
            Node(-1, Coordinate(6, 5)),
            Node(-1, Coordinate(0, 6)), Node(-1, Coordinate(1, 6)),
            Node(-1, Coordinate(2, 6)), Node(-1, Coordinate(3, 6)),
            Node(-1, Coordinate(4, 6)), Node(-1, Coordinate(5, 6)),
            Node(-1, Coordinate(6, 6)),
        ]
        GameAreaInfo.block_color_list = [
            Color.RED, Color.RED, Color.YELLOW,
            Color.YELLOW, Color.GREEN,
            Color.GREEN, Color.BLUE, Color.BLUE
        ]
        GameAreaInfo.base_color_list = [
            Color.RED, Color.YELLOW,
            Color.GREEN, Color.BLUE
        ]
        GameAreaInfo.bonus_color = Color.RED
        GameAreaInfo.intersection_list = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN]

        # ブロック取得の座標
        get_coords = [Coordinate(1, 1), Coordinate(1, 3), Coordinate(1, 5),
                      Coordinate(3, 1), Coordinate(3, 5),
                      Coordinate(5, 1), Coordinate(5, 3), Coordinate(5, 5)]
        # ブロック設置の座標
        set_coords = [Coordinate(0, 2), Coordinate(0, 3), Coordinate(0, 4),
                      Coordinate(2, 0), Coordinate(3, 0), Coordinate(4, 0),
                      Coordinate(2, 6), Coordinate(3, 6), Coordinate(4, 6),
                      Coordinate(6, 2), Coordinate(6, 3), Coordinate(6, 4)]


        # # ゲームエリア情報を作成する
        # camera_calibrator.make_game_area_info(self.__is_left_course)
        # ゲームエリア攻略を計画する
        motion_commands = GamePlanner.plan(self.__is_left_course)

        # 転送用ディレクトリを作成する
        os.makedirs(self.__SUBMIT_DIRECTORY_PATH, exist_ok=True)
        course_text = "Left" if self.is_left_course else "Right"
        base_color_dict = {GameAreaInfo.base_color_list[0].value: "East",
                           GameAreaInfo.base_color_list[1].value: "South",
                           GameAreaInfo.base_color_list[2].value: "West",
                           GameAreaInfo.base_color_list[3].value: "North"}
        bonus_direction_text = base_color_dict[GameAreaInfo.bonus_color.value]
        # ボーナスブロック運搬のコマンドファイルのコピー元
        bonus_command_source_path = "camera_system/bonus_datafiles/" + \
            bonus_direction_text + "Bonus" + course_text + ".csv"
        # ボーナスブロック運搬のコマンドファイルのコピー先
        bonus_command_file_path = self.__SUBMIT_DIRECTORY_PATH + "CarryBonus" + course_text + ".csv"
        # 生成するカラーブロック運搬のコマンドファイルのパス
        color_command_file_path = self.__SUBMIT_DIRECTORY_PATH + "GameArea" + course_text + ".csv"

        # ボーナスブロック運搬のコマンドファイルをコピーする
        shutil.copyfile(bonus_command_source_path, bonus_command_file_path)
        # カラーブロック運搬のコマンドファイルを生成する
        f = open(color_command_file_path, 'w')
        f.write(motion_commands)  # 計画したコマンドを書き込む
        f.close()
        print("Copy %s to %s\n" % (bonus_command_source_path, bonus_command_file_path))
        print("Create %s\n" % color_command_file_path)

        pass

    @property
    def is_left_course(self) -> bool:
        """Getter.

        Returns:
            bool: 左コースの場合 True
        """
        return self.__is_left_course

    @is_left_course.setter
    def is_left_course(self, is_left_course: bool) -> None:
        """Setter.

        Args:
            is_left_course (bool): 左コースの場合 True
        """
        self.__set_is_left_course(is_left_course)

    def __set_is_left_course(self, is_left_course: bool = True) -> None:
        actual_type = type(is_left_course)
        if actual_type is not bool:
            raise TypeError('Expected type is %s, actual type is %s.' % (bool, actual_type))
        self.__is_left_course = is_left_course

    @property
    def robot_ip(self) -> str:
        """Getter.

        Returns:
            str: 走行体のIPアドレス
        """
        return self.__robot_ip
