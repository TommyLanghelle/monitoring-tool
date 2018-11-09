import asyncio
import websockets
import json
import time
import os

interval = 5; #websocket serve interval in seconds

# get this from mysql
deviceList = [
  {
    "id": 1,
    "path": '10.10.10.10',
    "title": "stasjonær"
  }
]

def ping(hostname):
  response = os.system("ping -c 1 " + hostname + " -n 1")
  if response == 0:
    return True
  else:
    return False

async def serverStatus(websocket, path):
  while True:
    data = []
    for server in deviceList:
      data.append({
        "id": server["id"],
        "name": server["title"],
        "status": ping(server["path"])
      })
    await websocket.send(json.dumps(data))
    time.sleep(interval)

start_server = websockets.serve(serverStatus, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
