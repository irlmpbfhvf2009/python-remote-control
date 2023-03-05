import numpy as np
import cv2,socket
import PIL.Image as Image
from src.common.enum import General

class Client:
    def __init__(self):  
        # 建立一個 socket 物件
        self.client_socket = socket.socket()

        # host=General.IP.value
        host=General.RYAN_IP.value
        port=General.PORT.value
        server_address = (host, port)
        self.client_socket.connect(server_address)
        self.window_name = General.WINDOW_NAME.value
        self.response = '指令已執行！'
        
        cv2.namedWindow(self.window_name, 0)
        cv2.resizeWindow(self.window_name, 300, 300)  # 设置窗口大小
        self.mouse_click = 'not click'.encode()
        cv2.setMouseCallback(self.window_name,self.show_xy) # 設置滑鼠點擊事件
        
        while True:
            # 接收客戶端發來的資料
            try:
                self.window()
            except Exception as e:
                print(e)
                break
                        
        self.client_socket.close()
        
    def window(self):
        size = int(self.client_socket.recv(General.RECV_SIZE.value).decode('utf-8')) + 1
        self.client_socket.send(self.response.encode())
        data = self.client_socket.recv(size)
        imgbuffer = Image.frombuffer('RGB', (1920, 1080), data)
        self.client_socket.send(self.response.encode())
        img = cv2.cvtColor(np.asarray(imgbuffer), cv2.COLOR_RGB2BGR)
        self.client_socket.send(self.mouse_click)
        self.client_socket.recv(General.RECV_SIZE.value)
            
        cv2.imshow(self.window_name, img)
        cv2.waitKey(50)
        
    def show_xy(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_click=(str(x)+"-"+str(y)).encode()
        else:
            self.mouse_click='not click'.encode()