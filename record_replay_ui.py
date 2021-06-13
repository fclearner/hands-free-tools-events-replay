import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import pyautogui
import PyHook3 as pyHook
import pythoncom

import os
import time
from datetime import datetime

keyLists = []
timeLists = []
tLists_temp = []
tLists_temp.append(datetime.now())

def judgeRecord():
    if os.path.exists("c:/users/auto.txt"):
        f = open("c:/users/auto.txt", "r")
        if f.readline():
            return True
        else:
            return False
    else:
        return False

# 监听到鼠标事件调用
def onMouseEvent(event):
    if(event.MessageName != "mouse move"):# 因为鼠标一动就会有很多mouse move，所以把这个过滤下
        print(event.MessageName)
        if(event.MessageName == "mouse left up"):
            pass
        elif(event.MessageName == "mouse left down"):
            x, y = pyautogui.position()
            temp = []
            temp.append("click")
            temp.append(x)
            temp.append(y)
            keyLists.append(temp)
            tLists_temp.append(datetime.now())
            timeLists.append((tLists_temp[-1]-tLists_temp[-2]).seconds)
        else:
            pass
    return True # 为True才会正常调用，如果为False的话，此次事件被拦截

# 监听到键盘事件调用
def onKeyboardEvent(event):
    print(event.Key)# 返回按下的键
    if event.Key != "Escape":
        temp = []
        temp.append("key")
        temp.append(event.Key)
        keyLists.append(temp)
        tLists_temp.append(datetime.now())
        timeLists.append((tLists_temp[-1]-tLists_temp[-2]).seconds)
    else:
        f = open("c:/users/auto.txt", "a")
        j = 0
        for k in keyLists:
            s = ""
            for i in range(len(k)):
                if i != len(k)-1:
                    s += str(k[i])+"\t"
                else:
                    s += str(k[i])+"\n"
            print(s)
            f.write(s)
            f.write("sleep"+"\t"+str(timeLists[j])+"\n")
            j+=1
        f.close()
        sys.exit()
    return True

def replay():
    f = open("c:/users/auto.txt", "r")
    dataL = f.readlines()
    f.close()
    for l in dataL:
        temp = l.strip().split("\t")
        if temp[0] == "click":
            x = int(temp[1])
            y = int(temp[2])
            pyautogui.click(x, y)  #使用鼠标点击(x, y)
        elif temp[0] == "key":
            s = temp[1]
            if len(s) <= 2:
                pyautogui.typewrite(s)  #使用键盘输入字符abcde
            else:
                try:
                    pyautogui.press(s)
                except:
                    pass
        elif temp[0] == "sleep":
            t = temp[1]
            time.sleep(int(t))
        else:
            pass

def record():
    # 创建管理器
    hm = pyHook.HookManager()
    # 监听键盘
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    # 监听鼠标 
    hm.MouseAll = onMouseEvent
    hm.HookMouse()
    # 循环监听
    pythoncom.PumpMessages()

def clear():
    os.remove("c:/users/auto.txt")

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 button"
        self.left = 10
        self.top = 100
        self.width = 320
        self.height = 200
        self.initUI()
    
    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        """在窗体内创建button对象"""
        button1 = QPushButton("record", self)
        """方法setToolTip在用户将鼠标停留在按钮上时显示的消息"""
        button1.setToolTip("you can record events by clicking this button, press ESC end the record")
        """按钮坐标x = 100, y = 70"""
        button1.move(50, 50)
        """按钮与鼠标点击事件相关联"""
        button1.clicked.connect(self.on_click1)

        button2 = QPushButton("replay", self)
        """方法setToolTip在用户将鼠标停留在按钮上时显示的消息"""
        button2.setToolTip("you can replay the recorded events by clicking this button")
        """按钮坐标x = 100, y = 70"""
        button2.move(50, 100)
        """按钮与鼠标点击事件相关联"""
        button2.clicked.connect(self.on_click2)

        button3 = QPushButton("clear", self)
        """方法setToolTip在用户将鼠标停留在按钮上时显示的消息"""
        button3.setToolTip("you can clear the recorded events by clicking this button")
        """按钮坐标x = 100, y = 70"""
        button3.move(100, 75)
        """按钮与鼠标点击事件相关联"""
        button3.clicked.connect(self.on_click3)
        
        self.show()
    """创建鼠标点击事件"""
    @pyqtSlot()
    def on_click1(self):
        record()

    @pyqtSlot()
    def on_click2(self):
        if not judgeRecord():
            print("你还未记录脚本链,请进行记录,esc键退出记录")
        else:
            time.sleep(2)
            replay()

    @pyqtSlot()
    def on_click3(self):
        clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
