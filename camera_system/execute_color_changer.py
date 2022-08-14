"""
ColorChangerのchange_color関数を実行するファイル
@author kawano
実行コマンド
    $ python execute_color_changer.py
# """
import os
from tqdm import tqdm

import color_changer as cc

def execute_changer():
    """ ColorChangrファイル実行関数 """
    # 変換する画像の入っているフォルダを指定
    folder_path = "course_images"
    images_list = os.listdir(folder_path)
    
    # ColorChangrクラスのインスタンス化
    color_changer = cc.ColorChanger()

    for i in tqdm(images_list):
        path = os.path.join(folder_path, i)
        save_path = os.path.join("results", i)
        color_changer.change_color(path, save_path)
        break
    """
    path = os.path.join(folder_path, images_list[0])
    save_path = os.path.join("results", images_list[0])
    color_changer.change_color(path, save_path)
    # """
        
if __name__ == "__main__":
    execute_changer()
    print("終了")