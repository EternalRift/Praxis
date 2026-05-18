import asyncio 
import cv2
import json 
from aiortc import RTCPeerConnection, RTCSessionDescription,VideoStreamTrack
from av import VideoFrame

class CameraStreamTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Could Not Open Video Device. Is it set correctly?")
        
    async def recv(self):
        pts , time_base = await self.next_timestamp()
        ret, frame = self.cap.read()
        if not ret: return None
        video_frame = VideoFrame.from_ndarray(frame,format="bgr24")
        video_frame.time_base = time_base
        return video_frame
    
    def stop(self):
        if self.cap.isOpened():
            self.cap.release()
        super().stop()
class CamHost:
    def __init__(self,host='0.0.0.0',port=8888):
        self.host = host 
        self.port = port 
        self.pc = RTCPeerConnection()
        self.track = None 

    async def _handle_signaling(self,reader,writer):
        try:
            data = await reader.read(1024)
            if data.decode().strip() == "GET_OFFER":
                if not self.track:
                    self.track = CameraStreamTrack()
                self.pc.addTrack(self.track)
                offer = await self.pc.createOffer()
                await self.pc.setLocalDescription(offer)

                writer.write(json.dumps({
                    "sdp": self.pc.localDescription.sdp,
                    "type": self.pc.localDescription.type
                }).encode())
                await writer.drain()

                answer_dict = json.loads((await reader.read(4096)).decode())
                await self.pc.setRemoteDescription(RTCSessionDescription(sdp=answer_dict["sdp"],type=answer_dict["type"]))
        except Exception as e:
            print(f"Signaling Error:{e}")
        finally:
            writer.close()
    async def start(self):
        server = await asyncio.start_server(self._handle_signaling,self.host,self.port)
        async with server:
            await server.serve_forever()