"""
文字列をboolに変換するモジュール.

@author: Takahiro55555
"""

from typing import List


class StrToBool:
    """文字列をboolに変換するクラス."""

    @staticmethod
    def convert(v: str) -> bool:
        """文字列をboolに変換する関数.

        Args:
            v (str): boolに変換したい文字列('t', 'T', 'true', 'True', 'f', 'F', 'false', 'False')

        Raises:
            ValueError: 変換可能な文字列以外が入力されたときに発生

        Returns:
            bool: 変換結果
        """
        if v not in (StrToBool.true_str_list() + StrToBool.false_str_list()):
            expected = StrToBool.true_str_list() + StrToBool.false_str_list()
            raise ValueError('Unexpected value. actual="%s", expected="%s"' % (v, expected))
        return v in StrToBool.true_str_list()

    @staticmethod
    def true_str_list() -> List[str]:
        """Trueに変換する文字列のリストを返す関数.

        Returns:
            List[str]: Trueに変換する文字列のリスト
        """
        return ['t', 'T', 'true', 'True']

    @staticmethod
    def false_str_list() -> List[str]:
        """Falseに変換する文字列のリストを返す関数.

        Returns:
            List[str]: Falseに変換する文字列のリスト
        """
        return ['f', 'F', 'false', 'False']
