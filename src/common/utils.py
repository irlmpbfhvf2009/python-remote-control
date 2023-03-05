import socket

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP=str(s.getsockname()[0])
    s.close()
    return IP