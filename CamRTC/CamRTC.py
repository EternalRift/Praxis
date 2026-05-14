import host 
import client 
import os


def ReadParams():
    #funciton to read a settings txt to set correct ip and port for both host
    #and client TOOD: Provide instruction on how to correctly set params!
    file = os.open("settings.txt")
    pass 


class HeadsetStream:
    def __init__(self):
        self.ip = ip 
        self.port = port

    def start():
        headset = host.stream()
        headset.start()


class HeadsetView: 
    def __init__(self):
        self.jetson = client.ClientRTC()
        self.jeston.start()
    
    def view(self):
        #returns a pyAV stream to be piped into desired functions
        return self.jetson.stream()
        


HeadsetView.start_view()