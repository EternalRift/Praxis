This Libary is for the handling of real time camera streams between two devices.

host.py is the custom libary to run on the headset to send incoming camera frames over a local network down to the ai core (Nvidia Jetson). this is implimented within 'main.py' for easy cross compatablity *main.py might be changed to the root folder name for simplicity sake*

client.py is the custom libary to run on the jetson to handle the incoming video frames from the 'host.py' file and then enable the parsing of these video frames to be utilised in more client side applicaitons within this framework. *for now it will simply spawn a window to display the incoming video frames this will be changed to impliment simple returning of cv2 video frames*

