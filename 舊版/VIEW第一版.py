import numpy as np
import cv2
import socket
import PIL.Image as Image
from flask import Flask, render_template, Response, jsonify
app = Flask(__name__)
import io

@app.route('/')
def index():
    return render_template('index.html')

def getData():
    with open('IIPP.txt','r') as r:
        IP=r.read()
    host = "192.168.0.66"  # 對server端為主機位置
    port = 5555
    address = (host, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(address)  # 用來請求連接遠程服務器
        size=int(s.recv(1024).decode('utf-8'))
        indata='g'
        s.send(indata.encode())
        data = s.recv(size)
        s.close()
    except ConnectionRefusedError:
        print("目標電腦拒絕連線。")
        return ""
    return data

@app.route('/video')
def video():
    data = getData()
    if data=="":
        return "error"
    if len(data)!=0:
        img= Image.frombuffer('RGB', (1920, 1080), data)
        buffer = io.BytesIO()
        img.save(buffer, 'PNG')
        data = buffer.getvalue()
        buffer.close()
    res = app.make_response(data)
    res.headers["Content-Type"] = "image/png"
    return res
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False,port="5000")