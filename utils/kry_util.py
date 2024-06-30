#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/29 14:07
# @Author  : Kiriya
# @File    : kry_util.py
# @Description : 图像识别 for PC
import random
import time

import cv2

import pyautogui as gui
import os

# import win32con
import win32gui

# 默认相似度
default_similar = 0.8
# 截图路径
cap_path = "../screenshot.png"


def click(x, y):
    """
    左键点击
    :param x: 坐标x
    :param y: 坐标y
    """
    print("左键点击：", "x:", x, "y:", y)
    gui.leftClick(x=x, y=y)


def right_lick(x, y):
    """
    右键点击
    :param x: 坐标x
    :param y: 坐标y
    """
    print("右键点击：", "x:", x, "y:", y)
    gui.rightClick(x=x, y=y)


def screen_cap(hwnd, save_path):
    """
    截图
    :param save_path: 截图保存路径
    :param hwnd: 句柄
    """

    rect = win32gui.GetWindowRect(hwnd)

    # 使用win32gui获取窗口位置和大小
    x, y, width, height = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]

    # 设置截图区域为全屏
    screenshot = gui.screenshot(region=(x, y, width, height))

    # 保存截图到指定位置
    screenshot.save(save_path)
    return x, y, width, height


def find_img(hwnd, find_img_path, source_img_path=cap_path, similar=default_similar):
    """
    找图
    :param hwnd: 句柄
    :param source_img_path: 源图片路径
    :param find_img_path: 需要查找的图片路径
    :param similar: 相似度（匹配的阈值）
    :return: x,y坐标
    """
    # 取图片名字：用‘/’分割后取最后一个
    img_name = find_img_path.split("/")[-1]
    print("句柄【", hwnd, "】", "开始找图：", img_name)
    # 获取最新截图
    win_x, win_y, win_w, win_h = screen_cap(hwnd, source_img_path)

    # 读取待检查的图片和截图
    image = cv2.imread(find_img_path)
    screenshot = cv2.imread(source_img_path)

    # 将图片和截图转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # 使用模板匹配来查找图片在截图中的位置
    result = cv2.matchTemplate(gray_screenshot, gray_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 如果找到匹配的位置，则图片在截图中出现过
    if max_val >= similar:
        x, y = max_loc
        print("句柄【", hwnd, "】", "找到图片：", img_name, "x:", x, "y:", y)
        # 获取最佳匹配位置的坐标
        return x + win_x, y + win_y
    print("句柄【", hwnd, "】", "未找到图片：", img_name)
    return -1, -1


def find_img_and_click_ran(hwnd, find_img_path, source_img_path=cap_path, similar=default_similar):
    """
    找图 如果找到则在该图范围内点击一次
    :param hwnd: 句柄
    :param source_img_path: 源图片路径
    :param find_img_path: 需要查找的图片路径
    :param similar: 相似度（匹配的阈值）
    :return: 是否找到
    """
    x, y = find_img(hwnd, find_img_path, source_img_path, similar)
    if x < 0 and y < 0:
        return False

    # 获取查找图片长宽
    img = cv2.imread(find_img_path)
    height, width = img.shape[0:2]

    # print("图片x,y:", x, y)
    # print("图片w,h:", width, height)

    # 获取图片范围内随机坐标
    ran_x = random.randint(0, width)
    ran_y = random.randint(0, height)

    # print("偏移量x,y:", ran_x, ran_y)
    # print("偏移后x,y:", x + ran_x, y + ran_y)

    # 点击图片内随机坐标
    click(x + ran_x, y + ran_y)
    return True


def run(path):
    print("启动：", path)
    os.system(path)
    print("启动完成")


def delay(seconds):
    print("等待", seconds, "秒...")
    time.sleep(seconds)


# 根据窗口标题查询窗口句柄
def find_window(title):
    hwnd_list = []

    def callback(hwnd, _):
        if title.lower() in win32gui.GetWindowText(hwnd).lower():
            hwnd_list.append(hwnd)
        return True

    win32gui.EnumWindows(callback, None)
    if len(hwnd_list) > 0:
        print("成功找到窗口")
        return hwnd_list[0]
    print("未能找到窗口")
    return None


# 将窗口置顶
def set_top(hwnd):
    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        print(e)


def press_key(key):
    gui.press(key)
    print("按下按键", key)


def click_random_range(coordinates):
    """
    随机点击指定范围（多个）
    :param coordinates: [((1, 2), (3, 4)), ((5, 6), (7, 8))]
    """
    # 随机选一个范围
    random_coordinate_pair = random.choice(coordinates)
    # 左上坐标
    x1, y1 = random_coordinate_pair[0]
    # 右下坐标
    x2, y2 = random_coordinate_pair[1]
    x, y = get_random_xy(x1, y1, x2, y2)
    click(x, y)


def get_random_xy(x1, y1, x2, y2):
    x = random.randint(x1, x2)
    y = random.randint(y1, y2)
    return x, y


# def get_yaml_conf(yaml_path):
#     # 读取配置文件
#     with open(yaml_path, 'r') as file:
#         return yaml.safe_load(file)


def get_yaml_value(config, section, key):
    # 获取配置项的值
    return config[section][key]


# def write_yaml_conf(config, section, key, value, yaml_path):
#     # 写入配置文件
#     config[section][key] = value
#     with open(yaml_path, 'w') as file:
#         yaml.dump(config, file)


def paste(_str):
    gui.typewrite(_str)


def kill_by_name(name):
    os.system('taskkill /f /im ' + name)


def alt_f4():
    print("模拟按下 Alt 和 F4 键")
    # 模拟按下 Alt 和 F4 键
    gui.keyDown('alt')
    gui.press('f4')
    gui.keyUp('alt')
