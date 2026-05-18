# CamRTC

CamRTC is a lightweight Python library designed to stream a local camera feed over WebRTC with low latency. It is built to transmit video from a host machine to a client (such as a Jetson Nano) for accelerated image processing.

The library leverages `aiortc` for the WebRTC stream and utilizes its own signaling mechanism over a standard asyncio TCP socket.

## How it Works

The library is split into two main components:

1. **CamHost (`host.py`)**: Acts as the video source. It captures frames from the default camera (`cv2.VideoCapture(0)`) using OpenCV and wraps them in a custom WebRTC `VideoStreamTrack`. It runs an asyncio TCP server to listen for client connections. When a client connects and requests a stream, the host negotiates a WebRTC connection by exchanging SDP (Session Description Protocol) payloads and begins streaming the video track.
2. **Receiver (`client.py`)**: Acts as the client. It connects to the host's TCP server, requests an SDP offer, and replies with an SDP answer. Once the WebRTC connection is established, it starts a background capture loop, converts incoming WebRTC video frames into NumPy arrays (BGR24 format), and places them in an async queue. The `stream()` generator yields these frames for your application to consume.

## Usage

### Host (Streaming the Camera)
To start streaming your local camera, initialize and start the `CamHost`. By default, it binds to `0.0.0.0` on port `8888`.

```python
import asyncio
from CamRTC import CamHost

async def main():
    host = CamHost(host='0.0.0.0', port=8888)
    await host.start()

if __name__ == "__main__":
    asyncio.run(main())
```

### Client (Receiving the Stream)
To receive the stream on a client device, initialize the `Receiver` with the host's IP address and call `stream()`. 

```python
import asyncio
import cv2 
from CamRTC import Receiver

async def run_client():
    receiver = Receiver(host="127.0.0.1")
    print("Connecting...")

    async for frame in receiver.stream():
        cv2.imshow("remote", frame)
        # WaitKey is required for OpenCV to update the GUI window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    asyncio.run(run_client())
```