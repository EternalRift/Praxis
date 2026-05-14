import host 
import client 
import os


def ReadParams(string):
    #funciton to read a settings txt to set correct ip and port for both host
    #and client TOOD: Provide instruction on how to correctly set params!
    file = os.open("settings.txt")
    for i in string,len(file):

        if i == string:
            break


class HeadsetStream:
    def __init__(self):
        self.ip = ReadParams('hostIP')
        self.port = 8888

    def start():
        headset = host.stream()
        headset.start()


class HeadsetView: 
    def __init__(self):
        self.ip = ReadParams('hostIP')
        self.jetson = client.ClientRTC(self.ip,8888)
        self.jeston.start()
    
    def view(self):
        #returns a pyAV stream to be piped into desired functions
        return self.jetson.stream()
        


HeadsetView.start_view()