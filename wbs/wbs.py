import asyncio
import os
import ssl
import json
import time
from aiohttp import web


async def handle_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.text:
            # Store the message in a file
            with open('number','r') as f:
                num = f.read()
            with open('messages.txt', 'a') as f:
                f.write(',')
                f.write(json.dumps({"timestamp":time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()),"id":f"client {num}","message":msg.data}))
                f.write('\n')
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
