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
window_title = "300英雄"
# 游戏路径
game_path = "C:/JumpGame/300Hero/"
# 截图路径
cap_path = "../screenshot.png"
# 超时次数
time_out_count = 20

# 已获取数量
gong_xian = 0
# 今日已完成任务数（5贡献 * 3次）
task_num = 3


def loop_main():
    global gong_xian
    global task_num

    count = time_out_count
    # 当前位置
    next_position = "登录"
    kry.kill_by_name("300.exe")
    kry.delay(1)
    kry.kill_by_name("launcher.exe")
    kry.delay(1)

    # 获取游戏窗口
    hwnd = None
    while hwnd is None:
        hwnd = kry.find_window(window_title)
        kry.delay(1)
        if hwnd is None:
            count = count - 1
            if count <= 0:
                return
            kry.run(game_path + "launcher.exe")
            kry.delay(20)
        else:
            kry.set_top(hwnd)
            print(hwnd)
            next_position = "登录"
            count = time_out_count

    while next_position == "登录":
        count = count - 1
        if count <= 0:
            return
        kry.delay(1)
        # 输入账号 开始游戏
        start_x, start_y = kry.find_img(hwnd, "../resource/img-contribution/link_start.png")
        kry.delay(1)
        if start_x >= 0 and start_y >= 0:
            kry.delay(1)
            # 选区-相对坐标
            kry.click(start_x + 39, start_y - 322)
            kry.delay(0.3)
            kry.click(start_x - 820, start_y - 211)
            kry.delay(0.3)
            # 选区-相对坐标
            kry.click(start_x + 39, start_y - 322)
            kry.delay(0.3)
            kry.click(start_x - 820, start_y - 211)
            kry.delay(0.3)

            kry.click(start_x, start_y)
            next_position = "进入世界服"
            count = time_out_count

    while next_position == "进入世界服":
        count = count - 1
        if count <= 0:
            return
        # kry.delay(1)
        # 关闭广告
        kry.find_img_and_click_ran(hwnd, "../resource/img-contribution/bt_ad_close.png")
        # 关闭news
        daily_news_x, daily_news_y = kry.find_img(hwnd, "../resource/img-contribution/bt_daily_news_close.png")
        if daily_news_x >= 0 and daily_news_y >= 0:
            kry.click(daily_news_x + 30, daily_news_y + 3)
        # 进入社团
        if kry.find_img_and_click_ran(hwnd, "../resource/img-contribution/she_tuan.png"):
            kry.delay(1)
        # 进入社团战
        if kry.find_img_and_click_ran(hwnd, "../resource/img-contribution/battle_map.png"):
            kry.delay(1.5)
            # 进入世界服
            kry.alt_f4()
            kry.delay(3)
            next_position = "判断世界服"
            count = time_out_count
        kry.delay(1)

    while next_position == "判断世界服":
        count = count - 1
        if count <= 0:
            return
        # kry.delay(1)
        # 验证是否成功进入世界服
        play_x, play_y = kry.find_img(hwnd, "../resource/img-contribution/play_button.png")
        if play_x >= 0 and play_y >= 0:
            # 头像-相对坐标
            kry.click(play_x + 595, play_y + 15)
            kry.delay(0.5)
            # 排行榜
            if kry.find_img_and_click_ran(hwnd, "../resource/img-contribution/rank_bt.png"):
                if count > 3:
                    count = 3
            kry.delay(0.5)
            # 切换排行榜
            if kry.find_img_and_click_ran(hwnd, "../resource/img-contribution/bt_master_level_rank.png"):
                if count > 3:
                    count = 3
            kry.delay(0.5)
            # 查找标识：world_42
            mark_x, mark_y = kry.find_img(hwnd, "../resource/img-contribution/world_.png")
            if mark_x >= 0 and mark_y >= 0:
                # 回到大厅-相对坐标
                kry.click(play_x - 541, play_y + 14)
                next_position = "贡献币"
                count = time_out_count
        kry.delay(1)

    while next_position == "贡献币":
        count = count - 1
        if count <= 0:
            return
        # kry.delay(1)
        kry.find_img_and_click_ran(hwnd, "../resource/img-contribution/she_tuan.png")
        shop_x, shop_y = kry.find_img(hwnd, "../resource/img-contribution/she_tuan_shop.png")
        if shop_x >= 0 and shop_y >= 0:
            kry.click(shop_x, shop_y)
            # 领取贡献比
            kry.delay(0.3)
            kry.click(shop_x - 171, shop_y + 338)
            kry.delay(0.1)
            kry.click(shop_x + 148, shop_y + 338)
            kry.delay(0.1)
            kry.click(shop_x + 470, shop_y + 338)
            kry.delay(0.1)
            # 打印以获取的贡献总量
            gong_xian = gong_xian + task_num * 5
            return
        kry.delay(1)


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
    kry.set_top(hwnd)
    kry.delay(1)
    kry.find_img_and_click_ran(hwnd, "../resource/img-contribution/battle_map.png")


# 超时判定
def run_with_timeout(timeout):
    loop_thread = threading.Thread(target=loop_main)
    loop_thread.start()
    loop_thread.join(timeout=timeout)
    if loop_thread.is_alive():
        print("超时，重新开始循环。")
        loop_thread._stop()  # 强制停止线程（不推荐，但是简单有效）
        kry.delay(1)
        kry.kill_by_name("300.exe")
        kry.delay(1)
        kry.kill_by_name("launcher.exe")
        kry.delay(1)


if __name__ == '__main__':
    test_mode = False

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
        while True:
            try:
                loop_main()
            except Exception as e:
                print(f"发生异常了！【{e}】，不过我不在乎，给我继续跑！")
                continue
            # run_with_timeout(120)
            elapsed_time = time.time() - start_time  # 计算已经过去的时间
            print(
                f"程序已运行时间：{elapsed_time}秒，贡献总量{gong_xian}，当前速率{gong_xian / elapsed_time * 60 * 60}贡献/h")
