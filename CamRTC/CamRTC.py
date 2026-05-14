import host 
import client 
import os


def ReadParams(string):
    #funciton to read a settings txt to set correct ip and port for both host
    #and client TOOD: Provide instruction on how to correctly set params!
   with os.open('settings.txt','r') as infile:
       for line in infile:
           if line.startswith(string):
               return line
               


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
        #returns a pyAV stream to be piped into desired functions, piped return is a cv2 stream!
        return self.jetson.stream()
        

if __name__ == "__main__":
    print("ERROR \nThis program is intended as a libary and cannot function indipenditly please RTFM!!!")
