import asyncio 
import json 
from aiortc import RTCPeerConnection,RTCSessionDescription

class ScrnReceiver:

    def __init__(self,host,port=8889):
        self.host = host 
        self.port = port 
        self.pc = RTCPeerConnection()
        self.frame_queue = asyncio.Queue()

        self.pc.on("track",self._on_track)
    def _on_track(self,track):
        if track.kind == "video":
            print("Video Track Found Starting Capture Loop!")
            asyncio.ensure_future(self._capture_loop(track))
    async def _capture_loop(self,track):
        try:
            while True:
                frame = await track.recv()
                img = frame.to_ndarray(format="bgr24")
                await self.frame_queue.put(img)
        except Exception as e:
            print(f"Stream Stopped Or error: {e}")
    async def connect(self): 
        reader,writer = await asyncio.open_connection(self.host,self.port)
        try:
            writer.write(b"GET_OFFER")
            await writer.drain()

            offer_data = (await reader.read(4096)).decode()
            offer_dict = json.loads(offer_data)
            offer = RTCSessionDescription(sdp=offer_dict["sdp"],type=offer_dict["type"])
            await self.pc.setRemoteDescription(offer)

            answer = await self.pc.createAnswer()
            await self.pc.setLocalDescription(answer)

            writer.write(json.dumps({
                "sdp": self.pc.localDescription.sdp,
                "type": self.pc.localDescription.type
            }).encode())
            await writer.drain()
            print(f"Connected To {self.host}")
        finally:
            writer.close()
            await writer.wait_closed()
    async def stream(self):
        await self.connect()
        while True:
            frame = await self.frame_queue.get()
            yield frame