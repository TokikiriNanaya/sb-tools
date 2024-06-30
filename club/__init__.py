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
# 通用延迟时间（s）
common_delay = 2


def scroll_to_max(times=10, x=None, y=None):
    for i in range(times):
        kry.scroll(-1000, x, y)
        kry.delay(0.1)


# 刷新游戏页面
def refresh_game():
    hwnd = kry.find_window(window_title)
    if hwnd is None:
        return
    kry.set_top(hwnd)
    kry.delay(common_delay)
    # 刷新网页
    kry.f5()
    kry.delay(3)
    count = time_out_count
    while count > 0:
        if kry.find_img_and_click_ran(hwnd, "../resource/img-club/login.png"):
            kry.delay(common_delay)
        if kry.find_img_and_click_ran(hwnd, "../resource/img-club/server_name.png"):
            kry.delay(common_delay)
        if kry.find_img_and_click_ran(hwnd, "../resource/img-club/location.png"):
            kry.delay(common_delay)
            scroll_to_max(15)
            return
        if kry.find_img_and_click_ran(hwnd, "../resource/img-club/notice_close.png"):
            kry.delay(common_delay)
            scroll_to_max(15)
            return
        count = count - 1
        kry.delay(common_delay)
    refresh_game(hwnd)


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
    kry.delay(2)
    scroll_to_max()


if __name__ == '__main__':
    test_mode = False
    # test_mode = True

    # 开始运行的时间
    start_time = time.time()

    # 创建一个线程用于运行按键监听
    t = threading.Thread(target=key_listener)
    t.start()
    print(datetime.now(), " 程序开始运行（按F12退出）...")

    if test_mode:
        # 测试模式
        test()
    else:
        # 正常运行
        refresh_game()
        while True:

            loop_main()

            # 每30分钟刷新一次
            period = time.time() - start_time
            print(f"已运行{period / 60}分钟，{30 - (period / 60)}分钟后刷新页面")
            if period > (60 * 30):
                refresh_game()
                start_time = time.time()
