# ScrnRTC

ScrnRTC is a lightweight Python library designed to share a host's screen over WebRTC with low latency. It is built to transmit screen video from a host machine to a client (such as a headset) to mitigate the use of long-range HDMI/DP cables into the interface of the Praxis Headset.

The library leverages `aiortc` for the WebRTC stream, utilizes its own signaling mechanism over a standard asyncio TCP socket, and uses `mss` for fast, cross-platform screen capture.

## How it Works

The library is split into two main components:

1. **ScrnHost (`host.py`)**: Acts as the video source. It captures frames from the display monitor using `mss` and wraps them in a custom WebRTC `VideoStreamTrack`. It runs an asyncio TCP server to listen for client connections (default port `8889`). When a client connects and requests a stream via signaling (`GET_OFFER`), the host negotiates a WebRTC connection by exchanging SDP (Session Description Protocol) payloads and begins streaming the screen track.
2. **ScrnReceiver (`client.py`)**: Acts as the client. It connects to the host's TCP server, requests an SDP offer, and replies with an SDP answer. Once the WebRTC connection is established, it starts a background capture loop, converts incoming WebRTC video frames into NumPy arrays (BGR24 format), and places them in an async queue. The `stream()` generator yields these frames for your application to consume.

## Usage

### Host (Streaming the Screen)
To start streaming your screen, initialize and start the `ScrnHost`. By default, it binds to `0.0.0.0` on port `8889`.

```python
import asyncio
from ScrnRTC import ScrnHost

async def main():
    # Initialize the screen host
    host = ScrnHost(host='0.0.0.0', port=8889)
    await host.start()

if __name__ == "__main__":
    asyncio.run(main())
```

### Client (Receiving the Stream)
To receive the stream on a client device, initialize the `ScrnReceiver` with the host's IP address and iterate over `stream()`. 

```python
import asyncio
import cv2 
from ScrnRTC import ScrnReceiver

async def run_client():
    # Connect to the host machine's IP
    receiver = ScrnReceiver(host="127.0.0.1", port=8889)
    print("Connecting to stream...")

    try:
        async for frame in receiver.stream():
            cv2.imshow("Remote Screen", frame)
            
            # WaitKey is required for OpenCV to update the GUI window
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(run_client())
```
