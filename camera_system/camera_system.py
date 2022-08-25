"""カメラシステムモジュール.

カメラシステムにおいて、一番最初に呼ばれるクラスを定義している
@author: Takahiro55555
"""


class CameraSystem:
    """カメラシステムクラス."""

    def __init__(self, is_left_course: bool = True) -> None:
        """カメラシステムのコンストラクタ.

        Args:
            is_left_course (bool, optional): 左コースの場合 True. Defaults to True.
        """
        self.__set_is_left_course(is_left_course)

    def start(self):
        """
        ゲーム攻略を計画する.
        """
        # 通信を確立する

        # キャリブレーション

        # 開始合図を受け取るまで待機

        # ゲームエリア情報を生成する

        # 計画する

        # コマンドファイルを生成
        
        # コマンドファイルを送信(システム外)
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
