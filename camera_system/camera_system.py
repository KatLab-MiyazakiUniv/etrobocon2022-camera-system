"""カメラシステムモジュール.

カメラシステムにおいて、一番最初に呼ばれるクラスを定義している
@author: Takahiro55555 miyashita64 kawanoichi
"""
import os
from camera_calibrator import CameraCalibrator

from client import Client
from game_planner import GamePlanner


class CameraSystem:
    """カメラシステムクラス."""

    def __init__(self, is_left_course: bool = True) -> None:
        """カメラシステムのコンストラクタ.

        Args:
            is_left_course (bool, optional): 左コースの場合 True. Defaults to True.
        """
        self.__set_is_left_course(is_left_course)

    def start(self, camera_id=1) -> None:
        """ゲーム攻略を計画する."""
        # カメラキャリブレーションを開始する
        camera_calibrator = CameraCalibrator(camera_id)
        # GUIから座標を取得する
        camera_calibrator.start_camera_calibration()

        # 通信を開始する
        client = Client("127.0.0.1", 8080)
        # 開始合図を受け取るまで待機する
        client.wait_for_start_signal()

        # ゲームエリア情報を作成する
        camera_calibrator.make_game_area_info(self.__is_left_course)
        # ゲームエリア攻略を計画する
        motion_commands = GamePlanner.plan()

        # コマンドファイルを生成する
        os.makedirs("command_files", exist_ok=True)
        file_name = "GameAreaLeft.csv" if self.is_left_course else "GamereaRight.csv"  # ファイル名をセット
        f = open("command_files/" + file_name, 'w')
        f.write(motion_commands)  # 計画したコマンドを書き込む
        f.close()
        print("Create %s\n" % file_name)

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
