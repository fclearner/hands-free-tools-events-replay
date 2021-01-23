import pyautogui
import PyHook3 as pyHook
import pythoncom

import os
import sys

keyLists = []

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
    else:
        f = open("c:/users/auto.txt", "a")
        for k in keyLists:
            s = ""
            for i in range(len(k)):
                if i != len(k)-1:
                    s += str(k[i])+"\t"
                else:
                    s += str(k[i])+"\n"
            print(s)
            f.write(s)
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
            pyautogui.typewrite(s)  #使用键盘输入字符abcde
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

if __name__ == "__main__":
    if not judgeRecord():
        f = open("c:/users/auto.txt", "w")
        f.close()
        print("你还未记录脚本链,请进行记录,esc键退出记录")
        record()
    else:
        print("你已经记录了脚本链,如要重新记录,请删除c:/users/auto.txt")
        replay()
