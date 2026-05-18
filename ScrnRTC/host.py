import asyncio
import json 
import mss 
import numpy as np 
from aiortc import RTCPeerConnection, RTCSessionDescription,VideoStreamTrack
from av import VideoFrame

class ScreenStreamTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]
    
    async def recv(self):
        pts,time_base = await self.next_timestamp()

        screenshot = self.sct.grab(self.monitor)

        img = np.array(screenshot)
        img = img[:,:,:3]

        frame = VideoFrame.from_ndarray(img,format="bgr24")
        frame.pts = pts
        frame.time_base = time_base
        return frame 
    
class ScrnHost:

    def __init__(self,host='0.0.0.0',port=8889):
        self.host = host
        self.port = port 
        self.pc = RTCPeerConnection()
        self.track = None
    async def _handle_signaling(self,reader,writer):
        try:
            data = await reader.read(1024)
            if data.decode().strip() == 'GET_OFFER':
                if not self.track:
                    self.track = ScreenStreamTrack()
            self.pc.addTrack(self.track)

            offer = await self.pc.createOffer()
            await self.pc.setLocalDescription(offer)

            writer.write(json.dumps({
                "sdp": self.pc.localDescription.sdp,
                "type": self.pc.localDescription.type
            }).encode())
            await writer.drain()

            answer_data = await reader.read(4096)
            answer_dict = json.loads(answer_data.decode())
            await self.pc.setRemoteDescription(RTCSessionDescription(sdp=answer_dict["sdp"],type=answer_dict["type"]))
            print(f"Signaling Complete. Stream Started for client:")
        except Exception as e:
            print(f"Host Signal Error:{e}")
        finally:
            writer.close
    async def start(self):
        server = await asyncio.start_server(self._handle_signaling,self.host,self.port)
        print(f"Waiting on client connection on {self.host}:{self.port}")
        async with server:
            await server.serve_forever()
