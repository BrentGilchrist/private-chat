import asyncio
import os
import ssl
import json
from aiohttp import web

os.system('gnome-terminal -- node rjso.js')

async def handle_websocket(request):
    ws = web.WebSocketResponse()
    num = 0
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.text:
            # Store the message in a file
            with open('number','r') as f:
                num = f.read()
            num = int(num) + 1     
            with open('number','w') as f:
                f.write(str(num))
            with open('messages.txt', 'a') as f:
                f.write(',')
                f.write(json.dumps({"timestamp":None,"id":f"{num}","message":msg.data}))
                f.write('\n')
            num += 1
            with open('messages.txt', 'r') as f:
                messages = f.read()
            with open('messages.json','w') as f:
                f.write(f"[{messages}]")
            
        elif msg.type == web.WSMsgType.close:
            break

    return ws

app = web.Application()
app.add_routes([web.get('/ws', handle_websocket)])

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain('server.crt', 'server.key')

web.run_app(app, ssl_context=ssl_context)
