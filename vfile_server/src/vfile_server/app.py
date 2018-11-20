#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This provide aiohttp server to store files in memory
"""

import asyncio
import fs

from concurrent.futures import ProcessPoolExecutor
from aiohttp import web


class FSLock():
    files_dict = {}

    def get_file_lock(self, filename):
        if filename not in self.files_dict:
            self.files_dict[filename] = asyncio.Lock()
        return self.files_dict[filename]


def app(host="127.0.0.1", port="8080"):
    mem_fs = fs.open_fs('mem://')
    fs_lock = FSLock()
    routes = web.RouteTableDef()

    @routes.post("/rmdir")
    async def rmdir(request):
        json_req = await request.json()
        dirname = json_req["dirname"]
        try:
            mem_fs.removedir(dirname)
            return web.Response(status=200)
        except fs.errors.ResourceNotFound:
            return web.Response(status=404)

    @routes.post("/lsdir")
    async def lsdir(request):
        json_req = await request.json()
        dirname = json_req["dirname"]
        try:
            files = mem_fs.listdir(dirname)
            return web.json_response({"files": files})
        except fs.errors.ResourceNotFound:
            return web.Response(status=404)

    @routes.post("/mkdir")
    async def mkdir(request):
        json_req = await request.json()
        dirname = json_req["dirname"]
        if mem_fs.exists(dirname):
            return web.Response(status=303)
        else:
            mem_fs.makedirs(dirname)
            return web.Response(status=201)

    @routes.post("/mkfile")
    async def mkfile(request):
        # 201 <- return this code if created
        # 303 <- return this code if exists
        json_req = await request.json()
        filename = json_req["filename"]
        if mem_fs.exists(filename):
            return web.Response(status=303)
        else:
            mem_fs.touch(filename)
            return web.Response(status=201)

    @routes.post('/rmfile')
    async def rmfile(request):
        json_req = await request.json()
        filename = json_req["filename"]
        try:
            file_lock = fs_lock.get_file_lock(filename)
            await file_lock.acquire()
            mem_fs.remove(filename)
            file_lock.release()
            return web.Response(status=200)
        except fs.errors.ResourceNotFound:
            return web.Response(status=404)

    @routes.post('/readfile')
    async def readfile(request):
        json_req = await request.json()
        filename = json_req["filename"]
        if mem_fs.isfile(filename):
            file_lock = fs_lock.get_file_lock(filename)
            await file_lock.acquire()
            writer = web.StreamResponse(status=200)
            await writer.prepare(request)
            with mem_fs.open(filename, mode=u"rb") as readstream:
                chunksize = 8000
                while True:
                    # we need to handle situation when client closes stream
                    if request.transport.is_closing():
                        break
                    chunk = readstream.read(8000)
                    if chunk:
                        await writer.write(chunk)
                    else:
                        break
                await writer.write_eof()
            file_lock.release()
            return writer
        else:
            return web.Response(status=404)

    @routes.post('/writefile')
    async def writefile(request):
        reader = await request.multipart()
        field = await reader.next()
        filename = field.name

        if mem_fs.isfile(filename):
            file_lock = fs_lock.get_file_lock(filename)
            await file_lock.acquire()
            with mem_fs.open(filename, mode=u"wb") as writestream:
                while True:
                    chunk = await field.read_chunk()
                    if not chunk:
                        break
                    writestream.write(chunk)
            file_lock.release()
            return web.Response(status=200)
        else:
            return web.Response(status=404)

    @routes.post('/appendfile')
    async def appendfile(request):
        reader = await request.multipart()
        field = await reader.next()
        filename = field.name
        if mem_fs.isfile(filename):
            file_lock = fs_lock.get_file_lock(filename)
            await file_lock.acquire()
            with mem_fs.open(filename, mode=u"ab") as writestream:
                while True:
                    chunk = await field.read_chunk()
                    if not chunk:
                        break
                    writestream.write(chunk)
            file_lock.release()
            return web.Response(status=200)
        else:
            return web.Response(status=404)

    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host=host, port=port, reuse_port=True, reuse_address=True)

if __name__ == "__main__":
    app()
