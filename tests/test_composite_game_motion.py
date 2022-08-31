"""中点→ブロック置き場のゲーム動作のテストコードを記述するモジュール.

@author: mutotaka0426
"""

import unittest

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "camera_system"))
from camera_system.composite_game_motion import CompositeGameMotion  # noqa
from block_to_intersection import BlockToIntersection  # noqa
from block_to_middle import BlockToMiddle  # noqa
from intersection_to_block import IntersectionToBlock  # noqa
from intersection_to_middle import IntersectionToMiddle  # noqa
from middle_to_block import MiddleToBlock  # noqa
from middle_to_intersection import MiddleToIntersection  # noqa
from middle_to_middle import MiddleToMiddle  # noqa
from return_after_setup import ReturnAfterSetup  # noqa


class TestCompositeGameMotion(unittest.TestCase):
    """CompositeGameMotionのテスト."""

    def test_composite_game_motion(self):
        game_motion_list = CompositeGameMotion()

        # 各ゲーム動作のインスタンスを生成
        b2i = BlockToIntersection(45, "RED")
        b2m = BlockToMiddle(90)
        i2b = IntersectionToBlock(135, True, False)
        i2m = IntersectionToMiddle(180, True)
        m2b = MiddleToBlock(-45, True)
        m2i = MiddleToIntersection(-90, "BLUE")
        m2m = MiddleToMiddle(-135, True)
        ras = ReturnAfterSetup(-180, "intersection", "YELLOW")

        b2i.current_edge = "left"  # current_edgeの初期値を合わせる
        # 各ゲーム動作のインスタンスから一つずつコマンドを生成する
        expected = b2i.generate_command()
        expected += b2m.generate_command()
        expected += i2b.generate_command()
        expected += i2m.generate_command()
        expected += m2b.generate_command()
        expected += m2i.generate_command()
        expected += m2m.generate_command()
        expected += ras.generate_command()

        # 各ゲーム動作のインスタンスをセットする
        game_motion_list.append_game_motion(b2i)
        game_motion_list.append_game_motion(b2m)
        game_motion_list.append_game_motion(i2b)
        game_motion_list.append_game_motion(i2m)
        game_motion_list.append_game_motion(m2b)
        game_motion_list.append_game_motion(m2i)
        game_motion_list.append_game_motion(m2m)
        game_motion_list.append_game_motion(ras)

        b2i.current_edge = "left"  # current_edgeの初期値を合わせる
        actual = game_motion_list.generate_command()  # CompositeGameMotionからコマンドを生成

        self.assertEqual(expected, actual)
