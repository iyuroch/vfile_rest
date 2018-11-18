#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import ujson

"""
This package provide interface for vfile_server module
"""

class VFile():
    
    def __init__(self, server_addr):
        self._server_addr = server_addr
        self.session = aiohttp.ClientSession(json_serialize=ujson.dumps)

    def __enter__(self):
        return self

    def __exit__(self ,type, value, traceback):
        # TODO: expand if needed handling session etc.
        pass

    async def mkfile(self, filename):
        # TODO: exception if exists
        # create file on server side
        # return exception if already exists
        async with self.session.post("{}/createfile".format(self._server_addr,
                                json={'filename': filename})) as resp:
            if resp.status != 200:
                raise Exception("Cannot create file on server", resp.status)

    def removefile(self, filename):
        pass

    def readfile(self, filename):
        # bite reader here
        pass

    def writefile(self, filename):
        # bite writer here
        pass

    def appendfile(self, filename):
        # bite writer here
        pass

    def mkfolder(self, dirname):
        pass

    def removefolder(self, dirname):
        pass