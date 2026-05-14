import host 
import client 
import os


def ReadParams():
    #funciton to read a settings txt to set correct ip and port for both host
    #and client TOOD: Provide instruction on how to correctly set params!
    file = os.open("settings.txt")
    pass 


class HeadsetView: 
    def start_view():
        #init host stream class and starts the camera stream
        headset = host.stream()
        headset.start()


    def stream_view():
        pass 


HeadsetView.start_view()