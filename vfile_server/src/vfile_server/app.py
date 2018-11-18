#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This provide aiohttp server to store files in memory
"""

import asyncio

from fs import memoryfs.MemoryFS
from aiohttp import web

def app(host="127.0.0.1", port="8080"):
    mem_fs = MemoryFS()
    routes = web.RouteTableDef()

    @routes.get('/createfile')
    async def createfile(request):
        return web.Response(text="Hello, world")

    loop = asyncio.get_event_loop()
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host=host, port=port)

if __name__ == "__main__":
    app()