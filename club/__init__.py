import os
import threading
import time
from datetime import datetime

from pynput import keyboard

import utils.kry_util as kry

# 文件存放目录

# 找图相似度
similar = 0.8
# 游戏标题
window_title = "edge"
# 截图路径
cap_path = "screenshot.png"
# 超时次数
time_out_count = 15

common_delay = 2

# 刷新游戏页面
def refresh_game(hwnd):
    kry.f5()
    kry.delay(3)
    if kry.find_img_and_click_ran(hwnd, "../resource/img-club/location.png"):
        kry.delay(common_delay)

def use_tili(hwnd):
    if kry.find_img_and_click_ran(hwnd, "../resource/img-club/location.png"):
        kry.delay(common_delay)
        if kry.find_img_and_click_ran(hwnd, "../resource/img-club/add_tili.png"):
            kry.delay(common_delay)
            if kry.find_img_and_click_ran(hwnd, "../resource/img-club/potato.png"):
                kry.delay(common_delay)
            if kry.find_img_and_click_ran(hwnd, "../resource/img-club/confirm_use_tili.png"):
                kry.delay(common_delay)


def loop_main():
    hwnd = kry.find_window(window_title)
    if hwnd is None:
        return
    kry.set_top(hwnd)

    # 关闭公告弹窗
    if kry.find_img_and_click_ran(hwnd, "../resource/img-club/notice_close.png"):
        kry.delay(common_delay)
    if kry.find_img_and_click_ran(hwnd, "../resource/img-club/location.png"):
        kry.delay(common_delay)
    if kry.find_img_and_click_ran(hwnd, "../resource/img-club/tree.png"):
        kry.delay(common_delay)
    if kry.find_img_and_click_ran(hwnd, "../resource/img-club/tree_selected.png"):
        kry.delay(common_delay)
    if kry.find_img_and_click_ran(hwnd, "../resource/img-club/attack.png"):
        kry.delay(common_delay)
    if kry.find_img_and_click_ran(hwnd, "../resource/img-club/confirm.png"):
        # 判断体力是否不足
        if kry.find_img_is_exist(hwnd, "../resource/img-club/not_enough_tili.png"):
            # 体力不足 使用体力
            use_tili(hwnd)
        kry.delay(common_delay)


def on_press(key):
    # 当按下F12键时，停止监听并退出脚本
    if key == keyboard.Key.f12:
        os._exit(0)


def key_listener():
    # 在一个新的线程中开始监听按键
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


def test():
    hwnd = kry.find_window(window_title)
    if hwnd is not None:
        kry.set_top(hwnd)
        kry.delay(3)
        kry.find_img_and_click_ran(hwnd, "../resource/img-club/tree.png")


if __name__ == '__main__':
    test_mode = False

    # 创建一个线程用于运行按键监听
    t = threading.Thread(target=key_listener)
    t.start()
    print(datetime.now(), " 程序开始运行（按F12退出）...")

    if test_mode:
        # 测试模式
        test()
    else:
        # 正常运行
        while True:
            loop_main()
