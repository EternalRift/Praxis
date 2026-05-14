import av 
import cv2 
import asyncio 
import json 
from aiortc import RTCPeerConnection,RTCSessionDescription


class ClientRTC:
    def __init__(self,host_ip,port=8888):
        self.host_ip = host_ip 
        self.port = port 
        self.pc = RTCPeerConnection()
        self.video_track = None 
        self._connection_ready = asyncio.Event()
    
    
    async def start(self):
        @self.pc.on("track")
        def on_track(track):
            if track.kind == "video":
                self.video_track = track 
                self._connection_ready.set()
                
        self.pc.addTransceiver("video",direction="recvonly")

        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)

        try:
            reader , writer = await asyncio.open_connection(self.host_ip,self.port)
            payload = json.dumps({"sdp":self.pc.localDescription.sdp,"type":self.pc.localDescription.type})
            writer.write(payload.encode())
            await writer.drain()

            data = await reader.read(8192)
            awnser_data = json.loads(data.decode())
            awnser = RTCSessionDescription(sdp=awnser_data["sdp"], type=awnser_data["type"])
            await self.pc.setRemoteDescription(awnser)

            writer.close()
            await writer.wait_closed()

        except Exception as e: 
            return False
        await self._connection_ready.wait()
        return True
    async def stream(self):
        if not self.video_track: 
            raise RuntimeError("No Video Stream Avaliable Did you call connect function?")
        try:
            while True: 
                frame = await self.video_track.recv()
                return frame
        except Exception as e:
            print("FUCK!")
        


