import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import copy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import win32gui, win32ui, win32con, win32api
import sys
import keyboard
import pyautogui
import pyperclip
from ctypes import windll
from PIL import Image
1920
1200
X_Scream = 1920
Y_Scream = 1200
X_get_pos = int(300)
Y_get_pos = int(300)
X_get_Scream = int((X_Scream - X_get_pos)/2)
Y_get_Scream = int((Y_Scream - Y_get_pos)/2)
def window_capture(filename):
    name = "APEX legends"
    hwnd = win32gui.FindWindow(0, name)
    #hwnd = 1109  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
    return saveDC

def get_scream():
    # 截图部
    e = 1  # 改变函数f的弯曲方向，f是一个指数函数（e小于1时是凸函数)
    ke = (1 * 2000 / 303) ** (
                1 / e - 1)  # 函数f的系数,（2000/33）决定了对于函数f当指针与目标相距50像素时f(x)=x，（这是一个指数函数，画张图就非常明白了）。2000/33前的系数（1）用于妥善增大或减小50这个值
    f = lambda x: (ke * x) ** e if x >= 0 else -(-ke * x) ** e  # 这是一个‘指数函数’，只是在x小于0时它的图像是对称于x大于0时的图像的。

    hwnd = 0  # 目标窗口的句柄，0是全屏
    x = 0
    y = 0  # 为x,y设置一个初始值
    xs = 1920  # xs,ys代表窗口大小
    ys = 1080  # 由于代码多次修改，并没有做到只要修改xs、ys就能使程序匹配新的窗口大小，还需做很多调整
    x0 = xs / 2
    y0 = ys / 2  # x0,y0是窗口的中点
    nx = 0
    ny = 0  # 为x0,y0设置一个初始值

    hwndDC = win32gui.GetWindowDC(0)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()  # 以下几行均是在这个bitmap中作画的代码
    saveBitMap.CreateCompatibleBitmap(mfcDC, 300, 300)  # 检测范围可以再大点吗
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (X_get_pos, Y_get_pos), mfcDC, (X_get_Scream, Y_get_Scream),
                  win32con.SRCCOPY)  # 第一个二元数对是画作左上角在bitmap中的位置，第二个是画作与画作源的大小，第三个是画作源左上角在屏幕中的位置
    data = saveBitMap.GetBitmapBits()  # 获取bitmap中每个点的R.G.B.alpha值构成的一个元组（顺序是G.B.R.alpha）。已知的图像大小的情况下，这个有序元组结合二维空间中每一个点的色彩值信息

    saveBitMap.SaveBitmapFile(saveDC,"img_Winapi.bmp")
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    # 输出data后便可清空截图的缓存。由于未系统学习win32，原理不明。耗时极短。作为可选项
    # 耗时小于0.0005s/100次

    return data




global xsubx_,ysuby_,p_x,p_y,i_x,i_y,d_x,d_ylast_d_x,last_d_y
i_x = 0
i_y = 0
d_x = 0
d_y = 0
last_d_x = 0
last_d_y = 0
flag_poen = 0
while True:
    flag = 1
    data = get_scream()
    image = cv2.imread('img_Winapi.bmp', cv2.IMREAD_COLOR)
    205, 34, 24
    ball_color = 'red'
    color_dist = {'red': {'Lower': np.array([0, 160, 130]), 'Upper': np.array([6, 200, 160])},
                  'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
                  'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
                  }

    gs_frame = cv2.GaussianBlur(image, (5, 5), 0)  # 高斯模糊
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
    erode_hsv = cv2.erode(hsv, None, iterations=2)  # 腐蚀 粗的变细
    inRange_hsv = cv2.inRange(erode_hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)
    inRange_hsv = cv2.inRange(erode_hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])
    cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    try:
        c = max(cnts, key=cv2.contourArea)
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        cv2.drawContours(image, [np.int0(box)], -1, (0, 255, 255), 2)
        #print(f"c={c},rect={rect},box={box}")
        x = int(rect[0][0])
        y = int(rect[0][1])
        #cv2.circle(image, (x, y), 60, (0, 255, 255), -1)
        if keyboard.is_pressed('X'):
            if flag_poen == 1:
                flag_poen =0
                print("关闭")
            else:
                flag_poen =1
                print("开启")
        if flag_poen ==1 and (x!=0 and y!=0):# and
            try:
                pid_p = 0.4 # 比例系数
                pid_i = 0.0 # 微分系数
                pid_d = 0.02 # 积分系数
                x_, y_ = pyautogui.position()  # 返回鼠标的坐标
                x = int(x+X_get_Scream)          # 换算成标准数值
                y = int(y+Y_get_Scream)          # 换算成标准数值

                # 偏差量
                xsubx_ = x - x_
                ysuby_ = y - y_
                try:
                    # pid中的p
                    p_x = xsubx_ * pid_p
                    p_y = ysuby_ * pid_p
                except:
                    print("检查p")
                try:
                    # pid中的i
                    i_x = i_x + xsubx_ * pid_i
                    i_y = i_y + ysuby_ * pid_i
                    if i_x>=10:
                        i_x == 10
                    elif i_x<=-10:
                        i_x = -10
                    if i_y>=10:
                        i_y ==10
                    elif i_y<=-10:
                        i_y = -10
                except:
                    print("检查i")
                try:
                    # pid中的d
                    d_x = (d_x - last_d_x) * pid_d
                    d_y = (d_y - last_d_y) * pid_d
                    last_d_x = d_x
                    last_d_y = d_y
                except:
                    print("检查d")

                do_x = p_x + i_x + d_x
                do_y = p_y + i_y + d_y
                #print(f"x={do_x},y={do_y}")
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(do_x), int(do_y))

            except:
                print('Move Error')
    except:
        pass

    cv2.imshow('camera', hsv)  # 取消镜面翻转
    cv2.waitKey(1)