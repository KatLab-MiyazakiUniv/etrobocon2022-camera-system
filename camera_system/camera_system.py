"""カメラシステムモジュール.

カメラシステムにおいて、一番最初に呼ばれるクラスを定義している
@author: Takahiro55555 miyashita64
"""


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
        # ToDo: 通信を確立する(通信).

        # ToDo: キャリブレーションする(ゲームエリア情報).

        # ToDo: 開始合図を受け取るまで待機する(通信).

        # ToDo: ゲームエリア情報を生成する(ゲームエリア情報).

        # ToDo: 計画する.

        # ToDo: コマンドファイルを生成する(ゲーム動作).

        # ToDo: コマンドファイルを送信する(システム外).
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
