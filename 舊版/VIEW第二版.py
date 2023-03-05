import numpy as np
import cv2
import socket
import PIL.Image as Image


with open('IIPP.txt','r') as r:
    IP=r.read()

host = IP  # 對server端為主機位置
print("host="+host)
port = 5555
address = (host, port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)  # 用來請求連接遠程服務器

size=int(s.recv(1024).decode('utf-8'))
cv2.namedWindow("test", 0)
cv2.resizeWindow("test", 300, 300)  # 设置窗口大小

def show_xy(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy=str(x)+"-"+str(y)
        s.send(xy.encode())
        print(x,y)

indata='g'
while True:
    s.send(indata.encode())
    data = s.recv(size)
    img= Image.frombuffer('RGB', (1920, 1080), data)
    img2 = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    if len(data)==0:
        s.close()
        break
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


    cv2.imshow("test", img2)
    cv2.setMouseCallback("test",show_xy)
    cv2.waitKey(100)