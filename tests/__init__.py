"""パッケージの初期化を行うモジュール.

NOTE: このファイルが無いと、'python -m unittest'コマンドで'tests'ディレクトリ配下のテストコードを実行できない
@author: Takahiro55555
"""
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
