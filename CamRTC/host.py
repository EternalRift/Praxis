from av import VideoFrame 
import cv2 
import asyncio 
from aiortc import MediaStreamTrack, RTCPeerConnection , RTCSessionDescription 
import json 


class CameraVideoTrack(MediaStreamTrack):

    def __init__(self):
        
        kind = "video"
        super().__init__()
        self.camera = cv2.VideoCapture(0)

    async def stream(self):
        pts, time_base = await self.next_timestamp()
        ret,frame = self.cap.read()
        if not ret:
            return None
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        new_frame = VideoFrame.from_ndarray(frame,format="rgb24")
        new_frame.pts = pts
        new_frame.time_base = time_base 
        return new_frame 
    
class stream: 
    async def signal_handling(reader,writer):
        pc = RTCPeerConnection()
        pc.addTrack(CameraVideoTrack())

        data = await reader.read(8192)
        msg = json.loads(data.decode())
        offer = RTCSessionDescription(sdp=msg["sdp"], type=msg["type"])
        await pc.setRemoteDescription(offer)

        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        payload = json.dumps({"sdp":pc.localDescription.sdp,"type": pc.localDescription.type})
        writer.write(payload.encode())
        await writer.drain()
        
        while pc.connectionState != 'closed':
            await asyncio.sleep(1)

    async def startStream(self):
        #change ip to jetson / pi ip in final version
        server = await asyncio.start_server(self.signal_handling,'0.0.0.0',8888)
        print("Host is running. Waiting for client on port 8888...")
        async with server:
            await server.serve_forever()
    def start(self):
            asyncio.run(self.startStream())




