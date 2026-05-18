import asyncio
import json 
import numpy as np 
from aiortc import RTCPeerConnection, RTCSessionDescription

class Receiver:
    def __init__(self,host,port=8888):
        self.host = host 
        self.port = port
        self.pc = RTCPeerConnection()
        self.frame_queue = asyncio.Queue()
        self.pc.on("track", self._on_track)

    def _on_track(self,track):
        if track.kind == "video":
            print("Video Track Acknowlaged, starting Capture Loop")
            asyncio.ensure_future(self._capture_loop(track))

    async def _capture_loop(self,track):
        while True:
            try:
                frame = await track.recv()
                img = frame.to_ndarray(format="bgr24")
                await self.frame_queue.put(img)
            except Exception as e:
                print(f"Stream Has Ended Or An Error Has Occoured:{e}")
                break 

    async def _setup_connection(self):
        reader, writer = await asyncio.open_connection(self.host,self.port)
        try:
            #Ask for offer
            writer.write(b"GET_OFFER")
            await writer.drain()
            # Obtain Offer From Host
            offer_data = (await reader.read(4096)).decode()
            offer_dict = json.loads(offer_data)
            offer = RTCSessionDescription(sdp=offer_dict["sdp"],type=offer_dict["type"])

            # Set Remote Description and Create Answer
            await self.pc.setRemoteDescription(offer)
            answer = await self.pc.createAnswer()
            await self.pc.setLocalDescription(answer)

            #Send Answer back to host 
            answer_json = json.dumps({
                "sdp": self.pc.localDescription.sdp,
                "type": self.pc.localDescription.type
            })
            writer.write(answer_json.encode())
            await writer.drain()
            print(f"Connected To {self.host}. Stream Starting!")
        finally:
            writer.close()
            await writer.wait_closed()
    async def stream(self):
        await self._setup_connection()
        while True:
            frame = await self.frame_queue.get()
            yield frame 



