from src.common.enum import General
from PIL import ImageGrab
import socket,pyautogui,win32con,win32gui
from os import system

system("title TbtP2pShortcutService")

class Server:
    def __init__(self):
        
        yy= win32gui.FindWindow(None,"TbtP2pShortcutService")
        win32gui.ShowWindow(yy, win32con.SW_HIDE)
        
        host=General.IP.value
        port=General.PORT.value
        
        while True:
            # 建立一個 socket 物件
            server_socket = socket.socket()
            server_socket.bind((host, port))
            server_socket.listen(1)
            self.response='指令已執行！'
            print('等待客戶端連線...')
            while True:
                try:
                    self.client_socket, client_address = server_socket.accept()
                    print('已連線：', client_address)
                except OSError:
                    print('伺服器已關閉！')
                    break
                while True:
                    try:
                        self.window()
                    except Exception as e:
                        print(e)
                        break
                # 關閉連線
                self.client_socket.close()
                server_socket.close()
                
    def window(self):
        img = ImageGrab.grab(bbox=(0, 0, 1920, 1080)).tobytes()
        size = str(len(img)).encode()
        self.client_socket.send(size)
        self.client_socket.recv(General.RECV_SIZE.value)
        self.client_socket.send(img)
        self.client_socket.recv(General.RECV_SIZE.value)
        
        # 滑鼠點擊事件
        self.xy = self.client_socket.recv(1024).decode('utf-8')
        self.client_socket.send(self.response.encode())
        self.mouse_click()

        
    def mouse_click(self):
        if self.xy != 'not click':
            x, y = self.xy.split('-')
            if int(x) > 1920:
                return
            if int(y) > 1080:
                return
            pyautogui.click(int(x), int(y), clicks=2)
            