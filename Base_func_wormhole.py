# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 19:50:04 2019

@author: McLaren
"""

import cv2 as cv
import numpy as np
import win32gui, win32ui, win32con
import sys
import Global_Config as gc
#from Notice import sent_message

sys.path.append(gc.default_dir) 


def init_wormhole():
    '''
    Initialize the wormhole window.
    初始化虫洞软件的窗口
    
    
    Parameters
    ----------
    None.

    Returns
    -------
    None.

    '''
    hwnd = win32gui.FindWindow("Qt5QWindowIcon",gc.config[gc.const_phone]["name"]) # 窗口
    win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,gc.const_position,0,gc.config[gc.const_phone]["length"],649,0)
    

class Fuse:
    def __init__(self):
        init_wormhole()
        self.value = 0
        self.tolerant_time = 100     #截取50张图片后仍未发现对应目标则报错
                                    #防止程序死在死循环里    
    def increase(self):
        self.value += 1
        
    def reset(self):
        self.value = 0
        
    def alarm(self):
        if self.value >= self.tolerant_time:
            #sent_message(text='【FGO】: Encounter a fuse error.')
            print("Fuse Error!")
            sys.exit(0)
            

def match_template(filename,show_switch=True,err=0.77):
    
    #fuse.increase() 
    #print('\nFuse value now: %d' % fuse.value)###########################################
    temppath = gc.template_path_str + filename+".jpg"
    img = window_capture()
    cv.imwrite(gc.template_path_str +"test.jpg",img)
    # cv.imshow("Image", img) #for testing
    #img = cv.imread(imgpath)
    player_template = cv.imread(temppath)
    player = cv.matchTemplate(img, player_template, cv.TM_CCOEFF_NORMED)
    # print("matching "+filename)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(player)
    print(max_val,filename)
    #当图片中有与模板匹配度超过95%的部分时：
    if max_val>err:

        #框选出目标，并标出中心点
        corner_loc = (max_loc[0] + player_template.shape[1], max_loc[1] +player_template.shape[0])
        player_spot = (max_loc[0] + int(player_template.shape[1]/2), max_loc[1] + int(player_template.shape[0]/2))
        
        if show_switch:
            imgOut1=cv.circle(img, player_spot, 10, (0, 255, 255), -1)
            imgOut2=cv.rectangle(img, max_loc, corner_loc, (0, 0, 255), 3)
            # cv.namedWindow("FGO_MatchResult", cv.WINDOW_KEEPRATIO)
            # cv.imshow("FGO_MatchResult", img)
            # cv.imwrite(gc.template_path_str +"FGO_MatchResult1.jpg",imgOut1)
            # cv.imwrite(gc.template_path_str +"FGO_MatchResult2.jpg",imgOut2)
        #显示结果2秒钟
            k = cv.waitKey(1000)
            if k==-1:
                cv.destroyAllWindows()
        
        #fuse.reset()
        return True, player_spot
    else:        
        #fuse.alarm()
        return False, (-1,-1)
    

def window_capture():
    '''
    截取整个目标窗口，返回截取的图片
    Crop and return a picture of the entire targeted window
    
    Parameters
    ----------
    None
    
    Returns
    -------
    cropped : img
        The cropped picture of the window 
    '''
    
    hwnd = win32gui.FindWindow("Qt5QWindowIcon",gc.config[gc.const_phone]["name"]) # 窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    #获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    #saveBitMap.SaveBitmapFile(saveDC, filename)
    
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype = "uint8")
    img.shape = (height, width, 4)
    img = cv.cvtColor(img, cv.COLOR_RGBA2RGB)

    # bias = gc.config[gc.const_phone]["bias"]
    bias = 0
    cropped = img[16:height-26, (21+bias):width-(21+bias)]  # 裁剪坐标为[y0:y1, x0:x1]
    # cropped = img[120:height-26, (21+bias):width-(21+bias)]  # 裁剪坐标为[y0:y1, x0:x1]
    #cv.imwrite('C:/Users/Paul/Desktop/test/3.jpg', cropped) #for testing
    
    win32gui.DeleteObject(saveBitMap.GetHandle()) #释放内存
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd,hwndDC)
    
    return cropped

