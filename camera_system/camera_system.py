"""カメラシステムモジュール.

カメラシステムにおいて、一番最初に呼ばれるクラスを定義している
@author: Takahiro55555 miyashita64
"""

from client import Client
from composite_game_motion import CompositeGameMotion


class CameraSystem:
    """カメラシステムクラス."""

    def __init__(self, is_left_course: bool = True) -> None:
        """カメラシステムのコンストラクタ.

        Args:
            is_left_course (bool, optional): 左コースの場合 True. Defaults to True.
        """
        self.__set_is_left_course(is_left_course)

    def start(self) -> None:
        """ゲーム攻略を計画する."""
        # ToDo: キャリブレーションする(ゲームエリア情報).

        # 通信を開始する.
        client = Client("127.0.0.1", 8080)
        # 開始合図を受け取るまで待機する.
        client.wait_for_start_signal()

        # ToDo: ゲームエリア情報を生成する(ゲームエリア情報).

        # ToDo: 計画する.
        game_motion_list = CompositeGameMotion()  # TODO: 計画した結果のゲーム動作のリストをセットする

        # コマンドファイルを生成する
        file_name = "GameAreaLeft.csv" if self.is_left_course else "GameAreaRight.csv"  # ファイル名をセット
        f = open("command_files/" + file_name, 'w')
        f.write(game_motion_list.generate_command())  # ゲーム動作リストからコマンドを生成して書き込む
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
