from CamRTC import CamHost
import asyncio

async def main():
    host = CamHost()
    await host.start()

asyncio.run(main())