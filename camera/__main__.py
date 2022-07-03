"""
プロジェクトルートで、以下のコマンドを実行すると最初に呼び出されるファイル.

```
poetry run python camera
```
@author: Takahiro55555
"""

import argparse

from camera_system import CameraSystem
from str_to_bool import StrToBool

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Camera System settings.')

    # NOTE: argparseでtype=boolに設定すると、空文字以外Trueになってしまう模様
    #   参考資料: https://note.nkmk.me/python-argparse-bool/
    parser.add_argument('--is-left', type=str, choices=(StrToBool.true_str_list() + StrToBool.false_str_list()),
                        required=True, help='Lコースの場合Trueに、Rコースの場合Falseを設定する')
    args = parser.parse_args()
    cs = CameraSystem(is_left_course=StrToBool.convert(args.is_left))
    print('is_left_course: %s' % StrToBool.convert(args.is_left))
